#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Iterable

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


# --- настройки повторов ---
MAX_PASSES = 4          # сколько раз в сумме пытаться (1-й прогон + 3 повтора)
RETRY_SLEEP = "1:5"     # yt-dlp: рандомная пауза между ретраями (сек)
FIRST_PASS_THREADS = "8"
RETRY_PASS_THREADS = "2"  # на повторах часто лучше меньше параллелизма


_YT_ID_RE = re.compile(r"(?<![A-Za-z0-9_-])([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])")


def extract_youtube_id(url: str) -> str | None:
    """
    Пытаемся достать 11-символьный video_id из типовых URL:
    - youtu.be/<id>
    - youtube.com/watch?v=<id>
    - youtube.com/shorts/<id>
    """
    # Быстрый путь: ищем 11-символьный токен (обычно ID) в URL.
    # Для наших ссылок этого хватает.
    m = _YT_ID_RE.search(url)
    return m.group(1) if m else None


def read_archive_ids(archive_path: Path) -> set[str]:
    """
    yt-dlp пишет archive строками вида:
      youtube <id>
      youtu.be <id>
      ... (или другие экстракторы)
    Берём последний токен в строке.
    """
    ids: set[str] = set()
    if not archive_path.exists():
        return ids

    for line in archive_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        ids.add(parts[-1])
    return ids


def find_missing_urls(urls: Iterable[str], archived_ids: set[str]) -> list[str]:
    missing: list[str] = []
    for u in urls:
        vid = extract_youtube_id(u)
        # если ID не смогли вытащить — считаем "под вопросом" и тоже перекачаем
        if vid is None or vid not in archived_ids:
            missing.append(u)
    return missing


def run_yt_dlp(urls: list[str], threads: str) -> int:
    if not urls:
        return 0

    LINKS_FILE.write_text("\n".join(urls) + "\n", encoding="utf-8")

    outtmpl = str(OUT_DIR / "%(uploader)s" / "%(title)s [%(id)s].%(ext)s")

    cmd = [
        "yt-dlp",
        "-a", str(LINKS_FILE),

        "-N", threads,
        "--lazy-playlist",
        "--download-archive", str(ARCHIVE),

        # лучшее возможное качество
        "-f", "bv*+ba/b",

        # чуть более «живучие» настройки сети
        "--retries", "20",
        "--fragment-retries", "20",
        "--retry-sleep", RETRY_SLEEP,
        "--socket-timeout", "30",

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


def main() -> int:
    if not URLS:
        print("URLS пустой — добавь ссылки в список URLS.")
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    urls_to_try = list(URLS)

    for pass_no in range(1, MAX_PASSES + 1):
        threads = FIRST_PASS_THREADS if pass_no == 1 else RETRY_PASS_THREADS

        print(f"\n=== ПРОХОД {pass_no}/{MAX_PASSES} (urls: {len(urls_to_try)}, threads: {threads}) ===")
        rc = run_yt_dlp(urls_to_try, threads=threads)

        archived_ids = read_archive_ids(ARCHIVE)
        missing = find_missing_urls(URLS, archived_ids)

        if not missing:
            print("\n✅ Всё скачано (все ID есть в архиве).")
            return 0

        # Остались “дыры” — следующий проход делаем только по ним
        print(f"\n⚠ Осталось недокачанных/неуспешных: {len(missing)}")
        for u in missing[:10]:
            print("  -", u)
        if len(missing) > 10:
            print(f"  ... и ещё {len(missing) - 10}")

        urls_to_try = missing

        # Если yt-dlp вернул не 0, не выходим сразу — у нас есть повторы.
        # На последнем проходе вернём код yt-dlp, чтобы было видно, что были ошибки.
        if pass_no == MAX_PASSES:
            print("\n❌ После всех повторов всё ещё остались недокачанные ссылки.")
            return rc if rc != 0 else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
