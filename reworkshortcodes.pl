#!/usr/bin/perl

$file=$ARGV[0];
$debugflag=$ARGV[1];

$dbasefile = "UsedCodes";
if ($debugflag) { $dbasefile .= "TEST";}
$dbasefile .= '.txt';

print "Processing $file ....\n";
$time = time;
#$file = 'main.tex';		# Name the file
open(INFO, $file);		# Open the file
@lines = <INFO>;		# Read it into an array
close(INFO);			# Close the file
`mv $file $file.old-$time`;
print "Backup created: $file.old-$time\n";

my @alphanum = (0 .. 9, "a" .. "k","m","n","p" .. "z");
my $divisor = scalar @alphanum;

$code = 0;
open DBASE, $dbasefile;
@dbrows = <DBASE>;
$last_row = $dbrows[$dbrows-1];
@testcode = split(',',$last_row);
if ($testcode[0] > 0){ $code = $testcode[0]+1;}
close DBASE;
open DBASE, ">>$dbasefile";
`cp $dbasefile $dbasefile-$time`;


open INFO, ">$file";
# First clean up unnecessary equation testing


$counter = 1;
$insidetest = 0;
$insidetable= 0;
$skip=0;
$captionprinted = 0;
$tableprinted =0;
foreach $line (@lines)
{
   $skip=0;
   if ($line =~ /\\practiceinfo/)  # this is what to do with existing shortcodes
	{ #Start of the table stuff
		$insidetest=1;
	}
   	if ($insidetest == 1 )
    { 
        print "Sanity check ....\n";
        print $line;
        print "becomes ...\n";
        @fields = split('&',$line);
        foreach $field (@fields)
        {
           if ($field =~ /\)\s+[A-Za-z0-9]{3}(\s+|\\)/)
           {
                $shortcode = &enc($code);
                for ($i = 0 ; $i < 4 - length(&enc($code)) ; $i++)
                { 
                   $shortcode = "0".$shortcode;
                }
                $oldcode = $field =~ m/\)\s+([A-Za-z0-9]{3})(\s+|\\)/;
                if ($oldcode)
                { 
                    print DBASE $code.",".$1.",".$shortcode."\n";
                    $code++;
                }
                $field =~ s/\)\s+[A-Za-z0-9]{3}(\s+|\\)/) $shortcode$1/;
           } 
           if ($field =~ /\\end{tabular}/)
           {
                $insidetest=0;
                $skip=1;
           }
        }
        @newline = join("&",@fields);
        print @newline;
        print INFO @newline;

    } 
   if ($line =~ /\\insertpracticeinfo/)  # this is what to do wehen new shortcodes are required
   {
      $skip=1; # skip regular writing so we lose the insertpracticeinfo directive
      $line =~ m/\\insertpracticeinfo{(\d+)}/;
      $num_codes = $1;
      print "Automatically inserting shortcodes - number to insert $num_codes\n";
      print INFO "% Automatically inserted shortcodes - number to insert $num_codes\n";
      print INFO "\\par \\practiceinfo\n";
      print INFO "\\par \\begin{tabular}[h]{cccccc}\n";
      for ($j=0 ; $j < $num_codes ; $j++ )
      {
        $shortcode = &enc($code);
        for ($i = 0 ; $i < 4 - length(&enc($code)) ; $i++)
        {
            $shortcode = "0".$shortcode;
        }
        print INFO "% Question ".($j+1) ."\n";
        print INFO "(".($j+1) .".)\t".$shortcode."\t";
        print DBASE $code.",.---,".$shortcode."\n";
        if (($j+1)%6 == 0)
        {
            print INFO "\\\\ % End row of shortcodes";
        }else 
        {
            print INFO "&";
        }
        print INFO "\n";
        $code++;
      }
      print INFO "\\end{tabular}\n";
      print INFO "% Automatically inserted shortcodes - number inserted $num_codes\n";

   }
   if ($insidetest == 0 && $skip == 0 ){ print INFO $line;	}		# Print the array
}


exit 0;

sub dec {

  my $num = shift;

  # strip leading 0's
  $num =~ s/$0+//g;

  my ($y, $result) = (0, 0);

  foreach (split(//, reverse($num))) {
    my $found = 0;

    foreach my $item (@alphanum) {
      if ($item eq $_) {
        last;
      }
      $found++;
    }

    my $temp = $found * ($divisor ** $y);
    $result += $temp;
    $y++;
  }

  return $result;
}

sub reduce {
  return (int($_[0] / $divisor), $_[0] % $divisor);
}

sub enc {

  my $num = shift;
  my $end = "";

  my ($a, $b) = reduce($num);
  $end = $alphanum[$b] . $end;
  until ($a < $divisor) {
    ($a, $b) = reduce($a);
    $end = $alphanum[$b] . $end;
  }

  $end = $alphanum[$a] . $end unless $a == 0;

  return $end;
}



