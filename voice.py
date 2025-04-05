import whisper
import sounddevice as sd
import numpy as np

print(sd.query_devices())

sd.default.device = 18

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

sd.play(record_audio(5), samplerate=sample_rate, blocking=True)  # Record and play back for 5 seconds