import whisper
import pyaudio
import numpy as np
import wave
import threading

# Load the Whisper model
model = whisper.load_model("base")

# Set up PyAudio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024

# Initialize PyAudio
p = pyaudio.PyAudio()

# Function to capture audio from the microphone
def record_audio():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)
    frames = []
    
    print("Recording... Press Ctrl+C to stop.")
    
    while True:
        try:
            data = stream.read(CHUNK_SIZE)
            frames.append(data)
        except KeyboardInterrupt:
            print("Recording stopped.")
            break
    
    # Convert recorded audio to a numpy array
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    return audio_data

# Function to transcribe audio in chunks
def transcribe_real_time():
    while True:
        audio_data = record_audio()  # Capture audio
        # Temporarily save to a file
        with wave.open('temp_audio.wav', 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_data.tobytes())
        
        # Transcribe the audio chunk
        result = model.transcribe("temp_audio.wav")
        transcription = result['text']
        
        # Print the transcription (can be updated or processed as needed)
        print(f"Transcription: {transcription}")

# Start the transcription in a separate thread to process continuously
transcription_thread = threading.Thread(target=transcribe_real_time)
transcription_thread.start()
