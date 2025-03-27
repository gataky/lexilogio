"""Synthesizes speech from the input string of text."""
import os
import csv
import re
import sys
from google.cloud import texttospeech
from google.cloud.texttospeech_v1 import SynthesizeSpeechResponse


ANKI_MEDIA_LOCATION = "/Users/jeff/Library/Application Support/Anki2/User 1/collection.media"

word_match = re.compile(r"(?P<name>[\w\s]+)\[")
# something wrong with treesitter? causing weird indentation.  the following line resets it to normal
_ = re.compile(r"\]")

class Synthesize:

    def __init__(self):
        self.client: texttospeech.TextToSpeechClient = texttospeech.TextToSpeechClient()

    def text(self,
            text: str,
            language_code: str="el-GR",
            language_name: str="el-GR-Standard-B",
            path: str=ANKI_MEDIA_LOCATION):

        input_text = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=language_name,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response: SynthesizeSpeechResponse = self.client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        # The response's audio_content is binary.
        filepath = f"{path}/{text}.mp3"
        with open(filepath, "wb") as f:
            _ = f.write(response.audio_content)
            print(f'++ {text}')

def media_exists(text: str, path: str=ANKI_MEDIA_LOCATION) -> bool:
    return os.path.exists(f"{path}/{text}.mp3")

def extract_word(line: list[str]) -> str | None:
    match = re.match(word_match, line[1])
    if match is None:
        return None
    group = match.groupdict()
    return group.get("name")

if __name__ == "__main__":

    filename = sys.argv[1]
    print(filename)

    synth = Synthesize()

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:

            # ignore meta lines
            if line[0][0] == '#':
                continue

            word = extract_word(line)
            if word and media_exists(word):
                print(f"** {word}")
                continue
            elif word is None:
                print(f"!! {word}")
                continue

            synth.text(word)
