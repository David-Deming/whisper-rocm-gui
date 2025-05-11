const { spawn } = require('child_process');
const { ipcRenderer } = require('electron');
const path = require('path');

document.getElementById('browseBtn').addEventListener('click', async () => {
  const dir = await ipcRenderer.invoke('select-directory');
  if (dir) {
    document.getElementById('outputDir').value = dir;
  }
});

document.getElementById('transcribeBtn').addEventListener('click', () => {
  const fileInput = document.getElementById('audioInput');
  const outputDir = document.getElementById('outputDir').value;
  const modelSize = document.getElementById('modelSelect').value;

  if (!fileInput.files.length || !outputDir || !modelSize) {
    alert("Please fill in all fields.");
    return;
  }

  const audioPath = fileInput.files[0].path;
  const pythonPath = path.join(__dirname, 'venv', 'bin', 'python');

  const python = spawn(pythonPath, ['whisper_backend.py', audioPath, modelSize, outputDir]);

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
});
