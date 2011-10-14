#!/usr/bin/python
# coding=utf-8
# Copyright Johannes 2011
# mail@johanneswilm.org
# Licensed under the GPL v. 3

def lyx2tex(filename):
	basefilename=filename[:-4]
	print "Converting " + filename + " -> "+basefilename+".tex..."
	runcommand('lyx -e luatex -f all '+filename)
	#print "Removing extra headers..."
	#regex_remove_shell(basefilename+'.tex',r'(?s)\\begin{document}(.*)\\end{document}')
	#print "Remove extra bibliographies..." # remove natbib bibliographies
	#regex_replace(basefilename+'.tex',r'\\bibliography{([^}]*)}','')	
	print "Fixing latex..."
	runcommand('rpl "{[}" "[" '+basefilename+'.tex')
	runcommand('rpl "{]}" "]" '+basefilename+'.tex')
	runcommand('rpl -q ">{\\raggedright}" "" '+basefilename+'.tex')
	runcommand('rpl -q ">{\\raggedleft}" "" '+basefilename+'.tex')
	#runcommand('rpl -q "\\lyxdot " "." '+basefilename+'.tex')
	return filename[:-4]+'.tex'

from sys import exit
from commands import getstatusoutput

def runcommand(command,exit_on_failure=True):
	output = getstatusoutput(command)
	if (output[0] != 0 and exit_on_failure==True):
		print command
		print output[1]
		exit()
	return output

import re

def regex_replace(filename,from_string,to_string):
	orig_filecontents = file(filename).read()
	replacement_file = open(filename,'w')
	replacement_file.write(re.sub(from_string, to_string, orig_filecontents))
	replacement_file.close()
	return True

def split_html(filename,words):
	splits = words/5000
	regex_replace(filename,'<html><body><p>','')
	regex_replace(filename,'</body></html>','')
	orig_filecontents = file(filename).read()
	orig_filecontents_plist = orig_filecontents.split('<p>')
	orig_filecontents_plist_len = len(orig_filecontents_plist)
	orig_filecontents_plist_len_part = orig_filecontents_plist_len/splits
	for split in range(splits):
		part_filecontents = '<html><body><p>' + "<p>".join(orig_filecontents_plist[(orig_filecontents_plist_len_part*split):(orig_filecontents_plist_len_part*(split+1))]) + '</body></html>'
		part_file = open(filename[:-5]+'_'+str(split)+'.html','w')
		part_file.write(part_filecontents)
		part_file.close()
	runcommand('rm '+filename)
	return True

def spacerepl(matchobj):
	return matchobj.group(0)+matchobj.group(1).replace(' ','SPACEMARK')+matchobj.group(2)

def dotrepl(matchobj):
	return matchobj.group(0)+matchobj.group(1).replace('.','DOTMARK')+matchobj.group(2)

def commarepl(matchobj):
	return matchobj.group(0)+matchobj.group(1).replace(',','COMMAMARK')+matchobj.group(2)



