# WebCrawler

## Setup
- Configure WSL on windows system, follow tutorial here: 
    1. Run this in your Command Prompt in administrator mode: **dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart**
    2. Restart your computer
    3. Download ubuntu from microsoft store
    4. Initialize ubuntu
        Run these commands: 
            a. **sudo apt update**
            b. **sudo apt upgrade**

- Install Python if you haven't: Run these commands on Ubuntu Terminal
    1. sudo apt install python3
    2. python3 --version
    3. sudo apt install python3-pip

- Create a virtual environment by running the command: **python -m venv yourenvironmentname**
- Activate your environment by: **source yourenvironmentname/bin/activate**


- Install requirements.txt file: **pip install -r requirements.txt**