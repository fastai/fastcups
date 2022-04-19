# Installation

Execute `pip install -r requirements.txt` in the root of the repository.

In production increase the open file limit by running `ulimit -n 1000000` and verify by executing `ulimit -a` (one new connection == one new open file).

# Running the server

Execute `python 3cups.py` in the root of the repository.

Open a couple of tabs navigating to localhost:5000/student and one navigating to localhost:5000/teacher. Press a couple of the "buttons" at the bottom of the screen and see what happens :)
