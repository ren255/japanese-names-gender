# %%
import pandas as pd
from namedivider import GBDTNameDivider
from tqdm import tqdm

pd.options.display.unicode.east_asian_width = True


splits = {
    "train": "gendec-train.csv",
    "validation": "gendec-dev.csv",
    "test": "gendec-test.csv",
}
df = pd.read_csv("hf://datasets/tarudesu/gendec-dataset/" + splits["train"])
divider = GBDTNameDivider()

# %%

# 漢字の重複を取得
print("漢字の重複を処理中...")
unique_kanji = df["Kanji"].unique()
kanji_dict = {}
for name in tqdm(unique_kanji, desc="漢字分割"):
    result = divider.divide_name(name).to_dict()
    kanji_dict[name] = (result["family"], result["given"])

# 漢字の結果をマッピング
df["Kanji_Family"] = df["Kanji"].map(lambda x: kanji_dict[x][0])
df["Kanji_Given"] = df["Kanji"].map(lambda x: kanji_dict[x][1])

# ひらがなの重複を取得
print("\nひらがなの重複を処理中...")
unique_hiragana = df["Higarana"].unique()
hiragana_dict = {}
for name in tqdm(unique_hiragana, desc="ひらがな分割"):
    result = divider.divide_name(name).to_dict()
    hiragana_dict[name] = (result["family"], result["given"])

# ひらがなの結果をマッピング
df["Hiragana_Family"] = df["Higarana"].map(lambda x: hiragana_dict[x][0])
df["Hiragana_Given"] = df["Higarana"].map(lambda x: hiragana_dict[x][1])

# 結果を表示
print(f"\n処理完了!")
print(
    f"総行数: {len(df)}, ユニーク漢字: {len(unique_kanji)}, ユニークひらがな: {len(unique_hiragana)}"
)
print("\n結果サンプル:")
print(
    df[
        [
            "Gender",
            "Kanji",
            "Kanji_Family",
            "Kanji_Given",
            "Higarana",
            "Hiragana_Family",
            "Hiragana_Given",
        ]
    ].head(10)
)

# CSVで保存する場合
# df.to_csv('divided_names.csv', index=False)

# %%
