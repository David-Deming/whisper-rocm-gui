# Whisper ROCm GUI

**Whisper ROCm GUI** is a simple Python script that transcribes audio files using OpenAI's Whisper, installed from their official source
I built it because nvidia is a pain and I wanted to use my **AMD GPU** since my CPU was taking forever

It uses a semi user friendly GUI built with `tkinter`.  
Its a bit rough around the edges from a UI standpoint but it gets the job done... mostly

So far its only been tested inside a debian based **distrobox** on a fedora silverblue gaming PC mostly because my laptop finally died and I was too lazy to dual boot a normal fedora install
now also in a fedora and ubuntu based one too

Use at your own risk, this has not been thouroughly tested. You should never run scripts from the internet without reading them, so read my scripts first
yes, that includes you, who knows I could be a total dick

---

## Plans for the Future

- [ ] Polish the GUI or maybe switch to something nicer than `tkinter`
- [ ] Make the setup smoother for non-technical users
- [ ] Test in more environments

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

1. Clone this repo:
    ```bash
    git clone https://github.com/david-deming/whisper-rocm-gui.git
    cd whisper-rocm-gui
    ```

2. Run the setup script:
    ```bash
    ./setup.sh
    ```

3. Or read the script first and manually install things
    - System packages:
        - **Debian (APT)**: `python3 python3-pip python3-venv python3-tk ffmpeg git`
        - **Fedora (DNF)**: `python3 python3-pip python3-virtualenv python3-tkinter ffmpeg git`
    - Python packages make sure to use a venv:
        ```bash
        pip install -r requirements.txt
        ```

---

## Usage

```bash
source whisper-venv/bin/activate
python whisper-rocm-gui.py
