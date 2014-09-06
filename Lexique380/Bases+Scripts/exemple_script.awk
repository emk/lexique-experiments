# Programme sélectionnant les entrées ayant une fréquence supérieur à 100, les mots commençant par b et finissant par e
# gawk -f exemple_script.awk Graphemes.txt >Resultats.txt
# On lui dit que les colonnes sont séparées par des tabulations (FS="\t") et que l'on désire que les champs de sortie soient aussi séparés par des tab OFS="\t"
#Field Separator = tab(\t) and Output Field Separator=(\t)
BEGIN {FS="\t"; OFS="\t";}

  # Si la colonne 3 est >50 et que la colonne commence par b et que la colonne 1 finit par e alors écrit les colonnes 1 et 8 

{
	if (($8 > 50) && ($1 ~ /^b/) && ($1 ~ /e$/)){print $1,$8}
}
