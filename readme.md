Версия python - 3.9, необходимо устанавливать отдельно
Для быстрой смены версии можно использовать [pyenv](https://github.com/pyenv-win/pyenv-win/tree/master)

## Установка виртуального окружения
```
python -m venv venv
```
## Активация виртуального оуркжения
```
source venv/bin/activate  # linux
```
```
venv\Scripts\activate  # windows
```
## Установка зависимостей
ОБЯЗАТЕЛЬНО апдейт pip:
```
python -m pip install --upgrade pip
```
Установка:
```
pip install -r .\requirements.txt
```

## Запуск программы
```
python main.py
```