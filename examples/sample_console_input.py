# -*- coding: utf-8 -*-
from traceback import format_exc

from exonutils.console import ConsoleInput as Input


try:
    res = Input.get("Enter your fullname")
    print("  * Fullname: %s" % res)

    res = Input.get(
        "Enter your email", regex='^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.-]+$')
    print("  * Email: %s" % res)

    res = Input.get("Enter Password", hidden=True)
    Input.confirm("Confirm Password", res, hidden=True)
    print("  * Password: %s" % res)

    res = Input.number(
        "Choose PIN number (max 5 digits)", default='', vmin=0, vmax=99999)
    print(("  * PIN: %s" % res) if res else "  * No PIN set")

    res = Input.decimal(
        "Enter grade percent", vmin=0, vmax=100)
    Input.confirm("Confirm grade", res)
    print("  * Grade: %s%%" % res)

    res = Input.select("Select Color", ['red', 'blue', 'green'])
    print("  * Color: %s" % res)

    res = Input.yesno("Do you need updates", default='y')
    print("  * Updates: %s" % ('Enabled' if res else "Disabled"))

except ValueError as e:
    print("Error: %s" % str(e).strip())
except Exception:
    print(format_exc().strip())
except KeyboardInterrupt:
    print("\n-- terminated --")
