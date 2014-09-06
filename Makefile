all: lexique.sqlite3

# Create a text version of the first 10 columns of the Lexique database.
lexique.txt: Lexique380/Bases+Scripts/Lexique380.txt
	iconv -f ISO-8859-15 -t UTF-8 $< | tail -n+2 | cut -f 1-10 > $@

# Create our MySQL database.
lexique.sqlite3: createdb.sql lexique.txt
	sqlite3 $@ < createdb.sql

# Delete generated files.
clean:
	rm -f lexique.txt lexique.sqlite3

# These rules do not correspond to actual files, so mark them as such.
.PHONY: all clean
