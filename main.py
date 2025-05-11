import requests
import time
import os
import psutil
import mss
import webbrowser
import socket
import platform
from datetime import timedelta, datetime

TOKEN = ''  # Bot Token'ınızı buraya yazın
CHAT_ID = ''  # Sadece sizin chat ID'niz olmalı

URL = f"https://api.telegram.org/bot{TOKEN}/"
print("Bot başlatıldı...")
def clear_old_updates():
    """Eski mesajları temizler ve en son update_id'yi döner."""
    updates = get_updates()
    if 'result' in updates and len(updates['result']) > 0:
        last_update_id = updates['result'][-1]['update_id']
        return last_update_id + 1  # Sonraki mesajlar için offset
    return None


def get_updates(offset=None):
    url = URL + 'getUpdates'
    if offset:
        url += f'?offset={offset}'
    r = requests.get(url)
    return r.json()

def send_message(chat_id, text):
    url = URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

def send_photo(chat_id, photo_path):
    url = URL + 'sendPhoto'
    try:
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id}
            requests.post(url, files=files, data=data)
    except Exception as e:
        print(f"⚠️ Fotoğraf gönderilemedi: {str(e)}")
    finally:
        if os.path.exists(photo_path):
            os.remove(photo_path)  # Fotoğraf gönderildikten sonra dosyayı sil

def take_screenshot():
    with mss.mss() as sct:
        screenshot = sct.shot(output="screenshot.png")
    return screenshot

def get_status():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    mem_percent = memory.percent
    return f"💻 CPU Kullanımı: {cpu}%\n🧠 RAM Kullanımı: {mem_percent}%"

def get_disk_usage():
    usage = psutil.disk_usage('/')
    total = usage.total // (1024 ** 3)
    used = usage.used // (1024 ** 3)
    free = usage.free // (1024 ** 3)
    return f"💾 Disk Kullanımı:\nToplam: {total} GB\nKullanılan: {used} GB\nBoş: {free} GB"

def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    return f"⏱️ Çalışma Süresi: {str(timedelta(seconds=uptime.total_seconds()))}"

def create_file(filename):
    try:
        with open(filename, 'w') as f:
            f.write("Bu dosya bot tarafından oluşturulmuştur.")
        return f"✅ Dosya oluşturuldu: {filename}"
    except Exception as e:
        return f"⚠️ Dosya oluşturulamadı: {str(e)}"

