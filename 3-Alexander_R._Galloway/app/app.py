from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

TEX_FILES_DIR = os.path.join(os.getcwd(), 'static', 'txt_files')
print(TEX_FILES_DIR)

first_point = [
    "Universal Email Header Spoofer",
    "How To Hack Hotmail Passwords",
    "Confidential Business Proposal"
]

second_point = [
    "The Unknown Glitch",
    "Hitter",
    "Port Scanner",
    "Email Worm"
]

third_point = [
    "Perpetual Web Spider",
    "Fork bomb"
]

@app.route('/')
def index():
    return render_template('index.html', first_point=first_point, second_point=second_point, third_point=third_point)

@app.route('/file/<filename>')
def show_file(filename):
    
    files = os.listdir(TEX_FILES_DIR)
    print(f"filename = {filename}")
    file_extension = ""
    for file in files:
        file_name_without_extension = file.split('.')[0]
        if file_name_without_extension == filename:
            file_extension = '.' + file.split('.')[-1]
    
    original_filename = filename.replace(' ', '_') + file_extension
    file_path = os.path.join(TEX_FILES_DIR, original_filename)
    print(f"Searching for file: {original_filename}") 
    print(f"Full path to the file: {file_path}")  
    
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return render_template('content.html', content=file_content)
    except FileNotFoundError:
        return f"File not found: {original_filename}", 404

if __name__ == '__main__':
    app.run(debug=True)
