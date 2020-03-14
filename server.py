from flask import Flask, render_template, request, make_response
import werkzeug
import specto
import os
import time


app = Flask(__name__)

ALLOWED_EXTENSIONS = ['mp3', 'wav']
SOUND_DIRECTORY = 'files'
IMAGE_DIRECTORY = 'static'
SOUND_NAME = {'wav': 'sound.wav', 'mp3': 'sound.mp3'}
HTML_FILE = 'main.html'
error = {'format': 'Недопустимый формат файла!', 'file': 'Где-то произошла ошибка. Cкорее всего, файл не загружен.'}

def extension_check(filename):
    return filename.split('.')[-1] if '.' in filename else 'error'


def cleardir(dir):
    filelist = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith(".png")]
    for f in filelist:
        os.remove(os.path.join(IMAGE_DIRECTORY, f))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        cleardir(IMAGE_DIRECTORY) #очищаем папку с изображениями, чтобы не засорять сервер

        try:
            file_sound = request.files['sound']
            filename = werkzeug.secure_filename(file_sound.filename)
            extension = extension_check(filename)
            if extension in ALLOWED_EXTENSIONS:
                path_to_sound = os.path.join(SOUND_DIRECTORY, SOUND_NAME[extension])
                IMAGE_NAME = str(int(round(time.time() * 1000))) + '.png'  #Если так не делать, то кэшируется и показывается старая фотография
                path_to_image = os.path.join(IMAGE_DIRECTORY, IMAGE_NAME)
                file_sound.save(path_to_sound)
                specto.save_specgram(path_to_sound, path_to_image, extension)
                return render_template(HTML_FILE, spect=path_to_image)
            else:
                return render_template(HTML_FILE, error=error['format'])
        except Exception:
            return render_template(HTML_FILE, error=error['file'])



    if request.method == 'GET':
        return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)