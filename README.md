# French Vocabulary Frequency with Lexique

[Lexique 3](http://lexique.org/) is a French word database from the
Université de Savoie.  SQLite 3 is a fast, local database.  IPython is a
cool way to work with and visual scientific data.

## Viewing the notebook online

[A notebook with lots of interesting data][nb] is available via nbviewer.

[nb]: http://nbviewer.ipython.org/github/emk/lexique-experiments/blob/master/French%20Vocabulary%20Frequency%20with%20Lexique.ipynb

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
