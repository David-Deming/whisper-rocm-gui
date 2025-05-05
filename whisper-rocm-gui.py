import whisper
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import warnings
import queue

warnings.filterwarnings("ignore", category=UserWarning)

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"

def show_progress(root, message):
    win = tk.Toplevel(root)
    win.title("Please wait...")
    tk.Label(win, text=message).pack(pady=10)
    bar = ttk.Progressbar(win, mode='indeterminate')
    bar.pack(padx=20, pady=10, fill="x")
    bar.start()
    root.update()
    return win

def transcribe_audio(file_path, model_size, output_dir, root):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, base_name + ".txt")

    if os.path.exists(output_path):
        overwrite = messagebox.askyesno("File Exists", f"{output_path} already exists.\nOverwrite?")
        if not overwrite:
            messagebox.showinfo("Aborted", "Transcription canceled.")
            return

    progress_win = show_progress(root, "Transcribing... please wait.")
    done_queue = queue.Queue()

    def run():
        try:
            model = whisper.load_model(model_size).to("cuda")
            result = model.transcribe(file_path, verbose=False, language='en')

            with open(output_path, "w", encoding="utf-8") as f:
                for segment in result["segments"]:
                    start = format_timestamp(segment["start"])
                    end = format_timestamp(segment["end"])
                    text = segment["text"].strip()
                    f.write(f"[{start} --> {end}] {text}\n")

            done_queue.put(("success", output_path))
        except Exception as e:
            done_queue.put(("error", str(e)))

    def check_done():
        try:
            status, payload = done_queue.get_nowait()
            progress_win.destroy()
            if status == "success":
                messagebox.showinfo("Done", f"Transcription saved to:\n{payload}")
            else:
                messagebox.showerror("Error", f"An error occurred:\n{payload}")
        except queue.Empty:
            root.after(100, check_done)

    threading.Thread(target=run, daemon=True).start()
    root.after(100, check_done)

def get_model_popup(root):
    popup = tk.Toplevel(root)
    popup.title("Select Whisper Model")
    tk.Label(popup, text="Choose model size:").pack(pady=5)

    model_var = tk.StringVar(value="base")
    models = ["tiny", "base", "small", "medium", "large"]
    model_dropdown = ttk.Combobox(popup, textvariable=model_var, values=models, state="readonly")
    model_dropdown.pack(pady=5)

    def confirm():
        popup.model_choice = model_var.get()
        popup.destroy()

    tk.Button(popup, text="OK", command=confirm).pack(pady=10)
    popup.grab_set()
    root.wait_window(popup)

    return getattr(popup, "model_choice", "base")

def gui_mode():
    root = tk.Tk()
    root.withdraw()

    audio_file = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac *.ogg *.webm")]
    )
    if not audio_file:
        messagebox.showwarning("No File", "No audio file selected.")
        return

    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        messagebox.showwarning("No Folder", "No output folder selected.")
        return

    model_size = get_model_popup(root)
    transcribe_audio(audio_file, model_size, output_dir, root)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("This version uses a GUI. Just run: python whisper_rocm_gui.py")
        sys.exit(1)
    gui_mode()
