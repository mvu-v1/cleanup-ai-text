# PROGRAM NAME: PlainSight

## Text Cleanup Tool (CLI + Web UI)
--------------------------------

## What is PlainSight?

PlainSight is a small Python program that cleans up “smart typography” and awkward hidden characters that often appear when text comes from AI tools, Word/Docs, PDFs, or web pages.

These characters usually look normal to your eyes, but they can:

* break keyword searches and grep matches
* cause messy diffs in git
* make content look inconsistent across platforms
* leave “AI-ish” punctuation patterns in the text

PlainSight normalises that stuff into simple, predictable characters so your text is easier to search, copy, and reuse.

---

## Main Features

1. CLI mode (batch cleanup)

* Clean files in place
* Clean multiple files in one go
* Clean whole directories recursively
* Clean stdin and output to stdout (great for piping)

2. Web UI mode (Streamlit)

* Paste text into the browser
* Click Clean
* Copy the cleaned output

---

## What gets cleaned

PlainSight currently applies these replacements:

* –  becomes  -
* —  becomes  ,   (comma + space)
* " —" becomes  ,  (comma)
* “ and ” become "
* ’ becomes '
* … becomes ...
* • becomes *
* <2060> <2060> (with whitespace) becomes a normal space

You can change or add rules by editing the cleanup() function inside app.py.

---

## Requirements

Python:

* Python 3 (recommended 3.9+)

Web UI only:

* streamlit

CLI mode does not need any third-party packages.

---

## Install

Optional but recommended: create a virtual environment.

python3 -m venv venv
source venv/bin/activate

If you want the Web UI:

pip install streamlit

---

## How to run (CLI)

Clean one file (in place):
./app.py file.txt

Clean multiple files (in place):
./app.py file1.txt file2.txt

Clean directories recursively (in place):
./app.py dir1 dir2

Clean from stdin and print to stdout:
cat file.txt | ./app.py

Or:
./app.py < file.txt

Notes:

* directory cleanup is recursive
* hidden entries are skipped (names starting with a dot)
* cleaning files is in place, so keep backups if needed

---

## How to run (Web UI)

Start the browser UI:
./app.py --web

Streamlit will print a local URL, usually:
[http://localhost:8501](http://localhost:8501)

Workflow:

1. paste text into the Input box
2. click Clean
3. copy from the Cleaned output box

---

## How file edits work

For safety, PlainSight writes to a temporary file first:
originalname.ext.new

Then it replaces the original file.
This avoids half-written files, but it still overwrites the original content.

Tip: if the text matters, commit first or keep a backup.

---

## Troubleshooting

Web UI opens but output stays empty:

* make sure you clicked Clean
* try refreshing the page
* confirm streamlit is installed in the same environment you’re running ./app.py from

Streamlit not installed error:
pip install streamlit

---

## License

This project is licensed under the MIT License.

