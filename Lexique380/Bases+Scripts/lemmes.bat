@ECHO OFF
echo Ca prend un peu de temps... Veuillez patienter...
perl lemmes.pl lexique3.txt | sort >Lex3.lemmes.txt
echo La base Lex3.lemmes.txt a été crée
