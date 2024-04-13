from flask import Flask, request, jsonify,render_template, redirect, url_for
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok
import threading
import os
import subprocess

# Set your ngrok authtoken here
ngrok.set_auth_token('2ez4mG4qCQfLmKFJQBnkIMSAMsz_5AWBnChAwWYGhCWytJw4m')

app = Flask(__name__)
# run_with_ngrok(app)

# Setup ngrok
def start_ngrok():
    public_url = ngrok.connect(5000)
    print("ngrok tunnel \"{}\" -> \"http://127.0.0.1:5000\"".format(public_url))

# Start ngrok when app is run
threading.Thread(target=start_ngrok).start()

@app.route('/')
def index():
    image_folder = os.path.join(app.static_folder, 'images/model')
    image_filenames = [filename for filename in os.listdir(
        image_folder) if os.path.isfile(os.path.join(image_folder, filename))]
    image_folder_2 = os.path.join(app.static_folder, 'images/cloth')
    image_filenames_2= [filename for filename in os.listdir(
        image_folder_2) if os.path.isfile(os.path.join(image_folder_2, filename))]
    image_urls = [f'/static/images/model/{filename}' for filename in image_filenames]
    image_urls_1 = [f'/static/images/cloth/{filename}' for filename in image_filenames_2]
    
    
    return render_template('index.html', image_urls=image_urls, image_urls_1 = image_urls_1)

@app.route('/result')
def result():
    image_url = '/static/images/result/result.jpg' 
    return render_template('result.html', image_url=image_url)

@app.route('/convert',methods = ["POST"])
def convert_images():
    # Parse JSON data sent from the client
    data = request.get_json()
    filename1 = data.get('filename1')
    filename2 = data.get('filename2')
 ## python code ton convert the images and write the result in result.jpg
    # Debugging: print filenames to the console (server logs)
    print(f"Received filenames: {filename1}, {filename2}")

    with open('/content/drive/MyDrive/Capstone_Project/datasets/test_pairs.txt', 'w') as file:
        file.write(f"{filename1} {filename2}")

# Building the command to execute the Python script
    command = [
        "python", "/content/drive/MyDrive/Capstone_Project/test.py",
        "--name", "result",
        "--dataset_dir", "/content/drive/MyDrive/Capstone_Project/datasets/",
        "--checkpoint_dir", "/content/drive/MyDrive/Capstone_Project/checkpoints/",
        "--save_dir", "/content/drive/MyDrive/Capstone_Project/Image-Selector-main/Image-Selector-main/static/images"
    ]
    
    # Execute the command
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Script output:", result.stdout)
        return jsonify({
              'success': True,
              'message': 'Images processed successfully.'
          })

    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return jsonify({
            'success': False,
            'message': 'Failed to process images.',
            'error': str(e),
            'stderr': e.stderr
        })
    # # Return the result as JSON
    # return jsonify({
    #     'success': True,
    #     'message': 'Images processed successfully.'
    # })



if __name__ == '__main__':
    app.run()
