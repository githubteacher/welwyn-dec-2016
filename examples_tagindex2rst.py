#!/opt/BIOSTAT/qa/acp/bin/python3
# ------------------------------------------------------------------------------
# examples_tagindex2rst.py - Create a tag index reST file from example fragments
# ------------------------------------------------------------------------------
# Project:        STREAM
# Author:         Mark Luff
# Python version: 3.*
# ------------------------------------------------------------------------------
# Usage: python3 examples_tagindex2rst.py -d <output-directory> <directories...>
#
# Options:
#   -h, --help           show this help message and exit
#   -d DIR, --dir=DIR    Output directory
#
# The tag index file is output to the following path by default:
#
#     sphinx_um/source/tag_index.rst
#
# The example identifier is taken from the argument to the stream-example
# directive. The example description and tags are taken from the :short_desc:
# and :tags: options to the directive.
# ------------------------------------------------------------------------------

import sys
import re
import os
import datetime
from optparse import OptionParser

# ------------------------------------------------------------------------------
# Process/parse the options and arguments to the script
# ------------------------------------------------------------------------------

usage = "usage: python3 %prog [options] <directories...>"
parser = OptionParser(usage=usage)

parser.add_option('-d', '--dir', action = 'store', type = 'string',
                  dest = 'dir', default = 'sphinx_um/source/tag_examples',
                  help = 'Output directory')

(options, args) = parser.parse_args()

if not os.path.isdir(options.dir):
    print('Output directory does not exist:', options.dir)
    quit()

print('Output directory:', options.dir)

# If no arguments passed, then set to default search directories
if args == []:
    args = ['sphinx_um/source', 'sphinx_um/source/macro_ref']

print('Args:', args)

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))


# ------------------------------------------------------------------------------
# Initialise tags dictionary
# ------------------------------------------------------------------------------

tagsDict = {}


# ------------------------------------------------------------------------------
# Initialise dictionary that maps example ID to short description
# ------------------------------------------------------------------------------

idDict = {}


def submit_example(exampleID, title, shortDesc, tags, rstLines, directory, filename):
    """
    Submit all data for an example to the tags dictionary
    """

    if title == '' or title == '<unassigned>':
        title = '<' + directory + '/' + filename + '>'

    for tag in tags:
        # Is tag in dictionary?
        if tag not in tagsDict:
            tagsDict[tag] = {}

        if title not in tagsDict[tag]:
            tagsDict[tag][title] = {}

        #if title == '':
        #    tagsDict[tag].update({exampleID: [shortDesc, rstLines]})
        #else:
        #    tagsDict[tag].update({exampleID: [title + ' / ' + shortDesc, rstLines]})

        #tagsDict[tag].update({title: {exampleID: [shortDesc, rstLines]}})
        tagsDict[tag][title].update({exampleID: rstLines})

        #print('tagsDict02_post', tagsDict)

    if exampleID not in idDict:
        # Add to dictionary that maps exampleID to source doc path and short desc

        matchDir = re.search(r'\/source\/(.*)', directory + '/')

        if matchDir:
            if filename.endswith('.rst'):
                if matchDir.group(1) != '':
                    path = matchDir.group(1) + filename[:-4]
                else:
                    path = filename[:-4]

                idDict[exampleID] = [path]
                idDict[exampleID] += [shortDesc]
            else:
                print('WARNING: Invalid source filename: ' + filename + ' (must have .rst extension)')

        else:
            print('WARNING: Invalid source file path: ' + directory + '/' +  filename)


import docutils.parsers.rst
import docutils.utils
import docutils.frontend

parser = docutils.parsers.rst.Parser()
myfile = open('sphinx_um/source/foobar.rst')
input = myfile.read()
document = docutils.utils.new_document('sphinx_um/source/foobar.rst', settings = docutils.frontend.OptionParser(components=(docutils.parsers.rst.Parser,)).get_default_values())
parser.parse(input, document)
sys.exit(0)



#def get_indent(line):
#    """
#    Return the indentation level within a line, or -1 if line is empty.
#    """
#
#    matchIndent = re.match(r'\s*(\S)', line)
#
#    if matchIndent:
#        return matchIndent.start(1)
#    else:
#        return -1


class RST:
    def get_indent(self, line):
        """
        Return the indentation level within a line, or -1 if line is empty.
        """

        matchIndent = re.match(r'\s*(\S)', line)

        if matchIndent:
            return matchIndent.start(1)
        else:
            return -1

