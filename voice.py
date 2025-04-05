import whisper
import pyaudio
import numpy as np

# Initialize the real-time transcription system (using the default model)
model = whisper.load_model("base")

# Define audio parameters
RATE = 16000  # Sample rate (16kHz)
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Format for audio input (16-bit)
CHANNELS = 1  # Mono audio

# Set up PyAudio for capturing microphone input
p = pyaudio.PyAudio()

print(f"Device count:{p.get_default_input_device_info()}")  # This will list the number of audio devices available, can be used for debugging

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Start speaking...")

try:
    while True:
        # Capture audio data from the microphone
        audio_data = stream.read(CHUNK)

        # Convert audio data to a numpy array (required by realTimeSTT)
        audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

        # Perform speech-to-text on the audio chunk
        transcript = model.transcribe(audio_array)  # You can specify the language here, e.g., 'en' for English

        # Print the transcription result if any
        if transcript:
            print(f"Transcript: {transcript.get('text')}")

except KeyboardInterrupt:
    print("\nTerminating transcription...")
finally:
    # Close the microphone stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
