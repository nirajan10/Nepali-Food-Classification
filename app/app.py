from flask import Flask, request, url_for, redirect, render_template
import torch
import pandas as pd
from torchvision.transforms import transforms
from torchvision import models
from PIL import Image
import os
from PIL import UnidentifiedImageError

app = Flask(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

models_dir = os.path.abspath("models\model.pth")
model = torch.load(models_dir)
model.to(device)

df = pd.read_csv('app\\food_description.csv', index_col=[0])

def predict_image(model, image):
    class_names = ['aalu chop', 'bara', 'bhatmas sadeko', 'biryani', 'buff curry', 'chatamari', 'chhoila', 'chhurpi', 'chicken curry', 'chow mein', 'dalbhat', 'dhau(yogurt)', 'dhido', 'gajar ko halwa', 'gundruk', 'jeri(jalebi)', 'kakro ko achar', 'khaja set', 'khapse', 'kheer', 'kodo ko roti', 'kwati', 'laphing', 'lassi', 'momos', 'pani puri', 'phini roti', 'samosa', 'sekuwa', 'selroti', 'sisnu soup', 'sukuti', 'thukpa', 'yomari']
    
    # Load and preprocess the image
    transform = transforms.Compose(
        [transforms.Resize((224, 224)),
         transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension

    # Move the image to the GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    image = image.to(device)

    # Make predictions
    model.eval()
    with torch.no_grad():
        predictions = model(image)

    # Convert predictions to probabilities
    probs = torch.nn.functional.softmax(predictions[0], dim=0)

    # Get the predicted class index and confidence
    predicted_class_idx = torch.argmax(probs).item()
    confidence = 100 * probs[predicted_class_idx].item()

    # Return the result
    result = {
        "predicted_class": class_names[predicted_class_idx],
        "confidence": confidence
    }
    return result


@app.route("/")
def hello_world():
    return render_template('Image Classification.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # Check if the 'image' key is in the request.files dictionary
        if 'image' in request.files:
            try:
                image_file = request.files['image']
                image = Image.open(image_file)
                image = image.convert('RGB')
                output = predict_image(model, image)
                pred = f"Food is {output['predicted_class']} with {output['confidence']:.2f} confidence."
                des = f"{df.loc[output['predicted_class']][0]}"
                n_pred = "Food doesn't belong to any category."
                des2 = "It could be the result of things like food that isn't from Nepal, food that falls into more than one category, or food that isn't even food."

                if output['confidence'] >= 80:
                    return render_template('Image Classification.html', pred=pred, des=des, image=image)
                else:
                    return render_template('Image Classification.html', pred=n_pred, des2=des2, image=image)
            except UnidentifiedImageError:
                no_image_message = "Please upload a valid image."
                return render_template('Image Classification.html', no_image=no_image_message)
        else:
            no_image_message = "Please insert the image"
            return render_template('Image Classification.html', no_image=no_image_message)
    # Handle GET request or invalid POST request
    return render_template('Image Classification.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3000"), debug=True)