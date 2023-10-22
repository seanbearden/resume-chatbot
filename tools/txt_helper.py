from string import Template


def get_str_template(path):
    with open(path, 'r') as file:
        # Read the contents of the file into a string variable
        system_message_template = Template(file.read())
    return system_message_template

