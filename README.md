# French Vocabulary Frequency with Lexique

[Lexique 3](http://lexique.org/) is a French word database from the
Université de Savoie.  SQLite 3 is a fast, local database.  IPython is a
cool way to work with and visualize scientific data.

I'm also merging in the [French verb conjugation rules][fvcr] data set,
which will provide detailed information about regular verbs.

[fvcr]: http://sourceforge.net/projects/fvcr/

## Viewing the notebook online

[A notebook with lots of interesting data][nb] is available via nbviewer.

[nb]: http://nbviewer.ipython.org/github/emk/lexique-experiments/blob/master/French%20Vocabulary%20Frequency%20with%20Lexique.ipynb

## Licenses

- The data in the directory `Lexique380` is distributed under a Creative
  Commons license, which you can find in that directory.
- The [conjugation rules][fvcr] in `verbs-0-2-0.xml` are in the public
  domain, according to the SourceForge project page where I found them.

## Running it

You will need:

- A environment which defaults to UTF-8 encoding.
- A bunch of normal Unix/Linux command-line tools.
- `iconv`
- `sqlite3`
- Python 2.7.3 or later.
- `pip`

Run the following commands from the command line:

    # Install ipython and supporting libraries.
    pip install -U pandas
    pip install -U ipython[notebook]
    pip install -U brewer2mpl

    # Generate our database from the raw Lexique data.
    make

    # Open up our interactive notebook in a web browser.
    ipython notebook 'French Vocabulary Frequency with Lexique.ipynb'
