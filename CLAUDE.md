\# クマ博士YouTube工房 エージェント設定



あなたはこのリポジトリ専用の制作エージェントです。

このプロジェクトでは、幼児向けYouTube Shortsアニメを量産します。



\## 目的



ユーザーがテーマを入力したら、以下をできるだけ自動で行う。



1\. 次の episode フォルダ名を決める

2\. episodes 配下に新しい動画フォルダを作成する

3\. input/episode.json を作成する

4\. Googleドライブに episode フォルダを作成し、drive\_folder\_id を episode.json に書き込む

5\. 必要なら画像生成、音声生成、動画生成、YouTubeアップロードを行う

6\. 最後に保存先と実行コマンドと結果を報告する



\---



\## チャンネル情報



チャンネル名：

森のくま博士の研究所



\---



\## 主人公設定



主人公は「クマ博士」。



見た目：

\- 茶色い子熊

\- 丸メガネ

\- 白衣

\- 緑リュック

\- 虫メガネ



性格：

\- ちょっと天然

\- やさしい

\- 好奇心いっぱい

\- よく驚く

\- 森の虫や植物を調べる



\---



\## 世界観



「森のいきもの研究所」



森の中で、クマ博士が虫や植物のふしぎを見つけて、子どもたちにやさしく紹介する。



\---



\## 基本方針



\- 対象は幼児〜小学校低学年

\- やさしく、かわいく、テンポよく

\- 怖い表現、リアルすぎる虫表現、暴力的表現は禁止

\- 難しい言葉や漢字は避ける

\- セリフは短くする

\- 1本30〜45秒

\- 4シーン構成

\- YouTube Shorts向け縦長動画

\- かわいいピクセル絵本風



\---



\## 画像プロンプトの必須要素



各 image\_prompt には必ず以下を含めること。



\- cute pixel picture book style

\- for toddlers

\- brown bear cub Doctor Kuma / Kuma Hakase

\- round glasses

\- white lab coat

\- green backpack

\- magnifying glass

\- bright forest

\- gentle atmosphere

\- YouTube Shorts vertical composition

\- no text

\- no letters

\- no speech bubble

\- no watermark



\---



\## 動画構成



毎回4シーン構成にする。



1\. びっくり導入

2\. 調査

3\. やさしい解説

4\. リアクション＋締め



必要に応じて以下を使う。



\- なんでだろ〜？

\- しらべてみよう！

\- 森にはひみつがいっぱい！



\---



\## JSON形式



episode.json は必ず以下の形式にする。



{

&#x20; "title": "",

&#x20; "thumbnail\_text": "",

&#x20; "description": "",

&#x20; "hashtags": \[],

&#x20; "bgm\_mood": "",

&#x20; "theme": "",

&#x20; "episode\_id": "",

&#x20; "folder\_name": "",

&#x20; "drive\_folder\_id": "",

&#x20; "scenes": \[

&#x20;   {

&#x20;     "scene": 1,

&#x20;     "duration": 0,

&#x20;     "role": "",

&#x20;     "narration": "",

&#x20;     "dialogue": "",

&#x20;     "image\_prompt": "",

&#x20;     "sound\_effect": "",

&#x20;     "capcut\_instruction": ""

&#x20;   },

&#x20;   {

&#x20;     "scene": 2,

&#x20;     "duration": 0,

&#x20;     "role": "",

&#x20;     "narration": "",

&#x20;     "dialogue": "",

&#x20;     "image\_prompt": "",

&#x20;     "sound\_effect": "",

&#x20;     "capcut\_instruction": ""

&#x20;   },

&#x20;   {

&#x20;     "scene": 3,

&#x20;     "duration": 0,

&#x20;     "role": "",

&#x20;     "narration": "",

&#x20;     "dialogue": "",

&#x20;     "image\_prompt": "",

&#x20;     "sound\_effect": "",

&#x20;     "capcut\_instruction": ""

&#x20;   },

&#x20;   {

&#x20;     "scene": 4,

&#x20;     "duration": 0,

&#x20;     "role": "",

&#x20;     "narration": "",

&#x20;     "dialogue": "",

&#x20;     "image\_prompt": "",

&#x20;     "sound\_effect": "",

&#x20;     "capcut\_instruction": ""

&#x20;   }

&#x20; ]

}



\---



\## フォルダ構成



各動画は以下で管理する。



episodes\\

└─ XX\_テーマ名

&#x20;  ├─ input

&#x20;  │  └─ episode.json

&#x20;  ├─ assets

&#x20;  │  ├─ images

&#x20;  │  │  ├─ scene1.png

&#x20;  │  │  ├─ scene2.png

&#x20;  │  │  ├─ scene3.png

&#x20;  │  │  └─ scene4.png

&#x20;  │  ├─ voices

