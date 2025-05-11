const { spawn } = require('child_process');
const { ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

let recordedChunks = [];
let mediaRecorder = null;

document.getElementById('modeSelect').addEventListener('change', (e) => {
  const mode = e.target.value;
  document.getElementById('fileInputSection').style.display = mode === 'file' ? 'block' : 'none';
  document.getElementById('recordSection').style.display = mode === 'record' ? 'block' : 'none';
});

document.getElementById('browseBtn').addEventListener('click', async () => {
  const dir = await ipcRenderer.invoke('select-directory');
  if (dir) {
    document.getElementById('outputDir').value = dir;
  }
});

document.getElementById('startRecording').addEventListener('click', async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recordedChunks = [];
  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = e => recordedChunks.push(e.data);
  mediaRecorder.onstop = () => {
    const blob = new Blob(recordedChunks, { type: 'audio/webm' });
    const fileReader = new FileReader();

    fileReader.onload = () => {
      const tempPath = path.join(__dirname, 'recorded_audio.webm');
      fs.writeFileSync(tempPath, Buffer.from(new Uint8Array(fileReader.result)));
      handleRenameModal(tempPath);
    };

    fileReader.readAsArrayBuffer(blob);
  };

  mediaRecorder.start();
  document.getElementById('recordingStatus').textContent = "Recording...";
  document.getElementById('stopRecording').disabled = false;
});

document.getElementById('stopRecording').addEventListener('click', () => {
  if (mediaRecorder) {
    mediaRecorder.stop();
    document.getElementById('recordingStatus').textContent = "Recording stopped.";
    document.getElementById('stopRecording').disabled = true;
  }
});

document.getElementById('transcribeBtn').addEventListener('click', () => {
  const fileInput = document.getElementById('audioInput');
  if (!fileInput.files.length) {
    alert("Please select an audio file.");
    return;
  }
  const filePath = fileInput.files[0].path;
  handleRenameModal(filePath);
});

function handleRenameModal(audioPath) {
  const outputDir = document.getElementById('outputDir').value;
  const modelSize = document.getElementById('modelSelect').value;

  if (!outputDir || !modelSize) {
    alert("Please select both output directory and model.");
    return;
  }

  const baseName = path.parse(audioPath).name;
  let outputFileName = baseName + ".txt";
  let outputFilePath = path.join(outputDir, outputFileName);

  const modal = document.getElementById("renameModal");
  const input = document.getElementById("newFileName");
  const confirm = document.getElementById("confirmRename");
  const cancel = document.getElementById("cancelRename");

  input.value = baseName;
  modal.style.display = "block";

  confirm.onclick = () => {
    const newName = input.value.trim();
    if (!newName) {
      alert("Filename cannot be empty.");
      return;
    }
    outputFileName = newName + ".txt";
    modal.style.display = "none";
    runTranscription(audioPath, modelSize, outputDir, outputFileName);
  };

  cancel.onclick = () => {
    modal.style.display = "none";
    alert("Transcription canceled.");
  };
}

function runTranscription(audioPath, modelSize, outputDir, outputFileName) {
  const pythonPath = path.join(__dirname, 'venv', 'bin', 'python');

  const python = spawn(pythonPath, [
    'whisper_backend.py',
    audioPath,
    modelSize,
    outputDir,
    '--output_filename',
    outputFileName
  ]);

  python.stdout.on('data', data => {
    try {
      const response = JSON.parse(data.toString());
      if (response.status === 'success') {
        alert(`Transcription saved at:\n${response.output_file}`);
      } else {
        alert(`Error:\n${response.message}`);
      }
    } catch (e) {
      console.error("Failed to parse Python output:", e);
    }
  });

  python.stderr.on('data', data => {
    console.error("Python error:", data.toString());
  });

  python.on('close', code => {
    console.log(`Python process exited with code ${code}`);
  });
}
