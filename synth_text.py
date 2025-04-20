"""Synthesizes speech from the input string of text."""
import os
import os.path
import re
import sys
from google.cloud import texttospeech
from google.cloud.texttospeech_v1 import SynthesizeSpeechResponse
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID of your spreadsheet.
SPREADSHEET_ID = '1p39Sbnkx3G4swoSPJ2KKVKu-VwteKmaAQ9toFadd5cA'  # Replace with your spreadsheet ID
RANGE_NAME = 'Anki!A:Z'  # Replace with the desired sheet name and range
CERTS_JSON = '/Users/jeffor/Documents/lexilogio/bunes-282905-6d657cd60a3d.json'


ANKI_MEDIA_LOCATION = "/Users/jeff/Library/Application Support/Anki2/User 1/collection.media"
ANKI_MEDIA_LOCATION = "/Users/jeffor/Library/Application Support/Anki2/User 1/collection.media"

word_match = re.compile(r"(?P<name>[\w\s]+)\[")
# something wrong with treesitter? causing weird indentation.  the following line resets it to normal
_ = re.compile(r"\]")


def get_sheet_values() -> list[list[str]] | None:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        # This part is more relevant for user-based authentication.
        # For service accounts, we'll directly use the credentials file.
        pass
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the service account key file
            creds = Credentials.from_service_account_file(
                './bunes-282905-6d657cd60a3d.json', scopes=SCOPES) # Replace with the path to your JSON file

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Data:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
            # You can access individual cells like this: row[0], row[1], etc.
        return values

    except HttpError as err:
        print(f'An error occurred: {err}')
        return None


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

    synth = Synthesize()
    reader = get_sheet_values()
    if not reader:
        print("Could not get Anki sheet from cloud")
        sys.exit(1)

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
