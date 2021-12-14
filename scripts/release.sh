#!/bin/sh -x
DIRNAME="$(dirname $0)"

# set DISTRIBUTION_NAME variable
SRC_DISTRIBUTION_NAME="$(python3 setup.py --name)"
BDIST_NAME="$(echo $SRC_DISTRIBUTION_NAME | tr '\- ' _)"

# utility functions
source "$DIRNAME"/functions.sh

if ! branch_is_master_or_main;
then
    quit "Checkout branch 'master' before generating release." 1
fi

if ! branch_is_clean;
then
    echo "Tree contains uncommitted modifications:"
    git ls-files -m
    quit 1
fi
version=$(current_version);

if ! version_is_tagged "$version";
then
    echo "Current version $version isn't tagged."
    echo "Attempting to tag..."
    "$DIRNAME"/tag.sh || quit "Failed to tag a release." 1
fi

generate_dist(){
    python3 setup.py sdist bdist_wheel || quit "Failed to generate source & binary distributions." 1
}

version=$(current_version);

generate_dist;
echo "About to post the following distribution files to pypi.org."
ls -1 dist/"$SRC_DISTRIBUTION_NAME"-$version.* dist/"$BDIST_NAME"-$version*

if prompt_yes_no;
then
    python3 -m twine upload dist/"$SRC_DISTRIBUTION_NAME"-$version.* dist/"$BDIST_NAME"-$version*
fi

