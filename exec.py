import subprocess

def execute_command(command):
    """
    Executes a shell command and returns the output.
    
    :param command: The command to execute as a string or list of strings.
    :return: The output of the command as a string.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    
    
def main():
    # Example usage
    command = ["ls", "cd .venv"]  # Replace with your desired command
    output = execute_command(command)
    print(output)
    
    
if __name__ == "__main__":
    main()