```text
================================================================================
                            DROID SURGEON  ·  v1.1.1
                    Advanced Android Device Management Suite
================================================================================
[ LICENSE ] GNU General Public License v3.0 (GPL-3.0)
[ PLATFORM] Linux (Debian / Ubuntu / Kali / Arch)
[ STACK   ] Python 3 · PyQt5 · ADB · Fastboot · Scrcpy
[ FILE    ] Droid_Surgeon.py (Single-file application)
================================================================================
```

```bash
$ cat README.md | grep -A 100 "SECTION: ENGLISH"

================================================================================
[ SECTION: ENGLISH ]
================================================================================
> Droid Surgeon is a comprehensive, GUI-based desktop application designed 
> to bridge the gap between system-level Android engineering and daily 
> device management. Built purely with Python and PyQt5, it provides a 
> powerful interface to control and diagnose Android devices via ADB and Fastboot.

$ ./droid_surgeon --features
[+] Live Dashboard       : Battery, Storage, RAM, Thermal
[+] Hardware Control     : Key events, D-Pad, Touch gestures
[+] Screen Mirroring     : Scrcpy (Bitrate / FPS control)
[+] Fastboot Suite       : Flash, erase, format, slot switching
[+] Package Manager      : Disable, enable, stop, uninstall
[+] File Browser         : Pull, delete, mkdir
[+] Process Monitor      : Real-time PID viewer and killer
[+] Live Logcat          : Filter and export logs
[+] Terminal             : Raw ADB shell execution

$ # REQUIRED DEPENDENCIES (Debian/Ubuntu/Kali)
$ sudo apt update
$ sudo apt install python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtwebengine
$ sudo apt install android-tools-adb android-tools-fastboot scrcpy
$ sudo apt install libxcb-cursor0 libxcb-xinerama0

$ # REQUIRED DEPENDENCIES (Arch Linux)
$ sudo pacman -S python-pyqt5 qt5-svg qt5-webengine android-tools scrcpy

$ git clone https://github.com/mjv97373-tech/Droid-Surgeon.git
$ cd Droid-Surgeon
$ chmod +x Droid_Surgeon.py
$ python3 Droid_Surgeon.py

$ ./droid_surgeon --warning
- Fastboot operations (flash, erase, format) can permanently wipe data.
```

```bash
$ cat README.md | grep -A 100 "SECTION: PERSIAN"

================================================================================
[ SECTION: PERSIAN ]
================================================================================
> دروید سورجن یک برنامه جامع و گرافیکی برای دسکتاپ است که برای پر کردن 
> شکاف بین مهندسی سطح سیستم اندروید و مدیریت روزمره دستگاه طراحی شده است. 
> این برنامه به صورت تک‌فایل با پایتون و PyQt5 ساخته شده و رابط کاربری قدرتمندی 
> برای کنترل و عیب‌یابی گوشی‌های اندرویدی از طریق ADB و Fastboot ارائه می‌دهد.

$ ./droid_surgeon --features
[+] داشبورد زنده        : باتری، حافظه، رم، دما
[+] کنترل سخت‌افزار     : کلیدهای فیزیکی، دی‌پد، حرکات لمسی
[+] آینه کردن صفحه      : اسکرپی (کنترل بیت‌ریت و فریم ریت)
[+] ابزارهای فست‌بوت    : فلش، پاک کردن، فرمت، تغییر اسلات
[+] مدیریت پکیج‌ها      : غیرفعال، فعال، توقف، حذف برنامه‌ها
[+] مرورگر فایل         : دانلود، حذف، ساخت پوشه
[+] مانیتور پروسه‌ها     : مشاهده و کشتن پروسه‌ها
[+] مشاهده لاگ‌ها        : فیلتر و خروجی گرفتن از لاگ‌ها
[+] ترمینال             : اجرای دستورات خام ADB

$ # پیش‌نیازهای ضروری (دبیان/اوبونتو/کالی)
$ sudo apt update
$ sudo apt install python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtwebengine
$ sudo apt install android-tools-adb android-tools-fastboot scrcpy
$ sudo apt install libxcb-cursor0 libxcb-xinerama0

$ # پیش‌نیازهای ضروری (آرچ لینوکس)
$ sudo pacman -S python-pyqt5 qt5-svg qt5-webengine android-tools scrcpy

$ git clone https://github.com/mjv97373-tech/Droid-Surgeon.git
$ cd Droid-Surgeon
$ chmod +x Droid_Surgeon.py
$ python3 Droid_Surgeon.py

$ ./droid_surgeon --warning
- عملیات فست‌بوت (فلش، پاک کردن، فرمت) می‌تواند منجر به از دست رفتن دائمی داده‌ها شود.
```

