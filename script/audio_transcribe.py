import os
import subprocess
import io
import wave
from google.cloud import speech
from pydub import AudioSegment

# Set Google Cloud credentials (Update with your actual JSON file path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/paradox/Documents/github-singlecodehub/oasis-app-code/hoolimegpt/pathwell-datawarehouse-01fe36dffa1c.json"


def get_audio_properties(file_path):
    """Check sample rate and number of channels of an audio file."""
    with wave.open(file_path, "rb") as audio:
        sample_rate = audio.getframerate()
        channels = audio.getnchannels()
    return sample_rate, channels

def convert_audio(input_file, output_file="converted_audio.wav"):
    """Convert audio to mono, 16kHz, LINEAR16 format using FFmpeg."""
    try:
        command = [
            "ffmpeg", "-y", "-i", input_file,  # Input file
            "-ac", "1",  # Convert to mono
            "-ar", "16000",  # Resample to 16 kHz
            "-c:a", "pcm_s16le",  # LINEAR16 encoding
            output_file  # Output file
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_file
    except subprocess.CalledProcessError as e:
        print("FFmpeg conversion failed:", e)
        return None

def transcribe_audio(file_path):
    """Transcribe an audio file using Google Speech-to-Text API."""
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    audio = speech.RecognitionAudio(content=content)

    response = client.recognize(config=config, audio=audio)

    # Print and return transcription
    transcript = "\n".join([result.alternatives[0].transcript for result in response.results])
    return transcript if transcript else "No speech detected."

def main():
    input_audio = "/home/paradox/Downloads/harvard.wav"  # Update with your actual file path

    # Step 1: Check audio properties
    sample_rate, channels = get_audio_properties(input_audio)
    print(f"Original Audio: {sample_rate} Hz, {channels} channels")

    # Step 2: Convert if necessary
    if sample_rate != 16000 or channels != 1:
        print("Converting audio to mono, 16kHz...")
        converted_audio = convert_audio(input_audio)
    else:
        print("Audio is already in correct format. Skipping conversion.")
        converted_audio = input_audio

    # Step 3: Transcribe the converted audio
    print("Transcribing...")
    transcript = transcribe_audio(converted_audio)
    print("\nTranscription:\n", transcript)

if __name__ == "__main__":
    main()
