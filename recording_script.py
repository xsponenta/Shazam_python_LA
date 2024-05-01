import tkinter as tk
import pyaudio
import wave
from threading import Thread

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILE = "output.wav"

class RecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Recorder")

        self.button = tk.Button(master, text="Tap to Record", command=self.start_recording, font=("Helvetica", 14), width=20, height=3)
        self.button.pack(pady=20)

        self.status_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.status_label.pack()

        self.is_recording = False

    def start_recording(self):
        self.button.config(state=tk.DISABLED)
        self.status_label.config(text="Listening to the tune...")
        self.is_recording = True
        Thread(target=self.record_audio).start()

    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if not self.is_recording:
                break
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILE, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.status_label.config(text="Done!")
        self.button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.is_recording = False

def main():
    root = tk.Tk()
    app = RecorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
