import requests
import time
import os
import psutil
import mss
import webbrowser
import socket
from datetime import timedelta, datetime

TOKEN = '5047752978:AAFDWwYd9MkzEP10dPIVW5pKs8DhWya0Vx0'  # Bot Token'ınızı buraya yazın
CHAT_ID = '1269991242'  # Sadece sizin chat ID'niz olmalı

URL = f"https://api.telegram.org/bot{TOKEN}/"
print("Bot başlatıldı...")

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
    return (
        "📜 Komutlar ve Açıklamaları:\n\n"
        "🔍 Sistem Bilgisi Komutları:\n"
        "  - /status - 💻 CPU ve RAM kullanımını gösterir.\n"
        "  - /diskusage - 💾 Disk kullanımını gösterir.\n"
        "  - /uptime - ⏱️ Bilgisayarın çalışma süresini gösterir.\n"
        "  - /cpuinfo - 💻 CPU bilgilerini gösterir.\n"
        "  - /raminfo - 🧠 RAM bilgilerini gösterir.\n"
        "  - /diskinfo - 💾 Disk bilgilerini detaylı gösterir.\n"
        "  - /osinfo - 🖥️ İşletim sistemi bilgilerini gösterir.\n"
        "  - /systeminfo - 🖥️ Sistem bilgilerini detaylı gösterir.\n\n"
        "📸 Ekran Görüntüsü Komutları:\n"
        "  - /screenshot - 📸 Ekran görüntüsü alır.\n\n"
        "📂 Dosya ve Klasör İşlemleri:\n"
        "  - /createfile <dosya_adi> - 📝 Yeni bir dosya oluşturur.\n"
        "  - /deletefile <dosya_adi> - 🗑️ Belirtilen dosyayı siler.\n"
        "  - /renamefile <eski_ad> <yeni_ad> - 🔄 Dosya adını değiştirir.\n"
        "  - /deletefolder <klasor_yolu> - 🗑️ Belirtilen klasörü siler.\n"
        "  - /listfiles <dizin> - 📂 Belirtilen dizindeki dosyaları listeler.\n"
        "  - /copyfolder <kaynak> <hedef> - 📋 Klasörü kopyalar.\n"
        "  - /movefolder <kaynak> <hedef> - 🚚 Klasörü taşır.\n\n"
        "🔊 Sistem Kontrol Komutları:\n"
        "  - /lock - 🔒 Bilgisayarı kilitler.\n"
        "  - /hibernate - 💤 Bilgisayarı uyku moduna alır.\n"
        "  - /logoff - 🚪 Kullanıcı oturumunu kapatır.\n"
        "  - /suspend - 💤 Bilgisayarı askıya alır.\n"
        "  - /reboot - 🔄 Bilgisayarı yeniden başlatır.\n"
        "  - /restart - 🔄 Bilgisayarı yeniden başlatır.\n"
        "  - /shutdown - 🛑 Bilgisayarı kapatır.\n"
        "  - /cleartemp - 🧹 Geçici dosyaları temizler.\n\n"
        "🖥️ İşlem Yönetimi:\n"
        "  - /listprocesses - Çalışan işlemleri listeler.\n"
        "  - /killprocess <process_name> - Belirtilen işlemi sonlandırır.\n\n"
        "🌐 Ağ Komutları:\n"
        "  - /getip - Bilgisayarın IP adresini döner.\n"
        "  - /publicip - 🌐 Genel IP adresini döner.\n"
        "  - /traceroute <host> - 🌐 Belirtilen hosta traceroute işlemi yapar.\n"
        "  - /networkinfo - 🌐 Ağ bilgilerini gösterir.\n\n"
        "🔋 Pil ve Kullanıcı Komutları:\n"
        "  - /batteryinfo - 🔋 Pil durumu ve şarj bilgilerini gösterir.\n"
        "  - /whoami - 👤 Şu anki kullanıcıyı gösterir.\n"
        "  - /listusers - 👥 Sistemdeki kullanıcıları listeler.\n"
        "  - /activewindow - 🪟 Şu anda aktif olan pencerenin başlığını gösterir.\n\n"
        "ℹ️ Yardım ve Diğer Komutlar:\n"
        "  - /help - 📜 Bu yardım mesajını gösterir.\n"
    )

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

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return f"✅ Dosya adı değiştirildi: {old_name} → {new_name}"
    except Exception as e:
        return f"⚠️ Dosya adı değiştirilemedi: {str(e)}"

