import os
import shutil


def create(*, brick_name, set_as_input, template_folder):
    current_director = os.getcwd()
    full_path = os.path.join(current_director, brick_name)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    template_source_directory = get_template_directory(set_as_input, template_folder)
    copy(source_directory=template_source_directory, destination_directory=full_path)


def initialize(*, brick_name, set_as_input, template_folder):
    full_path = os.getcwd()
    template_source_directory = get_template_directory(set_as_input, template_folder)
    copy(source_directory=template_source_directory, destination_directory=full_path)


def get_template_directory(set_as_input, template_folder):
    if set_as_input:
        template_source_directory = os.path.join(template_folder, "input")
    else:
        template_source_directory = os.path.join(template_folder, "generic")
    return template_source_directory


def copy(*, source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)
    for file in os.listdir(source_directory):
        name = file
        file = os.path.join(source_directory, file)
        print("Copying {} to {}".format(file, destination_directory))
        if os.path.isfile(file):
            shutil.copy(file, destination_directory)
            continue
        copy(source_directory=file, destination_directory=os.path.join(destination_directory, name))
