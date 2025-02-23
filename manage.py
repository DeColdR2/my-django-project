#!/usr/bin/env python
import os
import sys

def main():
    """Основна функція запуску Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_django_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не вдалося імпортувати Django. Переконайтеся, що Django встановлено "
            "і що віртуальне середовище активовано."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
