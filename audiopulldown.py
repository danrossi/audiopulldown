#!/usr/bin/env python

# By: Daniel Rossi, <electroteque@gmail.com>
# Copyright (c) 2015 Electroteque Media

from os import walk, path, makedirs
import argparse
import subprocess

""" 24 bit wave audio pullup / pulldown prcoessing script.
This tool takes input and output directories and source and target framerates to calculate the speed change.
Example ./audiopulldown.py -i "test/source" -o "test/output" -s 25 -t 24 """


class AudioPulldown:
    def __init__(self, src_dir, dst_dir,  source, target, prefix):
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.source = source
        self.target = target
        self.prefix = prefix
        self.audio_rate = self.calcRate()

    """ Process the command through Ffmpeg """
    def processAudio(self, in_file, out_file):
        command = ["ffmpeg", "-y", "-i", in_file, "-filter:a", "atempo={}".format(self.audio_rate), "-write_bext", "1", "-acodec", "pcm_s24le", out_file]
        process = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        #print (" ".join(command))
        output, err = process.communicate()
        #print (output)
        #print (err)

    """ Create the sub directory if required """
    def createDir(self, root):
        if (root):
            out_dir = path.join(self.dst_dir, root)
            if not path.exists(out_dir):
                makedirs(out_dir)

    """ Calculate the speed rate. Audio: target / source. Video: source / target. """
    def calcRate(self):
        return self.target / self.source;

    """ Process the input directory and sub directory of audio files """
    def process(self):

        for root, dirs, files in walk(self.src_dir):
            current_root = root[len(self.src_dir) + 1:]
            self.createDir(current_root)

            for filename in files:
                if filename.endswith( ('.wav', '.WAV')):

                    # if a prefix is configured add it before the output file name.
                    if (self.prefix):
                        filename = "{}_{}".format(self.prefix, filename)

                    # format the input path
                    in_file = path.join(root, filename)

                    #format the output path
                    out_file = path.join(self.dst_dir, current_root, filename)

                    print ("Processing " + in_file)

                    #process the audio through ffmpeg
                    self.processAudio(in_file, out_file);

def main():

    parser = argparse.ArgumentParser(description='Audio pulldown/pullup pitch convertor using Ffmpeg.')
    parser.add_argument('-i',"--input", help="Source Path", required=True)
    parser.add_argument('-o', "--output", help="Processed Path", required=True)
    parser.add_argument('-s', "--source", help="Source frame rate", type=int, required=True)
    parser.add_argument('-t', "--target", help="Target frame rate", type=int, required=True)
    parser.add_argument('-p', "--prefix", help="Processed file prefix", required=False)
    args = parser.parse_args()

    audiopulldown = AudioPulldown(args.input, args.output, args.source, args.target, args.prefix)
    audiopulldown.process()



if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print ('ERROR: %s\n' % str(err))
        exit()

