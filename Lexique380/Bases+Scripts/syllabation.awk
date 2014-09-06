#!/usr/bin/gawk -f
#
# This script reads a tab-separated file and syllabifies the columns pointed to by the variable'phons' (ot the first column, by default).
#
#
# Author: Christophe Pallier (christophe.pallier@m4x.org)
#
# License: GNU (cf. http://www.gnu.org)
#
# Last update: 17 March 2005
# (original date: the first version of this script was written during 
#  my dissertation, in 1993)
#
# 2004/03/17: Ok for homophones (�jections)
#
# 2004/05/13: merge of the Brulex & Lexique versions
#             correction for the 'j'->'Z' (viellerie) in Lexique 
#             add rule '[td]R' (comment on 'autrefois' by Sprenger-Charolles)
# 2004/04/26: add rule with 5 consonnants (comment on 'exploit' by J. Goslin)
#
#    
#
# Note: changed \377 into y-umlaut to run under DOS (bug gawk).

BEGIN {
  FS="\t"; 
  OFS="\t";
  
  if (code=="brulex") {
    V="[aiouy�����^eE�AO_]"; # vowels
    C="[ptkbdgfs/vzjmnN�]"; # consonants except liquids & semivowels
    C1="[pkbgfs/vzj]";
    L="[lR]"; # liquids 
    Y="[��\377]"; # semi-vowels \377 stands for y-umlaut
    X="[ptkbdgfs/vzjmnN�xlR��\377]"; # all consonants 
  } else { # code == LAIPTTS)
    V="[iYeE2591a@oO�uy�]";   # Vowels
    C="[pbmfvtdnNkgszxSZGh]";  # Consonants except liquids & semivowels
    C1="[pkbgfsSvzZ]";
    L="[lR]"; # liquids
    Y="[j8w]"; # semi-vowels
    X="[pbmfvtdnNkgszSZGlRrhxGj8w]";   # all consonants, including semivowels
  }
  if (phons==0) phons=2;
}

{
 a=$phons;
 n=1
}

{
   while (i= match (a, V V)) {
    a=substr(a,1,i) "-" substr(a,i+1,length(a)); n++; }

  while (i= match(a, V X V)) { 
    a=substr(a,1,i) "-" substr(a,i+1,length(a)); n++}

  while (i=match(a, V Y Y V)) {
    a=substr(a,1,i+1) "-" substr(a,i+2, length(a)); n++} 

  while (i=match(a, V C Y V)) {
    a=substr(a,1,i) "-" substr(a,i+1, length(a)); n++} 

  while (i=match(a, V L Y V)) {
    a=substr(a,1,i) "-" substr(a,i+1, length(a)); n++}

  while (i=match(a, V "[td]R" V)) {
    a=substr(a,1,i) "-" substr(a,i+1, length(a)); n++} 

  while (i=match(a, V "[td]R" Y V)) {
    a=substr(a,1,i) "-" substr(a,i+1, length(a)); n++} 

  while (i=match(a, V C1 L V)) {
    a=substr(a,1,i) "-" substr (a,i+1,length(a)); n++}

  while (i=match(a, V X X V)) {
    a=substr(a,1,i+1) "-" substr(a,i+2, length(a)); n++}

  while (i= match(a, V X X X V)) {
    a=substr(a,1,i+1) "-" substr(a,i+2,length(a)); n++}

  while (i=match(a, V X X X X V)) {
    a=substr(a,1,i+1) "-" substr(a,i+2,length(a)); n++}

  while (i=match(a, V X X X X X V)) {
    a=substr(a,1,i+1) "-" substr(a,i+2,length(a)); n++}

# Give the correct syllable count for homophones
if (a~/;/){
   split(a, nb, ";")
   nb[1]=gsub(/-/,"-",nb[1])+1
   nb[2]=gsub(/-/,"-",nb[2])+1
   n=nb[1] ";" nb[2]
   }

# suppress the final schwa (^) in some multisyllabic words 
# notr^ -> notR
# ar-bR^   =>  aRbR
  b=gensub(/-([^-]+)\^$/,"\\1",1,a) ;  
  if (b!=a) { # there is a schwa to delete
    a=b; 
    $phons=substr($phons,1,length($phons)-1);
    n--;
      }
# meme chose quand schwa='*'
  b=gensub(/-([^-]+)\*$/,"\\1",1,a) ;  
  if (b!=a) { # there is a schwa to delete
    a=b; 
    $phons=substr($phons,1,length($phons)-1);
    n--;
      }


# compute the CVY skeleton
  sk= "";
  for (i=1;i<=length(a);i++) {
    ph=substr(a,i,1);
    if (ph~V) sk=sk"V";
    else if ((ph~C)||(ph~L)) sk=sk"C";
    else if (ph~Y) sk=sk"Y";
    else sk=sk ph;
  }
}

{ print a,n,sk }
