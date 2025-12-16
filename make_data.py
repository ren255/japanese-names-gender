# %%
import pandas as pd
import numpy as np
import romkan
from namedivider import BasicNameDivider
from time import time
from typing import List, Tuple, Dict, Callable
import math
import matplotlib.pyplot as plt
import importlib


enamdict = pd.read_csv("names/enamdict.csv")
facebook = pd.read_csv("names/facebook.csv")
gendec = pd.read_csv("names/gendec.csv")
name_origin = pd.read_csv("names/name_origin.csv")
fb_stats = pd.read_csv("names/fb_stats.csv")
wiki = pd.read_csv("names/wiki.csv")

enamdict.columns = ["sex", "kanji", "hiragana", "romaji"]
wiki.columns = ["sex", "kanji", "hiragana", "birth_year"]
name_origin.columns = ["kanji", "hiragana", "romaji", "sex"]
gendec.columns = ["sex", "kanji", "hiragana", "romaji"]
facebook.columns = ["first_name", "last_name", "sex", "country"]
fb_stats.columns = ["name", "male", "frequency_score"]


def preprocess_gendec(df: pd.DataFrame) -> pd.DataFrame:
    basic_divider = BasicNameDivider()
    df["hiragana"] = df["romaji"].apply(romkan.to_hiragana)
    df["hiragana"] = df["hiragana"].str.split().str[1]
    df["romaji"] = df["romaji"].str.split().str[1]
    df["kanji"] = df["kanji"].apply(lambda x: basic_divider.divide_name(x).given)

    df["sex"] = df["sex"].str.lower()

    return df[["sex", "kanji", "hiragana"]]


def preprocess_facebook(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df["sex"] == "M", "sex"] = "male"
    df.loc[df["sex"] == "F", "sex"] = "female"

    df = df.dropna(subset=["first_name", "sex"])
    df["hiragana"] = df["first_name"].apply(romkan.to_hiragana)
    df = df[~df["hiragana"].str.contains(r"[a-zA-Z]", regex=True, na=False)]

    mask = ~df["hiragana"].str.fullmatch(r"[ぁ-んー]+", na=False)
    df["kanji"] = df["hiragana"].where(mask)
    df.loc[mask, "hiragana"] = None
    df = df[df["kanji"].isna() | df["kanji"].str.fullmatch(r"[一-龯]+", na=False)]

    return df[["sex", "kanji", "hiragana"]]


wiki["birth_year"] = pd.to_numeric(wiki["birth_year"], errors="coerce").astype("Int64")
facebook = preprocess_facebook(facebook)
gendec = preprocess_gendec(gendec)

wiki["dataset"] = "wiki"
facebook["dataset"] = "facebook"
gendec["dataset"] = "gendec"
enamdict["dataset"] = "enamdict"
name_origin["dataset"] = "name_origin"
dataset = pd.concat([wiki, facebook, gendec, enamdict, name_origin], ignore_index=True)
dataset = dataset[["dataset", "sex", "kanji", "hiragana", "birth_year"]]
dataset.to_csv("dataset.csv", index=False)
# %%
