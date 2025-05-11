#!/bin/bash
echo ""
echo "Whisper ROCm GUI Setup Script"
echo ""
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "Remember, you should NEVER run a script that you got from the internet without reading it first"
echo "that means you should read this script before you run it, I could be an idiot and/or malicious"
echo "and the idiot option is likely"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
echo ""

# detect distro
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Cant figure out the OS, but dont worry buddy"
    echo "You can install dependencies manually"
    echo "Debian based (apt): sudo apt install python3.11 python3-pip python3.11-venv python3-tk ffmpeg git"
    echo "RHEL based (dnf): sudo dnf install python3.11 python3-pip python3.11-virtualenv python3-tkinter ffmpeg git"
    exit 1
fi

# install system packages
install_debian_packages() {
    echo "Installing packages for Debian/Ubuntu, enter password when prompted"
    echo "Dont forget to read the script first so you know what youre installing"
    sudo apt update
    sudo apt install -y python3.11 python3-pip python3.11-venv python3-tk ffmpeg git
}

install_fedora_packages() {
    echo "Installing packages for Fedora, enter password when prompted"
    echo "Dont forget to read the script first so you know what youre installing"
    sudo dnf install -y python3.11 python3-pip python3-virtualenv python3-tkinter ffmpeg git
}

if [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
    echo "Debian based:"
    read -p "Do you want to install required system packages now? (y/n): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        install_debian_packages
    else
        echo "Skipping package installation. You should install these on your own then:"
        echo "python3.11 python3-pip python3-venv python3-tk ffmpeg git"
    fi

elif [[ "$DISTRO" == "fedora" ]]; then
    echo "Fedora based:"
    echo "A recent Fedora update has started causing an selinux issue that is making this not work."
    echo "you should use a debian based system."
    echo "on Fedora, this will work inside a debain distrobox."
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo "it would be super cool if you want to help fix the fedora issue btw"
    sleep 2
    exit 1
    #read -p "Do you want to install required system packages now? (y/n): " confirm
    #if [[ "$confirm" =~ ^[Yy]$ ]]; then
    #    install_fedora_packages
    #else
    #    echo "Skipping package installation. You should install these on your own then:"
    #    echo "python3.11 python3-pip python3-virtualenv python3-tkinter ffmpeg git"
    #fi

else
    echo "Unsupported or undetected distribution, or I screwed up the script."
    echo "Please install dependencies manually:"
    echo "Debian (apt):    python3.11 python3-pip python3-venv python3-tk ffmpeg git"
    echo "Fedora (dnf):    python3.11 python3-pip python3-virtualenv python3-tkinter ffmpeg git"
    exit 1
fi

echo
read -p "Create and activate a Python virtual environment now? This will include installing whisper from the official github (y/n): " create_venv

if [[ "$create_venv" =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment (venv) in ./venv"
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt -c constraints.txt --extra-index-url https://download.pytorch.org/whl/rocm5.7
else
    echo "Skipping virtual environment setup. You can do it manually later:"
    echo "python3.11 -m venv venv"
    echo "source venv/bin/activate"
    echo "pip install -r requirements.txt -c constraints.txt --extra-index-url https://download.pytorch.org/whl/rocm5.7"
    echo "please contribute to the project to make it better for the next person"
fi
