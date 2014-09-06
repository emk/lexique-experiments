# S'utilise en conjonction avec voisins1.pl
# Ouvrir voisins1.pl pour avoir plus d'explications

open(UN,"<$ARGV[0]");
while(<UN>){

	$lettre=0;
	chomp;
	@F=split("\t");
	#@F=@F;
	for ($i=1;$i<@F;$i++){
		$vois{$F[$i]}++;
		}
}
close(UN);

open(DEUX,"<$ARGV[0]");
while(<DEUX>){
	chomp;
	@F=split("\t");
	for ($i=1;$i<@F;$i++){
	#if($vois{$F[$i]}==1){$vois{$F[$i]}=0;}
	#$vois{$F[$i]}--;
	$somvois{$F[0]} += $vois{$F[$i]}
}
}
close(DEUX);



foreach $i (keys %somvois){
	$som=$somvois{$i}-(length($i));
	print "$i\t$som\n";
}	


#print $vois{"dan_e"};
#print $vois{"arb_e"};
