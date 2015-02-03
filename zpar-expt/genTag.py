#!/usr/bin/python
# Filename: countDPos.py
import string
import sys

def getTags( input_file ):
	fin = file(input_file);
	posSet = set();
	depSet = set();
	for line in fin:
		words = line.strip().split(' ');
		if len(words) < 4 :
			continue;
		posSet.add(words[1]);
		depSet.add(words[3]);
	fin.close();
	postags = '"-NONE-", "-BEGIN-", "-END-" ';
	posnum = 0;
	for word in posSet:
		if word == "-NONE-" or word == "-BEGIN-" or word == "-END-":
			continue;
		postags = postags + ',"' + word + '"'
		posnum += 1;
	deptags = '"-NONE-", "-ROOT-"';
	depnum = 0;
	for word in depSet:
		if word == "-NONE-" or word == "-ROOT-":
			continue;
		deptags = deptags + ',"' + word + '"'
		depnum += 1;
	return (postags, posnum, deptags, depnum);

def getEnum( num, tag ):
	enum = ''
	if tag == 'TAG':
		enum = 'PENN_TAG_NONE=0, PENN_TAG_BEGIN, PENN_TAG_END';
		closed = 'false, true, true';
	else:
		enum = 'PENN_DEP_NONE=0, PENN_DEP_ROOT';
	i = 0;
	while i < num :	
		enum = enum + ', PENN_' + tag +'_' + str(i);
		if tag == 'TAG':
			closed += ', false'
		i = i+1;
	enum += ', PENN_' + tag + '_COUNT'
	if tag == 'DEP':
		return enum
	return (enum, closed);


def replacePos(replace_file, tags, enum, tag, closed=''):
	fin = file(replace_file);
	fstr = '';
	for lines in fin:
		if lines.strip() == 'const std::string PENN_TAG_STRINGS[] = {};':
			lines = 'const std::string PENN_TAG_STRINGS[] = {' +  tags + '};\n'
		elif lines.strip() == 'const std::string PENN_DEP_STRINGS[] = {};':
			lines = 'const std::string PENN_DEP_STRINGS[] = {' + tags + '};\n'
		elif lines.strip() ==  'enum PENN_TAG_CONSTANTS {};':
			lines = 'enum PENN_TAG_CONSTANTS {' + enum + '};\n'
		elif lines.strip() == 'enum PENN_DEP_LABELS {};':
			lines = 'enum PENN_DEP_LABELS {' + enum + '};\n'
		elif lines.strip() == 'const bool PENN_TAG_CLOSED[] = {};':
			lines = 'const bool PENN_TAG_CLOSED[] = {' + closed + '};\n';
		fstr += lines;
	filename = tag + '.h';
	fout = file( filename, 'w');
	fout.write(fstr);
	fin.close();
	fout.close();

def main(input_file, replace_file1, replace_file2):
	( postags, posnum, deptags, depnum ) = getTags( input_file );
	( posenum, closed) = getEnum( posnum, 'TAG' );
	( depenum ) = getEnum( depnum, 'DEP' ); 
	replacePos(replace_file1, postags, posenum, 'pos', closed);
	replacePos(replace_file2, deptags, depenum, 'label');



if __name__ == "__main__": 
  if len(sys.argv) != 4:
    usage()
    sys.exit(1)
  main(sys.argv[1], sys.argv[2], sys.argv[3]);
