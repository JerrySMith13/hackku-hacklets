import subprocess
from merlin import Response, MerlinClient
from enum import Enum
import os
from errorstuff import Err, LogCommandOutput
def block_until_key(signal) -> bool:
    if input() == signal:
        return False
    else:
        return True

class RunSignal(Enum):
    EXIT_SUCCESSFUL = 0
    EXIT_UNSUCCESSFUL = 1
    FIX_ERR_WITH_MERLIN = 2
    EXIT_ABORTED = 3
        
def run_response(res: Response, client: MerlinClient, prompt: str, checkBeforeExecution: bool=False) -> tuple[RunSignal, ]:

    current_dir = os.getcwd()
    command_results: list[tuple[str, str]] = []
    
    print(res.intro + "\n")
    for i in range(len(res.commands)):
        command = res.commands[i]
        message = res.line_by_line[i]
        if checkBeforeExecution:
            print("Ok to run '{}'? (press 'N' key to abort)")
            if not block_until_key('N'):
                return (RunSignal.EXIT_ABORTED)
            
        print(f"Current command: {message} | Would you like to run it? (press 'N' to skip, 'Enter' to run)")
        if not block_until_key("N"):
            continue  # Skip this command if 'N' is pressed
        
        if 'cd' in command.strip():
            try:
                # Extract the target directory
                target_dir = command.split('cd ', 1)[1].strip()
                # Handle relative paths
                new_dir = os.path.join(current_dir, target_dir)
                # Update and change to new directory
                os.chdir(new_dir)
                current_dir = os.getcwd()
                print(f"Changed directory to: {current_dir}")
                continue
            except Exception as e:
                print(f"Error changing directory: {e}")
                return (RunSignal.FIX_ERR_WITH_MERLIN, Err(command, str(e), ""))
        
        result = subprocess.run(command, shell=True, check=False, capture_output=True, cwd=current_dir)
        if result.returncode != 0:
            errmsg = result.stderr
            out = result.stdout
            print("Error happened while running the following command:")
            print(command)
            print("Would you like Merlin to fix it? (press N for no)")
            if not block_until_key('N'):
                return (RunSignal.EXIT_UNSUCCESSFUL, None)
            else:
                return (RunSignal.FIX_ERR_WITH_MERLIN, Err(command, errmsg, out))
        
        command_output = result.stdout.decode('utf-8') if hasattr(result.stdout, 'decode') else str(result.stdout)
        print(command_output)
        command_results.append((command, command_output))

        
    print(res.conclusion, end='\n\n')
    logobj = LogCommandOutput((prompt, res.intro, res.conclusion), command_results)
    client.add_to_history(logobj)
    return (RunSignal.EXIT_SUCCESSFUL, None)
            
                    
                        
                
                    
            
            
    