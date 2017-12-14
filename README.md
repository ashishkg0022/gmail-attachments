# Gmail Attachment Downloader

This program is a Python script that downloads attachments found in the inbox of the user's Gmail account, based on a specific sender's address.

## Getting Started

### Prerequisites

- Python 2.5+

### Installing

1. Enable IMAP after logging in to your Google (Gmail) account.
2. Give permission to [less secure apps in Gmail](https://myaccount.google.com/lesssecureapps).
3. Download/clone repository.
4. Run `python gui.py`

[Note that a CLI-specific version has also been added; and can be used by : `python ga-cli.py`]

## Usage

- Interface presents you with Your e-mail, Password and Query e-mail fields.
- After correctly entering all the fields, hit Enter or click OK.
- Finally, it will download all attachments from the queried sender's emails onto the specific directory.
- You can view each email's contents from the list displayed.
- It will not download an attachment if it already exists in the directory.

## Built With

- Python
- QT 4
- The following packages from the Python 3 standard libraries:
  - [imaplib](https://docs.python.org/3/library/imaplib.html)
  - [email](https://docs.python.org/3/library/email.html)

