import subprocess
from merlin import Response
from enum import Enum
import os
from errorstuff import Err
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
        
def run_response(res: Response, checkBeforeExecution: bool=False) -> tuple[RunSignal, ]:
    process_path = os.getcwd()
    
    print(res.intro + "\n")
    for i in range(len(res.commands)):
        command = res.commands[i]
        message = res.line_by_line[i]
        if checkBeforeExecution:
            print("Ok to run '{}'? (press 'N' key to abort)")
            if not block_until_key('N'):
                return (RunSignal.EXIT_ABORTED)
            
        print(f"Current command: {message}")
        block_until_key("")
        result = subprocess.run(command, shell=True, check=False, capture_output=True, cwd=os.getcwd())
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
        print(result.stdout.decode('utf-8') if hasattr(result.stdout, 'decode') else str(result.stdout))
                   
    return (RunSignal.EXIT_SUCCESSFUL, None)
            
                    
                        
                
                    
            
            
    