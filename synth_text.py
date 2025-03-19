"""Synthesizes speech from the input string of text."""
import os
import csv
import re
from google.cloud import texttospeech


ANKI_MEDIA_LOCATION = "/Users/jeffor/Library/Application Support/Anki2/User 1/collection.media"

class Synthesize:

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def text(
            self,
            text: str,
            language_code: str="el-GR",
            language_name: str="el-GR-Standard-B",
            path: str=ANKI_MEDIA_LOCATION
        ):

        input_text = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=language_name,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        # The response's audio_content is binary.
        filepath = f"{path}/{text}.mp3"
        with open(filepath, "wb") as f:
            f.write(response.audio_content)
            print(f'{text} audio written to "{filepath}"')


def media_exists(text: str, path: str=ANKI_MEDIA_LOCATION) -> bool:
    return os.path.exists(f"{path}/{text}.mp3")


def extract_word(line: list[str]) -> str:
    return re.match(r"(?P<name>\w+)\[", line[1]).groupdict().get("name")

if __name__ == "__main__":

    synth = Synthesize()

    with open('test.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if line[0][0] == '#':
                continue
            word = extract_word(line)
            if media_exists(word):
                print(f"{word} exists")
                continue
            synth.text(word)
