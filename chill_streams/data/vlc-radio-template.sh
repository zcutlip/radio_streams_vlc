#!/bin/sh

PIDDIR="$HOME/.local/var/"
PIDFILE="$PIDDIR/vlc-radio.pid"
SELFPID=$$

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

rm_pidfile(){
    # https://stackoverflow.com/questions/360201/how-do-i-kill-background-processes-jobs-when-my-shell-script-exits/2173421#2173421
    trap - TERM INT EXIT
    if [ "$(read_pid)" = $$ ];
    then
        rm "$PIDFILE"
    fi
    ps -g $$
    reverse_kill $SELFPID
    reset
}

kill_old || exit $?
write_pid || exit $?

# Trapping TERM causes us to never exit for some reason
# trap rm_pidfile TERM
trap rm_pidfile INT
trap rm_pidfile EXIT
