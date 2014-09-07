# Import some libraries we'll need.
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import brewer2mpl
from IPython.display import HTML

# Generate some pretty colors for plots. The defaults are horrible.
colors = brewer2mpl.get_map('Dark2', 'Qualitative', 8).mpl_colors

# Connect to the database.
db = sqlite3.connect("lexique.sqlite3")

# Run a simple SQL command and return the result.
def sql(command, **kw):
    return pd.read_sql(command, db, **kw)
