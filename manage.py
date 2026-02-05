#!/usr/bin/env python
"""
manage.py - Management script for Viaduct.

This module provides the main() entry point used to run administrative
commands via Django's management utility.
"""

import os
import sys

def main():
	"""
    Run administrative tasks.

    :rtype: None

    Example::

        # Run Django management commands from the command line
        $ ./manage.py runserver
    """
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viaduct.settings')
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
