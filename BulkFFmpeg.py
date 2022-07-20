# BulkFFmpeg.py
version = "1.2"
# Max Laurie 14/07/2022

# Simple bulk FFmpeg command script
# Asks for a command, a folder and then loops through the filetype(s) specified performing the command

# 1.2 changelog
# Files that failed but still created a 0kb file were being falsely labelled successful transcodes
# Added a secondary check on line 135 so output files under 10kb are flagged as failed

import os
import sys
import platform


def clear_screen():
    if platform.system() == "Darwin" or platform.system() == "Linux":
        os.system("reset")
    elif platform.system() == "Windows":
        os.system("cls")
    else:
        pass
    banner()


def banner():
    print("  ____        _ _    _____ _____                       ")
    print(" | __ ) _   _| | | _|  ___|  ___| __ ___  _ __   ___  __ _ ")
    print(" |  _ \\| | | | | |/ / |_  | |_ | '_ ` _ \\| '_ \\ / _ \\/ _` |")
    print(" | |_) | |_| | |   <|  _| |  _|| | | | | | |_) |  __/ (_| |")
    print(" |____/ \\__,_|_|_|\\_\\_|   |_|  |_| |_| |_| .__/ \\___|\\__, |")
    print(f"       Max Laurie v{version}                   |_|         |___/ ")


def get_ffmpeg_command():
    command_part_one = "ffmpeg -v error -stats -i"

    user_confirmed = ""
    while user_confirmed != "y":
        command_part_two = input("\nFFmpeg command arguments: ")
        desired_ext = input("Output file extension: ")
        print(f"Command to run: {command_part_one} <Input file> {command_part_two} <Output file>.{desired_ext}")

        while user_confirmed not in ["y", "n"]:
            user_confirmed = input("Confirm command [y/n]: ")

    return command_part_one, command_part_two, desired_ext


def get_input_folder():
    input_folder = ""
    while os.path.isdir(input_folder) is False:
        input_folder = input("\nFolder to work on: ")
        input_folder = return_fixed_dirpath(input_folder)

        if os.path.isdir(input_folder) is False:
            print("Folder is unreachable or you don't have the correct permissions")

    os.chdir(input_folder)
    return input_folder


def return_fixed_dirpath(input_folder):
    return os.path.normpath(input_folder.strip())


def get_files_to_work_on(input_folder):
    input_filetypes = input("Filetype(s) to work on (if multiple, separate by comma): ")
    input_files = []

    if "," in input_filetypes:
        input_filetypes = input_filetypes.split(",")
        for filetype in input_filetypes:
            filetype = filetype.strip()
            for file in os.listdir(input_folder):
                if filetype_check(file, filetype) == True:
                    input_files.append(file)
    else:
        for file in os.listdir(input_folder):
            if filetype_check(file, input_filetypes) == True:
                input_files.append(file)
        
    
    if len(input_files) == 0:
        script_exit("No files found to work on!")
    else:
        return input_files


def filetype_check(file, filetype):
    path_and_ext = os.path.splitext(file)
    if path_and_ext[1].casefold() == f".{filetype}" and not file.startswith("."):
        return True
    else:
        return False


def script_exit(exitText):
    print("\n" + exitText)
    input("Press enter to exit...\n")
    sys.exit()


def return_available_filename(file, desired_ext):
    basename = os.path.splitext(file)[0]
    output_filename = basename + "_OUT" + "." + desired_ext
    i = 2
    while os.path.isfile(output_filename):
        output_filename = basename + "_OUT_" + str(i) + "." + desired_ext
        i += 1
    return output_filename


def return_video_spec(input_file, spec):
    return os.popen(f'ffprobe -i "{input_file}" -select_streams v:0 -show_entries stream={spec} -v 0 -of compact=p=0:nk=1').read()


def ffmpeg_command(command_part_one, command_part_two, input_file, output_file):
    os.system(f'{command_part_one} "{input_file}" {command_part_two} "{output_file}"')


def main():
    command_part_one, command_part_two, desired_ext = get_ffmpeg_command()
    input_folder = get_input_folder()
    input_files = get_files_to_work_on(input_folder)

    files_complete, i = [], 1
    for file in input_files:
        output_file = return_available_filename(file, desired_ext)

        print(f"\nProcessing {i}/{len(input_files)} - {file}")
        ffmpeg_command(command_part_one, command_part_two, file, output_file)

        if os.path.isfile(output_file) and os.path.getsize(output_file) > 10000:
            print("Done!")
            files_complete.append("MADE - " + output_file)
        else:
            print("Failed :(")
            files_complete.append("FAIL - " + output_file)
        i += 1

    print("\nFiles processed:")
    for file in files_complete:
        print(file)

    script_exit("All done!")


if __name__ == "__main__":
    clear_screen()
    main()
