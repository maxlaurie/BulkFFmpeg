# BulkFFmpeg.py
version = "1.0"
# Max Laurie 07/07/2022

# Simple bulk FFmpeg command script
# Asks for a folder and then loops through the filetype(s) specified performing the command on line 113/114

import os
import sys
import platform

class VideoFile:
    def __init__(self, file):
        self.codec = return_video_spec(file, "codec_name")
        self.profile = return_video_spec(file, "profile")
        self.width = return_video_spec(file, "width")
        self.height = return_video_spec(file, "height")
        self.field_order = return_video_spec(file, "field_order")
        self.frame_rate = return_video_spec(file, "r_frame_rate")
        self.filename = file
        self.basename = os.path.splitext(file)[0]
        self.ext = os.path.splitext(file)[1]


def clear_screen():
    if platform.system() == "Darwin" or platform.system() == "Linux":
        os.system("reset")
    elif platform.system() == "Windows":
        os.system("cls")
    else:
        pass


def banner():
    print("  ____        _ _    _____ _____                       ")
    print(" | __ ) _   _| | | _|  ___|  ___| __ ___  _ __   ___  __ _ ")
    print(" |  _ \\| | | | | |/ / |_  | |_ | '_ ` _ \\| '_ \\ / _ \\/ _` |")
    print(" | |_) | |_| | |   <|  _| |  _|| | | | | | |_) |  __/ (_| |")
    print(" |____/ \\__,_|_|_|\\_\\_|   |_|  |_| |_| |_| .__/ \\___|\\__, |")
    print(f"       Max Laurie v{version}                   |_|         |___/ ")




def get_input_folder():
    input_folder = ""
    while os.path.isdir(input_folder) is False:
        input_folder = input("Folder to work on: ")
        input_folder = return_fixed_dirpath(input_folder)
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
    input("Press enter to exit...")
    sys.exit()


def return_available_filename(file_path, desired_ext):
    output_filename = file_path + "_OUT" + desired_ext
    i = 2
    while os.path.isfile(output_filename):
        output_filename = file_path + "_OUT_" + str(i) + desired_ext
        i += 1
    return output_filename


def return_video_spec(input_file, spec):
    return os.popen(f'ffprobe -i "{input_file}" -select_streams v:0 -show_entries stream={spec} -v 0 -of compact=p=0:nk=1').read()


def ffmpeg_command(command_part_one, command_part_two, input_file, output_file):
        os.system(f'{command_part_one} "{input_file}" {command_part_two} "{output_file}"')


def main():
    command_part_one = "ffmpeg -v quiet -stats -i"
    command_part_two = "-vcodec prores -profile:v 1 -acodec copy -map 0"
    print(f"\nCommand to run: {command_part_one} <Input file> {command_part_two} <Output file>")

    input_folder = get_input_folder()
    input_files = get_files_to_work_on(input_folder)

    files_complete, i = [], 1
    for file in input_files:
        current_file = VideoFile(file)
        output_file = return_available_filename(current_file.basename, current_file.ext)

        print(f"\nProcessing {i}/{len(input_files)} - {current_file.filename}")
        ffmpeg_command(command_part_one, command_part_two, current_file.filename, output_file)

        if os.path.isfile(output_file):
            print("Done!")
            files_complete.append(output_file)
        else:
            print("Failed :(")
            files_complete.append("FAILED - " + output_file)
        i += 1

    print("\nFiles processed:")
    for file in files_complete:
        print(file)

    script_exit("Script complete")


if __name__ == "__main__":
    clear_screen()
    banner()
    main()
