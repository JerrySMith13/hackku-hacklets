import os
import platform
import subprocess

def speakMerlin(text: str):
    """
    Generate and play TTS audio that mimics an old man's voice using espeak.

    :param text: The text to convert to speech.
    """
    try:
        # Customize espeak parameters for an old man's voice
        pitch = 50  # Lower pitch for a deeper voice
        speed = 100  # Slow down the speech
        voice = "en+m7"  # Use a male voice (f4 is a deeper male voice)

        # Construct the espeak command
        command = f'espeak -p {pitch} -s {speed} -v {voice} "{text}"'

        # Execute the command based on the OS
        if platform.system() == "Windows":
            subprocess.Popen(command, shell=True)
        else:  # macOS and Linux
            subprocess.Popen(command, shell=True)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    speakMerlin("Hello! I am the great merlin")
    print("Trying to print wiuthhothu blocking")