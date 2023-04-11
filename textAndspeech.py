from google.cloud import speech
from google.cloud import texttospeech
import io

class testAndspeech:
    def __init__(self):
        self.ogg = "voice.ogg"
        self.textclient = speech.SpeechClient()
        self.speechclient = texttospeech.TextToSpeechClient()

    def stt(self):
        # The name of the audio file to transcribe
        with io.open(self.ogg, 'rb') as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
            enable_automatic_punctuation=True
        )

        # Detects speech in the audio file
        response = self.textclient.recognize(config=config, audio=audio)
        return response

    def tts(self, reply_message):

        input_text = texttospeech.SynthesisInput(text=reply_message)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
        )

        response = self.speechclient.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        return response
