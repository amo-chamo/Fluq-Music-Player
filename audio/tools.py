from mutagen import File
import os

from pydub import AudioSegment


def read_binary_file(file_path: str):
    with open(file_path, "rb") as file:
        data = file.read()
    return data


def get_audio_duration(path):
    audio = File(path)
    if audio is None or not hasattr(audio, 'info'):
        raise ValueError("Unsupported or corrupted audio file.")
    return int(audio.info.length)


def convert_wav_to_ogg(input_folder: str = "in-WAV", output_folder: str = "out-OGG", bitrate: str = "320k"):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        if file.endswith(".wav"):
            print(f"Converting {file}...")
            wav_path = os.path.join(input_folder, file)
            ogg_filename = os.path.splitext(file)[0] + ".ogg"
            ogg_path = os.path.join(output_folder, ogg_filename)

            audio = AudioSegment.from_wav(wav_path)
            audio.export(ogg_path, format="ogg", bitrate=bitrate)

            print(f"Successfully Converted: {file} -> {ogg_filename}\n")


if __name__ == '__main__':
    convert_wav_to_ogg()
