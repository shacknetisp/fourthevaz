#!/bin/bash
#Fourth Evaz Unix Daemon
#Usage: ./unixdaemon.sh <command> [<path to userdata>]
#Commands:
#    start
#    stop
#    restart
#    reinit

if [ $# -lt 1 ]
then
echo "Usage: ./unixdaemon.sh <command> [<path to userdata>]"
exit 1
fi

if [ $# -eq 1 ]
then
path='./userdata'
else
path=$2
fi

pidfile="$2/pid"

function start {
    nohup ./__init__.py "$2" &
    echo "$!" > "$path/pid"
    echo Running with PID $!
}

function stop {
    kill -SIGTERM $(cat "$path/pid")
    echo Stopped PID $(cat "$path/pid")
}

if [ "$1" == "start" ]
then
    start
fi
if [ "$1" == "stop" ]
then
    stop
fi
if [ "$1" == "restart" ]
then
    stop
    start
fi
if [ "$1" == "reinit" ]
then
    kill -SIGHUP $(cat "$path/pid")
    echo Reinited PID $(cat "$path/pid")
fi
