# Programme s�lectionnant les entr�es ayant une fr�quence sup�rieur � 100, les mots commen�ant par b et finissant par e
# gawk -f exemple_script.awk Graphemes.txt >Resultats.txt
# On lui dit que les colonnes sont s�par�es par des tabulations (FS="\t") et que l'on d�sire que les champs de sortie soient aussi s�par�s par des tab OFS="\t"
#Field Separator = tab(\t) and Output Field Separator=(\t)
BEGIN {FS="\t"; OFS="\t";}

  # Si la colonne 3 est >50 et que la colonne commence par b et que la colonne 1 finit par e alors �crit les colonnes 1 et 8 

{
	if (($8 > 50) && ($1 ~ /^b/) && ($1 ~ /e$/)){print $1,$8}
}
