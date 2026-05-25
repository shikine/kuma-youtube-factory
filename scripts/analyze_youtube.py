import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

steps = [
    ("YouTube統計取得", "fetch_youtube_stats.py"),
    ("分析レポート作成", "make_youtube_report.py"),
]

for label, script in steps:
    print(f"\n=== {label} 開始 ===")
    result = subprocess.run(
        ["py", str(ROOT_DIR / "scripts" / script)] + sys.argv[1:],
        check=True
    )
    print(f"=== {label} 完了 ===")

print("\n分析完了しました。")
print(f"レポート: {ROOT_DIR / 'analytics' / 'reports' / 'youtube_report.md'}")
