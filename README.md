# hackku-hacklets
To use Merlin, do the following:
1. Initialize a venv
   - You don't wanna install these beefy packages globally, so save some trouble and create/activate a venv.
   - You can do this by running the following command(s):
     ```bash
     python3 -m venv name
     ```
     On linux/mac:
     ```bash
     source ./name/bin/activate
     ```
     On Windows:
     ```batch
     ./name/Scripts/Activate.bat
     ```
   - Next, install dependencies from hackku-hacklets/requirements.txt
   - You can do this by running the following command:
     ```
     ./name/bin/pip3 install -r requirements.txt
     ```
   - Finally, run main-process.py from the virtual environment.
   - Do this by running:
     ```
     ./name/bin/python3 main-process.py
     ```
   - Ta-da! The project should open Merlin's terminal interface and start talking to you
     
     
     
