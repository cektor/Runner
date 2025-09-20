<a href="#">
    <img src="https://raw.githubusercontent.com/pedromxavier/flag-badges/main/badges/TR.svg" alt="made in TR">
</a>

# Runner
This application allows you to run an Internet Speed Test and see test measurements. Cross Platform Operable with Graphical User Interface..

<h1 align="center">Runner Logo</h1>

<p align="center">
  <img src="runnerlo.png" alt="Runner Logo" width="150" height="150">
</p>


----------------------

# Linux Screenshot
![Linux(pardus)](screenshot/runner_linux.png)  

# Windows Screenshot
![Windows(11)](screenshot/runner_windows.png) 

--------------------
Install Git Clone and Python3

Github Package Must Be Installed On Your Device.

git
```bash
sudo apt install git -y
```

Python3
```bash
sudo apt install python3 -y 

```

pip
```bash
sudo apt install python3-pip

```

# Required Libraries

PyQt5
```bash
pip install PyQt5
```
PyQt5-sip
```bash
pip install PyQt5 PyQt5-sip
```

PyQt5-tools
```bash
pip install PyQt5-tools
```

Required Libraries for Debian/Ubuntu
```bash
sudo apt-get install python3-pyqt5
sudo apt-get install qttools5-dev-tools
```
speedtest-cli
```bash
pip install speedtest-cli
```

----------------------------------


# Installation
Install Runner

```bash
sudo git clone https://github.com/cektor/Runner.git
```
```bash
cd Runner
```

```bash
python3 runner.py

```

# To compile

NOTE: For Compilation Process pyinstaller must be installed. To Install If Not Installed.

pip install pyinstaller 

Linux Terminal 
```bash
pytohn3 -m pyinstaller --onefile --windowed runner.py
```

Windows VSCode Terminal 
```bash
pyinstaller --onefile --noconsole runner.py
```

MacOS VSCode Terminal 
```bash
pyinstaller --onefile --noconsole runner.py
```

# To install directly on Windows or Linux





Linux (based debian) Terminal: Linux (debian based distributions) To install directly from Terminal.
```bash
wget -O Setup_Linux64.deb https://github.com/cektor/Runner/releases/download/1.00/Setup_Linux64.deb && sudo apt install ./Setup_Linux64.deb && sudo apt-get install -f -y
```

Windows Installer CMD (PowerShell): To Install from Windows CMD with Direct Connection.
```bash
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cektor/Runner/releases/download/1.00/Setup_Win64.exe' -OutFile 'Setup_Win64.exe'; Start-Process -FilePath '.\Setup_Win64.exe' -Wait"

```

Release Page: https://github.com/cektor/Runner/releases/tag/1.00

----------------------------------
