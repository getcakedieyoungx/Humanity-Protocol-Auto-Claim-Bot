# Auto Daily Claim $RWT Humanity Protocol Bot

## Introduction
This bot automates the daily claiming of $RWT rewards from the Humanity Protocol using multiple wallets. It is designed to be easy to set up and use.

## Getting Started

Follow these steps to set up and run the bot on your local machine.

### 1. Clone the Repository

To start, clone this repository to your local machine using Git:

```bash
git clone https://github.com/vinskasenda/HumanityTestnet-Bot.git
```

### 2. Change Directory to the Cloned Folder

Navigate to the folder where the repository was cloned:

```bash
cd HumanityTestnet-Bot
```

### 3. Create the private_keys.txt File
Create a private_keys.txt file in the root directory of the project. This file should contain one private key per line, like so:

```python
private_key_1
private_key_2
private_key_3
...
```

### 4. Install Required Dependencies
Make sure you have Python installed on your system. Then, install the required dependencies using the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 5. Run the Bot
Once everything is set up, you can run the bot with the following command:

```bash
python3 bot.py
```