def fit_for_html(html_file):
	regex_replace(html_file,'{}`','`')# cleaning up
	regex_replace(html_file,r'\\%','PERCENTAGE')
	regex_replace(html_file,r'%([^\n]*)\n',r'\n')# cleaning up
	regex_replace(html_file,'PERCENTAGE',r'<span class="notranslate">\\%</span>')	
	regex_replace(html_file,r'^^','<html><body><div class="notranslate"><p>')
	regex_replace(html_file,r'$$','</p></body><html>')
	regex_replace(html_file,r'\n\n',r'\n</p><p>\n')
	regex_replace(html_file,r'<body>\n</p>',r'<body>\n')
	regex_replace(html_file,r'\\begin{document}',r'\\begin{document}</p></div>\n<p>')
	regex_replace(html_file,r'\\\\','SLASH')
	regex_replace(html_file,r'\\\[','BEGINPARENTESIS')
	regex_replace(html_file,r'\\\]','ENDPARENTESIS')
	regex_replace(html_file,r'\\\{','BEGINBRACKET')
	regex_replace(html_file,r'\\\}','ENDBRACKET')
	regex_replace(html_file,r'\{\}','EMPTYBRACKET')
	regex_replace(html_file,r'\\protect','')	
	regex_replace(html_file,r'\\(hline|tabularnewline|ldots| \& |item)',r'<span class="notranslate">\\\1</span>') # without contents
	regex_replace(html_file,r'\\(index){([^}]*)}',r'<span class="notranslate">\\\1{</span>\2<span class="notranslate">endparentesis</span>') # translate contents
	regex_replace(html_file,r'\\(citep|citet|citetitle|citeauthor|begin|includegraphics|label|bibliography|input|include|ref|vref|pageref)({|\[)([^}]*)}',r'<span class="notranslate">\\\1\2\3endparentesis</span>') # don't translate contents
	regex_replace(html_file,r'\\(end)({|\[)([^}]*)}',r'</p><p class="notranslate">\\\1\2\3endparentesis</p><p>') # don't translate contents and add paragraph end	
	regex_replace(html_file,r'\\(emph){([^}]*)}',r'<span class="notranslate">\\\1{</span>\2<span class="notranslate">endparentesis</span>') # translate contents
	regex_replace(html_file,r'\\(chapter|section|subsection|subsubsection|chapter\*|section\*|subsection\*|subsubsection\*|caption|footnote){([^}]*)}',r'<span class="notranslate">\\\1{</span>\2<span class="notranslate">}</span>') # translate contents
	regex_replace(html_file,r'\\(chapter|section|subsection|subsubsection|chapter\*|section\*|subsection\*|subsubsection\*|caption|footnote)\[([^\]]*)\]{([^}]*)}',r'<span class="notranslate">\\\1[</span>\2<span class="notranslate">]{</span>\3<span class="notranslate">}</span>') # translate contents
	regex_replace(html_file,r'\\(addcontentsline)({[^}]*})({[^}]*}){([^}]*)}',r'<span class="notranslate">\\\1\2\3{</span>\4<span class="notranslate">}</span>') # translate some contents
	regex_replace(html_file,r'\\(item</span>) \[{([^}]*)}\]',r'\\\1 <span class="notranslate">[</span>\2<span class="notranslate">]</span>') # don't translate and remove extra bracket
	regex_replace(html_file,r'([|{)([^]}]*)(]|})',spacerepl) # temporarily remove spaces inside arguments
	regex_replace(html_file,r'([|{)([^]}]*)(]|})',dotrepl) # temporarily remove dots inside arguments
	regex_replace(html_file,r'([|{)([^]}]*)(]|})',commarepl) # temporarily remove commas inside arguments
	regex_replace(html_file,r'\\(parencites)([^\s\\\<\.\,]*)(\r|\s|\\|\<|\.|\,|\r)',r'<span class="notranslate">\\\1\2</span>\3') # don't translate contents, goes on forever
	regex_replace(html_file,'endparentesis','}') 
	regex_replace(html_file,r'</span>({|\[)([^\s\r]*)(\r|\s)',r'\1\2</span>\3') # some arguments fell outside of span
	regex_replace(html_file,'&','<span class=\"notranslate\">&amp;</span>')
	regex_replace(html_file,r' \\\$',r'<span class="notranslate">-\\$</span>') # with space in front
	regex_replace(html_file,r'\\\$',r'<span class="notranslate">\\$</span>')
	regex_replace(html_file,'~','<span class="notranslate">~</span>')
	regex_replace(html_file,'\`',r'<span class="notranslate">`</span>')
	regex_replace(html_file,'\'s',"APOSMARKs") # genetive s singular
	regex_replace(html_file,'s\'',"sAPOSMARK") # genetive s plural
	regex_replace(html_file,r'([A-z])\'([A-z])',r"\1APOSMARK\2") # inside word, not likely quotation marks
	regex_replace(html_file,'\''," <span class=\"notranslate\">'</span>")
	regex_replace(html_file,'APOSMARK','\'')
	regex_replace(html_file,'SPACEMARK',' ')
	regex_replace(html_file,'DOTMARK','.')
	regex_replace(html_file,'COMMAMARK','.')
	regex_replace(html_file,'BEGINPARENTESIS',r'<span class="notranslate">\\\[</span>')
	regex_replace(html_file,'ENDPARENTESIS',r'<span class="notranslate">\\\]</span>')
	regex_replace(html_file,'BEGINBRACKET',r'<span class="notranslate">\\\{</span>')
	regex_replace(html_file,'ENDBRACKET',r'<span class="notranslate">\\\}</span>')
	regex_replace(html_file,'SLASH',r'<span class="notranslate">\\\\</span>')
	regex_replace(html_file,'EMPTYBRACKET',r'<span class="notranslate">{}</span>')
	regex_replace(html_file,r'</span>\.',r'.</span>')
	regex_replace(html_file,'</span>,',',</span>')
#	regex_replace(html_file,r'{','BEGINBRACKET')
#	regex_replace(html_file,r'}','ENDBRACKET')	
	return True
	

		
def import_lyx():
	lyx_files = runcommand('ls *lyx')[1].split()
	for lyx_file in lyx_files:
		tex_file = lyx2tex(lyx_file)
		html_file = tex_file.replace('.','_') + '.html'
		runcommand('cp ' + tex_file + ' ' + html_file)
		fit_for_html(html_file)
		words = int(runcommand('wc -w ' + html_file)[1].split()[0])
		if words / 5000 > 1:
			split_html(html_file,words)

def exclamrepl(matchobj):
	return matchobj.group(0).replace('! ','!')

def fix_latex():
	tex_files = runcommand('ls *tex')[1].split()
	for tex_file in tex_files:
		regex_replace(tex_file,r'Translated version of ([^\.]*)\.html','') # remove header
		regex_replace(tex_file,r'\\index{([^}]*)}',exclamrepl) # replace exclamation marks
		regex_replace(tex_file,r'({|\[) ',r'\1') # remove extra spaces
		regex_replace(tex_file,r' (}|\])',r'\1') # remove extra spaces
		regex_replace(tex_file,r' \\index',r'\\index') # remove extra spaces
		regex_replace(tex_file,r'` ',r'`') # remove extra spaces
		regex_replace(tex_file,' \'','\'') # remove extra spaces
		regex_replace(tex_file,' ~ ','~') # remove extra spaces
		regex_replace(tex_file,r' \\\\$',r'\\$') # remove extra spaces
		regex_replace(tex_file,r'\-\\\\$',r'\\$') # remove extra spaces

import sys

if __name__ == "__main__":
	sys_argv=sys.argv
	command_options="i"
	if len(sys_argv) > 1 and sys_argv[1][0]== '-':
		command_options=sys_argv.pop(1)[1:]
	if 'h' in command_options:
		print
		print "Usage:"
		print sys_argv[0]+" -[hif]"
		print
		print "h)elp"
		print "i)import"
		print "f)ix output"
		print
	if 'i' in command_options:
		import_lyx()
	if 'f' in command_options:
		fix_latex()