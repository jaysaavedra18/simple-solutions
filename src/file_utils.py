# audio_io.py
"""Provides functions for audio input/output operations (read, write, concat)."""
import json
import os
import random

from pydub import AudioSegment

from audio_file import AudioFile

# Audio input/output functions

def get_audio_files(directory: str) -> list:
    """Retrieve a list of audio file names (MP3 and WAV) from the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith((".mp3", ".wav"))]


def get_audio_info(audio_files: list) -> tuple:
    """Calculate the total size (bytes) and length (seconds) of audio files."""
    # If a single file path is provided as a string, convert it to a list
    if isinstance(audio_files, str):
        audio_files = [audio_files]

    # Sum size and length of audio_files
    total_size = sum(os.path.getsize(file) for file in audio_files)
    total_length = sum(AudioSegment.from_file(file).duration_seconds for file in audio_files)
    return total_size, total_length


def concatenate_audio(selected_files: list, audio_directory: str) -> AudioSegment:
    """
    Concatenate multiple audio files specified in the 'selected_files' list into one AudioSegment.
    
    Notes:
    - The 'selected_files' list should contain the names of the audio files (e.g., ["file1.mp3", "file2.wav"]).
    - The concatenation order follows the order in the 'selected_files' list.
    """
    # Initialize an empty AudioSegment object to hold the concatenated audio
    concatenated_audio = AudioSegment.silent(duration=0)

    for file in selected_files:
        audio_path = os.path.join(audio_directory, file)
        audio_segment = AudioSegment.from_file(audio_path)
        concatenated_audio += audio_segment

    return concatenated_audio


def export_audio(audio: AudioSegment, file_path: str) -> None:
    """Export an AudioSegment object to an MP3 audio file at the specified file path."""
    audio.export(get_unique_file_name(file_path), format="mp3")

# text_io.py

# Text input/output functions

def read_text_blocks(file_path):
    """
    Read text blocks from a file and split them based on double line breaks.

    Args:
        file_path (str): The path to the file containing text blocks.

    Returns:
        list: A list of text blocks.

    Note:
        This function assumes that the file contains text blocks separated by
        two consecutive newline characters. If the file does not
        follow this format, the function behavior may not be as expected.

    """
    with open(file_path, "r") as file:
        text_blocks = file.read().split("\n\n")
        return text_blocks
    

def write_first_lines_to_file(text_blocks, output_file):
    """
    Write the first line of each text block in the input list to a specified output file.

    Parameters:
    text_blocks (list): A list of text blocks, where each block is a string with one or more lines.
    output_file (str): The path to the output file where the first lines will be written.

    Notes:
    - The output file is overwritten if it already exists; if it doesn't exist, it will be created.
    """
    with open(output_file, "w") as file:
        for text_block in text_blocks:
            lines = text_block.split("\n")
            first_line = lines[0].strip()
            if first_line:
                file.write(first_line + "\n")


def get_unique_file_name(file_path):
    """
    Generate a unique file name by adding a counter suffix to the base file name if the file already exists.

    Parameters:
    file_path (str): The original file path for which a unique name is needed.

    Returns:
    str: A unique file path based on the input 'file_path', ensuring that the file does not already exist
    in the specified location.
    """
    base_name, extension = os.path.splitext(file_path)
    unique_path = file_path
    counter = 1

    while os.path.exists(unique_path):
        unique_path = f"{base_name} ({counter}){extension}"
        counter += 1

    return unique_path


def parse_text_block_into_song(text):
    """
    Parse a text block containing song information and extract relevant details.

    Parameters:
    text (str): A text block containing multiple lines of song information.

    Returns:
    dict: A dictionary containing the extracted song details, including song name, artist name,
    artist link, and licenses.

    Notes:
    - The input 'text' parameter is expected to be a string with multiple lines, where the first line is
      in the format "Song Name by Artist | Artist Link".
    - The resulting dictionary includes the extracted details under the keys: "song_name", "artist_name",
      "artist_link", and "licenses".
    """
    lines = text.strip().split('\n')

    # Extract song name, artist name, and artist link from the first line
    song_info = lines[0].split(' by ')
    song_name = song_info[0].strip()
    artist_info = song_info[1].split(' | ')
    artist_name, artist_link = artist_info[0].strip(), artist_info[1].strip()

    # Extract licenses from lines 2 to 4 (if they exist) as a list
    licenses = [line.strip() for line in lines[1:4]]

    return {
        "song_name": song_name,
        "artist_name": artist_name,
        "artist_link": artist_link,
        "licenses": licenses
    }


# json_io.py

# JSON/object input/output functions

def write_json(objects, file_path):
    """
    Serialize a list of objects and write the JSON representation to a file.

    Parameters:
    objects (list): A list of objects to be serialized to JSON.
    file_path (str): The file_path (including the file name) where the JSON data will be written.
    """
    # Serialize to JSON
    json_data = [vars(obj) if not callable(
        getattr(obj, "to_dict", None)) else obj.to_dict() for obj in objects]

    # Write JSON data to the file
    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)


def read_json(file_path, target_class):
    """
    Read JSON data from a file and convert it into a list of objects of the specified class.

    Parameters:
    file_path (str): The path to the JSON file to be read.
    target_class (class): The class to which the JSON data should be converted.

    Returns:
    list: A list of objects of the specified class, created from the JSON data in the file.
    If the JSON file is empty or invalid, an empty list is returned.
    """
    try:
        with open(file_path, "r") as json_file:
            loaded_data = json.load(json_file)
            # print("Loaded Data:", loaded_data)  # Print loaded data
    except (json.JSONDecodeError, FileNotFoundError):
        return []

    loaded_objects = []
    for data in loaded_data:
        if "songs" in data:
            songs = [AudioFile(**song_data) for song_data in data["songs"]]
            data["songs"] = songs
        loaded_objects.append(target_class(**data))

    return loaded_objects




# file_io.py

# General file input/output functions

def select_random_files(file_path, file_count):
    """
    Selects a specified number of random files from a directory.

    Args:
        file_path (str): Path to the directory containing the files.
        file_count (int): The number of random files to select.

    Returns:
        list: A list of randomly selected file names.
    """
    files = [f for f in os.listdir(file_path) if f.endswith(
        ".mp3") or f.endswith(".wav")]
    return random.sample(files, file_count)


def make_directory(directory):
    """
    Creates a directory if it does not already exist.

    Args:
        directory (str): The path of the directory to create.
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

