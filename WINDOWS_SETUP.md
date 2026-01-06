# Windows Setup Guide 🪟

Детальна інструкція встановлення на Windows для конвертера відео → ASCII.

## Проблема: NumPy Build Error

Якщо ви бачите помилку:
```
BackendUnavailable: Cannot import 'setuptools.build_meta'
```

Це означає, що NumPy намагається скомпілюватись з джерела, але відсутні build-утиліти. На Windows це трапляється часто.

## Рішення 1: Оновити pip та встановити build tools (РЕКОМЕНДОВАНО) ✅

### Крок 1: Оновити pip

```cmd
python -m pip install --upgrade pip setuptools wheel
```

### Крок 2: Встановити пакети

```cmd
pip install -r requirements.txt
```

Якщо це все ще не працює, переходьте на рішення 2.

## Рішення 2: Встановити за окремими кроками

```cmd
# Спочатку installуємо базові пакети
pip install --upgrade pip
pip install setuptools wheel

# Потім numpy окремо
pip install numpy

# Потім інші пакети
pip install opencv-python
pip install Pillow
pip install colorama
pip install tqdm
pip install pydub
```

## Рішення 3: Використати pre-built wheels

Якщо ви знаєте вашу версію Python, можна скачати pre-built wheels для NumPy:

1. Перейти на https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
2. Скачати файл для вашої версії Python (наприклад, `numpy-1.26.0-cp311-cp311-win_amd64.whl` для Python 3.11)
3. Встановити:
   ```cmd
   pip install C:\path\to\numpy-1.26.0-cp311-cp311-win_amd64.whl
   pip install -r requirements.txt
   ```

## Рішення 4: Використати Anaconda (Найпростіше)

Якщо у вас встановлена Anaconda:

```cmd
# Створити conda environment
conda create -n video-ascii python=3.11
conda activate video-ascii

# Встановити всі пакети через conda
conda install opencv numpy pillow colorama tqdm
pip install pydub

# Клонувати репозиторій
git clone https://github.com/MrWildefox/video-to-ascii-art.git
cd video-to-ascii-art

# Запустити
python main.py -f badapple.mp4 -w 100 --audio
```

## FFmpeg для Windows

Для звукового функціоналу потрібен FFmpeg.

### Метод 1: Chocolatey (Найпростіше, якщо встановлено)

```cmd
choco install ffmpeg
```

### Метод 2: Ручне встановлення

1. Завантажити з https://ffmpeg.org/download.html
2. Розпакувати у папку (наприклад `C:\ffmpeg`)
3. Додати до PATH:
   - Натиснути `Win + X` → Search: "Environment Variables"
   - Клікнути "Edit the system environment variables"
   - Нажати "Environment Variables..."
   - Під "System variables" натиснути "New"
   - Variable name: `Path`
   - Variable value: `C:\ffmpeg\bin` (або де ви розпакували)
   - Нажати OK

### Метод 3: Winget

```cmd
winget install FFmpeg
```

### Перевірити встановлення

```cmd
ffmpeg -version
```

Має показати версію FFmpeg.

## Повна послідовність встановлення на Windows

```cmd
# 1. Клонувати репозиторій
git clone https://github.com/MrWildefox/video-to-ascii-art.git
cd video-to-ascii-art

# 2. Створити virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Оновити pip
python -m pip install --upgrade pip setuptools wheel

# 4. Встановити залежності
pip install -r requirements.txt

# 5. Встановити FFmpeg (якщо нема)
choco install ffmpeg
# або завантажити звідси: https://ffmpeg.org/download.html

# 6. Перевірити установку
ffmpeg -version
python main.py --help

# 7. Запустити!
python main.py -f badapple.mp4 -w 100 --audio
```

## Помилки й рішення

### Помилка: "python: command not found"

Використовувати `python` замість `py` або додати Python до PATH.

```cmd
# Спробуйте
python --version
# Або
py --version
```

### Помилка: "pip: command not found"

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Помилка: "OpenCV not found"

```cmd
pip install --upgrade opencv-python
```

### Помилка: "FFmpeg not found" (для звуку)

Установіть FFmpeg одним з методів вище.

### Помилка: "Bad encoding" або символи виглядають неправильно

Використовувати **Windows Terminal** замість Command Prompt:

1. Завантажити Windows Terminal з Microsoft Store
2. Відкрити Windows Terminal
3. Натиснути на стрілку вниз
4. Вибрати PowerShell або Command Prompt
5. Перейти в папку проекту
6. Запустити скрипт

### Помилка: "Cannot find module pydub"

```cmd
pip install pydub
```

### Помилка: "Color not working"

Переконайтесь, що використовуєте **Windows Terminal**, а не Command Prompt:

```cmd
# Windows Terminal підтримує ANSI кольори
python main.py -f video.mp4 -w 100 --color
```

## Рекомендовані параметри для Windows

```cmd
# Базовий запуск
python main.py -f video.mp4

# Зі звуком
python main.py -f video.mp4 --audio

# З кольором в Windows Terminal
python main.py -f video.mp4 --color

# Оптимально для Windows (зменшена ширина)
python main.py -f badapple.mp4 -w 80 --audio

# Максимальна якість (якщо потужний комп)
python main.py -f video.mp4 -w 120 --audio --color
```

## Python версія

Перевірте вашу версію Python:

```cmd
python --version
```

Потрібна версія 3.8 або новіша.

### Якщо встановлена стара версія Python

1. Завантажити Python 3.11 з https://www.python.org/downloads/
2. Встановити (переконайтесь, що позначено "Add Python to PATH")
3. Перезагрузити CMD
4. Перевірити: `python --version`

## Virtual Environment на Windows

### Створити

```cmd
python -m venv venv
```

### Активувати

```cmd
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1

# Якщо помилка про скрипти в PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Деактивувати

```cmd
deactivate
```

## Проблеми з локалізацією

Якщо ви бачите помилки про кодування (наприклад, у імені користувача з кириличними символами):

1. Переконайтесь, що використовуєте Windows Terminal
2. Встановіть кодування UTF-8:
   ```cmd
   chcp 65001
   ```
3. Спробуйте запустити з абсолютного шляху без кириличних символів

## IDE рекомендації

### PyCharm (як у вас)

1. Відкрити проект
2. File → Settings → Project → Python Interpreter
3. Додати interpreter → Add → Existing Environment
4. Вибрати `venv\Scripts\python.exe`
5. OK

### VS Code

1. Встановити Python extension
2. Ctrl+Shift+P → Python: Select Interpreter
3. Вибрати з вашого venv

## Тестування інсталяції

```cmd
# Перевірити Python
python --version

# Перевірити pip
pip --version

# Перевірити пакети
python -c "import cv2; print('OpenCV OK')"
python -c "import numpy; print('NumPy OK')"
python -c "import pydub; print('PyDub OK')"

# Перевірити FFmpeg
ffmpeg -version

# Запустити помічь
python main.py --help
```

Якщо все OK, можна запускати:

```cmd
python main.py -f badapple.mp4 -w 100 --audio
```

## Контакти для допомоги

Якщо проблеми персистють, відкрийте Issue на GitHub:
https://github.com/MrWildefox/video-to-ascii-art/issues

Наведіть:
- Вашу версію Python
- Вашу версію Windows
- Повну помилку
- Результат `pip list`

Удачі! 🎬✨
