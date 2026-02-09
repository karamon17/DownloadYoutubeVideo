import yt_dlp
from contextlib import redirect_stdout, redirect_stderr
import io

# Список ссылок на видео
video_urls = [
        "https://youtu.be/gY6TfBx_Itc", "https://youtu.be/YivjioY8b7M", "https://youtu.be/A1SI3dXeMCk", "https://www.youtube.com/shorts/aQqJcMEyYOE", "https://youtu.be/blIaGmKXIz8", "https://www.youtube.com/shorts/HcG7M0Tk2b8", "https://www.youtube.com/shorts/ZWFUCjsSTPU", "https://youtu.be/79uIiW0qTWo", "https://youtu.be/r5YsdH3MyPw", "https://www.youtube.com/shorts/At98S0UvzW4", "https://www.youtube.com/shorts/JlR2dDzVGMY", "https://youtu.be/ob159ts1oQA", "https://youtu.be/vBIKaa6_rTA", "https://youtu.be/SZ2eL-JmmpE", "https://youtu.be/rKtOw4JazDw", "https://youtu.be/d8cVrwv8wf0", "https://youtu.be/PkcCcdaeEBY", "https://youtu.be/YUbqPUNBx0Q", "https://youtu.be/S6h9RyYgr2s", "https://youtu.be/wSUZoHjWFgo", "https://www.youtube.com/shorts/1cEcEQUnmgM", "https://youtu.be/TjDUqlBILy8", "https://youtu.be/XQPbs77mIgI", "https://youtu.be/nVk4neH9_3Q", "https://youtu.be/bFzP39j7QR0", "https://youtu.be/pa-7FLK4Npw", "https://youtu.be/ry5-UJw8Qn8", "https://youtu.be/gg-TRwWq0rs", "https://youtu.be/zj56m49REP0", "https://youtu.be/m0u8e14vIpU", "https://www.youtube.com/shorts/44sBAJD9xTE", "https://youtu.be/Wc2q6xF3JTg", "https://youtu.be/sH2DE7VdFlE", "https://youtu.be/KWvnNxw_alA", "https://youtu.be/WD6lroSm5To", "https://youtu.be/dsczgz61ib0", "https://youtu.be/H1ZkVG4Ocus", "https://youtu.be/9JkPxJnwpEw", "https://youtu.be/aWF7jq8wR2w", "https://youtu.be/c4IuahDiLTs", "https://youtu.be/DS-79TrNCoE", "https://youtu.be/Xaz8eCzqtIE"

]

class SilentLogger:
    def debug(self, msg):   pass   # убрать шум от debug
    def info(self, msg):    pass   # убрать обычные сообщения
    def warning(self, msg): pass   # убрать WARNING
    def error(self, msg):   pass   # если хочешь видеть ошибки, закомментируй pass и сделай print(msg)

# Функция для получения канала с использованием yt_dlp
def get_channel_name(url):
    ydl_opts = {
        'cookiefile': r'd:\youtube\need things\cookies.txt',  # путь к твоему файлу cookies
        'quiet': True,  # Отключение вывода предупреждений
        'force_generic_extractor': True,
        'no_warnings': True,
        'logger': SilentLogger()
    }
    # Дополнительно глушим неожиданный вывод в stdout/stderr из внутренних вызовов
    f_out, f_err = io.StringIO(), io.StringIO()
    with redirect_stdout(f_out), redirect_stderr(f_err):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    return info.get('uploader', 'Не удалось получить канал')

# Проходим по всем ссылкам
for url in video_urls:
    try:
        channel_name = get_channel_name(url)
        print(f'{url} {channel_name}')
    except Exception as e:
        print(f'Ошибка при обработке {url}: {e}')


