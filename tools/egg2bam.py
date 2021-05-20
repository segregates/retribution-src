import os
import subprocess

def convertEggToBam(directory):
	os.chdir(directory)
	fails = []
	for root, dirs, files in os.walk(directory):
		for name in files:
			if name.endswith('.egg') or name.endswith('.egg.pz'):
				print 'Converting %s to .egg...' % name 
				path = '%s%s%s' % (root, os.sep, name)
				bamPath = '%s.bam' % path[:len(path)-4]
				if os.path.exists(bamPath):
					print 'Removing old bam...'
					os.remove(bamPath)
				cmd = 'egg2bam -o %s.bam %s' % (path[:len(path)-4], path)
				p = subprocess.Popen(cmd)
				v = p.wait()
				if v != 0:
					print 'Failed to convert %s!' % name
					fails.append(name)
					if len(fails) > 20:
						raise Exception("Failed to convert %s! Exceeded 20 count failure. Exiting" % fails)


if __name__ == "__main__":
	convertEggToBam('..%sresources' % os.sep)
	print 'Process complete!'