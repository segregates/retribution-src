'''
Author: Michael Wass
Date: July 2nd, 2015

This scripts job is to input a model that contains FFTW support and export a model that does not.
Output will be in the same directory as input. Files are outputted with the extension .bam_newModel,
delete or rename your inputted model and change your new models extension to .bam

## Usage ##
python RemoveFFTW.py --input inputFile
python RemoveFFTW.py --everything folderPath

## Example ##
python RemoveFFTW.py --input pir_m_are_isl_delFuego_wave_idle.bam

written file: pir_m_are_isl_delFuego_wave_idle.bam_newModel

## TODO ##
- Add egg support.
- Finish documentation
'''

from panda3d.core import *
loadPrcFileData('', 'window-type none')
from direct.showbase import ShowBase
import argparse
import sys
import os
import time

base = ShowBase.ShowBase()

# Adding arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='This is the original model with FFTW support.')
parser.add_argument('--everything', help='This searches every folder in the path provided.')
args = parser.parse_args()

isFFTWPanda = PandaSystem.getGlobalPtr().hasSystem("fftw")
if isFFTWPanda is not True:
    raise Exception("The version of Panda3D you are using does not have FFTW support! You must use a Panda3D version with FFTW support in order for this tool to work.")

if args.input and args.everything == None:
    print "Usage: python RemoveFFTW.py --input inputFile"
    print "Usage: python RemoveFFTW.py --everything folderPath"
    sys.exit(1)

if args.everything:
    counter = 0
    for root, _, filenames in os.walk(args.everything):
        for filename in filenames:
            if filename.endswith('.bam'):
                filepath = os.path.join(root, filename).replace("\\", "/")
                print "Working on... %s" % filepath
                inputtedModel = loader.loadModel(filepath)
                # Rewrite model, which removes the compression
                inputtedModel.writeBamFile('%s_newModel' % filepath)
                # Remove variable so it can be reused
                del inputtedModel
                # Delete original file.
                os.unlink(filepath)
                # Keep track of number of files edited
                counter = counter + 1
    print "Renaming files..."
    if not counter:
        counter = 0
    renamecount = 0
    time.sleep(3)
    for root, _, filenames in os.walk(args.everything):
        for filename in filenames:
            if filename.endswith('.bam_newModel'):
                filepath = os.path.join(root, filename).replace("\\", "/")
                newname = filepath.split('_newModel')
                os.rename(filepath, newname[0])
                print "Renaming file... %s" % newname[0]
                renamecount = renamecount + 1
    print "Done. %s files rewrote. %s files renamed." % (counter, renamecount)
    sys.exit(0)

elif args.input:
    # Make sure that the file inputted is a .bam
    if not '.bam' in args.input:
        raise ValueError("Invalid file inputted!")
    # Load model
    inputtedModel = loader.loadModel('%s' % args.input)
    # Rewrite model, which removes the compression.
    inputtedModel.writeBamFile('%s_newModel' % args.input)
    # Delete original file
    os.unlink(inputtedModel)
    del inputtedModel
    # Change file extension to bam
    ext = os.path.splitext(args.input + "_newModel")
    if ext == ".bam_newModel":
        os.rename(args.input + "_newModel", args.input)
    # Notify user of model being sucessfully converted
    print "Generated %s" % args.input
    sys.exit(0)

if __name__ == '__main__':
    base.run()
elif not __name__ == '__main__':
    print "__name__ is not the main module!"
    sys.exit(1)
else:
    print "Program failed to run for some reason."
    sys.exit(1)
