#!/usr/bin/env bash
set -euo pipefail
python3 -c 'import sys; assert sys.version_info[:2] == (3,14), "This lab requires Python 3.14"'
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
