import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT_DIR / "analytics" / "raw" / "youtube_video_stats.json"
REPORT_PATH = ROOT_DIR / "analytics" / "reports" / "youtube_report.md"

THEME_KEYWORDS = [
    "ダンゴムシ", "オトシブミ", "ハネアリ", "アリ", "ホタル", "カエル", "ガ", "チョウ",
    "バッタ", "カブトムシ", "クワガタ", "トンボ", "セミ", "テントウムシ", "ミツバチ",
    "シカ", "タヌキ", "キツネ", "リス", "ウサギ", "モグラ", "ハリネズミ",
    "キノコ", "コケ", "マツ", "ドングリ", "タンポポ", "スミレ",
    "タマゴ", "さなぎ", "幼虫", "成虫", "変態",
    "光", "色", "音", "においにおい", "ふしぎ",
]

NEXT_THEME_SUGGESTIONS = [
    "クモの巣はなんであんなに強いの？",
    "アリはなんであんなに力もちなの？",
    "チョウはなんで色がカラフルなの？",
    "セミはなんで土の中にいるの？",
    "カブトムシはなんで角があるの？",
    "キノコはなんで森にはえるの？",
    "ドングリはなんであんなにまるいの？",
    "タヌキはなんでしっぽがふさふさなの？",
    "カタツムリはなんで殻をしょってるの？",
    "ミミズはなんで土の中をほるの？",
]


def load_data():
    if not JSON_PATH.exists():
        raise FileNotFoundError(
            f"データファイルが見つかりません: {JSON_PATH}\n"
            "先に py scripts\\fetch_youtube_stats.py を実行してください。"
        )
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def like_rate(v):
    return v["like_count"] / v["view_count"] if v["view_count"] > 0 else 0.0


def comment_rate(v):
    return v["comment_count"] / v["view_count"] if v["view_count"] > 0 else 0.0


def detect_themes(videos):
    counter = Counter()
    for v in videos:
        text = v["title"] + " " + " ".join(v.get("tags") or [])
        for kw in THEME_KEYWORDS:
            if kw in text:
                counter[kw] += 1
    return counter.most_common(10)


