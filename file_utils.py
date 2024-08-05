import os
import shutil


def list_files(directory):
    """
    Lists all files in the specified directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        list of str: A list containing the names of all files in the directory.
    """
    try:
        if not os.path.exists(directory):
            print("Directory does not exist.")
            return []

        return os.listdir(directory)
    except Exception as e:
        print(f"Error listing files in directory '{directory}': {e}")
        return []


def create_output_dir(directory):
    """
    Creates a directory if it does not exist.

    Args:
        directory (str): Path to the directory.
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print(f"Failed to create directory '{directory}': {e}")


def does_dir_exist(directory):
    """
    Checks if the specified directory exists.

    Args:
        directory (str): Path to the directory.

    Returns:
        bool: True if the directory exists, False otherwise.
    """
    try:
        return os.path.isdir(directory)
    except Exception as e:
        print(f"Error checking if directory '{directory}' exists: {e}")
        return False


def clear_dir(directory):
    """
    Deletes the specified directory and all its contents.

    Args:
        directory (str): Path to the directory.
    """
    try:
        shutil.rmtree(directory)
    except Exception as e:
        print(f"Error clearing directory '{directory}': {e}")


def handle_empty_file(file_path):
    """
    Deletes the file if it is empty.

    Args:
        file_path (str): Path to the file.
    """
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)
    except Exception as e:
        print(f"Error handling empty file '{file_path}': {e}")


def write_to_file(file_name, entries):
    """
    Writes the concatenation configuration entries to a file.

    Args:
        file_name (str): The name of the configuration file to write to.
        entries (list of str): The configuration entries to write.
    """
    try:
        with open(file_name, 'w') as file:
            for entry in entries:
                file.write(entry)
    except Exception as e:
        print(f"Error writing to file '{file_name}': {e}")


def remove_file(file_name):
    """
    Removes the specified file.

    Args:
        file_name (str): The name of the file to be removed.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be removed due to permission issues.
    """
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except PermissionError:
        print(f"Permission denied to remove file '{file_name}'.")
    except Exception as e:
        print(f"Error removing file '{file_name}': {e}")
