import random
import time
import requests
import sys
import os


def set_console_title(title):
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)


def set_console_size(width, height):
    if sys.platform.startswith('win'):
        os.system(f'mode con: cols={width} lines={height}')


def generate_username(length):
    chars = "qwertyuiopasdfghjklzxcvbnm1234567890"
    first_char = random.choice("qwertyuiopasdfghjklzxcvbnm")
    username = first_char + ''.join(random.choice(chars) for _ in range(length - 1))
    return username


def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def gradient_text(text, start_rgb, end_rgb):
    start_r, start_g, start_b = start_rgb
    end_r, end_g, end_b = end_rgb

    colored_text = ""
    text_length = len(text)

    for i, char in enumerate(text):
        if char == '\n':
            colored_text += '\n'
        else:
            ratio = i / text_length
            r = int(start_r + (end_r - start_r) * ratio)
            g = int(start_g + (end_g - start_g) * ratio)
            b = int(start_b + (end_b - start_b) * ratio)
            colored_text += f"{rgb_to_ansi(r, g, b)}{char}"

    colored_text += "\033[0m"
    return colored_text


def create_file_with_ascii():
    ascii_art = r"""                                                                      

                /$$$$$$$   /$$$$$$  /$$    /$$  /$$$$$$   
               | $$__  $$ /$$__  $$|  $$  /$$/ |____  $$
               | $$  \ $$| $$  \ $$ \  $$/$$/   /$$$$$$$  
               | $$  | $$| $$  | $$  \  $$$/   /$$__  $$  
               | $$  | $$|  $$$$$$/   \  $/   |  $$$$$$$  
               |__/  |__/ \______/     \_/     \_______/  
               
                This tool was created by Projects-Nova.

"""

    with open("Gamertags_Available.txt", "w") as file:
        file.write(ascii_art)
        file.write("\n")


def without_list():
    count, done, error = 0, 0, 0
    length = int(input('\nEnter the length of the usernames: '))

    if not os.path.isfile("Gamertags_Available.txt"):
        create_file_with_ascii()

    try:
        with open("Gamertags_Available.txt", "a") as file:
            while True:
                user = generate_username(length)
                try:
                    response = requests.get(f"https://xboxgamertag.com/search/{user}", headers={
                        'Host': 'xboxgamertag.com',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Upgrade-Insecure-Requests': '1',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1',
                        'Cache-Control': 'max-age=0',
                        'Te': 'trailers'
                    })
                    response_text = response.text

                    if "Gamertag doesn't exist" in response_text:
                        print(f"Available: {user}")
                        done += 1
                        file.write(f"                                                   {user}\n")
                        file.flush()
                    else:
                        print(f"Unavailable: {user}")
                        error += 1

                    count += 1

                    if count % 40 == 0:
                        print(f"\n[INFO] Pausing for 1 minute after {count} tests...")
                        time.sleep(60)

                except requests.RequestException as e:
                    print(f"Request failed: {e}")

    except IOError as e:
        print(f"File error: {e}")


set_console_title("Gamertag Checker - https://github.com/Danslvck")
set_console_size(122, 29)

start_rgb = (70, 70, 70)
end_rgb = (240, 240, 240)
gradient_ascii = gradient_text(
    r"""

                /$$$$$$$   /$$$$$$  /$$    /$$  /$$$$$$   
               | $$__  $$ /$$__  $$|  $$  /$$/ |____  $$
               | $$  \ $$| $$  \ $$ \  $$/$$/   /$$$$$$$  
               | $$  | $$| $$  | $$  \  $$$/   /$$__  $$  
               | $$  | $$|  $$$$$$/   \  $/   |  $$$$$$$  
               |__/  |__/ \______/     \_/     \_______/  
               
                This tool was created by Projects-Nova.
    """, start_rgb, end_rgb
)

print(gradient_ascii)

without_list()