def make_report(data):
    videos = data["videos"]
    fetched_at = data.get("fetched_at", "")
    channel_id = data.get("channel_id", "")

    total = len(videos)
    total_views = sum(v["view_count"] for v in videos)
    total_likes = sum(v["like_count"] for v in videos)
    total_comments = sum(v["comment_count"] for v in videos)
    avg_views = total_views / total if total > 0 else 0
    avg_like_rate = (
        sum(like_rate(v) for v in videos) / total if total > 0 else 0
    )
    avg_comment_rate = (
        sum(comment_rate(v) for v in videos) / total if total > 0 else 0
    )

    top_by_views = sorted(videos, key=lambda v: v["view_count"], reverse=True)[:10]
    top_by_likes = sorted(videos, key=like_rate, reverse=True)[:10]

    theme_counter = detect_themes(videos)

    lines = []
    lines.append(f"# YouTube分析レポート")
    lines.append(f"")
    lines.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    lines.append(f"データ取得日時: {fetched_at}  ")
    lines.append(f"channel_id: {channel_id}")
    lines.append(f"")

    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 1. 総動画数")
    lines.append(f"")
    lines.append(f"**{total} 本**")
    lines.append(f"")

    lines.append(f"## 2. 総再生数")
    lines.append(f"")
    lines.append(f"**{total_views:,} 回**")
    lines.append(f"")

    lines.append(f"## 3. 平均再生数")
    lines.append(f"")
    lines.append(f"**{avg_views:,.1f} 回 / 本**")
    lines.append(f"")

    lines.append(f"## 4. いいね率（平均）")
    lines.append(f"")
    lines.append(f"**{avg_like_rate * 100:.2f}%**")
    lines.append(f"（総いいね数: {total_likes:,}）")
    lines.append(f"")

    lines.append(f"## 5. コメント率（平均）")
    lines.append(f"")
    lines.append(f"**{avg_comment_rate * 100:.3f}%**")
    lines.append(f"（総コメント数: {total_comments:,}）")
    lines.append(f"")

    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 6. 再生数上位 10 本")
    lines.append(f"")
    lines.append(f"| # | タイトル | 再生数 | いいね | コメント | URL |")
    lines.append(f"|---|---------|--------|--------|----------|-----|")
    for i, v in enumerate(top_by_views, 1):
        lines.append(
            f"| {i} | {v['title']} "
            f"| {v['view_count']:,} "
            f"| {v['like_count']:,} "
            f"| {v['comment_count']:,} "
            f"| [リンク]({v['video_url']}) |"
        )
    lines.append(f"")

    lines.append(f"## 7. いいね率上位 10 本")
    lines.append(f"")
    lines.append(f"| # | タイトル | いいね率 | 再生数 | URL |")
    lines.append(f"|---|---------|---------|--------|-----|")
    for i, v in enumerate(top_by_likes, 1):
        rate = like_rate(v) * 100
        lines.append(
            f"| {i} | {v['title']} "
            f"| {rate:.2f}% "
            f"| {v['view_count']:,} "
            f"| [リンク]({v['video_url']}) |"
        )
    lines.append(f"")

    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 8. タイトルに含まれるテーマ傾向")
    lines.append(f"")
    if theme_counter:
        for kw, count in theme_counter:
            lines.append(f"- **{kw}**: {count} 本")
    else:
        lines.append(f"- データが少ないため傾向分析は次回以降")
    lines.append(f"")

    lines.append(f"## 9. 次に試すべきテーマ案")
    lines.append(f"")
    lines.append(f"以下は未制作テーマの候補です。")
    lines.append(f"上位の再生数・いいね率を参考に優先順位をつけてください。")
    lines.append(f"")

    existing_titles = " ".join(v["title"] for v in videos)
    suggested = []
    for theme in NEXT_THEME_SUGGESTIONS:
        kw = re.sub(r"[はなんでのあんがいるのするいつよどを？！]", "", theme)[:4]
        if kw not in existing_titles:
            suggested.append(theme)
        if len(suggested) >= 5:
            break

    for theme in suggested[:5]:
        lines.append(f"- {theme}")
    if not suggested:
        lines.append(f"- （候補リストをカスタマイズしてください）")
    lines.append(f"")

    lines.append(f"## 10. 制作改善メモ")
    lines.append(f"")

    if total == 0:
        lines.append(f"- まだ動画がありません。初回投稿後に分析できます。")
    else:
        best_view = top_by_views[0] if top_by_views else None
        best_like = top_by_likes[0] if top_by_likes else None

        if best_view:
            lines.append(f"- 再生数トップ: **「{best_view['title']}」** → このテーマの類似テーマを試す")
        if best_like and best_like.get("title") != (best_view or {}).get("title"):
            lines.append(f"- いいね率トップ: **「{best_like['title']}」** → 構成・解説の参考にする")

        if avg_like_rate < 0.01:
            lines.append(f"- いいね率が低め → サムネ文字・タイトルのキャッチコピーを見直す")
        if avg_comment_rate < 0.001:
            lines.append(f"- コメント率が低め → 締めセリフで「コメントしてね！」を入れてみる")
        if avg_views < 100:
            lines.append(f"- 再生数が少ない段階 → ハッシュタグと公開タイミングを最適化する")

        lines.append(f"- 夜の森テーマ（ホタル・ガ）と昼テーマの反応差を比較する")
        lines.append(f"- 虫テーマ・動物テーマ・植物テーマで反応に差があるか確認する")
        lines.append(f"- 1シーン目のびっくり表現がリテンションに影響するか検証する")

    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*このレポートは `py scripts\\make_youtube_report.py` で再生成できます。*")

    return "\n".join(lines)


def main():
    print(f"データ読み込み中: {JSON_PATH}")
    data = load_data()

    print("レポート生成中...")
    report = make_report(data)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(f"レポート保存: {REPORT_PATH}")
    print(f"動画数: {len(data['videos'])} 本")


if __name__ == "__main__":
    main()
