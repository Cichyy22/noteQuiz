import os
from wsgiref.util import FileWrapper

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import numpy as np
from scipy.io import wavfile
import plotly.graph_objects as go
from noteQuiz import settings
from pydub import AudioSegment
import tqdm
import subprocess
import base64


FPS = 30
FFT_WINDOW_SECONDS = 0.034
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FREQ_MIN = 10
FREQ_MAX = 1000
RESOLUTION = (1920, 1080)
SCALE = 2


def freq_to_number(f):
    return 69 + 12*np.log2(f/440.0)


def note_name(n):
    return NOTE_NAMES[n % 12] + str(int(n/12 - 1))


def plot_fft(p, xf, fs, notes, dimensions=(960, 540)):
    layout = go.Layout(
        title="Frequency Spectrum",
        autosize=False,
        width=dimensions[0],
        height=dimensions[1],
        xaxis_title="Frequency (note)",
        yaxis_title="Magnitude",
        font={'size': 24, 'color': 'white'},
        paper_bgcolor='black',
        plot_bgcolor='black',
        xaxis=dict(
            tickfont=dict(color='white'),
            title=dict(font=dict(color='white'))
        ),
        yaxis=dict(
            tickfont=dict(color='white'),
            title=dict(font=dict(color='white'))
        )
    )

    fig = go.Figure(layout=layout,
                    layout_xaxis_range=[FREQ_MIN, FREQ_MAX],
                    layout_yaxis_range=[0, 1]
                    )

    fig.add_trace(go.Scatter(
        x=xf,
        y=p,
        line=dict(color='white')
    ))

    for note in notes:
        note_name_with_freq = f"{note[1]} ({note[0]} Hz)"
        # Dodaj informacje o dźwięku
        fig.add_annotation(xref="paper", yref="paper",
                           x=0.9, y=0.9,
                           text=note_name_with_freq,
                           font={'size': 48, 'color': 'white'},
                           showarrow=False)
    return fig


def extract_sample(audio, frame_number, FRAME_OFFSET, FFT_WINDOW_SIZE):
    end = frame_number * FRAME_OFFSET
    begin = int(end - FFT_WINDOW_SIZE)

    if end == 0:
        # We have no audio
        return np.zeros((np.abs(begin)), dtype=float)
    elif begin < 0:
        # We have some audio, fill with zeros
        return np.concatenate([np.zeros((np.abs(begin)), dtype=float), audio[0:end]])
    else:
        # Return the next sample
        return audio[begin:end]


def find_top_notes(fft, num, xf):
    if np.max(fft.real) < 0.001:
        return []

    lst = [x for x in enumerate(fft.real)]
    lst = sorted(lst, key=lambda x: x[1], reverse=True)

    idx = 0
    found = []
    found_note = set()
    while (idx < len(lst)) and (len(found) < num):
        # if the index is in the bounds of xf
        if lst[idx][0] < len(xf):
            f = xf[lst[idx][0]]
            y = lst[idx][1]
            n = freq_to_number(f)
            if not np.isinf(n):  # if n is not infinity
                n0 = int(round(n))
                name = note_name(n0)
                if name not in found_note:
                    found_note.add(name)
                    s = [f, note_name(n0), y]
                    found.append(s)
        idx += 1
    return found


def proccess_audio(request):
    AudioSegment.ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"
    if request.method == 'POST':
        uploaded_file = request.FILES['audio_file']
        fs, audio = wavfile.read(uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        # Are MEDIA_ROOT exist
        media_root_dir = os.path.dirname(file_path)
        if not os.path.exists(media_root_dir):
            os.makedirs(media_root_dir)
        audio = audio.T[0]
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        FRAME_STEP = (fs / FPS)  # audio samples / video frame
        FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
        AUDIO_LENGTH = len(audio) / fs

        xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1 / fs)
        FRAME_COUNT = int(AUDIO_LENGTH * FPS)
        FRAME_OFFSET = int(len(audio) / FRAME_COUNT)

        # Maximum amplitude to scale.
        mx = 0
        for frame_number in range(FRAME_COUNT):
            sample = extract_sample(audio, frame_number, FRAME_OFFSET, FRAME_STEP)

            # window array == sample array
            window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, len(sample), False)))

            fft = np.fft.rfft(sample * window)
            fft = np.abs(fft).real
            mx = max(np.max(fft), mx)

        frame_directory = os.path.join(settings.MEDIA_ROOT, 'frames')

        if not os.path.exists(frame_directory):
            os.makedirs(frame_directory)
            # print(f"Utworzono katalog {frame_directory}")

        # Animation
        for frame_number in tqdm.tqdm(range(FRAME_COUNT)):
            sample = extract_sample(audio, frame_number, FRAME_OFFSET, FRAME_STEP)

            # Ensure that the window array has the same length as the sample array
            window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, len(sample), False)))

            fft = np.fft.rfft(sample * window)
            fft = np.abs(fft) / mx
            s = find_top_notes(fft, 1, xf)

            fig = plot_fft(fft.real, xf, fs, s, RESOLUTION)

            frame_path = os.path.join(settings.MEDIA_ROOT, 'frames', f"frame{frame_number}.png")

            # try:
            #     fig.write_image(frame_path, format='png', scale=2)
            #     print(f"Plik {frame_path} został zapisany.")
            # except Exception as e:
            #     print(f"Błąd podczas zapisywania pliku {frame_path}: {e}")
            fig.write_image(frame_path, format='png', scale=2)



        video_output = os.path.join(settings.MEDIA_ROOT, 'output.mp4')

        # frame_directory = os.path.join(settings.MEDIA_ROOT, 'frames')

        cmd = [
            'ffmpeg',
            '-y',
            '-r', str(FPS),
            '-f', 'image2',
            '-s', '1920x1080',
            '-i', os.path.join(frame_directory, 'frame%d.png'),  # Zmiana ścieżki do katalogu z klatkami
            '-i', file_path,  # Użyj oryginalnego pliku audio
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            video_output
        ]

        subprocess.run(cmd)
        for frame_number in range(FRAME_COUNT):
            frame_path = os.path.join(frame_directory, f"frame{frame_number}.png")
            os.remove(frame_path)
        video_url = os.path.join(settings.MEDIA_ROOT, 'output.mp4')

        if os.path.exists(video_url):
            with open(video_url, 'rb') as video_file:
                encoded_video = base64.b64encode(video_file.read()).decode('utf-8')
                return JsonResponse({'video': encoded_video})
        else:
            return JsonResponse({'error': 'Plik wideo nie istnieje.'}, status=404)

    return render(request, 'proccess_audio.html')
