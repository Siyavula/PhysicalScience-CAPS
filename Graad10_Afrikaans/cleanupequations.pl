#!/usr/bin/perl

$file=$ARGV[0];

print "Processing $file ....\n";

#$file = 'main.tex';		# Name the file
open(INFO, $file);		# Open the file
@lines = <INFO>;		# Read it into an array
close(INFO);			# Close the file
`mv $file $file.old`;

open INFO, ">$file";
# First clean up unnecessary equation testing

$counter = 1;
$insidemathtest = 0;
$insidemath= 0;
$insidetable = 0;
$skip=0;
foreach $line (@lines)
{
   $skip=0;
   if ($line =~ /\\typeout{math as usual width = \\the\\mymathboxwidth}/)
   {
    $skip=1;
   }
   if ($line =~ /\\settowidth{\\mymathboxwidth}{\\begin{equation}/) 
	{ 
		$name = $line;
		$name =~ s/\\settowidth{\\mymathboxwidth}{.*//;
        print INFO $name;
		$insidemathtest=1;
	}
   	if ($insidemathtest == 1 )
    { 
        if ($line =~ /end of conditional for this bit of math/)
        {
            $insidemathtest=0;
            $skip=1;
        }
        if ($line =~ /else, if it doesn/)
        {
           $insidemath=0;
        }
        if ($insidemath==1)
        {
            print INFO $line;
        }
        if ($line =~ /if the math fits, do it again, for real/)
        {
           $insidemath=1;
        }
    } 
   	if ($insidemathtest == 0 && $skip == 0 ){ print INFO $line;	}		# Print the array
}



