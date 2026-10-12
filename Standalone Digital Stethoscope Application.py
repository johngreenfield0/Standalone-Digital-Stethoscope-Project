# Standalone Digital Stethoscope Application for Raspberry Pi
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sounddevice as sd
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StethoscopeApp:
    def init(self, master):
        self.master = master
        self.device_index = self.find_usb_mic()
        self.duration = 30  # seconds
        self.fs = 44100  # Sampling frequency
        self.recorded_data = None

        self.build_ui()

    def find_usb_mic(self):
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if 'usb' in dev['name'].lower() or 'pnp' in dev['name'].lower():
                print(f"USB mic found at index {i}: {dev['name']}")
                return i
        messagebox.showerror("Error", "No USB microphone found.")
        raise RuntimeError("No USB microphone found.")

    def build_ui(self):
        self.master.title("Digital Stethoscope")
        self.master.geometry("900x700")
        self.master.configure(bg='white')

        self.status = tk.Label(self.master, text="Status: Idle", font=("Arial", 14), bg="white", fg="blue")
        self.status.pack(pady=10)

        btn_frame = tk.Frame(self.master, bg='white')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Record Heart Sound", bg="green", fg="white", font=("Arial", 12),
                  command=lambda: self.record_and_save("heart"), width=20).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(btn_frame, text="Record Lung Sound", bg="purple", fg="white", font=("Arial", 12),
                  command=lambda: self.record_and_save("lung"), width=20).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(btn_frame, text="Clear Plot", bg="red", fg="white", font=("Arial", 12),
                  command=self.clear_plot, width=20).grid(row=0, column=2, padx=10, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(9, 4), dpi=100)
        self.ax.set_title("Filtered Signal")
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Amplitude")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(pady=20)

    def bandpass_filter(self, data, lowcut, highcut):
        nyq = 0.5 * self.fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(4, [low, high], btype='band')
        return signal.filtfilt(b, a, data)

    def record_and_save(self, mode):
        if mode == "heart":
            lowcut, highcut = 20, 150
            filename = "heart.wav"
        else:
            lowcut, highcut = 100, 1000
            filename = "lung.wav"

        self.status.config(text=f"Recording {mode.capitalize()} Sound...", fg="red")
        self.master.update()

        try:
            recording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=1, dtype='float32',
                               device=self.device_index)
            sd.wait()

            data = recording.flatten()
            filtered = self.bandpass_filter(data, lowcut, highcut)
            normalized = np.int16(filtered / np.max(np.abs(filtered)) * 32767)

            wavfile.write(filename, self.fs, normalized)

            self.plot_waveform(filtered)
            self.status.config(text=f"{mode.capitalize()} Recording Saved to {filename}", fg="green")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Recording failed", fg="red")

    def plot_waveform(self, data):
        self.ax.clear()
        self.ax.plot(data, color='blue')
        self.ax.set_title("Filtered Signal")
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()

    def clear_plot(self):
        self.ax.clear()
        self.ax.set_title("Filtered Signal")
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()
        if name == "main":
    root = tk.Tk()
    app = StethoscopeApp(root)
    root.mainloop()