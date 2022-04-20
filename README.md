# Installation

Execute `pip install -r requirements.txt` in the root of the repository.

In production increase the open file limit by running `ulimit -n 1000000` and verify by executing `ulimit -a` (one new connection == one new open file).

# Running the server

Execute `python 3cups.py` in the root of the repository.

Open a couple of tabs navigating to localhost:5000 and one navigating to localhost:5000/teacher. Press a couple of the "buttons" at the bottom of the screen and see what happens :)

*Important:* Do make sure to restart the server before every class! Otherwise, there exist (at least) two scenarios that otherwise will not be handled and will result in incorrect reporting on active counts:

* student keeping their tab open indefinitely and not showing up for subsequent class but being connected to the Internet at class time
* student powering off their laptop or losing Internet connection and us never receiving the disconnect event (I think these get timed out after a while but have not verified)

If we ever put any auth on the teacher interface, we might handle this more gracefully by adding a button to "reset class" which would clean the server state, but probably for now restarting the server is okay.
