import os


def get_parent_dir_path(current_dir, target_dir_name):
    while True:

        if os.path.basename(current_dir) == target_dir_name:
            break  # Exit the loop when the desired parent directory is found
        else:
            current_dir = os.path.dirname(current_dir)
        if os.path.ismount(current_dir):  # Exit the loop if the filesystem root is reached
            print(f'The directory named {target_dir_name} was not found in the path tree.')
            break
    return current_dir

