# Gmail Attachment Downloader

This program is a Python script that downloads attachments found in the inbox of the user's Gmail account, based on a specific sender's address.

## Getting Started

### Prerequisites

- Python 3

### Installing

1. Enable IMAP after logging in to your Google (Gmail) account.
2. Give permission to [less secure apps in Gmail](https://myaccount.google.com/lesssecureapps).
3. Download/clone repository.
4. Run `python3 script.py`

## Usage

- The program prompts the user for a Gmail login.
- Then it asks for the id of any other email account.
- Finally, it downloads all attachments from the sender's emails onto the user's computer.
- It will not download an attachment if it already exists in the folder.

## Built With

- Python 3
- The following packages from the Python 3 standard libraries:
  - [imaplib](https://docs.python.org/3/library/imaplib.html)
  - [email](https://docs.python.org/3/library/email.html)

