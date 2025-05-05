# Whisper ROCm GUI
Whisper ROCm GUI is a simple python script that transcribes audio files using OpenAI's Whisper. I made it because nvidia is a pain and I wanted to use my AMD card. It has a semi user friendly GUI using tkinter. It is very unpolished from a UI standpoint, but it does the job well enough. So far I have only tested this running inside a Debian based distrobox on my gaming PC running Fedora Silverblue, not for any real reason other than my laptop finally died.

Plans for the future:
·	Polish up the GUI, maybe use something prettier than tkinter
·	Set up script to get it running for non-technical users
·	Test for compatibility in different environments

Requirements
·	Python 3.9+
·	ROCm compatible AMD GPU
·	PyTorch 
·	Whisper without modifications installed from the official source

Installation:

