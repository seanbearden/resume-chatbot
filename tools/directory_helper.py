import os


def create_nested_directory(path):
    """
    Create a nested directory if it does not already exist.

    :param path: Path to the directory to be created.
    """
    if not os.path.exists(path):
        os.makedirs(path)
