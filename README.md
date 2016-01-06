audiopulldown.py
============

24 bit wave audio pullup / pulldown prcoessing script.

This tool takes input and output directories and source and target framerates to calculate the speed change.

Required when converting audio clips or audio stems from 24fps to 25fps or 25fps to 24fps.

Requirements
------------

 - Ffmpeg
 - Python

Examples
--------

### Basic Example

```
./audiopulldown.py -i "test/source" -o "test/output" -s 25 -t 24

```

Options
--------

    | Param | Description |
    | --- | --- |
    | -i | The input directory |
    | -o | The output destination directory for the processed files |
    | -s | The source frame rate |
    | -t | The target frame rate |
    | -p | Processed file prefix |

Support
--------

This is supplied as-is.