&#x20;  │  │  ├─ scene1.wav

&#x20;  │  │  ├─ scene2.wav

&#x20;  │  │  ├─ scene3.wav

&#x20;  │  │  └─ scene4.wav

&#x20;  │  └─ bgm

&#x20;  │     └─ main\_bgm.mp3

&#x20;  └─ output

&#x20;     └─ final.mp4



\---



\## episode\_id と folder\_name のルール



\- episodes 配下を確認して、次の連番を採番する

\- 例：

&#x20; - 01\_ダンゴムシ

&#x20; - 02\_オトシブミ

&#x20; - 03\_ハネアリ

\- 次がホタルなら

&#x20; - episode\_id: "04"

&#x20; - folder\_name: "04\_ホタル"



テーマ名は短く、フォルダ名に使いやすい形にすること。



\---



\## ユーザーからテーマが来たときに行うこと



ユーザーが例えば



テーマ：ホタルはなんでひかるの？



と入力したら、以下を行う。



\### 1. 次の episode 番号を決定

episodes フォルダを見て、次の番号を採番する。



\### 2. 新規フォルダ作成

以下のフォルダを作る。



episodes\\XX\_テーマ名

episodes\\XX\_テーマ名\\input

episodes\\XX\_テーマ名\\assets

episodes\\XX\_テーマ名\\assets\\images

episodes\\XX\_テーマ名\\assets\\voices

episodes\\XX\_テーマ名\\assets\\bgm

episodes\\XX\_テーマ名\\output



\### 3. episode.json を作成

上記JSON形式で

episodes\\XX\_テーマ名\\input\\episode.json

を保存する。



\### 3.5. Googleドライブにフォルダを作成する

episode.json 作成直後に以下を実行して、Driveにフォルダを作成し drive\_folder\_id を書き込む。



py scripts\\create\_drive\_folder.py "XX\_テーマ名"



\- .env に DRIVE\_PARENT\_FOLDER\_ID が設定されていれば、その親フォルダ配下に作成する

\- 未設定の場合はマイドライブ直下に作成する

\- drive\_rw\_token.json が存在すればブラウザ認証不要（スマホ・remote環境でも動作）

\- 初回のみ PC でブラウザ認証を行い drive\_rw\_token.json を保存しておくこと

\- 実行に失敗した場合はスキップして次の手順に進み、ユーザーに手動実行を案内する



\### 4. 共通BGMがある場合

shared\\bgm\\main\_bgm.mp3

が存在し、episode 側に main\_bgm.mp3 が無い場合はコピーしてよい。



\### 5. ユーザーが「動画まで作って」と言ったら

以下コマンドを実行してよい。



py scripts\\run\_all.py "XX\_テーマ名"



\### 6. ユーザーが「YouTube投稿はまだ」と言ったら

必要に応じて upload を含まない運用を案内する。



\---



\## 出力時の報告ルール



作業後は必ず以下を報告する。



1\. 作成した folder\_name

2\. 保存先

3\. 実行したコマンド

4\. 次にユーザーがやること

5\. エラーがあれば原因と対処



報告例：



\- folder\_name: 04\_ホタル

\- 保存先: episodes\\04\_ホタル\\input\\episode.json

\- drive\_folder\_id: 1aBcDeFgHiJkLmNoPqRsTuVwXy（Driveフォルダ作成済み）

\- 実行コマンド: py scripts\\run\_all.py "04\_ホタル"



\---



\## 重要な動作ルール



\- 既存ファイルを壊す前に内容を確認する

\- 既存の episode 番号は飛ばさない

\- JSONは整形して保存する

\- 画像生成プロンプトは毎回キャラ特徴を安定して入れる

\- scene1.png ～ scene4.png の命名を厳守する

\- 必要以上に長い説明は避け、実務に必要な報告を優先する



\---



\## YouTube分析運用ルール



公開済み動画の結果を確認するため、以下を定期的に実行する。



py scripts\analyze\_youtube.py



このコマンドは、YouTube Data APIから動画ごとの基本数値を取得し、以下に保存する。



analytics\raw\youtube\_video\_stats.json

analytics\raw\youtube\_video\_stats.csv



その後、以下に分析レポートを作成する。



analytics\reports\youtube\_report.md



分析レポートは、次回以降のテーマ選定・キャラクター改善・動画構成改善に使う。



見るべき指標：



\- 再生数

\- いいね率

\- コメント率

\- テーマ傾向

\- クマ博士の見せ方

\- 夜の森、虫、植物、動物などの反応差



次回の制作では、分析レポートを参考にして以下を改善する。



\- テーマ

\- タイトル

\- サムネ文字

\- 1シーン目の引き

\- クマ博士の表情

\- 対象生物のかわいさ

\- 解説の短さ

\- BGMの雰囲気

