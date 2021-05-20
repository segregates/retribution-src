import glob, subprocess, os

os.chdir('../')

try:
    print 'Using unstaged files.'
    files = subprocess.Popen(['git', 'diff', '--name-only'], stdout=subprocess.PIPE).communicate()[0].replace('\r', '').split('\n')
    files = [file for file in files if file.endswith('.py') and 'importer.py' not in file]
except:
    print 'Using all files.'
    files = [fileName for fileName in glob.glob('*/*/*.py') if '__init__.py' not in fileName]

print 'Detected %s Python scripts.' % len(files)

def modifyFiles(files, func):
    count = 0

    for name in files:
        if func(name):
            count += 1
    
    return count

def hasOneOfStrings(base, strings):
    if 'DEFAULT_TEXT' in base:
        return False

    for string in strings:
        if string in base:
            return True
    
    return False

def writeLines(fileName, lines):
    file = open(fileName, 'w')
    
    for line in lines:
        file.write(line)

    file.close()

def removeImports(fileName, imports):
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
    
    newLines = [line for line in lines if not hasOneOfStrings(line, imports)]
    
    if len(newLines) == len(lines):
        return False

    writeLines(fileName, newLines)
    return True

def convertTabs(fileName):
    file = open(fileName, 'r')
    contents = file.read()
    file.close()
    
    if '\t' not in contents:
        return False
    
    tab = ' ' * 4
    contents = contents.replace('\t', tab)
    file = open(fileName, 'w')
    file.write(contents)
    file.close()
    return True

def convertEmptySpaces(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()
    
    newLines = [line.rstrip(' \r\t') for line in lines]
    
    if lines == newLines:
        return False
    
    writeLines(fileName, newLines)
    return True

def removeImportsFromAll(files):
    imports = ['from panda3d.', 'from pandac.']
    return modifyFiles(files, lambda fileName: removeImports(fileName, imports))

def hasElement(line, element):
    return (' ' + element) in line or ('(' + element) in line or (element + ')') in line or (element + '(') in line or (element != 'Notify' and (element + '.') in line)

def addImports(fileName, packageName, elements):
    file = open(fileName, 'r')
    contents = file.read()
    file.close()
    presentElements = []
    
    for element in elements:
        if element.startswith('_'):
            continue
        if element in ['Geom', 'Loader', 'Event']:
            continue
        if hasElement(contents, element):
            presentElements.append(element)
    
    if not presentElements:
        return False
    
    if 'GeomVertexData' in presentElements and 'Geom' not in presentElements:
        presentElements.append('Geom')

    contents = 'from %s import %s\n' % (packageName, ', '.join(sorted(presentElements))) + contents
    file = open(fileName, 'w')
    file.write(contents)
    file.close()
    return True

def addImportsToAll(files, packageName):
    elements = {}
    elements.update(__import__(packageName, fromlist=['*']).__dict__)
    print 'Package %s has %s elements.' % (packageName, len(elements))
    return modifyFiles(files, lambda fileName: addImports(fileName, packageName, elements))

count = removeImportsFromAll(files)
print 'Removed imports from %s scripts.' % count
count = modifyFiles(files, convertTabs)
print 'Converted tabs in %s scripts.' % count
count = modifyFiles(files, convertEmptySpaces)
print 'Converted empty spaces in %s scripts.' % count

for package in ('bullet', 'core', 'direct', 'egg', 'fx', 'ode', 'physics', 'rocket', 'skel', 'vision', 'vrpn'):
    package = 'panda3d.' + package
    count = addImportsToAll(files, package)
    print 'Imported package %s in %s scripts.' % (package, count)