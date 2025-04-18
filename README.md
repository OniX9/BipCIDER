# BipCIDER

Welcome to 

██████╗░██╗██████╗░░█████╗░██╗██████╗░███████╗██████╗░
██╔══██╗██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██████╦╝██║██████╔╝██║░░╚═╝██║██║░░██║█████╗░░██████╔╝
██╔══██╗██║██╔═══╝░██║░░██╗██║██║░░██║██╔══╝░░██╔══██╗
██████╦╝██║██║░░░░░╚█████╔╝██║██████╔╝███████╗██║░░██║
╚═════╝░╚═╝╚═╝░░░░░░╚════╝░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝       
This repository contains a Python-based implementation for finding the seed phrase of an active BTC account.

Disclaimer: This is for educational purposes only. We are not responsible for any actions taken!

---

## Features

- Bruteforce different bip032 seed phrases.
- Use proxy servers as actors for peak speeds.
- Add email address for instant notification via SMTP
- Easy to set up and run.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- `pip` (Python package manager)

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/OniX9/BipCIDER.git
    cd bipcider
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create .env file:
    ```bash
    cat > .env
    ```
    Then press ***Enter***.

3. Add fill your email details into .env:
    ```.env
    GMAIL_APP_PASSWORD = Sender Gmail app password here
    EMAIL_FROM = sender...@gmail.com
    EMAIL_TO = "recieving email address"
    ```

---

## Usage

1. Navigate to the project directory:
    ```bash
    cd BipCIDER
    ```

2. Run the script:
    ```bash
    python3 main.py
    ```

3. Follow the on-screen instructions to start the mining simulation.

---

## How It Works

1. The script generates 12 random seed phrases.
2. Converts the seed phrases to a wallet address. 
2. Then checks the address's balance. 
3. The goal is to test the strength of btc wallets via seed phrases randomization.

---

## Successful Output Example

```plaintext
Press Ctrl+C to stop the process
Cycle 7 - Address: 141TRBKdYxPtPcG24bLbmDUXeai3ayCkpg, Balance: 0.0 BTC, Seed Phrase: attack fatigue key hidden sweet profit taste trick right lonely quarter defense
----------------------------------------
Total checks: 5032, Failed checks: 0, Success rate: 100.00%
Execution duration: 12.278784 seconds
```

---

## Disclaimer

This project is for **educational purposes only**. Use responsibly.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

Happy Bip-Ciding! 🚀