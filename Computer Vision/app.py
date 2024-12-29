from flask import Flask, render_template, request, send_from_directory, redirect, url_for # type: ignore
import cv2
import numpy as npX
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

# Define image processing functions
def edge_detection(image):
    return cv2.Canny(image, 100, 200)

def sharpen(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def smooth(image):
    return cv2.GaussianBlur(image, (9, 9), 0)

def grey_level_transform(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Route for main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and filter processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    # Read the image
    image = cv2.imread(filepath)
    
    # Apply the selected filter
    filter_type = request.form['filter']
    if filter_type == 'edge_detection':
        result = edge_detection(image)
    elif filter_type == 'sharpen':
        result = sharpen(image)
    elif filter_type == 'smooth':
        result = smooth(image)
    elif filter_type == 'grey_level':
        result = grey_level_transform(image)
    else:
        return redirect(url_for('index'))
    
    # Save the processed image
    output_filename = f"processed_{file.filename}"
    output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
    if filter_type == 'grey_level':
        cv2.imwrite(output_path, result)
    else:
        cv2.imwrite(output_path, cv2.cvtColor(result, cv2.COLOR_GRAY2BGR))
    
    return redirect(url_for('processed_file', filename=output_filename))

# Route to serve processed image
@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
