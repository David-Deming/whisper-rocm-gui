# Whisper ROCm GUI

**Whisper ROCm GUI** is a simple Python script that transcribes audio files using OpenAI's Whisper, installed from their official source. It allows you to use an AMD GPU instead of an nvidia GPU. This has been tested and works on my 7900xtx and also a 6950xt. Please let me know if you have any issues, anyone wanting to help is welcome to help improve this and add new features.

I built it because nvidia is a pain and I wanted to use my **AMD GPU** since my CPU was taking forever. 

It uses a semi user friendly GUI built with `tkinter`.  
Its a bit rough around the edges from a UI standpoint but it gets the job done... mostly. 

So far its only been tested inside various distroboxes on a fedora silverblue gaming PC. Yes I am aware, weird choice of machine to develop anything on, my laptop finally died and I was too lazy to dual boot a normal fedora install. 

Use at your own risk, this has not been thouroughly tested. You should never run scripts from the internet without reading them, so read my scripts first. 
yes, that includes you, who knows I could be a total dick

---

## Plans for the Future

- [ ] Polish the GUI or maybe switch to something nicer than `tkinter`
- [ ] Make the setup smoother for non-technical users
- [ ] Test in more environments
- [ ] add in ability to record sound to pass to whisper (push to talk?)
- [ ] other fun stuff

---

## Requirements

- Python 3.9+
- ROCm-compatible AMD GPU. I am using a 7900xtx
- PyTorch ROCm build
- Whisper installed from OpenAI's official repo at https://github.com/openai/whisper
- `ffmpeg`
- `tkinter`

---

## Installation

1. Clone this repo and get setup:
    ```bash
    git clone https://github.com/david-cant-code/whisper-rocm-gui.git
    ```
   ```bash
    cd whisper-rocm-gui
   ```
    ```bash
    chmod +x setup.sh
    ```

2. Run the setup script:
    ```bash
    ./setup.sh
    ```

3. Or read the script first and manually install things
    - System packages:
        - **Debian (APT)**: `python3 python3-pip python3-venv python3-tk ffmpeg git`
        - **Fedora (DNF)**: `python3 python3-pip python3-virtualenv python3-tkinter ffmpeg git`

---

## Usage

```bash
source venv/bin/activate
python whisper-rocm-gui.py
