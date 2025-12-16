# %%
import pandas as pd
import romkan

# To sex,kanji,hiragana,romaji

wiki = pd.read_csv("japanese-celeb-dataset/data.csv")


wiki["kanji"] = wiki["kanji"].str.split(" ").str[1]
wiki["hiragana"] = wiki["hiragana"].str.split(" ").str[1]

wiki["birth_year"] = pd.to_numeric(wiki["birth_year"], errors="coerce").astype("Int64")
wiki = wiki[["sex", "kanji", "hiragana", "birth_year"]]
wiki.to_csv("names/wiki.csv", index=False)

# %%
