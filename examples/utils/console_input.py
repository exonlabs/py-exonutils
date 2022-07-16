# -*- coding: utf-8 -*-
from exonutils.utils.console import Console


def repr(res):
    if res is None:
        return '<none>'
    return res if res else '<empty>'


def main():
    ch = Console()

    res = ch.get_value("Enter your first name", required=True)
    print("  * First name: %s" % repr(res))

    res = ch.get_value("Enter your last name", default='', required=False)
    print("  * Last name: %s" % repr(res))

    res = ch.get_value(
        "Enter your email", regex='^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.-]+$')
    print("  * Email: %s" % repr(res))

    res = ch.get_password("Enter Primary Password", required=True)
    ch.confirm_password("Confirm Password", res)
    print("  * Primary Password: %s" % repr(res))

    res = ch.get_password("Enter Secondary Password (optional)")
    if res:
        ch.confirm_password("Confirm Secondary Password", res)
    print("  * Secondary Password: %s" % repr(res))

    res = ch.get_number(
        "Choose PIN number (0-9999)", required=True, vmin=0, vmax=9999)
    print("  * PIN: %s" % repr(res))

    res = ch.get_number(
        "Choose limit (min:-10, max:10)", default=0, vmin=-10, vmax=10)
    print("  * limit: %s" % repr(res))

    res = ch.get_decimal(
        "Enter grade percent", required=True, vmin=0, vmax=100)
    print("  * Grade: %s%%" % repr(res))

    res = ch.select_value(
        "Select Color", ['red', 'blue', 'green'], default='red')
    print("  * Color: %s" % repr(res))

    res = ch.select_yesno("Do you need updates", required=True)
    print("  * Updates: %s" % ('Enabled' if res else "Disabled"))


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("\n-- terminated --")
