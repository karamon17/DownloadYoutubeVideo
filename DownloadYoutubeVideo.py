#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

# 1) ТУТ правишь ссылки
URLS = [
    "https://youtu.be/gY6TfBx_Itc"
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
    (OUT_DIR / "tmp").mkdir(parents=True, exist_ok=True)

    # пишем links.txt
    LINKS_FILE.write_text("\n".join(URLS) + "\n", encoding="utf-8")

    # шаблон имени файла: по папкам автора, чтобы было удобно в Premiere
    outtmpl = str(OUT_DIR / "%(uploader)s" / "%(title)s [%(id)s].%(ext)s")

    cmd = [
        "yt-dlp",
        "-a", str(LINKS_FILE),
        "-N", "8",
        "--lazy-playlist",
        "--download-archive", str(ARCHIVE),
        "-f", "bv*[vcodec^=avc]+ba[acodec^=mp4a]/b[vcodec^=avc]",
        "--merge-output-format", "mp4",
        "--no-warnings",
        "-o", outtmpl,
    ]

    if COOKIES.exists():
        cmd += ["--cookies", str(COOKIES)]
    else:
        print(f"⚠ cookies.txt не найден по пути: {COOKIES} — продолжаю без cookies.")

    print("Запуск:\n", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    # запускаем из OUT_DIR, чтобы все служебные файлы лежали там
    proc = subprocess.run(cmd, cwd=str(OUT_DIR))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
