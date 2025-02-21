import whisper

def set_whisper(model_name: str = "turbo"):
    return whisper.load_model(model_name)
    
model = set_whisper()
    
def transcribe_audio(file):
    return model.transcribe(file)