# Lemmes 1.0 par Boris New

# Permet de générer une base organisée par lemmes
# Utilisation:
# perl lemme.pl lexique3.txt | sort >lex3.lemmes.txt

$,="\t";

LINE:
while(<>){
	if ($.==1){next LINE;}
	chomp;
	@F = split("\t");
	$F[3]=substr($F[3],0,3);
	$cgram{"$F[2]$F[3]"} = $F[3];
	$ortho{"$F[2]$F[3]"} .= "$F[0];";
	$phono{"$F[2]$F[3]"} .= "$F[1];";
	if ($F[5]ne""){$genre{"$F[2]$F[3]"} .= "$F[4];";}
	if ($F[6]ne""){$nombre{"$F[2]$F[3]"} .= "$F[5];";}
	$freqfilm{"$F[2]$F[3]"} .= "$F[8];";
	$freqlivre{"$F[2]$F[3]"} .= "$F[9];";
	$freqlemfilm{"$F[2]$F[3]"} = "$F[6];";
	$freqlemlivre{"$F[2]$F[3]"} = "$F[7];";
}
print "1_lemme","2_cgram","3_ortho","4_phono","5_genre","6_nombre","7_freqfilms","8_freqlivres","9_freqlemfilms","10_freqlemlivres";
print "\n";
foreach $i (keys %cgram) {
# Là j'ai frefrant seul 
 if ($i ne ""){
	$cgram{"$i"}  =~ s/\;$//g;
	$ortho{"$i"}  =~ s/\;$//g;
	$phono{"$i"}  =~ s/\;$//g;
	$genre{"$i"}  =~ s/\;$//g;
	$nombre{"$i"} =~ s/\;$//g;
	$freqfilm{"$i"}    =~ s/\;$//g;
	$freqlivre{"$i"}   =~ s/\;$//g;
	$freqlemfilm{"$i"} =~ s/\;$//g;
	$freqlemlivre{"$i"}=~ s/\;$//g;
	$mot = $i;
	$mot =~ s/[A-Z].*//g;
 print $mot, $cgram{$i}, $ortho{$i}, $phono{$i}, $genre{$i}, $nombre{$i}, $freqfilm{$i}, $freqlivre{$i}, $freqlemfilm{$i}, $freqlemlivre{$i};
 print "\n";
}
}