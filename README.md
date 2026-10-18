::: {align="center"}
# ⚕️ DROID SURGEON

### Advanced Android Device Management Suite

**Control · Inspect · Mirror · Diagnose**

A desktop toolkit built with Python and PyQt5, integrating Android Debug
Bridge (ADB), Fastboot, and scrcpy.

[English](#english) · [فارسی](#فارسی) · [Русский](#русский)

**Version:** 1.1.1 · **License:** GNU GPL v3.0
:::

------------------------------------------------------------------------

`<a name="english">`{=html}`</a>`{=html} \## 🇬🇧 English

### Overview

**DROID SURGEON** is a desktop graphical interface for managing and
inspecting Android devices through established command-line tools. It
brings common ADB, Fastboot, and scrcpy workflows together in a dark,
resizable interface.

> DROID SURGEON is a front-end for external Android tools, not a
> replacement for them. Available operations depend on the connected
> device, Android version, permissions, bootloader state, and installed
> tool versions.

### Features

-   **Dashboard:** device overview and available battery, storage,
    memory, thermal, and uptime information.
-   **ADB control:** send hardware-key events and perform tap, swipe,
    long-press, pinch, and scroll gestures.
-   **Screen mirroring:** launch scrcpy and configure bitrate, frame
    rate, maximum size, orientation, and supported display options.
-   **Fastboot tools:** access supported bootloader operations.
    Flashing, erasing, slot changes, and other bootloader actions can
    permanently affect a device.
-   **Package management:** inspect installed packages and use available
    package actions.
-   **File browser:** browse supported device paths and perform
    available file operations.
-   **Process viewer:** inspect running processes and use supported
    process actions.
-   **Logcat:** view Android system logs in real time.
-   **Network diagnostics:** access the network-related diagnostics
    provided by the application.
-   **Terminal and reference:** run supported ADB/Fastboot workflows
    through the interface and consult the built-in quick reference.
-   **Adjustable UI:** change interface scale from 70% to 140%; the
    setting is saved.

### Requirements

**Host system** - Linux is the primary documented environment; package
commands below target Debian, Ubuntu, and Kali Linux. - Python 3. -
PyQt5. - Android platform tools: `adb` and `fastboot`. - `scrcpy` for
screen mirroring. - A USB cable and an Android device, or an
appropriately configured Android virtual device, for device operations.

**Android device** - Enable **Developer options → USB debugging** for
ADB operations. - Unlock the device and accept its debugging
authorization prompt when requested. - Fastboot features require a
device that supports Fastboot and has been booted into its
bootloader/fastboot mode. - Some operations require additional device
permissions or an unlockable bootloader.

### Install prerequisites

#### Debian / Ubuntu / Kali Linux

``` bash
sudo apt update
sudo apt install -y python3 python3-pyqt5 android-tools-adb android-tools-fastboot scrcpy
```

#### Arch Linux

``` bash
sudo pacman -Syu
sudo pacman -S python python-pyqt5 android-tools scrcpy
```

Package names and available versions can vary by distribution. If a
package is unavailable, consult your distribution's official
repositories and documentation.

### Download the project

If you have cloned the repository:

``` bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>
```

Replace the placeholders with the actual repository URL and directory
name. If you downloaded the Python file directly, open a terminal in the
folder containing `Droid_Surgeon.py`.

### Verify the dependencies

``` bash
python3 --version
python3 -c "import PyQt5; print('PyQt5 OK')"
adb version
fastboot --version
scrcpy --version
```

If you only need the GUI and do not plan to use a missing external tool,
some screens may still open, but the associated functionality will not
work.

### Run DROID SURGEON

``` bash
python3 Droid_Surgeon.py
```

If the application reports a missing executable, install the
corresponding system package and verify that the command is available in
your `PATH`.

### Connect an Android device

1.  On the Android device, open **Settings → About phone**.
2.  Tap **Build number** repeatedly until Developer options are enabled.
    Menu names vary by manufacturer.
3.  Open **Developer options** and enable **USB debugging**.
4.  Connect the device using a data-capable USB cable.
5.  Accept the RSA debugging authorization prompt on the device.
6.  Refresh the ADB device list in DROID SURGEON.

Check the connection from a terminal:

``` bash
adb devices
```

If the device shows `unauthorized`, unlock it and accept the
authorization prompt. If no device appears, try another USB port or data
cable and check the operating system's USB permissions.

### Start screen mirroring

1.  Confirm that ADB detects and authorizes the device.
2.  Open the **MIRROR** tab.
3.  Choose the desired bitrate, FPS, maximum size, and orientation.
4.  Press **START**.

The mirror uses scrcpy installed on the host system. Some options depend
on the installed scrcpy version.

### Fastboot workflow

Fastboot is a separate device mode; a device visible to ADB is not
necessarily visible to Fastboot.

``` bash
adb devices
adb reboot bootloader
fastboot devices
```

When finished, use the application's supported reboot action or, where
appropriate:

``` bash
fastboot reboot
```

**Warning:** Do not flash, erase, unlock, or change partitions unless
you understand the device-specific procedure and have verified the image
files. These actions may erase data, make the device unbootable, or
affect its warranty. Never use images intended for a different model or
variant.

### Troubleshooting

  -----------------------------------------------------------------------
  Problem                             What to try
  ----------------------------------- -----------------------------------
  `adb: command not found`            Install `android-tools-adb` or the
                                      platform-tools package for your
                                      distribution.

  `fastboot: command not found`       Install `android-tools-fastboot` or
                                      the relevant platform-tools
                                      package.

  `scrcpy` is missing                 Install scrcpy from your
                                      distribution's official package
                                      source.

  Device is `unauthorized`            Unlock the device and accept its
                                      USB debugging authorization prompt.

  No device is listed                 Check the USB cable, USB mode,
                                      port, permissions, and debugging
                                      setting.

  Fastboot list is empty              Reboot into bootloader/fastboot
                                      mode and check USB access and
                                      drivers/permissions.

  PyQt5 import fails                  Install the distribution's PyQt5
                                      package and verify which Python
                                      interpreter is running the app.

  A scrcpy option fails               Check `scrcpy --help`; supported
                                      flags differ between versions.
  -----------------------------------------------------------------------

Restart ADB if needed:

``` bash
adb kill-server
adb start-server
adb devices
```

### Safety and responsible use

-   Use the software only with devices you own or are explicitly
    authorized to manage.
-   Review the target device and selected operation before making
    changes.
-   Back up important data before package removal, file changes,
    flashing, erasing, or bootloader operations.
-   Treat Logcat and device files as potentially sensitive; avoid
    publishing logs containing personal information, tokens, or
    identifiers.
-   USB debugging grants powerful access. Disable it when you no longer
    need it, especially on shared or untrusted computers.
-   The project is provided **without warranty**. The author is not
    responsible for data loss, device damage, or misuse.

### License

DROID SURGEON declares **GNU General Public License v3.0 (GPL-3.0)**.
See the repository's `LICENSE` file for the complete license text. If
redistributing the project, include the license and comply with its
terms.

------------------------------------------------------------------------

`<a name="فارسی">`{=html}`</a>`{=html} \## 🇮🇷 فارسی

### معرفی

**DROID SURGEON** یک ابزار گرافیکی دسکتاپ برای مدیریت و بررسی دستگاه‌های
اندرویدی است. این برنامه با Python و PyQt5 ساخته شده و قابلیت‌های
ابزارهای ADB، Fastboot و scrcpy را در یک رابط تیره و قابل تنظیم گرد هم
می‌آورد.

> این برنامه یک رابط گرافیکی برای ابزارهای خارجی اندروید است، نه جایگزین
> آن‌ها. قابلیت‌های قابل استفاده به مدل دستگاه، نسخه اندروید، سطح دسترسی،
> وضعیت بوت‌لودر و نسخه ابزارهای نصب‌شده بستگی دارد.

### امکانات

-   **داشبورد دستگاه:** نمایش اطلاعات قابل دسترس باتری، حافظه، فضای
    ذخیره‌سازی، دما و مدت روشن‌بودن دستگاه.
-   **کنترل ADB:** ارسال کلیدهای سخت‌افزاری و اجرای ژست‌هایی مانند لمس،
    کشیدن، لمس طولانی، pinch و اسکرول.
-   **نمایش زنده صفحه:** اجرای scrcpy و تنظیم نرخ بیت، FPS، اندازه
    تصویر، جهت صفحه و گزینه‌های پشتیبانی‌شده.
-   **ابزارهای Fastboot:** دسترسی به عملیات پشتیبانی‌شده در حالت بوت‌لودر؛
    بعضی عملیات ممکن است اطلاعات را پاک یا دستگاه را غیرقابل بوت کنند.
-   **مدیریت بسته‌ها:** مشاهده بسته‌های نصب‌شده و استفاده از عملیات موجود
    برای آن‌ها.
-   **مدیریت فایل‌ها:** مرور مسیرهای قابل دسترس دستگاه و انجام عملیات
    پشتیبانی‌شده.
-   **مشاهده فرایندها:** بررسی فرایندهای در حال اجرا و استفاده از عملیات
    موجود.
-   **Logcat:** مشاهده زنده گزارش‌های سیستم اندروید.
-   **عیب‌یابی شبکه:** دسترسی به قابلیت‌های تشخیصی شبکه‌ای که برنامه ارائه
    می‌دهد.
-   **ترمینال و راهنما:** اجرای گردش‌کارهای پشتیبانی‌شده ADB/Fastboot و
    استفاده از راهنمای داخلی.
-   **تنظیم اندازه رابط:** تغییر مقیاس رابط از ۷۰ تا ۱۴۰ درصد و ذخیره
    تنظیمات.

### پیش‌نیازها

-   سیستم Linux؛ دستورات زیر برای Debian، Ubuntu و Kali Linux نوشته
    شده‌اند.
-   Python 3 و کتابخانه PyQt5.
-   ابزارهای Android Platform Tools شامل `adb` و `fastboot`.
-   ابزار `scrcpy` برای نمایش صفحه دستگاه.
-   کابل USB دارای قابلیت انتقال داده یا یک دستگاه مجازی اندروید که
    به‌درستی پیکربندی شده باشد.

برای عملیات ADB، گزینه **USB debugging** را از بخش Developer options
فعال کنید. برای عملیات Fastboot نیز دستگاه باید از این حالت پشتیبانی کند
و در حالت بوت‌لودر/Fastboot قرار گرفته باشد.

### نصب پیش‌نیازها

#### Debian / Ubuntu / Kali Linux

``` bash
sudo apt update
sudo apt install -y python3 python3-pyqt5 android-tools-adb android-tools-fastboot scrcpy
```

#### Arch Linux

``` bash
sudo pacman -Syu
sudo pacman -S python python-pyqt5 android-tools scrcpy
```

نام بسته‌ها و نسخه‌های موجود ممکن است بسته به توزیع متفاوت باشد. در صورت
خطا، مخازن رسمی توزیع خود را بررسی کنید.

### دریافت پروژه

اگر پروژه در یک مخزن Git قرار دارد:

``` bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>
```

مقادیر داخل علامت‌های `< >` را با آدرس واقعی مخزن و نام پوشه جایگزین
کنید. اگر فقط فایل پایتون را دانلود کرده‌اید، ترمینال را در همان پوشه‌ای
باز کنید که `Droid_Surgeon.py` در آن قرار دارد.

### بررسی نصب

``` bash
python3 --version
python3 -c "import PyQt5; print('PyQt5 نصب است')"
adb version
fastboot --version
scrcpy --version
```

### اجرای برنامه

``` bash
python3 Droid_Surgeon.py
```

اگر برنامه اعلام کرد یکی از ابزارهای خارجی پیدا نشده است، بسته مربوطه را
نصب کنید و مطمئن شوید فرمان آن در `PATH` سیستم قابل اجراست.

### اتصال دستگاه اندرویدی

۱. وارد **Settings → About phone** شوید.

۲. چند بار روی **Build number** بزنید تا Developer options فعال شود.

۳. وارد Developer options شوید و **USB debugging** را فعال کنید.

۴. دستگاه را با کابل USB دارای قابلیت انتقال داده متصل کنید.

۵. در صورت نمایش درخواست مجوز، پیام تأیید RSA را روی دستگاه بپذیرید.

۶. فهرست دستگاه‌ها را در برنامه به‌روزرسانی کنید.

برای بررسی اتصال:

``` bash
adb devices
```

اگر وضعیت `unauthorized` نمایش داده شد، دستگاه را باز کنید و مجوز اتصال
را بپذیرید. اگر دستگاه نمایش داده نشد، کابل، پورت USB، مجوزهای سیستم و
تنظیمات اشکال‌زدایی را بررسی کنید.

### نمایش صفحه دستگاه

۱. ابتدا مطمئن شوید دستگاه از طریق ADB شناسایی شده است.

۲. وارد زبانه **MIRROR** شوید.

۳. نرخ بیت، FPS، اندازه تصویر و جهت صفحه را تنظیم کنید.

۴. روی **START** بزنید.

نمایش صفحه به نصب بودن scrcpy روی سیستم میزبان نیاز دارد. همه گزینه‌ها در
تمام نسخه‌های scrcpy در دسترس نیستند.

### استفاده از Fastboot

ADB و Fastboot دو حالت متفاوت هستند؛ شناسایی دستگاه در ADB به معنی
شناسایی آن در Fastboot نیست.

``` bash
adb devices
adb reboot bootloader
fastboot devices
```

برای خروج از Fastboot، از گزینه ریبوت برنامه یا در صورت مناسب بودن از
فرمان زیر استفاده کنید:

``` bash
fastboot reboot
```

**هشدار مهم:** فلش‌کردن، پاک‌کردن پارتیشن‌ها، بازکردن بوت‌لودر و تغییر
اسلات‌ها می‌توانند اطلاعات را پاک کنند یا دستگاه را از کار بیندازند. قبل
از هر عملیات، دستورالعمل مخصوص مدل دستگاه و سازگاری فایل‌های ایمیج را
بررسی کنید.

### رفع خطاهای رایج

  -----------------------------------------------------------------------
  مشکل                                راهکار
  ----------------------------------- -----------------------------------
  فرمان `adb` پیدا نمی‌شود             بسته ADB یا Android Platform Tools
                                      را نصب کنید.

  فرمان `fastboot` پیدا نمی‌شود        بسته Fastboot را نصب کنید.

  scrcpy اجرا نمی‌شود                  نصب scrcpy و سازگاری نسخه آن را
                                      بررسی کنید.

  دستگاه `unauthorized` است           درخواست مجوز USB debugging را روی
                                      گوشی تأیید کنید.

  دستگاه نمایش داده نمی‌شود            کابل، پورت، تنظیمات USB و مجوزها را
                                      بررسی کنید.

  دستگاه در Fastboot نیست             وارد حالت بوت‌لودر/Fastboot شوید و
                                      اتصال USB را بررسی کنید.

  PyQt5 پیدا نمی‌شود                   نصب بسته PyQt5 و مفسر Python مورد
                                      استفاده را بررسی کنید.
  -----------------------------------------------------------------------

برای راه‌اندازی مجدد ADB:

``` bash
adb kill-server
adb start-server
adb devices
```

### امنیت و استفاده مسئولانه

-   فقط روی دستگاه‌هایی کار کنید که مالک آن‌ها هستید یا مجوز صریح
    مدیریتشان را دارید.
-   قبل از اجرای عملیات، دستگاه هدف و فرمان انتخاب‌شده را بررسی کنید.
-   پیش از حذف بسته‌ها، تغییر فایل‌ها، فلش یا پاک‌کردن اطلاعات، نسخه
    پشتیبان تهیه کنید.
-   گزارش‌های Logcat و فایل‌های دستگاه ممکن است حاوی اطلاعات خصوصی باشند؛
    پیش از انتشار آن‌ها اطلاعات حساس را حذف کنید.
-   USB debugging دسترسی قدرتمندی ایجاد می‌کند؛ پس از اتمام کار، به‌ویژه
    روی رایانه‌های عمومی یا غیرقابل اعتماد، آن را غیرفعال کنید.
-   برنامه بدون ضمانت ارائه می‌شود و نویسنده مسئول خسارت ناشی از
    ازدست‌رفتن داده‌ها، آسیب دستگاه یا استفاده نادرست نیست.

### مجوز

مجوز اعلام‌شده برای DROID SURGEON، **GNU GPL نسخه ۳.۰** است. متن کامل
مجوز باید در فایل `LICENSE` مخزن قرار داشته باشد. هنگام بازتوزیع پروژه،
شرایط مجوز را رعایت کنید.

------------------------------------------------------------------------

`<a name="русский">`{=html}`</a>`{=html} \## 🇷🇺 Русский

### Обзор

**DROID SURGEON** --- настольное графическое приложение для управления
Android-устройствами и их диагностики. Оно создано на Python с
использованием PyQt5 и объединяет рабочие процессы ADB, Fastboot и
scrcpy в тёмном интерфейсе с настраиваемым масштабом.

> Приложение является графическим интерфейсом для внешних
> Android-инструментов, а не их заменой. Доступные функции зависят от
> модели устройства, версии Android, разрешений, состояния загрузчика и
> версий установленных инструментов.

### Возможности

-   **Панель устройства:** доступная информация о батарее, хранилище,
    памяти, температуре и времени работы.
-   **Управление через ADB:** отправка аппаратных клавиш и выполнение
    жестов --- касание, свайп, длительное нажатие, pinch и прокрутка.
-   **Трансляция экрана:** запуск scrcpy и настройка битрейта, FPS,
    максимального размера, ориентации и поддерживаемых параметров
    отображения.
-   **Инструменты Fastboot:** доступ к поддерживаемым операциям
    загрузчика. Некоторые операции могут стереть данные или нарушить
    загрузку устройства.
-   **Управление пакетами:** просмотр установленных пакетов и доступные
    операции с ними.
-   **Файловый менеджер:** просмотр доступных путей устройства и
    поддерживаемые файловые операции.
-   **Просмотр процессов:** анализ запущенных процессов и доступные
    операции управления.
-   **Logcat:** просмотр системных журналов Android в реальном времени.
-   **Сетевая диагностика:** доступ к сетевым диагностическим функциям
    приложения.
-   **Терминал и справка:** выполнение поддерживаемых сценариев
    ADB/Fastboot и встроенная справочная информация.
-   **Масштаб интерфейса:** настройка от 70% до 140% с сохранением
    параметров.

### Требования

-   Linux; приведённые команды предназначены для Debian, Ubuntu и Kali
    Linux.
-   Python 3 и PyQt5.
-   Android Platform Tools: `adb` и `fastboot`.
-   `scrcpy` для трансляции экрана.
-   USB-кабель с передачей данных или корректно настроенное виртуальное
    Android-устройство.

Для работы через ADB включите **Developer options → USB debugging**. Для
функций Fastboot устройство должно поддерживать Fastboot и находиться в
режиме загрузчика/Fastboot.

### Установка зависимостей

#### Debian / Ubuntu / Kali Linux

``` bash
sudo apt update
sudo apt install -y python3 python3-pyqt5 android-tools-adb android-tools-fastboot scrcpy
```

#### Arch Linux

``` bash
sudo pacman -Syu
sudo pacman -S python python-pyqt5 android-tools scrcpy
```

Названия пакетов и доступные версии могут различаться в зависимости от
дистрибутива. При ошибках проверьте официальные репозитории вашей
системы.

### Получение проекта

Если проект размещён в Git-репозитории:

``` bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>
```

Замените значения в `< >` реальным URL репозитория и именем каталога.
Если вы скачали только Python-файл, откройте терминал в каталоге, где
находится `Droid_Surgeon.py`.

### Проверка зависимостей

``` bash
python3 --version
python3 -c "import PyQt5; print('PyQt5 OK')"
adb version
fastboot --version
scrcpy --version
```

### Запуск

``` bash
python3 Droid_Surgeon.py
```

Если приложение сообщает об отсутствующей внешней программе, установите
соответствующий системный пакет и убедитесь, что команда доступна через
`PATH`.

### Подключение Android-устройства

1.  Откройте **Настройки → О телефоне**.
2.  Несколько раз нажмите **Номер сборки**, чтобы включить параметры
    разработчика.
3.  Включите **Отладку по USB** в параметрах разработчика.
4.  Подключите устройство USB-кабелем с поддержкой передачи данных.
5.  Разрешите отладку, подтвердив RSA-запрос на устройстве.
6.  Обновите список ADB-устройств в приложении.

Проверить подключение можно командой:

``` bash
adb devices
```

Если отображается `unauthorized`, разблокируйте устройство и подтвердите
запрос авторизации. Если устройство не найдено, проверьте кабель,
USB-порт, разрешения системы и настройки отладки.

### Трансляция экрана

1.  Убедитесь, что ADB обнаруживает устройство и авторизация
    подтверждена.
2.  Откройте вкладку **MIRROR**.
3.  Настройте битрейт, FPS, максимальный размер и ориентацию.
4.  Нажмите **START**.

Для трансляции требуется установленный на компьютере scrcpy. Поддержка
отдельных параметров зависит от версии scrcpy.

### Работа с Fastboot

ADB и Fastboot --- разные режимы. Наличие устройства в ADB не означает,
что оно будет обнаружено в Fastboot.

``` bash
adb devices
adb reboot bootloader
fastboot devices
```

Чтобы выйти из Fastboot, используйте доступную функцию перезагрузки
приложения или, если это подходит для устройства:

``` bash
fastboot reboot
```

**Внимание:** прошивка, стирание разделов, разблокировка загрузчика и
изменение слотов могут привести к потере данных или невозможности
загрузки устройства. Используйте только образы, предназначенные для
точной модели и её варианта, и заранее изучите инструкции производителя.

### Решение распространённых проблем

  -----------------------------------------------------------------------
  Проблема                            Что проверить
  ----------------------------------- -----------------------------------
  `adb: command not found`            Установите пакет ADB или Android
                                      Platform Tools.

  `fastboot: command not found`       Установите пакет Fastboot.

  scrcpy не найден                    Установите scrcpy из официального
                                      источника пакетов дистрибутива.

  Устройство имеет статус             Подтвердите запрос USB-отладки на
  `unauthorized`                      устройстве.

  Устройство не отображается          Проверьте кабель, порт, режим USB и
                                      системные разрешения.

  Устройство отсутствует в Fastboot   Перейдите в режим
                                      загрузчика/Fastboot и проверьте
                                      USB-подключение.

  Не импортируется PyQt5              Проверьте установку PyQt5 и
                                      используемый интерпретатор Python.
  -----------------------------------------------------------------------

При необходимости перезапустите ADB:

``` bash
adb kill-server
adb start-server
adb devices
```

### Безопасность и ответственное использование

-   Используйте приложение только на собственных устройствах или при
    наличии явного разрешения владельца.
-   Перед выполнением операции проверяйте целевое устройство и выбранное
    действие.
-   Создавайте резервные копии перед удалением пакетов, изменением
    файлов, прошивкой или стиранием данных.
-   Logcat и файлы устройства могут содержать конфиденциальные данные.
    Удаляйте личную информацию перед публикацией журналов.
-   USB-отладка предоставляет широкие возможности доступа. Отключайте её
    после завершения работы, особенно на общих или ненадёжных
    компьютерах.
-   Программа предоставляется **без гарантий**. Автор не несёт
    ответственности за потерю данных, повреждение устройства или
    неправильное использование.

### Лицензия

Для DROID SURGEON заявлена лицензия **GNU General Public License v3.0
(GPL-3.0)**. Полный текст лицензии следует включить в файл `LICENSE`
репозитория. При распространении проекта соблюдайте условия лицензии.

------------------------------------------------------------------------

::: {align="center"}
**DROID SURGEON · v1.1.1**

*Inspect responsibly. Modify carefully. Always back up first.*
:::