class Directive(RST):
    # name       - directive name
    # arguments  - arguments given to the directive, as a list
    # options    - options given to the directive, as a dictionary mapping option names to values
    # content    - directive content - a list of text lines
    # srcline    - line number in the source file on which the directive appears   
    # length     - length of directive (number of lines)
    # indent     - indendation level of directive

    def __init__(self, name = '', arguments = [], options = {}, content = [], srcline = -1, length = 0, indent = 0):
        self.name = name
        self.arguments = arguments
        self.options = options
        self.content = content
        self.srcline = srcline
        self.length = length
        self.indent = indent

    def next_line(self, lines):
        pass

    def read_directive(self, lines, index):
        self.__init__()

        processFlag = True
        linesLen = len(lines)
        i = index

        matchName = re.match(r'\s*(\.)\. (\S+)::\s*(\S+)', lines[i])
        if matchName:
            self.name = matchName.group(2)
            arguments = matchName.group(3)
            self.srcline = index
            self.indent = self.get_indent(lines[i])
        else:
            return 0

        #while self.get_indent(self.next_line(), lines):

        self.arguments = arguments


        while processFlag and i < linesLen:
            line = lines[i]
            i += 1

    def print(self):
        print(" name:       ", self.name)
        print(" arguments:  ", self.arguments)
        print(" options:    ", self.options)
        print(" content:    ", self.content)
        print(" srcline:    ", self.srcline)
        print(" length:     ", self.length)
        print(" indent:     ", self.indent)

dd = Directive()
dd.read_directive(['', '', '  .. rst-header:: foo', '          bar', '     :short_desc: my desc', '        is here', '', '     body', '', '  .. continued::'], 2)
dd.print()
sys.exit(0)





def process_file(directory, filename, source_filename, title = '<unassigned>', instr = ''):
    """
    Extract examples and their metadata from a file and add to tags dictionary
    """

    pathname = directory + '/' + filename
    print('\n' + instr + 'Processing file:', pathname)

    fileIn = open(pathname)

    processTitleFlag = False

    # Flag to indicate that STREAM example directive is being processed
    processExampleFlag = False

    exampleID = ''
    shortDesc = ''
    tags = []
    rstLines = []
    currentIndent = -1

    # Indentation of a matched directive (-1 means unset)
    directiveIndent = -1

    # Copy lines in file to list of lines
    lines = []
    for line in iter(fileIn):
        lines += [line.rstrip()]

    lineCount = len(lines)

    #print(lines)
    #sys.exit(0)

    #for line in lines:

    lineIndex = 0
    while lineIndex < lineCount:
        line = lines[lineIndex]
        lineIndex += 1

        # Get indent level of current line - to determine when a directive ends
        currentIndent = RST.get_indent(line)

        if title == '<unassigned>':

            # Look for rst-header directive and its indentation
            matchHeader = re.match(r'\s*\.\. rst-header::\s*\S+', line)

            if matchHeader:
                # rst-header directive found

                processTitleFlag = True
                title = '<searching...>'
                directiveIndent = currentIndent
                continue

        elif title == '<searching...>':

            # Look for blank line that marks end of directive options
            if re.match(r'\s*$', line):
                # End of directive options - no title option was found

                title = ''
                continue

            # Look for title option in rst-header directive
            matchTitle = re.match(r'\s+:title:\s*(\S.*)', line)

            if matchTitle:
                # Title option found - get title

                title = matchTitle.group(1)
                print(instr + 'Title found:', title)
                continue

        if processTitleFlag:

            # Look for end of rst-header directive
            if currentIndent <= directiveIndent and currentIndent != -1:
                processTitleFlag = False
                directiveIndent = -1

            else:
                continue

        # Look for include directive
        matchInclude = re.match(r'\s*\.\. include::\s*(\S+)', line)

        if matchInclude:
            # Process included file
            process_file(directory, matchInclude.group(1), filename, title, instr + '  ')

        # Look for STREAM example directive and its indentation
        matchExample = re.match(r'\s*\.\. stream-example::\s*(\S+)', line)

        if matchExample:
            # STREAM example directive found

            if processExampleFlag and currentIndent <= directiveIndent:
                # Previous example needs to be processed first

                # Submit all data to tags dictionary
                submit_example(exampleID, title, shortDesc, tags, rstLines, directory, source_filename)

                shortDesc = ''
                tags = []
                rstLines = []

            # Get example identifier
            exampleID = matchExample.group(1)
            processExampleFlag = True

            print(instr + 'Example found:', exampleID)

            # Set directive indentation level and store dedented line
            directiveIndent = currentIndent
            rstLines.append(line[directiveIndent:])

            continue

        if processExampleFlag:
            # Process options from example directive

            # Check for example short description option
            matchShortDesc = re.match(r'\s*:short_desc:\s*(\S.*)', line)

            if matchShortDesc:
                # Example short description option found - get short description
                shortDesc = matchShortDesc.group(1)
                rstLines.append(line[directiveIndent:])
                continue

            # Check for example tags option
            matchTags = re.match(r'\s*:tags:\s*(\S.*)', line)

            if matchTags:
                # Example short description option found - get short description
                tags = matchTags.group(1).split()
                print(instr + '   Tags found:', tags)
                rstLines.append(line[directiveIndent:])
                continue

            # Look for end of example directive
            if currentIndent <= directiveIndent and currentIndent != -1:

                # Submit all data to tags dictionary
                submit_example(exampleID, title, shortDesc, tags, rstLines, directory, source_filename)

                processExampleFlag = False
                exampleID = ''
                shortDesc = ''
                tags = []
                rstLines = []
                directiveIndent = -1

            else:
                rstLines.append(line[directiveIndent:])

    # Check if any example at the end of the file has not yet been submitted
    if processExampleFlag:
        submit_example(exampleID, title, shortDesc, tags, rstLines, directory, source_filename)

    fileIn.close()


