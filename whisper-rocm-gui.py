import whisper
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import warnings

# Suppress non-critical warnings
warnings.filterwarnings("ignore", category=UserWarning)

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"

def transcribe_audio(file_path, model_size, output_dir):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, base_name + ".txt")

    if os.path.exists(output_path):
        overwrite = messagebox.askyesno("File Exists", f"{output_path} already exists.\nOverwrite?")
        if not overwrite:
            messagebox.showinfo("Aborted", "Transcription canceled.")
            return

    print(f"Loading model: {model_size}")
    model = whisper.load_model(model_size).to("cuda")

    result = model.transcribe(file_path, verbose=False, language='en')

    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"[{start} --> {end}] {text}\n")

    messagebox.showinfo("Done", f"Transcription saved to:\n{output_path}")

def gui_mode():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    # Pick audio file
    audio_file = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.flac *.ogg *.webm")])
    if not audio_file:
        messagebox.showwarning("No File", "No audio file selected.")
        return

    # Pick output directory
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        messagebox.showwarning("No Folder", "No output folder selected.")
        return

    # Ask for model size
    def get_model():
        popup = tk.Tk()
        popup.title("Select Whisper Model")
        tk.Label(popup, text="Choose model size:").pack(pady=5)
        model_var = tk.StringVar(value="base")
        models = ["tiny", "base", "small", "medium", "large"]
        model_dropdown = ttk.Combobox(popup, textvariable=model_var, values=models, state="readonly")
        model_dropdown.pack(pady=5)

        def confirm():
            popup.model_choice = model_var.get()
            popup.destroy()

        tk.Button(popup, text="OK", command=confirm).pack(pady=5)
        popup.mainloop()
        return getattr(popup, "model_choice", "base")

    model_size = get_model()
    transcribe_audio(audio_file, model_size, output_dir)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("This version uses GUI. Just run: python amd_gui.py (no arguments).")
        sys.exit(1)
    gui_mode()
