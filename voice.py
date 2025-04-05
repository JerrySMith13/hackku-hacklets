import whisper
import sounddevice as sd
import numpy as np
import os

model = whisper.load_model("base")  # Load the Whisper model

print(sd.query_devices())

sd.default.device = int(input("Enter the device ID for the microphone: "))  # Set the default input device
sd.default.dtype = 'float16'  # Set the default data type for recording

sample_rate = sd.default.samplerate  # Use the default sample rate of the device
if sample_rate is None:
    sample_rate = 16000  # Fallback to a default sample rate if not set

def record_audio(duration=5):
    """
    Record audio from the microphone for a given duration.
    
    :param duration: Duration in seconds to record audio.
    :return: Recorded audio as a NumPy array.
    """
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float16')
    sd.wait()  # Wait until recording is finished
    print("Recording complete.")
    return audio_data  

def transcribe_audio(audio_data):
    """
    Transcribe audio data using the Whisper model.
    
    :param audio_data: NumPy array containing the recorded audio.
    :return: Transcribed text.
    """
    # Whisper expects the audio to be in a specific format, so we need to convert it to the correct format
    audio_data = np.squeeze(audio_data)
    audio_data = audio_data.astype(np.float32)
    result = model.transcribe(audio_data, language='en')    
    return result['text']

if __name__ == "__main__":
    try:
        print(transcribe_audio(record_audio(duration=5)))
    except Exception as e:
        print(f"An error occurred: {e}")
        os.system("pactl list short sources")
