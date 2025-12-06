# %%

import pandas as pd

dataset = pd.read_csv("dataset.csv")
dataset.columns = ["dataset", "sex", "kanji", "hiragana"]
# %%
