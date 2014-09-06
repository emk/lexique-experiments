# Programme sélectionnant les entrées commençant par b et finissant par e, ayant une fréquence de lemme supérieur à 50 (corpus films)
# Ex d'utilisation: perl exemple_script.pl Lexique3.txt >Resultats.txt
$,="\t";

# Parcourt chaque ligne du fichier jusqu'à la fin
while(<>){
  # Enlève le retour chariot (\n) à la fin de la ligne
  chomp;
  # Met les champs séparés par un tab (\t) dans le tableau @F 
  @F = split("\t");
  # Si la colonne 3 est >50 et que la colonne commence par b et que la colonne 1 finit par e alors écrit les colonnes 1 et 7 
	if (($F[6] > 50) && ($F[0] =~ /^b/) && ($F[0] =~ /e$/)){
		# Ecrit les colonnes 1 (nom) et 8 (fréquence frantext)
		print $F[0],$F[6];
		print"\n";
	}
}

