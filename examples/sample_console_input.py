# -*- coding: utf-8 -*-
from traceback import format_exc

from exonutils.console import ConsoleInput as Input


def repr(res):
    if res is None:
        return '<none>'
    return res if res else '<empty>'

try:
    res = Input.get("Enter your first name", required=True)
    print("  * First name: %s" % repr(res))

    res = Input.get("Enter your last name", default='', required=False)
    print("  * Last name: %s" % repr(res))

    res = Input.get(
        "Enter your email", regex='^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.-]+$')
    print("  * Email: %s" % repr(res))

    res = Input.passwd("Enter Primary Password", required=True)
    Input.confirm_passwd("Confirm Password", res)
    print("  * Primary Password: %s" % repr(res))

    res = Input.passwd("Enter Secondary Password (optional)")
    if res:
        Input.confirm_passwd("Confirm Secondary Password", res)
    print("  * Secondary Password: %s" % repr(res))

    res = Input.number(
        "Choose PIN number (0-9999)", required=True, vmin=0, vmax=9999)
    print("  * PIN: %s" % repr(res))

    res = Input.number(
        "Choose limit (min:-10, max:10)", default=0, vmin=-10, vmax=10)
    print("  * limit: %s" % repr(res))

    res = Input.decimal(
        "Enter grade percent", required=True, vmin=0, vmax=100)
    print("  * Grade: %s%%" % repr(res))

    res = Input.select(
        "Select Color", ['red', 'blue', 'green'], default='red')
    print("  * Color: %s" % repr(res))

    res = Input.yesno("Do you need updates", required=True)
    print("  * Updates: %s" % ('Enabled' if res else "Disabled"))

except ValueError as e:
    print("Error: %s" % str(e).strip())
except Exception:
    print(format_exc().strip())
except KeyboardInterrupt:
    print("\n-- terminated --")
