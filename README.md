# WebCrawler
## Description
The WebCrawler class is designed for scraping web content using either the requests library or Selenium WebDriver, with abstracted features such as randomizing request, header rotation, session management (requests), politness delay, logging. 
## Setup
### Step 1
- Configure WSL on windows system, follow tutorial here: 
    1. Run this in your Command Prompt in administrator mode: **dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart** OR install wsl from microsoft store
    2. Restart your computer, not needed if you download WSL from microsoft store.
    3. Download ubuntu from microsoft store.
    4. Initialize ubuntu
        Run these commands: 
            a. **sudo apt update**
            b. **sudo apt upgrade**

------------------------------------------------------------------------------------------------------------------------------
### Step 2
- Install Python if you haven't: Run these commands on Ubuntu Terminal.
    1. sudo apt install python3
    2. python3 --version
    3. sudo apt install python3-pip

------------------------------------------------------------------------------------------------------------------------------
### Step 3
- Create a virtual environment by running the command: **python -m venv yourenvironmentname**
- Activate your environment by: **source yourenvironmentname/bin/activate**


- Install requirements.txt file: **pip install -r requirements.txt**

- Make sure you have installed chrome or any chromium browser

------------------------------------------------------------------------------------------------------------------------------
### Step 4
- Refer example_request.py to have a look on how to make request using requests or selenium.

------------------------------------------------------------------------------------------------------------------------------