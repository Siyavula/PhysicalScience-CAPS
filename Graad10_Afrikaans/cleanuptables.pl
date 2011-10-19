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
$insidetabletest = 0;
$insidetable= 0;
$skip=0;
$captionprinted = 0;
$tableprinted =0;
foreach $line (@lines)
{
   $skip=0;
   if ($line =~ /\\typeout{table as usual width = \\the\\mytableboxwidth}/)
   {
    $skip=1;
   }
   if ($line =~ /% how many colspecs?/) 
	{ #Start of the table stuff
		$insidetabletest=1;
	}
   	if ($insidetabletest == 1 )
    { 
        if ($line =~ /}% ending lr\/para test clause/)
        {   #done with all of this table stuff
            $captionprinted=0;
            $insidetabletest=0;
            $skip=1;
            $tableprinted=0;
        }
        if ($line =~ /%\\end{table}/)
        {  # done with the good table to output
           $insidetable=0;
           #$name = $line;
           #$name =~ s/} % end mytableboxwidth set//;
           #print INFO $name;
        }
        if ($insidetable==1)
        {   # output the good table
            if ($line =~ /% count in rowspan/ || $line =~ /% align\/colidx/  || $line =~ /% rowcount/ || $line =~ /% Formatting a regular cel/ 
            || $line =~ /% rowspan info/)# || $line =~ /% make-rowspan-placeholders/)
            {   # skip huge numbers of comments
                $skip=1;
            }
            if ($skip==0) { print INFO $line; }
            $skip=0;
        }
        if ($line =~ /}{ % else/ && $tableprinted == 0 )
        {  # start the good table - there are two that meet this criteria
           $insidetable=1;
           $tableprinted=1;
           $name = $line;
           $name =~ s/}{ % else/\\begin{table}[H]/;
           print INFO $name;
        }
        if ($line =~ /\\small\\bfseries/ && $captionprinted == 0 && $tableprinted==1 )
        {  # print the caption
           $name = $line;
           $name =~ s/center/caption/g;
           print INFO $name;
           print INFO "\\end{table}\n";
           $captionprinted=1;
        }
    } 
   	if ($insidetabletest == 0 && $skip == 0 ){ print INFO $line;	}		# Print the array
}



