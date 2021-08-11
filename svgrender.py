import os
import sys
import cairosvg

help_string = """
Typical usage:
\t svgrender . my_rendered_video.mp4
"""

def outputvid_is_valid(vidname: str):
    if ".mp4" in vidname:
        return True
    else:
        return False

def help():
    print(help_string)

def mainprocess(input_folder, output_vid):
    # List for holding a list of generated png files
    # that were converted from svg by cairosvg
    generated_temp_pics = []
    # Run cairosvg to turn the rendered svgs into pngs
    for file in os.listdir(input_folder):
        output_pic = file.replace(".svg", ".png")
        cairosvg.svg2png(url=file, write_to=output_pic)
        generated_temp_pics.append(output_pic)
    # Call ffmpeg
    command = "ffmpeg -i %d.png {}".format(output_vid)
    print("[INFO] Running command: {}".format(command))
    os.system(command)
    # Delete temporary generated png files once they've
    # been merged into video
    for pic in generated_temp_pics:
        os.remove(pic)

# Parse command line arguments
if len(sys.argv) < 2:
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
    if outputvid_is_valid(output_arg):
        mainprocess(input_arg, output_arg)
    else:
        print("ERROR: your output video name {} isn't a valid name".format(output_arg))
    # Check if the inputs are valid
