#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
    load_dotenv()

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError("Couldn't import Django") from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
