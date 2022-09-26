# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from exonutils.utils.shell import Shell


def main():
    tmp_path = os.path.join(gettempdir(), 'foobar')

    print("\nCreating test dir under tmp")
    code, out, err = Shell.run('mkdir -p -m 775 %s' % tmp_path)
    if code != 0:
        print("failed:", code, out, err, "\n")
        return
    print("success")

    test_file = os.path.join(tmp_path, 'file1.txt')

    print("\nCreating test file")
    code, out, err = Shell.run([
        'echo "Some test data" > %s' % test_file,
        'ls -l %s/' % tmp_path,
    ])
    if code != 0:
        print("failed:", code, out, err, "\n")
        return
    print(out)

    print("\nRead test file")
    code, out, err = Shell.run('cat %s' % test_file)
    if code != 0:
        print("failed:", code, out, err, "\n")
        return
    print('-----')
    print(out)
    print('-----')

    print("\nClean up")
    code, out, err = Shell.run('rm -rf %s' % tmp_path)
    if code != 0:
        print("failed:", code, out, err, "\n")
        return
    print("success")

    print()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("\n-- terminated --")
