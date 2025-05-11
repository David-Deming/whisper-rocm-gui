import whisper
import os
import sys
import argparse
import json

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
        print(json.dumps({"status": "error", "message": f"{output_path} already exists."}))
        return

    try:
        model = whisper.load_model(model_size)
        model = model.to("cuda")
        result = model.transcribe(file_path, verbose=False, language='en')

        with open(output_path, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()
                f.write(f"[{start} --> {end}] {text}\n")

        print(json.dumps({"status": "success", "output_file": output_path}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio using Whisper.")
    parser.add_argument("file_path", help="Path to the audio file")
    parser.add_argument("model_size", help="Size of Whisper model (e.g., base, small, medium)")
    parser.add_argument("output_dir", help="Directory to save the transcription")

    args = parser.parse_args()

    transcribe_audio(args.file_path, args.model_size, args.output_dir)
