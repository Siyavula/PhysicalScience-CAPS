#!/usr/bin/perl

$file = 'main.tex';		# Name the file
open(INFO, $file);		# Open the file
@lines = <INFO>;		# Read it into an array
close(INFO);			# Close the file
$counter = 1;
$inside = 0;
foreach $line (@lines)
{
   if ($line =~ 'chapter{') 
	{ 
		close(INFO);			# Close the file
		$name = $line;
		$name =~ s/\\chapter{(.*) - Grade.*/\1/;
		$name =~ s/ //g;
		$name =~ s/\W//g;
		open(INFO, '>PhysSci_Gr10_Ch_'.$counter."-$name.tex");
		$counter++;
		$inside=1;
	}
   	if ($inside == 1 ){ print INFO $line;	}		# Print the array
}



