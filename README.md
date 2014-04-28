Yelp-Dataset
============

http://www.yelp.com/dataset_challenge/

## Installation
Download the dataset and place all the files `yelp_academic_dataset_*.json` in a directory called `data/` which is part of the gitignore.

You should have the following installed:

- `scipy`
- `numpy`
- `textblob`
- `sklearn` (can be installed through `pip install -U scikit-learn`)
- `nltk`
- `sqlalchemy`

After you install textblob, you need to run the following:

    python -m textblob.download_corpora

## Database
We are using SQLite with SqlAlchemy as the ORM.

To auto-create the database schema and populate the tables, run `import_data_to_sql` in `parse.py`

    $ python -i parse.py
    >>> import_data_to_sql()

Great it's imported, now what? Read [the docs](http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#querying). You can do some cool queries based on the three models we have: Tip, Business, Review (see `db.py`).

An example query:

    session.query(Tip).filter(Tip.bid == 'U7jOpLoLXYphWFqS6JO8mQ').all()

