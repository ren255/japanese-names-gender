# %%
import pandas as pd
import matplotlib.pyplot as plt
import pyperclip as clip

dataset = pd.read_csv("dataset.csv")
dataset.columns = ["dataset", "sex", "kanji", "hiragana", "birth_year"]


# %%


def count_unique(df):

    df2 = df.copy()
    df2_with_all = pd.concat(
        [df2, df2.assign(dataset="all")], ignore_index=True  # dataset="all" を追加
    )

    rows = []
    for ds, sub in df2_with_all.groupby("dataset"):
        both = sub[sub["kanji"].notna() & sub["hiragana"].notna()]

        rows.append(
            {
                "dataset": ds,
                "total_count": len(sub),
                "kanji_unique": sub["kanji"].dropna().nunique(),
                "hiragana_unique": sub["hiragana"].dropna().nunique(),
                "both_unique": both.drop_duplicates(["kanji", "hiragana"]).shape[0],
            }
        )

    # index=dataset にして返す
    return pd.DataFrame(rows).set_index("dataset").sort_index()


from matplotlib.ticker import FuncFormatter


# --- 自動単位フォーマッタ（1,234 → 1.23k など） ---
def human_format(x, pos):
    if x >= 1_000_000_000:
        return f"{x/1_000_000_000:.2f}B"
    elif x >= 1_000_000:
        return f"{x/1_000_000:.2f}M"
    elif x >= 1_000:
        return f"{x/1_000:.2f}k"
    else:
        return f"{int(x)}"


def plot_unique_with_totals(result: pd.DataFrame):
    result = result.sort_values("total_count", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))

    # unique 棒グラフ
    result.drop(axis=1, columns=["total_count"]).plot(
        kind="bar", ax=ax, rot=0, width=0.7
    )

    x = range(len(result))

    # total_count の水平線
    for i, (ds, row) in enumerate(result.iterrows()):
        total = row["total_count"]

        ax.hlines(
            y=total,
            xmin=i - 0.35,
            xmax=i + 0.35,
            colors="black",
            linestyles="dashed",
            linewidth=1.6,
            label="total_count" if i == 0 else None,
        )

        ax.text(
            i,
            total,
            human_format(total, None),  # "12.3k" のような表記
            ha="center",
            va="bottom",
            fontsize=9,
        )

    # --- Y軸を自動で k/M/B にする ---
    ax.yaxis.set_major_formatter(FuncFormatter(human_format))

    ax.set_title("Unique Counts + Total Size", fontsize=15)
    ax.set_ylabel("Count")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend()

    plt.tight_layout()
    plt.show()


# %%
result = count_unique(dataset)
result_dataset = result[result.index != "all"]
plot_unique_with_totals(result_dataset)

type_result = result.T
type_result = type_result.rename(columns={"all": "total_count"})
type_result = type_result[type_result.index != "total_count"]
plot_unique_with_totals(type_result)
print(result)

# %%

import pandas as pd


def kanji_sex_count(df: pd.DataFrame, kanji_col="kanji", sex_col="sex") -> pd.DataFrame:

    # 漢字を1文字ずつ分解
    kanji_sex_df = (
        df[[kanji_col, sex_col]]
        .dropna(subset=[kanji_col])
        .astype({kanji_col: str})
        .assign(kanji_char=lambda x: x[kanji_col].apply(list))
        .explode("kanji_char")
    )

    # 漢字 × sex で集計
    kanji_sex_counts = (
        kanji_sex_df.groupby(["kanji_char", sex_col])
        .size()
        .reset_index(name="count")
        .rename(columns={"kanji_char": "kanji"})
    )

    # ratio 列を追加（全体のデータ数に対する比率）
    kanji_sex_counts["ratio"] = kanji_sex_counts["count"] / len(df)

    return kanji_sex_counts


