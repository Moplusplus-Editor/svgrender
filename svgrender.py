#!/usr/bin/env python
import os
import sys
import re
import imageio
import cairosvg
# Get it from https://cairosvg.org/
from tqdm import tqdm
# Note that svgrender requires the imageio ffmpeg plugin
# You may install it with 'pip install imageio-ffmpeg'

help_string = """
Typical usage:
\t svgrender.py . my_rendered_video.mp4
"""

def outputvid_is_valid(vidname: str):
    if vidname.endswith(".mp4"):
        return True
    else:
        return False

def inputdir_is_valid():
    # TODO: check if a given directory
    # relative or absolute exists
    return True;

def charsplit(word: str):
    # Splits words into a list of their
    # component characters
    # E.g. "hi" -> ["h", "i"]
    return list(char for char in word)


def get_number_in_word(word: str):
    temp = re.findall(r"\d+", word)
    num = temp[0]
    return num


def subtract_fromstr(parent_word: str, subtract_word: str):
    # Usage: subtract_fromstr("hello", "he")
    # -> "llo"
    # We split both of the words into lists of characters
    parent_word_list = charsplit(parent_word)
    subtract_word_list = charsplit(subtract_word)
    # We need to check if the word actually can be subtracted
    # E.g. you can't subtract "egg" from "oranges"
    # but you can subtract "egg" from "baconandcheesesandwich"
    if set(subtract_word_list).issubset(parent_word_list):
        result = re.sub(subtract_word, "", parent_word, 1)
        return result
    else:
        raise ValueError(
            "Your word '{}' cannot be subtracted from word '{}'".format(
                subtract_word, parent_word
            )
        )

def sort_dict_bykeys(dic: dict):
    dic2 = {}
    for i in sorted(dic):
        dic2[i] = dic[i]
    return dic2

def sort_list_of_filenames(ls: list):
    # Turns an imporperly sorted list
    # of numbers into one with proper
    # numerical order
    # E.g. ['4.svg', '49.svg', '5.svg', '55.svg'] 
    # -> ['4.svg', '5.svg', '49.svg', '55.svg']

    # We will first convert the list to a dictionary
    # By extracting the number, placing it as the key
    # and setting the remainder of the element as the value
    # E.g. ['4.svg', '49.svg', '5.svg', '55.svg'] 
    # -> {4: '.svg', 49: '.svg', 5: '.svg', 55: '.svg'}
    temp_files_dict = {}
    for element in ls:
        number_key = int(get_number_in_word(str(element)))
        string_value = subtract_fromstr(element, str(number_key))
        # Insert the key-value pair into dict
        temp_files_dict[number_key] = string_value
    # Then we sort the dictionary by key
    sorted_dict = sort_dict_bykeys(temp_files_dict)
    # After that we will merge the sorted dictionary into a list again
    output_list = []
    for key in sorted_dict:
        value = sorted_dict[key]
        merged_key_and_value = str(key) + value
        output_list.append(merged_key_and_value)
    return output_list

def help():
    print(help_string)

def mainprocess(input_folder, output_vid):
    # List for holding a list of generated png files
    # that were converted from svg by cairosvg
    generated_temp_pics = []
    generated_imagelist = []
    # Run cairosvg to turn the rendered svgs into pngs
    print("[1] Running conversion...")
    for file in os.listdir(input_folder):
        if ".svg" in file:
            generated_imagelist.append(file)
    # Sort the generated_temp_pics list to be in numerical order
    # This is because of a Windows-specific issue that likes to list
    # files in order of their first digit not in ascending order like
    # what Python typically does
    generated_imagelist = sort_list_of_filenames(generated_imagelist)
    for file in generated_imagelist:
        output_pic = file.replace(".svg", ".png")
        cairosvg.svg2png(url=file, write_to=output_pic)
        generated_temp_pics.append(output_pic)
        print("\t[INFO] Converted {} to {}".format(file, output_pic))
    # Merge images to video through imageio
    # TQDM handles the progress bar
    print("[2] Merging converted PNGs to video...")
    # Create a video file and append the images generated previously
    # We must specify macro_block_size=2 because the (1920, 1080) video
    # dimensions are not perfectly divisible by 16
    writer = imageio.get_writer(output_vid, fps=24, mode="I", macro_block_size=2)
    video_progress_pics = tqdm(generated_temp_pics)
    for pic in video_progress_pics:
        video_progress_pics.set_description("Processing {}".format(pic))
        im = imageio.imread(pic)
        writer.append_data(im)
    writer.close()
    # Delete temporary generated png files once they've
    # been merged into video
    for pic in generated_temp_pics:
        os.remove(pic)
    # Show success message
    print("Sucess! Your video is now available at ./{}!".format(output_vid))

# Parse command line arguments
if len(sys.argv) < 3:
    print("ERROR: you entered not enough arguments!")
    help()
elif len(sys.argv) > 3:
    print("ERROR: you entered too many arguments!")
    help()
else:
    input_arg = sys.argv[1]
    if input_arg == ".":
        input_arg = os.getcwd()
    output_arg = sys.argv[2]
    print("Your options:\n- Input folder: {}\n- Output filename: {}".format(input_arg, output_arg))
    # Check if the inputs are valid
    if outputvid_is_valid(output_arg):
        mainprocess(input_arg, output_arg)
    else:
        print("ERROR: your output video name {} isn't a valid name".format(output_arg))
