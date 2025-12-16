# c0308_btl_hk251

Project for SecureChat (assignment) and related research problems.

Overview
-
- `smc` — Main implementation of the SecureChat assignment (server/client, ECDH/ECDSA simulation and Burp extension helpers).
- `code` — Research-assignment code for individual problems:
	- `problem1b/` — Python implementation and Dockerfile for problem 1b.
	- `problem1c/` — `find_x.py` for problem 1c.
	- `problem2/` — multi-time-pad analysis (`multi_time_pad.py`) and ciphertexts.
- `report` — LaTeX source for the project report; building this produces `report.pdf` (main LaTeX file is `report/main.tex`).

Quick start
-
- Requirements: Python 3.8+ and typical LaTeX toolchain (e.g., `latexmk` or `pdflatex`).

- Run the SecureChat simulation (example):
	```powershell
	cd smc/legacy_code
	python smc.py
	```
	(See `smc/legacy_code/README.md` for more details and dependencies.)

- Build the LaTeX report (from repository root):
	```bash
	cd report
	latexmk -pdf main.tex
	```
	or
	```bash
	pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
	```

Notes
-
- The `smc` folder contains a `burp_ext/` directory with Burp extension scripts and an intercept server for testing.
- The `code/problem1b` contains a Dockerfile and `docker-compose.yml` to reproduce that task in a container.
- See `smc/legacy_code/requirements.txt` for Python package dependencies used by the SecureChat implementation.

If you want, I can:
- run the LaTeX build for `report/main.tex` now, or
- run the Python demo in `smc/legacy_code` to verify it runs locally.
