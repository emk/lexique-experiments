# PointUni.pl 1.00 Boris New
# Prend en première colonne une liste de mots TRIEE (faites un "sort votrefichier.txt" avant)
# Donne le point d'unicité
# Ex: perl pointuni.pl PetiteBase.txt >Resultats.txt

$"="\t";
$,="\t";
open(UN,"<$ARGV[0]"); 
# Il scanne le fichier une première fois afin d'avoir le prochain mot
while(<UN>){ 
	chomp;
	@F=split("\t");
	$mot[$.]=$F[0];
}
close(UN); 
# Recommence le scanne du fichier
open(DEUX,"<$ARGV[0]"); 
LINE:
while(<DEUX>){ 
	$pointuni = 1;
	$tok = "";
	$prev_tok = "";
	$next_tok = "";

	chomp;
	@F=split("\t");
	@G=split("",$F[0]);
	@next_mot=split("",$mot[$.+1]);
	@prev_mot=split("",$mot[$.-1]);
	# Scanne pour chaque lettre du mot de la première colonne
	for ($i=0;$i<@G;$i++){
	 #Crée les tokens (suite de lettres) du mot, du mot qui le précède, et du mot qui suit
		$tok .= $G[$i];
		$prev_tok .= $prev_mot[$i];
		$next_tok .= $next_mot[$i];
		if ($i == @G-1){print @F,"$pointuni\n"; next LINE;}
		if (($tok eq $next_tok)||($tok eq $prev_tok)){
			$pointuni++;}
		elsif ( ( ($tok ne $next_tok)&&($tok ne $prev_tok))){
			print @F,"$pointuni\n"; next LINE;}
	}
}
 
close(DEUX); 
