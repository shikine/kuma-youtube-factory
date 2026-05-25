\# クマ博士YouTube工房



幼児向けYouTube Shorts「クマ博士の森のいきもの研究所」の自動生成パイプライン。



\## 基本フロー



1\. Claude Codeでepisode作成

2\. 画像を生成して `assets/images/inbox` に入れる

3\. `py scripts/run\_after\_images.py "XX\_テーマ名"` を実行

4\. final.mp4生成

5\. 必要に応じてYouTubeへアップロード



\## 動画生成



```powershell

py scripts/run\_after\_images.py "04\_ホタル"

