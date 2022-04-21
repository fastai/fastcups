# Installation

Execute `pip install -r requirements.txt` in the root of the repository.

In production increase the open file limit by running `ulimit -n 1000000` and verify by executing `ulimit -a` (one new connection == one new open file).

# Running the server

Execute `python fastcups.py` in the root of the repository.
