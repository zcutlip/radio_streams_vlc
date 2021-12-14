#!/bin/sh -x -e

quit(){
    if [ $# -gt 1 ];
    then
        echo "$1"
        shift
    fi
    exit $1
}

if [ -f "$DOTFILES"/virtualenvwrapper/virtualenvwrapper.rc ];
then
    . "$DOTFILES"/virtualenvwrapper/virtualenvwrapper.rc
fi
mkvirtualenv -r ./dev-reqs.txt "chill_streams" || quit "Unable to make virtual environment." 1
