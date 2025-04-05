import whisper
import sounddevice as sd
import numpy as np

model = whisper.load_model("base")  # Load the Whisper model

# List available devices and set a valid device index
# print(sd.query_devices())
sd.default.device = 0  # Replace 0 with the index of your desired input device
sd.default.dtype = 'float16'  # Set the default data type for recording
sd.default.samplerate = 16000  # Set the default sample rate for recording

def record_audio(duration=5):
    """
    Record audio from the microphone for a given duration.
    
    :param duration: Duration in seconds to record audio.
    :return: Recorded audio as a NumPy array.
    """
    audio_data = sd.rec(int(duration * sd.default.samplerate), samplerate=sd.default.samplerate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
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
    print("Recording audio...")
    audio_data = record_audio(duration=5)
    print("Transcribing audio...")
    transcription = transcribe_audio(audio_data)
    print(f"Transcribed text: {transcription}")