# ------------------------------------------------------------------------------
# Get a list of all entries in search directories, with full path
# ------------------------------------------------------------------------------

dirContent = []
for dir in args:
    dirContent += [dir + '/' + s for s in os.listdir(dir)]


# ------------------------------------------------------------------------------
# Get the list of RST files only
# ------------------------------------------------------------------------------

fileList = [f for f in dirContent if os.path.isfile(f) and f.lower().endswith('.rst')]
#print('Files:', fileList)


# ------------------------------------------------------------------------------
# Process RST files
# ------------------------------------------------------------------------------

for f in fileList:
    directory = os.path.split(f)[0]
    filename = os.path.split(f)[1]
    process_file(directory, filename, filename)



#print('tagsDict:', tagsDict)



# ------------------------------------------------------------------------------
# Add slash to end of directory path if needed
# ------------------------------------------------------------------------------

if options.dir[-1] == '/':
    pathOutStr = options.dir
else:
    pathOutStr = options.dir + '/'



if tagsDict:

    # --------------------------------------------------------------------------
    # Create tags index reST file
    # --------------------------------------------------------------------------

    tagIndexFileStr = 'tag_index.rst'


    tagIndexFile = open(pathOutStr + tagIndexFileStr, 'w')

    # --------------------------------------------------------------------------
    # Output header for reST file
    # --------------------------------------------------------------------------

    tagIndexFile.write('.. rst-header:: tag_index\n')
    tagIndexFile.write('   :title: Tags Index\n\n')

    tagIndexFile.write('   Generated using ' + os.path.basename(__file__) +
                       ' script.\n\n')

    # --------------------------------------------------------------------------
    # Output title for reST file
    # --------------------------------------------------------------------------

    tagIndexFile.write('- Click on an example under a tag to go to the example on its original page.\n')
    tagIndexFile.write('- Click on a tag to go to a page with all examples for that tag.\n\n')

    print()
    for tag in sorted(tagsDict):
        #print('tag:', tag)
        tagIndexFile.write('.. _tag_' + tag + ':\n\n')
        tagIndexFile.write(':doc:`' + tag + '<TAG_EXAMPLES_' + tag + '>`\n\n')

        tagExampleFile = open(pathOutStr + 'TAG_EXAMPLES_' + tag + '.rst', 'w')
        tagExampleFile.write('.. rst-header:: TAG_EXAMPLES_' + tag + '\n')
        tagExampleFile.write('   :title: Examples for ' + tag + ' tag\n')
        tagExampleFile.write('   :orphan:\n\n')


        titleSubDict = tagsDict[tag]
        for title in sorted(titleSubDict):
            #tagIndexFile.write('\n- ' + title + '\n\n')

            #for subDict in titleSubDict[title]:
            subDict = titleSubDict[title]
            for exampleID in sorted(subDict):
                #tagIndexFile.write('- :ref:`' + subDict[exampleID][0] + '<example_' + exampleID + '>`\n')
                #tagIndexFile.write('  - :stream-example:`' + exampleID + '`\n')
                tagIndexFile.write('- ' + title + ' / :stream-example:`' + exampleID + '`\n')
            
                n = 1
                for line in subDict[exampleID]:
                    if n == 1:
                        tagExampleFile.write(line + '_tagpage\n')
                    else:
                        tagExampleFile.write(line + '\n')
                    n = n + 1

        tagIndexFile.write('\n')

        tagExampleFile.close()
        print('Creation of', pathOutStr + 'TAG_EXAMPLES_' + tag + '.rst', 'successful.')

    tagIndexFile.close()
    print('\nCreation of', pathOutStr + tagIndexFileStr, 'successful.')


if idDict:

    # --------------------------------------------------------------------------
    # Create text file that maps example ID to source path and description
    # --------------------------------------------------------------------------

    idFile = open(pathOutStr + 'example_description_lookup.txt', 'w')

    for id in sorted(idDict):
        idFile.write(id + '||||' + idDict[id][0] + '||||' + idDict[id][1] + '\n')

    idFile.close()
