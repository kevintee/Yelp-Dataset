Yelp-Dataset
============

http://www.yelp.com/dataset_challenge/

Download the dataset and place all the files `yelp_academic_dataset_*.json` in a directory called `data/` which is part of the gitignore.

You should have the following installed:

- `scipy`
- `numpy`
- `textblob`
- `sklearn` (can be installed through `pip install -U scikit-learn`)
- `nltk`

After you install textblob, you need to run the following:

    python -m textblob.download_corpora