import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def plt_word_cloud(sex_counts: pd.DataFrame):
    """
    男性・女性の漢字ワードクラウドを左右並べて表示（正方形・空白少なめ）
    """
    wc_params = {
        "font_path": "/home/ren255/Downloads/fornt/static/NotoSansJP-Regular.ttf",
        "width": 800,
        "height": 600,
        "background_color": "white",
        "prefer_horizontal": 1.0,
    }
    # male / female 分割
    male_df = sex_counts[sex_counts["sex"] == "male"]
    female_df = sex_counts[sex_counts["sex"] == "female"]

    # WordCloud用辞書化
    male_dict = dict(zip(male_df["kanji"], male_df["ratio"]))
    female_dict = dict(zip(female_df["kanji"], female_df["ratio"]))

    # 正方形のWordCloud設定
    wc_params = {
        "font_path": "/home/ren255/Downloads/fornt/static/NotoSansJP-Regular.ttf",
        "width": 600,
        "height": 600,
        "background_color": "white",
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 幅は短めに調整

    # 男性ワードクラウド
    wc_male = WordCloud(**wc_params).generate_from_frequencies(male_dict)
    axes[0].imshow(wc_male, interpolation="bilinear")
    axes[0].axis("off")
    axes[0].set_title("Male Kanji WordCloud", fontsize=16)

    # 女性ワードクラウド
    wc_female = WordCloud(**wc_params).generate_from_frequencies(female_dict)
    axes[1].imshow(wc_female, interpolation="bilinear")
    axes[1].axis("off")
    axes[1].set_title("Female Kanji WordCloud", fontsize=16)

    plt.subplots_adjust(wspace=0.05)  # 空白を極力狭く
    plt.show()


# %%
sex_kanji_ctn = kanji_sex_count(
    dataset,
    kanji_col="kanji",
    sex_col="sex",
)
plt_word_cloud(sex_kanji_ctn)


# %%
def word_cloud(dataset, name):
    print(name)
    sex_kanji_ctn = kanji_sex_count(
        dataset,
        kanji_col="kanji",
        sex_col="sex",
    )
    plt_word_cloud(sex_kanji_ctn)


word_cloud(dataset[dataset["dataset"] == "facebook"], "facebook")
word_cloud(dataset[dataset["dataset"] == "wiki"], "wiki")
word_cloud(dataset, "all")
# %%
word_cloud(dataset[dataset["birth_year"] < 1950], "~1950")
word_cloud(dataset[dataset["birth_year"] > 1950], "1950~")
word_cloud(dataset[dataset["birth_year"] > 2000], "2000~")


# %%
# %%
def count_dataset_exclusive(df):
    """各データセットにしか含まれない名前をカウント"""
    rows = []
    datasets = df["dataset"].unique()

    for ds in datasets:
        ds_data = df[df["dataset"] == ds]
        other_data = df[df["dataset"] != ds]

        # kanji only exclusive
        ds_kanji = set(ds_data["kanji"].dropna())
        other_kanji = set(other_data["kanji"].dropna())
        kanji_exclusive = len(ds_kanji - other_kanji)

        # hiragana only exclusive
        ds_hiragana = set(ds_data["hiragana"].dropna())
        other_hiragana = set(other_data["hiragana"].dropna())
        hiragana_exclusive = len(ds_hiragana - other_hiragana)

        # both exclusive
        ds_both = set(zip(ds_data["kanji"].fillna(""), ds_data["hiragana"].fillna("")))
        ds_both = {pair for pair in ds_both if pair[0] and pair[1]}
        other_both = set(
            zip(other_data["kanji"].fillna(""), other_data["hiragana"].fillna(""))
        )
        other_both = {pair for pair in other_both if pair[0] and pair[1]}
        both_exclusive = len(ds_both - other_both)

        rows.append(
            {
                "dataset": ds,
                "both": both_exclusive,
                "kanji": kanji_exclusive,
                "hiragana": hiragana_exclusive,
            }
        )

    return pd.DataFrame(rows)


def plt_exclusive_counts(dataset, exclusive=False):
    if not exclusive:
        exclusive_counts = count_dataset_exclusive(dataset)
    else:
        exclusive_counts = dataset

    # 総合カウント
    total_counts = result_dataset[
        ["both_unique", "kanji_unique", "hiragana_unique"]
    ].reset_index()
    total_counts.columns = ["dataset", "both", "kanji", "hiragana"]

    # プロット
    fig, ax = plt.subplots(figsize=(10, 6))

    x_labels = ["both", "kanji", "hiragana"]
    x_pos = range(len(x_labels))
    width = 0.6

    # 各データセットごとにスタック
    bottom = [0, 0, 0]
    for _, row in exclusive_counts.iterrows():
        values = [row["both"], row["kanji"], row["hiragana"]]
        ax.bar(x_pos, values, width, bottom=bottom, label=row["dataset"])
        bottom = [b + v for b, v in zip(bottom, values)]

    # exclusive合計のテキスト表示
    for i in x_pos:
        ax.text(
            i,
            bottom[i],
            human_format(bottom[i], None),
            ha="center",
            va="bottom",
            fontsize=9,
        )

    if not exclusive:
        # 総合カウントの破線
        for i, col in enumerate(x_labels):
            total = total_counts[col].sum()
            ax.hlines(
                y=total,
                xmin=i - 0.35,
                xmax=i + 0.35,
                colors="black",
                linestyles="dashed",
                linewidth=1.6,
            )
            ax.text(
                i,
                total,
                human_format(total, None),
                ha="center",
                va="bottom",
                fontsize=9,
            )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels)
    ax.set_ylabel("Count")
    ax.set_title("Dataset-Exclusive Counts (Stacked)")
    ax.yaxis.set_major_formatter(FuncFormatter(human_format))
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()
    return exclusive_counts


# %%
exclusive = plt_exclusive_counts(dataset)

# %%
