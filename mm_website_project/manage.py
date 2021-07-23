#!/home/lblk/Documents/dev/python/mm_website/venv/bin/python3.8

#  changes between production and dev repos to make :
#  - virtual env path
#  - activate prod or dev data base
#  - activate/deactivate admin tool bar (middleware, installed apps, debug=true/false
#  - activate/deactivate local/remote host (allowed hosts)
#  - activate/deactivate STATIC_ROOT in settings.py ? Change "asset" url to "static" as it was before ?

# test 16h39 25.06.21, added after I edited gitignore with manage.py and removed it from
# git index (git rm --cached [file])

"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm_website_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
