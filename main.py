import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Fajl saqlash joyi
UPLOAD_FOLDER = '/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fajl turi
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Fajl yuklash funksiyasi
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fajl yuklash funksiyasi
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Fajl yuklanmadi'
    file = request.files['file']
    if file.filename == '':
        return 'Fajl nomi bo\'lishi kerak'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Fajl yuklandi'

# Fajl yuklash uchun HTML sahifasi
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Fajl Yuklash</title>
    <style>
        #drop-zone {
            width: 300px;
            height: 200px;
            border: 2px dashed #ccc;
            border-radius: 5px;
            text-align: center;
            padding: 20px;
            margin: 20px;
        }
    </style>
</head>
<body>
    <h1>Fajl Yuklash</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" id="file">
        <label for="file">Fajl yuklash</label>
        <div id="drop-zone">Fajlni burayga surib yuklang</div>
        <input type="submit" value="Yuklash">
    </form>
    <script>
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('file');

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.style.background = 'lightblue';
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.style.background = '';
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.style.background = '';
            fileInput.files = e.dataTransfer.files;
        });

        fileInput.addEventListener('change', () => {
            dropZone.style.background = '';
        });
    </script>
</body>
</html>
