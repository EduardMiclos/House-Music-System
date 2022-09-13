class VoiceCommand:
    def __init__ (self, callback: object, audio_path: str, text: str = None) -> None:
        self.text = text
        self.callback = callback
        self.audio_path = audio_path
