# orth2cv.pl by Boris New (http://www.borisnew.org)
# Use it for having the abstract orthographic representation: for instance, if you give him arbre he will produce vcccv

# Ex: perl orth2cv.pl Lexique3.txt | cut -f12,13,18 >sortie.txt

### Use French locales (useless but can be helpful in another script)
#use locale; use POSIX 'locale_h';
#setlocale(LC_CTYPE, "fr_FR.ISO8859-1");

$"="\t";
$,="\t";

while(<>) {
	@F=split("\t");
	if ($. != 1){print"@F";}
	else {
	
	$F[11] =~ s/[���������������]/V/g;
	$F[11] =~ s/�/C/g;
	$F[12] =~ s/[���������������]/V/g;
	$F[12] =~ s/�/C/g;
	$F[17] =~ s/[���������������]/V/g;
	$F[17] =~ s/�/C/g;
	
	print "@F";
	}
}
	