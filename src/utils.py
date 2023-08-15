# utils.py

# Conversion/formatting functions

def seconds_to_formatted_time(seconds):
    """
    Convert a time duration in seconds to a formatted string representing the time in hours, minutes, and seconds.

    Parameters:
    seconds (float or int): Time duration in seconds.

    Returns:
    str: A formatted string representing the time duration in "HH:MM:SS" format.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def formatted_time_to_seconds(formatted_time):
    """
    Convert a formatted time string in "HH:MM:SS" format to time duration in seconds.

    Parameters:
    formatted_time (str): A formatted time string in "HH:MM:SS" format.

    Returns:
    float: Time duration in seconds.
    """
    hours, minutes, seconds = map(int, formatted_time.split(":"))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def bytes_to_formatted_size(file_size_bytes):
    """
    Convert a file size in bytes to a formatted string with units (e.g., "MB", "GB").

    Parameters:
    file_size_bytes (int): File size in bytes.

    Returns:
    str: Formatted file size string with units.
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0

    while file_size_bytes >= 1024 and unit_index < len(units) - 1:
        file_size_bytes /= 1024
        unit_index += 1

    return f"{file_size_bytes:.2f} {units[unit_index]}"


def formatted_size_to_bytes(formatted_size):
    """
    Convert a formatted file size string with units to bytes.

    Parameters:
    formatted_size (str): Formatted file size string with units (e.g., "2.50 MB").

    Returns:
    int: File size in bytes.
    """
    size, unit = formatted_size.split()
    size = float(size)
    unit_index = ["B", "KB", "MB", "GB", "TB"].index(unit)
    bytes_size = size * (1024 ** unit_index)
    return int(bytes_size)
