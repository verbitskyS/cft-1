import numpy
import scipy.io.wavfile
from pydub import AudioSegment
from tempfile import mktemp
import matplotlib.pyplot as plt

def get_wave_data(path):
    sample_rate, wave_data = scipy.io.wavfile.read(path)
    if isinstance(wave_data[0], numpy.ndarray):
        wave_data = wave_data.mean(1)
    return sample_rate, wave_data

def get_mp3_data(path):  #для построения спектрограммы для mp3 форматы нужно сначала конвертировать в wav
    mp3_audio = AudioSegment.from_file(path, format="mp3")  # read mp3
    wname = mktemp('.wav')  # испольуем временный файл
    mp3_audio.export(wname, format="wav")  #конвертируем в wav
    sample_rate, data = get_wave_data(wname)
    return sample_rate, data


def save_specgram(path_sound, path_image, extension='wav'):
    if extension == 'wav':
       sample_rate, data = get_wave_data(path_sound)
    elif 'mp3':
       sample_rate, data = get_mp3_data(path_sound)
    fig = plt.figure()
    cmap = plt.get_cmap('magma')
    plt.specgram(data, NFFT=256, pad_to=256, mode='magnitude', Fs=sample_rate, cmap=cmap)
    plt.xlabel('Время (с)')
    plt.ylabel('Частота (Гц)')
    plt.colorbar(format='%+2.0f dB')
    fig.savefig(path_image)