```bash
$ cat README.md | grep -A 100 "SECTION: RUSSIAN"

================================================================================
[ SECTION: RUSSIAN ]
================================================================================
> Droid Surgeon — это комплексное настольное приложение с графическим 
> интерфейсом для управления Android-устройствами. Написано на Python и PyQt5 
> (в виде одного файла) и предоставляет мощный интерфейс для контроля и 
> диагностики устройств через ADB и Fastboot.

$ ./droid_surgeon --features
[+] Живая панель         : Батарея, Память, ОЗУ, Температура
[+] Управление железом   : Кнопки, D-Pad, Жесты
[+] Зеркалирование       : Scrcpy (Битрейт / FPS)
[+] Fastboot             : Прошивка, стирание, форматирование
[+] Менеджер пакетов     : Отключение, включение, удаление
[+] Файловый менеджер    : Скачивание, удаление, создание папок
[+] Монитор процессов    : Просмотр и завершение процессов
[+] Логи (Logcat)        : Фильтрация и экспорт логов
[+] Терминал             : Выполнение команд ADB

$ # НЕОБХОДИМЫЕ ЗАВИСИМОСТИ (Debian/Ubuntu/Kali)
$ sudo apt update
$ sudo apt install python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtwebengine
$ sudo apt install android-tools-adb android-tools-fastboot scrcpy
$ sudo apt install libxcb-cursor0 libxcb-xinerama0

$ # НЕОБХОДИМЫЕ ЗАВИСИМОСТИ (Arch Linux)
$ sudo pacman -S python-pyqt5 qt5-svg qt5-webengine android-tools scrcpy

$ git clone https://github.com/mjv97373-tech/Droid-Surgeon.git
$ cd Droid-Surgeon
$ chmod +x Droid_Surgeon.py
$ python3 Droid_Surgeon.py

$ ./droid_surgeon --warning
- Операции Fastboot (прошивка, стирание, формат) могут безвозвратно удалить данные.
```

```bash
$ cat README.md | grep -A 100 "SECTION: GLOBAL"

================================================================================
[ SECTION: GLOBAL ]
================================================================================
$ ./droid_surgeon --shortcuts
[ 1 - 9 ]  -->  Switch Tabs
[ 0 ]      -->  Terminal
[ F5 ]     -->  Refresh Devices
[ F11 ]    -->  Toggle Fullscreen
[ Ctrl + ] -->  Increase UI Scale
[ Ctrl - ] -->  Decrease UI Scale
[ Ctrl 0 ] -->  Reset UI Scale to 100%
[ Ctrl Q ] -->  Quit Application

$ ./droid_surgeon --contact
> GITHUB   : github.com/mjv97373-tech
> TELEGRAM : t.me/ExpilotLinux
> LICENSE  : GNU GPL v3.0
> STATUS   : STABLE

[ "Behind every render is a world that refused to stay imaginary." ]
================================================================================
```

```bash
$ cat README.md | grep -A 100 "SECTION: LICENSE"

================================================================================
[ SECTION: LICENSE (GNU GPL v3.0) ]
================================================================================
> Droid Surgeon is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> Droid Surgeon is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program. If not, see <https://www.gnu.org/licenses/>.

$ wget https://www.gnu.org/licenses/gpl-3.0.txt -O LICENSE
$ cat LICENSE | head -n 5
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
================================================================================
[ EOF ] End of File.
================================================================================
```
