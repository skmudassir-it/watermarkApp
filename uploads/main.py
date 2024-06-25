from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = "apple"
app.config['PIC'] = 'uploads'

photos = UploadSet('photos',IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators = [
            FileAllowed(photos, 'Only Images are Allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.rout('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['PIC'], filename)

@app.rout('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename = filename)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True)