def delete_file(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
            return f"✅ Dosya silindi: {filename}"
        else:
            return f"⚠️ Dosya bulunamadı: {filename}"
    except Exception as e:
        return f"⚠️ Dosya silinemedi: {str(e)}"

def lock_computer():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "🔒 Bilgisayar kilitlendi."

def hibernate_computer():
    os.system("shutdown /h")
    return "💤 Bilgisayar uyku moduna alındı."

def logoff_user():
    os.system("shutdown /l")
    return "🚪 Kullanıcı oturumu kapatıldı."

def list_processes():
    processes = [proc.info for proc in psutil.process_iter(['pid', 'name'])]
    process_list = "\n".join([f"{p['pid']} - {p['name']}" for p in processes])
    return f"🖥️ Çalışan İşlemler:\n{process_list}"

def kill_process(process_name):
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                proc.kill()
                return f"✅ İşlem sonlandırıldı: {process_name}"
        return f"⚠️ İşlem bulunamadı: {process_name}"
    except Exception as e:
        return f"⚠️ İşlem sonlandırılamadı: {str(e)}"

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"🌐 IP Adresi: {ip_address}"
    except Exception as e:
        return f"⚠️ IP adresi alınamadı: {str(e)}"
def get_help():
    return """🤖 *Komut Listesi*:

/status - Sistem durumu hakkında genel bilgi verir.
/screenshot - Ekran görüntüsü alır ve gönderir.
/diskusage - Disk kullanım bilgilerini gösterir.
/uptime - Bilgisayarın açık kalma süresini gösterir.
/lock - Bilgisayarı kilitler.
/logoff - Kullanıcı oturumunu kapatır.
/listprocesses - Çalışan işlemleri listeler.
/killprocess [işlem_adı] - Belirtilen işlemi sonlandırır. Örnek: /killprocess notepad.exe
/getip - Yerel IP adresini gösterir.
/publicip - Genel (public) IP adresini gösterir.
/batteryinfo - Pil durumu hakkında bilgi verir.
/osinfo - İşletim sistemi bilgilerini gösterir.
/systeminfo - Sistem bilgilerini detaylı şekilde gösterir.
/cleartemp - Geçici dosyaları temizler.
/whoami - Oturum açan kullanıcıyı gösterir.
/activewindow - Aktif pencere başlığını gösterir.
/traceroute [host] - Belirtilen host’a traceroute komutu çalıştırır. Örnek: /traceroute google.com
/restart - Bilgisayarı yeniden başlatır.
/shutdown - Bilgisayarı kapatır.
/openurl [url] - Belirtilen URL'yi açar. Örnek: /openurl https://google.com
/openprogram [program_yolu] - Belirtilen programı açar. Örnek: /openprogram C:\\Windows\\notepad.exe
/help - Bu komutları listeler.
"""

def restart_computer():
    os.system("shutdown /r /t 0")
    return "🔄 Bilgisayar yeniden başlatılıyor..."

def shutdown_computer():
    os.system("shutdown /s /t 0")
    return "🛑 Bilgisayar kapatılıyor..."

def open_url(url):
    try:
        webbrowser.open(url)
        return f"🌐 URL açıldı: {url}"
    except Exception as e:
        return f"⚠️ URL açılamadı: {str(e)}"

def open_program(program_path):
    try:
        os.startfile(program_path)
        return f"🚀 Program açıldı: {program_path}"
    except Exception as e:
        return f"⚠️ Program açılamadı: {str(e)}"

def get_cpu_info():
    return f"💻 CPU Çekirdek Sayısı: {psutil.cpu_count(logical=True)}\n💻 CPU Frekansı: {psutil.cpu_freq().current} MHz"

def get_ram_info():
    memory = psutil.virtual_memory()
    total = memory.total // (1024 ** 3)
    available = memory.available // (1024 ** 3)
    return f"🧠 RAM Bilgisi:\nToplam: {total} GB\nKullanılabilir: {available} GB"

def get_disk_info():
    usage = psutil.disk_usage('/')
    total = usage.total // (1024 ** 3)
    used = usage.used // (1024 ** 3)
    free = usage.free // (1024 ** 3)
    return f"💾 Disk Bilgisi:\nToplam: {total} GB\nKullanılan: {used} GB\nBoş: {free} GB"

def ping_host(host):
    try:
        response = os.system(f"ping -n 1 {host}")
        if response == 0:
            return f"✅ {host} erişilebilir."
        else:
            return f"⚠️ {host} erişilemez."
    except Exception as e:
        return f"⚠️ Ping işlemi başarısız: {str(e)}"

def get_network_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"🌐 Ağ Bilgisi:\nHostname: {hostname}\nIP Adresi: {ip_address}"
    except Exception as e:
        return f"⚠️ Ağ bilgisi alınamadı: {str(e)}"

def suspend_computer():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "💤 Bilgisayar askıya alındı."

def reboot_computer():
    os.system("shutdown /r /t 0")
    return "🔄 Bilgisayar yeniden başlatılıyor..."

def get_current_user():
    return f"👤 Şu anki kullanıcı: {os.getlogin()}"

def list_users():
    try:
        users = os.popen("net user").read()
        return f"👥 Kullanıcılar:\n{users}"
    except Exception as e:
        return f"⚠️ Kullanıcılar listelenemedi: {str(e)}"

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            secs_left = battery.secsleft
            plugged = battery.power_plugged
            time_left = str(timedelta(seconds=secs_left)) if secs_left != psutil.POWER_TIME_UNLIMITED else "Sınırsız"
            status = "🔌 Prize takılı" if plugged else "🔋 Batarya kullanılıyor"
            return f"🔋 Pil Bilgisi:\nYüzde: {percent}%\nKalan Süre: {time_left}\nDurum: {status}"
        else:
            return "⚠️ Pil bilgisi alınamıyor (cihazınızda pil yok olabilir)."
    except Exception as e:
        return f"⚠️ Pil bilgisi alınamadı: {str(e)}"

def get_os_info():
    try:
        os_info = platform.uname()
        return f"🖥️ İşletim Sistemi Bilgisi:\nSistem: {os_info.system}\nSürüm: {os_info.release}\nMakine: {os_info.machine}"
    except Exception as e:
        return f"⚠️ İşletim sistemi bilgisi alınamadı: {str(e)}"

def delete_folder(folder_path):
    try:
        import shutil
        shutil.rmtree(folder_path)
        return f"✅ Klasör silindi: {folder_path}"
    except Exception as e:
        return f"⚠️ Klasör silinemedi: {str(e)}"

def list_files(directory):
    try:
        files = os.listdir(directory)
        return f"📂 {directory} içindeki dosyalar:\n" + "\n".join(files)
    except Exception as e:
        return f"⚠️ Dosyalar listelenemedi: {str(e)}"

def get_public_ip():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        return f"🌐 Genel IP Adresi: {ip}"
    except requests.RequestException as e:
        return f"⚠️ Genel IP adresi alınamadı: {str(e)}"

def traceroute(host):
    try:
        response = os.popen(f"tracert {host}").read()
        return f"🌐 Traceroute Sonucu:\n{response}"
    except Exception as e:
        return f"⚠️ Traceroute işlemi başarısız: {str(e)}"

def clear_temp_files():
    try:
        temp_dir = os.getenv('TEMP')
        import shutil
        shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        return "✅ Geçici dosyalar temizlendi."
    except Exception as e:
        return f"⚠️ Geçici dosyalar temizlenemedi: {str(e)}"

def get_system_info():
    try:
        info = os.popen("systeminfo").read()
        return f"🖥️ Sistem Bilgisi:\n{info}"
    except Exception as e:
        return f"⚠️ Sistem bilgisi alınamadı: {str(e)}"

def who_am_i():
    try:
        username = os.getlogin()
        return f"👤 Şu anki kullanıcı: {username}"
    except Exception as e:
        return f"⚠️ Kullanıcı bilgisi alınamadı: {str(e)}"

def get_active_window():
    try:
        import win32gui
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return f"🪟 Aktif Pencere: {window}"
    except ImportError:
        return "⚠️ Aktif pencere bilgisi alınamadı: 'win32gui' modülü eksik."
    except Exception as e:
        return f"⚠️ Aktif pencere bilgisi alınamadı: {str(e)}"

def handle_command(command, chat_id):
    try:
        # Komutları olduğu gibi işliyoruz, küçük harfe çevirme ve boşluk temizleme kaldırıldı
        if command == '/status':
            return get_status()
        elif command == '/screenshot':
            screenshot_path = take_screenshot()
            send_photo(chat_id, screenshot_path)
            return "📸 Ekran görüntüsü alındı ve gönderildi."
        elif command == '/diskusage':
            return get_disk_usage()
        elif command == '/uptime':
            return get_uptime()
        elif command == '/lock':
            return lock_computer()
        elif command == '/logoff':
            return logoff_user()
        elif command == '/listprocesses':
            return list_processes()
        elif command.startswith('/killprocess'):
            try:
                process_name = command.split(' ', 1)[1]
                return kill_process(process_name)
            except IndexError:
                return "⚠️ Lütfen işlem adını belirtin. Örnek: /killprocess notepad.exe"
        elif command == '/getip':
            return get_ip_address()
        elif command == '/batteryinfo':
            return get_battery_info()
        elif command == '/osinfo':
            return get_os_info()
        elif command == '/publicip':
            return get_public_ip()
        elif command.startswith('/traceroute'):
            try:
                host = command.split(' ', 1)[1]
                return traceroute(host)
            except IndexError:
                return "⚠️ Lütfen bir host belirtin. Örnek: /traceroute google.com"
        elif command == '/cleartemp':
            return clear_temp_files()
        elif command == '/systeminfo':
            return get_system_info()
        elif command == '/whoami':
            return who_am_i()
        elif command == '/activewindow':
            return get_active_window()
        elif command.startswith('/openurl'):
            try:
                url = command.split(' ', 1)[1]
                return open_url(url)
            except IndexError:
                return "⚠️ Lütfen bir URL belirtin. Örnek: /openurl https://google.com"
        elif command.startswith('/openprogram'):
            try:
                program_path = command.split(' ', 1)[1]
                return open_program(program_path)
            except IndexError:
                return "⚠️ Lütfen bir program yolu belirtin. Örnek: /openprogram C:\\Windows\\notepad.exe"
        elif command == '/help':
            return get_help()
        elif command == '/restart':
            return restart_computer()
        elif command == '/shutdown':
            return shutdown_computer()
        else:
            return "❓ Bilinmeyen komut. Lütfen /help komutunu kullanarak geçerli komutları görün."
    except Exception as e:
        return f"⚠️ Hata oluştu: {str(e)}"

def main():
    last_update_id = None
 # Eski mesajları temizle
    last_update_id = clear_old_updates()

    while True:
        try:
            updates = get_updates(last_update_id)

            if 'result' in updates and len(updates['result']) > 0:
                for update in updates['result']:
                    # Güncellenen last_update_id
                    last_update_id = update['update_id'] + 1
                    message = update.get('message', {})
                    from_id = message.get('from', {}).get('id')
                    text = message.get('text', '')

                    # Gelen mesajı terminale yazdır
                    print(f"Gelen mesaj: {text}")

                    if from_id != int(CHAT_ID):
                        send_message(from_id, "⛔ Bu botu kullanmaya yetkin yok!")
                        continue

                    response = handle_command(text, from_id)
                    if response:
                        send_message(from_id, response)

            time.sleep(2)  # 2 saniyede bir yeni mesaj kontrol et
        except KeyboardInterrupt:
            print("Bot durduruldu.")
            break  # Kullanıcı tarafından durdurulduğunda döngüyü kır
        except Exception as e:
            print(f"⚠️ Hata: {str(e)}")

if __name__ == '__main__':
    main()
