# Random 1.00 Boris New
# Effectue un tirage aléaoire de 5000 lignes dans un fichier (changer "nombre" pour en tirer plus ou moins)
# gawk -f random.awk Lexique3.txt >PetiteBase.txt

function roll(n){return (1 + int(rand()* n))}
{
nombre=5000;
a[NR]=$0;
}
END{

for (i=1;i<=nombre;i++){
	nb[i]=roll(FNR);}
for (i=1;i<=nombre;i++){print a[nb[i]]}
} 