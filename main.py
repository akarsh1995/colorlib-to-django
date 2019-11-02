import sys

from colorlib_to_django import ColorLib

if __name__ == '__main__':
    args = sys.argv
    c = ColorLib(args[1])
    c.get_django_ready_template()
