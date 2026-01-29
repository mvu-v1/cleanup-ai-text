#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def cleanup(text: str) -> str:
    text = re.sub("–", "-", text)
    text = re.sub("—", ", ", text)
    text = re.sub(r" —", ",", text)
    text = re.sub("“", '"', text)
    text = re.sub("”", '"', text)
    text = re.sub("’", "'", text)
    text = re.sub("…", "...", text)
    text = re.sub("•", "*", text)
    text = re.sub(r"<2060>\s+<2060>", " ", text)
    return text


def cleanup_file(path: Path) -> None:
    if not path.is_file():
        return

    tmp = path.with_name(path.name + ".new")
    with path.open("r", encoding="utf-8", errors="replace") as reader, \
         tmp.open("w", encoding="utf-8", errors="replace") as writer:
        for line in reader:
            writer.write(cleanup(line))

    os.replace(tmp, path)


def cleanup_dir(dir_path: Path) -> None:
    if not dir_path.is_dir():
        return

    for entry in dir_path.iterdir():
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            cleanup_dir(entry)
        else:
            cleanup_file(entry)


def run_cli(paths: list[str]) -> int:
    if paths:
        for item in paths:
            p = Path(item)
            if p.is_dir():
                cleanup_dir(p)
            else:
                cleanup_file(p)
        return 0

    data = sys.stdin.read()
    if data:
        sys.stdout.write(cleanup(data))
    return 0

def run_web() -> int:
    import streamlit as st

    st.set_page_config(page_title="Text Cleanup", layout="wide")
    st.title("Text Cleanup")
    st.write("Paste your text on the left, click Clean, then copy from the right.")

    # Init state
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""
    if "cleaned_text" not in st.session_state:
        st.session_state["cleaned_text"] = ""

    col1, col2 = st.columns(2)

    with col1:
        st.text_area(
            "Input",
            key="input_text",
            height=320,
            placeholder="Paste text here...",
        )
        clicked = st.button("Clean", type="primary")

    # Important: update state BEFORE rendering the output box
    if clicked:
        st.session_state["cleaned_text"] = cleanup(st.session_state["input_text"])
        st.success("Done. Copy from the cleaned output box.")

    with col2:
        st.text_area(
            "Cleaned output",
            value=st.session_state["cleaned_text"],
            height=320,
        )

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Cleanup text (CLI + Streamlit UI).")
    parser.add_argument("--web", action="store_true", help="Launch Streamlit UI")
    # internal flag used when Streamlit re-runs the script
    parser.add_argument("--mode", choices=["cli", "web"], default="cli", help=argparse.SUPPRESS)
    parser.add_argument("paths", nargs="*", help="Files/dirs to clean in place. If none, read stdin.")
    args, _unknown = parser.parse_known_args()

    # If Streamlit is executing the script, we pass --mode web so it renders UI
    if args.mode == "web":
        return run_web()

    # If user asked for web, start Streamlit and pass --mode web to this script
    if args.web:
        try:
            import streamlit  # noqa: F401
        except Exception:
            print("Streamlit is not installed. Install it with: pip install streamlit", file=sys.stderr)
            return 2

        cmd = [
            sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__),
            "--", "--mode", "web"
        ]
        return subprocess.call(cmd)

    return run_cli(args.paths)


if __name__ == "__main__":
    raise SystemExit(main())

