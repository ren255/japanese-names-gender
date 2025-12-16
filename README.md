# 日本人名前データ

4つのデータセットから作成されています。
420k件全てに性別データがあり、6割のデータは漢字とひらがな両方揃っています。

| dataset     | size | 男性割合 | ソース                                                                                                                  | repo                                                                                                       | note                         |
| ----------- | ---- | -------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------- |
| facebook    | 150k | 57.2%    | [facebook5.3億人漏洩データ](https://www.theguardian.com/technology/2021/apr/03/500-million-facebook-users-website-hackers) | **[philipperemy/name-dataset](https://github.com/philipperemy/name-dataset)**                           | 漢字orひらがな　どちらかのみ |
| enamdict    | 116k | 16.4%    | [ENAMDICT/JMnedict](https://www.edrdg.org/enamdict/enamdict_doc.html)                                                      | **[rgamici/japanese-names](https://github.com/rgamici/japanese-names)**                                 | 重複なし                     |
| name_origin | 90k  | 60.4%    | [名前由来](https://myoji-yurai.net/prefectureRanking.htm)                                                                  | [shuheilocale/japanese-personal-name-dataset](https://github.com/shuheilocale/japanese-personal-name-dataset) | 重複なし                     |
| gendec      | 64k  | 49.8%    | [shuheilocale/japanese-personal-name-dataset](https://github.com/shuheilocale/japanese-personal-name-dataset)              | [tarudesu/gendec-dataset](https://huggingface.co/datasets/tarudesu/gendec-dataset)                            | 研究目的のみ                 |
| wiki        | 39k  | 32.9%    | Wiki                                                                                                                    | [japanese-celeb-dataset](https://github.com/ren255/japanese-celeb-dataset)                                    | wikiからのスクレイピング     |

## 重複

gendecはname_originのうちの頻出データであるため使用はおすすめしないが何故か2.2kの非重複データ(kanji*hiragana)を持つ。

### 各データセット内のunique

![1765925965192](image/README/1765925965192.png)
![1765925975700](image/README/1765925975700.png)\

| dataset     | total_count | kanji_unique | hiragana_unique | both_unique |
| :---------- | ----------: | -----------: | --------------: | ----------: |
| all         |      457885 |       146568 |           30647 |      190714 |
| enamdict    |      116009 |        93176 |           15810 |      116009 |
| facebook    |      149566 |        11240 |           15024 |           0 |
| gendec      |       64139 |        35974 |             934 |       44429 |
| name_origin |       89635 |        69002 |            8759 |       89435 |
| wiki        |       38536 |        15120 |            5437 |       16718 |

### facebookを除く 漢字またひらがなが同一の重複

| dataset     | gendec_dup | enamdict_dup | name_origin_dup | total_dup |        non_dup |
| :---------- | ---------: | -----------: | --------------: | --------: | -------------: |
| gendec      |          0 |         8763 |           42091 |     42134 | **2295** |
| enamdict    |       8763 |            0 |           23428 |     23471 |          92538 |
| name_origin |      42091 |        23428 |               0 |     56799 |          32636 |

### 各datasetのみが所有するunique

![1765926791202](image/README/1765926791202.png)

|   | dataset     |  both | kanji | hiragana |
| -: | :---------- | ----: | ----: | -------: |
| 0 | wiki        |  6403 |  4646 |     1270 |
| 1 | facebook    |     0 |  3466 |     9744 |
| 2 | gendec      |  2282 |   208 |        5 |
| 3 | enamdict    | 90524 | 66870 |     8846 |
| 4 | name_origin | 31056 | 18801 |     2322 |

### 各datasetのみが所有するunique 割合

![1765927262718](image/README/1765927262718.png)
