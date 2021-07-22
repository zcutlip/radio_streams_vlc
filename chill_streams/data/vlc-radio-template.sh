#!/bin/sh

PIDDIR="$HOME/.local/var/"
PIDFILE="$PIDDIR/vlc-radio.pid"
SELFPID=$$

# these get overridden later
_VLC_RADIO_PATH=""
_CHILL_STREAMS_VERSION=""


echo_sleep(){
    if [ $# -ne 2 ];
    then
        return 1
    fi
    echo "$1"
    if [ "$DEBUG" == "1" ];
    then
        sleep $2
    fi
    return 0

}


write_pid(){
    mkdir -p "$PIDDIR"
    if [ -f "$PIDFILE" ];
    then
        sleep 2
    fi
    echo $$ >"$PIDFILE"
}

read_pid(){
    _pid=""
    if [ -f "$PIDFILE" ];
    then
        read -r _pid <"$PIDFILE"
    fi
    printf "%s" "$_pid"
}

kill_old(){
    if [ -f "$PIDFILE" ];
    then

        oldpid="$(read_pid)"
        if [ -z "$oldpid" ];
        then
            return 1
        fi
        if ps -p "$oldpid";
        then
            reverse_kill "$oldpid" || return $?
        else
            return 0
        fi
        # _pid=""
    fi
}

reverse_kill(){
    pid="$1"
    ps -g $pid -o pid= | sort -r | while read p;
    do
        if [ $p != $SELFPID ];
        then
            # for some reason, unless we explicitly specify -INT
            # chld processes don't go down
            kill -INT $p
        fi
    done
}

cleanup(){
    trap - TERM INT EXIT
    if [ "$(read_pid)" = $$ ];
    then
        rm "$PIDFILE"
    fi
    # always succeed
    return 0
}

cleanup_and_self_terminate(){
    cleanup
    ps -g $$
    reverse_kill $SELFPID
    reset
}

update_script(){
    _ret=1
    echo_sleep "Checking if script needs updating" 1
    if [ "$_CHILL_STREAMS_VERSION" != "$($_VLC_RADIO_PATH --bare-version)" ];
    then
        echo "Updating bootstrap script"
        "$_VLC_RADIO_PATH" --write-shell-script
        _ret=$?
        echo_sleep "Done" 1
        return $_ret
    fi
    echo "Bootstrap script does not need updating"
    return $_ret

}

kill_old || exit $?
write_pid || exit $?

# Trapping TERM causes us to never exit for some reason
# trap cleanup_and_self_terminate TERM
trap cleanup_and_self_terminate INT
trap cleanup_and_self_terminate EXIT