def copy_folder(source, destination):
    try:
        import shutil
        shutil.copytree(source, destination)
        return f"✅ Klasör kopyalandı: {source} → {destination}"
    except Exception as e:
        return f"⚠️ Klasör kopyalanamadı: {str(e)}"

def move_folder(source, destination):
    try:
        import shutil
        shutil.move(source, destination)
        return f"✅ Klasör taşındı: {source} → {destination}"
    except Exception as e:
        return f"⚠️ Klasör taşınamadı: {str(e)}"

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
            plugged = "Evet" if battery.power_plugged else "Hayır"
            return f"🔋 Pil Durumu: %{percent}\n🔌 Şarjda mı: {plugged}"
        else:
            return "⚠️ Pil bilgisi alınamadı."
    except Exception as e:
        return f"⚠️ Pil bilgisi alınamadı: {str(e)}"

def get_os_info():
    try:
        os_info = os.uname()
        return f"🖥️ İşletim Sistemi Bilgisi:\nSistem: {os_info.sysname}\nSürüm: {os_info.release}\nMakine: {os_info.machine}"
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
        ip = requests.get('https://api.ipify.org').text
        return f"🌐 Genel IP Adresi: {ip}"
    except Exception as e:
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
    except Exception as e:
        return f"⚠️ Aktif pencere bilgisi alınamadı: {str(e)}"

def handle_command(command, chat_id):
    try:
        command = command.lower().strip()
        
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
        elif command == '/hibernate':
            return hibernate_computer()
        elif command == '/logoff':
            return logoff_user()
        elif command == '/listprocesses':
            return list_processes()
        elif command.startswith('/killprocess'):
            try:
                process_name = command.split(' ', 1)[1].strip()
                return kill_process(process_name)
            except IndexError:
                return "⚠️ Lütfen işlem adını belirtin. Örnek: /killprocess notepad.exe"
        elif command == '/getip':
            return get_ip_address()
        elif command.startswith('/createfile'):
            try:
                filename = command.split(' ', 1)[1].strip()
                if not filename:
                    raise ValueError("Dosya adı boş olamaz.")
                return create_file(filename)
            except IndexError:
                return "⚠️ Lütfen dosya adını belirtin."
            except ValueError as e:
                return f"⚠️ {str(e)}"
        elif command.startswith('/deletefile'):
            try:
                filename = command.split(' ', 1)[1].strip()
                if not filename:
                    raise ValueError("Dosya adı boş olamaz.")
                return delete_file(filename)
            except IndexError:
                return "⚠️ Lütfen silinecek dosya adını belirtin."
            except ValueError as e:
                return f"⚠️ {str(e)}"
        elif command.startswith('/deletefolder'):
            try:
                folder_path = command.split(' ', 1)[1].strip()
                return delete_folder(folder_path)
            except IndexError:
                return "⚠️ Lütfen silinecek klasör yolunu belirtin."
        elif command.startswith('/listfiles'):
            try:
                directory = command.split(' ', 1)[1].strip()
                return list_files(directory)
            except IndexError:
                return "⚠️ Lütfen bir dizin belirtin."
        elif command == '/batteryinfo':
            return get_battery_info()
        elif command == '/osinfo':
            return get_os_info()
        elif command == '/publicip':
            return get_public_ip()
        elif command.startswith('/traceroute'):
            try:
                host = command.split(' ', 1)[1].strip()
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
        elif command == '/help':
            return get_help()
        elif command == '/restart':
            return restart_computer()
        elif command == '/shutdown':
            return shutdown_computer()
        else:
            return "❓ Bilinmeyen komut."
    except Exception as e:
        return f"⚠️ Hata oluştu: {str(e)}"

def main():
    last_update_id = None

    while True:
        try:
            updates = get_updates(last_update_id)

            if 'result' in updates and len(updates['result']) > 0:
                for update in updates['result']:
                    last_update_id = update['update_id'] + 1
                    message = update['message']
                    from_id = message['from']['id']
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

if __name__ == '__main__':
    main()
