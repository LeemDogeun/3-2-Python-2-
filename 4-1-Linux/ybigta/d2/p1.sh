#!/bin/bash

pip install -r requirements.txt

CHECK_PID=$(pgrep -f check.py)
if [ ! -z "$CHECK_PY_PID" ]; then
    kill -9 $PARENT_PID
fi

SESSION_NAME="dogeun_session"
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    tmux new-session -d -s $SESSION_NAME
fi

tmux send-keys -t $SESSION_NAME "python check.py" C-m

