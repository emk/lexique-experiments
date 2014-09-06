# Prend des mots de la première colonne du fichier d'entrées et les écrit à l'envers arbre -> erbra
# gawk -f reverse.awk Graphemes.txt >Resultats.txt

BEGIN{FS="\t";OFS="\t";}
{
split($1, tab, "");
for (i=length($1);i>0;i--){ 
if (i != 1){printf tab[i]}
else {printf tab[i] "\n";}
}
}