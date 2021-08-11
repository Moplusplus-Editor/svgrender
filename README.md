# SVGRender

VecFX, the graphics engine that powers Mo++, always renders animations as vector image sequences due to performance and reliability considerations. However, it currently lacks the ability to convert a render sequence into a video (though this is planned in the near future). In the meantime, SVGRender is a command-line tool that does the conversions for you.

## Dependencies

You must have `ffmpeg`, `python` and `cairo` installed to build from source. However, if you download the pre-compiled binaries, you don't need anything installed.

## Installation

Make sure you have the dependencies. Once you've got that done, run `python package.py`. The executable will be found in the `dist/` folder.

## Usage

```
svgrender . my_rendered_video.mp4
# renders all the svgs in the current folder to one mp4 file
```
