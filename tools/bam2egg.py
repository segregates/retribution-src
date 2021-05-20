import os
import subprocess

def convertBamToEgg(directory):
	os.chdir(directory)
	for root, dirs, files in os.walk(directory):
		for name in files:
			if name.endswith('.bam'):
				print 'Converting %s to .egg...' % name 
				path = '%s%s%s' % (root, os.sep, name)
				cmd = 'bam2egg -o %s.egg %s' % (path[:len(path)-4], path)
				p = subprocess.Popen(cmd)
				v = p.wait()
				if v != 0:
					raise Exception("Failed to convert %s!" % name)

if __name__ == "__main__":
	convertBamToEgg('..%sresources' % os.sep)
	print 'Process complete!'