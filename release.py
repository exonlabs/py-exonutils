# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
import re
from subprocess import Popen, PIPE
from traceback import format_exc


def is_repo_clean():
    return Popen(['git', 'diff', '--quiet']).wait() == 0


def get_repo_tags():
    res = Popen(['git', 'tag'], stdout=PIPE).communicate()[0]
    return [l.decode() for l in res.splitlines()]


def set_repo_tag(tag):
    Popen(['git', 'tag', tag]).wait()


def do_repo_checkout(tag=None):
    Popen(['git', 'checkout', tag if tag else '-']).wait()


def do_repo_commit(message, *args):
    message = message % args
    Popen(['git', 'commit', '-am', message]).wait()


def get_version():
    fpath = os.path.join('setup.py')
    if not os.path.isfile(fpath):
        raise RuntimeError("No package setup file '%s'" % fpath)

    with open(fpath, 'r') as f:
        for line in iter(f):
            match = re.search(r"__VERSION__ = '(.*?)'", line.strip())
            if match:
                ver = match.group(1)
                return ver[:-4] if ver.endswith('.dev') else ver


def set_version(version):
    fpath = os.path.join('setup.py')
    if not os.path.isfile(fpath):
        raise RuntimeError("No package setup file '%s'" % fpath)

    with open(fpath, 'r') as f:
        lines = f.readlines()

    chk = False
    contents = []
    for l in lines:
        match = re.search(r"__VERSION__ = '(.*?)'", l)
        if match:
            contents.append("__VERSION__ = '%s'\n" % version)
            chk = True
        else:
            contents.append(l)

    if not chk:
        raise RuntimeError(
            "could not find '__VERSION__' pattern in %s" % fpath)

    with open(fpath, 'w') as f:
        f.writelines(contents)


def bump_version(version):
    parts = [int(i) for i in version.split('.')]
    if len(parts) >= 3:
        parts[-1] += 1
    elif len(parts) >= 2:
        parts.append(1)
    else:
        parts.extend([0, 1])
    return '.'.join(map(str, parts))


def create_packages():
    Popen(['make', 'build']).wait()


def setup_dev_package():
    Popen(['make', 'setup-dev']).wait()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if not is_repo_clean():
        raise RuntimeError("uncommitted changes detected")

    if len(sys.argv) >= 2:
        version = sys.argv[1].strip()

        print("\n-- Releasing: v%s --\n" % version)

        if version not in get_repo_tags():
            raise RuntimeError("tag '%s' does not exists" % version)

        do_repo_checkout(tag=version)

        create_packages()

        do_repo_checkout(tag=None)

    else:
        version = get_version()
        if not version:
            raise RuntimeError("could not detect version")

        print("\n-- Releasing: v%s --\n" % version)

        if version in get_repo_tags():
            raise RuntimeError("tag '%s' already exists" % version)

        set_version(version)
        do_repo_commit("Release version '%s'", version)
        set_repo_tag(version)

        create_packages()

        next_version = bump_version(version)
        set_version('%s.dev' % next_version)
        do_repo_commit("Bump version to '%s'", next_version)

    setup_dev_package()


if __name__ == '__main__':
    try:
        main()
        print("\n-- Done --\n")
    except RuntimeError as e:
        print('Error: %s' % str(e).strip())
    except Exception:
        print(format_exc().strip())
    except KeyboardInterrupt:
        print("\n-- terminated --")
