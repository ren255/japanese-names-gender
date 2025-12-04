# 日本人名前データ

4つのデータセットから作成されています。
420k件全てに性別データがあり、6割のデータは漢字とひらがな両方揃っています。

| dataset     | size | 割合 | 男性割合 | ソース                                                                                                                  | repo                                                                                                       | note                                 |
| ----------- | ---- | ---- | -------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| facebook    | 150k | 36%  | 57.2%    | [facebook5.3億人漏洩データ](https://www.theguardian.com/technology/2021/apr/03/500-million-facebook-users-website-hackers) | **[philipperemy/name-dataset](https://github.com/philipperemy/name-dataset)**                           | 漢字またはひらがなのどちらかのみ     |
| enamdict    | 116k | 28%  | 16.4%    | [ENAMDICT/JMnedict](https://www.edrdg.org/enamdict/enamdict_doc.html)                                                      | **[rgamici/japanese-names](https://github.com/rgamici/japanese-names)**                                 | 分布に大きな特徴あり                 |
| name_origin | 90k  | 21%  | 60.4%    | [名前由来](https://myoji-yurai.net/prefectureRanking.htm)                                                                  | [shuheilocale/japanese-personal-name-dataset](https://github.com/shuheilocale/japanese-personal-name-dataset) | 性別ごとの漢字とその読みデータの展開 |
| gendec      | 64k  | 15%  | 49.8%    | 一般的な名前データ                                                                                                      | [tarudesu/gendec-dataset](https://huggingface.co/datasets/tarudesu/gendec-dataset)                            | 研究目的のみ                         |
