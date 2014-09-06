# Fréquences de token et de type des mots finissant par ent et par ant ayant le son /an/
# Je donne ce fichier car il montre comment calculer des fréquences de type et de token
# Ex d'utilisation: perl freq_en.pl Lexique3.txt >Resultats.txt
while(<>){
	@F=split("\t");
	if(($F[0] =~ /ent$/)&&($F[1] =~ /\@$/)){
	$freqtokent = $freqtokent+$F[8];
	$freqtypeent++;
	}
	if(($F[0] =~ /ant$/)&&($F[1] =~ /\@$/)){
	$freqtokant = $freqtokant+$F[8];
	$freqtypeant++;
	}
	
}
print "freqtokent $freqtokent freqtypeent $freqtypeent freqtokant $freqtokant freqtypeant $freqtypeant";