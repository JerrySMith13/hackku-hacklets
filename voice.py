import whisper
import sounddevice as sd
import numpy as np

model = whisper.load_model("base")  # Load the Whisper model

print(sd.query_devices())

sd.default.device = 18
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
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
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
    audio_data = np.squeeze(audio_data)  # Remove extra dimensions if necessary
    result = model.transcribe(audio_data, language='en')
    
    return result['text']

if __name__ == "__main__":
    print(transcribe_audio(record_audio(duration=5)))