#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
from pathlib import Path

# 1) ТУТ правишь ссылки
URLS = [
    "https://youtu.be/gY6TfBx_Itc",
    "https://youtu.be/YivjioY8b7M",
    "https://youtu.be/A1SI3dXeMCk",
    "https://www.youtube.com/shorts/aQqJcMEyYOE?feature=share",
    "https://youtu.be/blIaGmKXIz8",
    "https://www.youtube.com/shorts/HcG7M0Tk2b8",
    "https://www.youtube.com/shorts/ZWFUCjsSTPU",
    "https://youtu.be/79uIiW0qTWo",
    "https://youtu.be/r5YsdH3MyPw",
    "https://www.youtube.com/shorts/At98S0UvzW4",
    "https://www.youtube.com/shorts/JlR2dDzVGMY",
    "https://youtu.be/ob159ts1oQA",
    "https://youtu.be/vBIKaa6_rTA",
    "https://youtu.be/SZ2eL-JmmpE",
    "https://youtu.be/rKtOw4JazDw",
    "https://youtu.be/d8cVrwv8wf0",
    "https://youtu.be/PkcCcdaeEBY",
    "https://youtu.be/YUbqPUNBx0Q",
    "https://youtu.be/S6h9RyYgr2s",
    "https://youtu.be/wSUZoHjWFgo",
    "https://www.youtube.com/shorts/1cEcEQUnmgM",
    "https://youtu.be/TjDUqlBILy8",
    "https://youtu.be/XQPbs77mIgI",
    "https://youtu.be/nVk4neH9_3Q",
    "https://youtu.be/bFzP39j7QR0",
    "https://youtu.be/pa-7FLK4Npw",
    "https://youtu.be/ry5-UJw8Qn8",
    "https://youtu.be/gg-TRwWq0rs",
    "https://youtu.be/zj56m49REP0",
    "https://youtu.be/m0u8e14vIpU",
    "https://www.youtube.com/shorts/44sBAJD9xTE",
    "https://youtu.be/Wc2q6xF3JTg",
    "https://youtu.be/sH2DE7VdFlE",
    "https://youtu.be/KWvnNxw_alA",
    "https://youtu.be/WD6lroSm5To",
    "https://youtu.be/dsczgz61ib0",
    "https://youtu.be/H1ZkVG4Ocus",
    "https://youtu.be/9JkPxJnwpEw",
    "https://youtu.be/aWF7jq8wR2w",
    "https://youtu.be/c4IuahDiLTs",
    "https://youtu.be/DS-79TrNCoE",
    "https://youtu.be/Xaz8eCzqtIE"
]

# 2) ТУТ правишь папку, куда сохранять
OUT_DIR = Path(r"d:\youtube\СНИ\Kurzhaar_draghaar\materials") if os.name == "nt" else Path.home() / "yt_cuts"

# 3) (опционально) путь к cookies.txt
COOKIES = Path(r"d:\youtube\need things\cookies.txt")

# 4) файл-архив чтобы не перекачивать
ARCHIVE = OUT_DIR / "downloaded.txt"

# 5) временный файл со ссылками
LINKS_FILE = OUT_DIR / "links.txt"


def main() -> int:
    if not URLS:
        print("URLS пустой — добавь ссылки в список URLS.")
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # пишем links.txt
    LINKS_FILE.write_text("\n".join(URLS) + "\n", encoding="utf-8")

    # имя файла
    outtmpl = str(OUT_DIR / "%(uploader)s" / "%(title)s [%(id)s].%(ext)s")

    cmd = [
        "yt-dlp",
        "-a", str(LINKS_FILE),
        "-N", "8",
        "--lazy-playlist",
        "--download-archive", str(ARCHIVE),

        # ЛУЧШЕЕ ВОЗМОЖНОЕ КАЧЕСТВО
        "-f", "bv*+ba/b",

        "--no-warnings",
        "-o", outtmpl,
    ]

    if COOKIES.exists():
        cmd += ["--cookies", str(COOKIES)]
    else:
        print(f"⚠ cookies.txt не найден по пути: {COOKIES} — продолжаю без cookies.")

    print("Запуск:\n", " ".join(f'"{c}"' if " " in c else c for c in cmd))

    proc = subprocess.run(cmd, cwd=str(OUT_DIR))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
