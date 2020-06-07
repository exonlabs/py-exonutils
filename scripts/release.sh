#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PKG=$(grep 'pkg_name =' setup.py |cut -d"'" -f2)

# check clean repo
git diff --quiet || { echo -e "\nError!\nuncommitted changes in repo\n"; exit 1; }

build_pkgs () {
    . ../venv3/bin/activate
    python setup.py sdist bdist_wheel clean --all
    deactivate
    . ../venv2/bin/activate
    python setup.py sdist bdist_wheel clean --all
    deactivate
}

REL=$1
[ "$REL" ] || { echo -e "\nError!\nenter release number\n"; exit 1; }
if $(git tag |grep -q "$REL") ;then
    echo -e "\n-- Generating: $PKG $REL"
    (set -x
        git checkout $REL
        build_pkgs
    )
else
    echo -e "\n-- New Release: $PKG $REL"
    (set -x
        git checkout master
        sed -i "s/^__version__.*/__version__ = \"$REL\"/g" $PKG/__init__.py
        git commit -am "Release version '$REL'"
        git tag $REL
        build_pkgs
        NREL=$(echo "$REL" |awk -F. '{for(i=1;i<NF;i++){printf $i"."}{printf $NF+1".dev0"}}')
        sed -i "s/^__version__.*/__version__ = \"${NREL}\"/g" $PKG/__init__.py
    )
fi

# back to master branch
(set -x
    git checkout master
    . ../venv3/bin/activate
    pip install -e ./
    deactivate
)

echo -e "\n-- Done\n"
