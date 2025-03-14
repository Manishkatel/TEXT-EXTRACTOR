from app import app
from flask import request, render_template, url_for,abort
import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Manish\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

ALLOWED_HOSTS = {"textextract.com"}

@app.before_request
def limit_remote_addr():
    host = request.host.split(":")[0]  # Extract domain without port
    if host not in ALLOWED_HOSTS:
        abort(403)  # Forbidden

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

    # Execute if request is GET
    if request.method == "GET":
        full_filename =  'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename, text=None, error_message=None)

    # Execute if request is POST
    if request.method == "POST":
        # Check if an image is uploaded
        image_upload = request.files.get('image_upload')

        if image_upload:
            try:
                # Process uploaded image
                imagename = image_upload.filename
                image = Image.open(image_upload)

                # Converting image to array
                image_arr = np.array(image.convert('RGB'))
                # Converting image to grayscale
                gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
                # Converting image back to RGB
                image = Image.fromarray(gray_img_arr)

                # Generating unique image name for dynamic image display
                letters = string.ascii_lowercase
                name = ''.join(random.choice(letters) for i in range(10)) + '.png'
                full_filename = 'uploads/' + name

                # Extracting text from image
                custom_config = r'-l eng --oem 3 --psm 6'
                text = pytesseract.image_to_string(image, config=custom_config)

                # Remove unwanted symbols
                characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
                for character in characters_to_remove:
                    text = text.replace(character, "")

                # Converting string into list for separate lines
                text_lines = text.split("\n")
                text_lines = [line.strip() for line in text_lines if line.strip()]  # Removing empty lines

                # Save image for display
                img = Image.fromarray(image_arr, 'RGB')
                img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

                # Returning template with the image and extracted text
                return render_template('index.html', full_filename=full_filename, text=text_lines, error_message=None)
            except Exception as e:
                # If there is an error with image processing (e.g., invalid image format)
                print(f"Error processing image: {e}")
                full_filename = 'images/white_bg.jpg'
                return render_template('index.html', full_filename=full_filename, text=["No text extracted."], error_message=None)
        else:
            # If no image is uploaded, display the warning message
            full_filename = 'images/white_bg.jpg'
            return render_template('index.html', full_filename=full_filename, text=None, error_message="Please upload the image.")

# Main function
if __name__ == '__main__':
    app.run(debug=True)
    
