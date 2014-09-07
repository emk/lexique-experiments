-- Make sure our encoding is sane.
PRAGMA encoding = "UTF-8";

-- Set up our original data table.  This is pretty raw.
CREATE TABLE lexique (
ortho TEXT,
phon TEXT,
lemme TEXT,
cgram TEXT,
genre TEXT,
nombre TEXT,
freqlemfilms2 REAL,
freqlemlivres REAL,
freqfilms2 REAL,
freqlivres REAL);
CREATE INDEX lexique_lemme ON lexique (lemme);

-- Import the raw data we generated above.
.separator "\t"
.import "lexique.txt" lexique

-- Create a table containing just the lemmas, not the inflections.  Note
-- that one word may appear multiple times with different parts of speech
-- or gender.
--
-- lemme       cgram       genre       nombre      freqfilms2  freqlivres
-- ----------  ----------  ----------  ----------  ----------  ----------
-- être        VER                                 31195.28    14266.5   
-- je          PRO:per                 s           25983.2     10862.77  
-- de          PRE                                 25220.86    38928.92  
-- ne          ADV                                 22287.84    13841.89  
-- avoir       AUX                                 18539.88    12764.81  
-- pas         ADV                                 18188.15    8795.14   
-- la          ART:def     f           s           14946.48    23633.92  
-- tu          PRO:per                 s           14661.76    2537.03   
-- le          ART:def     m           s           13652.76    18310.95  
-- vous        PRO:per                 p           13589.7     3507.16   
-- il          PRO:per     m           s           13222.93    15832.09  
-- et          CON                                 12909.08    20879.73  
-- avoir       VER                                 12871.23    5937.79   
-- à           PRE                                 12190.4     19209.05  
-- un          ART:ind     m           s           12087.62    13550.68
CREATE TABLE lemme AS
  SELECT lemme, cgram, genre, nombre,
         SUM(freqfilms2) AS freqfilms2, SUM(freqlivres) AS freqlivres
    FROM lexique
    GROUP BY lemme, cgram, genre, nombre;
CREATE INDEX lemme_lemme ON lemme (lemme);
CREATE INDEX lemme_freqfilms2 ON lemme (freqfilms2);
CREATE INDEX lemme_freqlivres ON lemme (freqlivres);
CREATE INDEX lemme_cgram ON lemme (cgram);

-- Like 'lemme', except we ignore parts of speech, gender and number,
-- and just lump everything together.  So 'avoir', etc., should only
-- appear once.
--
-- lemme       freqfilms2  freqlivres
-- ----------  ----------  ----------
-- être        40411.41    21709.87  
-- avoir       32134.77    19230.64  
-- je          25988.48    10862.77  
-- de          25220.96    38928.92  
-- ne          22297.51    13852.97  
-- pas         18315.21    9129.33   
-- le          16953.5     20735.14  
-- la          16028.08    24877.3   
-- tu          14674.16    2543.85   
-- vous        13589.7     3507.16
CREATE TABLE lemme_simple AS
  SELECT lemme,
         SUM(freqfilms2) AS freqfilms2, SUM(freqlivres) AS freqlivres
    FROM lexique
    GROUP BY lemme;
CREATE UNIQUE INDEX lemme_simple_lemme ON lemme_simple (lemme);
CREATE INDEX lemme_simple_freqfilms2 ON lemme_simple (freqfilms2);
CREATE INDEX lemme_simple_freqlivres ON lemme_simple (freqlivres);

CREATE TABLE verbe AS
  SELECT lemme,
         CASE
           WHEN lemme = 'aller' THEN 'aller'
           WHEN lemme LIKE '%er' THEN 'er'
           WHEN lemme LIKE '%ir' THEN 'ir'
           WHEN lemme LIKE '%re' THEN 're'
         END AS groupe,
         SUM(freqfilms2) AS freqfilms2,
         SUM(freqlivres) AS freqlivres
    FROM lemme
    WHERE cgram IN ('VER', 'AUX')
    GROUP BY lemme;
CREATE UNIQUE INDEX verbe_lemme ON verbe (lemme);
CREATE INDEX verbe_groupe ON verbe (groupe);
CREATE INDEX verbe_freqfilms2 ON verbe (freqfilms2);
CREATE INDEX verbe_freqlivres ON verbe (freqlivres);
