# Prend des mots de la premi�re colonne du fichier d'entr�es et les �crit � l'envers arbre -> erbra
# gawk -f reverse.awk Graphemes.txt >Resultats.txt

BEGIN{FS="\t";OFS="\t";}
{
split($1, tab, "");
for (i=length($1);i>0;i--){ 
if (i != 1){printf tab[i]}
else {printf tab[i] "\n";}
}
}