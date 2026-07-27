#!/bin/bash

if [ "$#" -lt 4 ]; then
    echo "Usage: $0 <session_name> <target_url> <files_wordlist> <dirs_wordlist> [optional_ffuf_flags...]"
    exit 1
fi

SESSION_NAME="$1"
URL="$2"
FILES_WL="$3"
DIRS_WL="$4"
shift 4
EXTRA_ARGS="$*"

tmux new-session -d -s "$SESSION_NAME" "bash -i -c 'ffuf -u \"$URL/FUZZ\" -w \"$FILES_WL\" $EXTRA_ARGS'"
tmux split-window -h -t "$SESSION_NAME" "bash -i -c 'ffuf -u \"$URL/FUZZ\" -w \"$DIRS_WL\" $EXTRA_ARGS'"

echo "Tmux session '$SESSION_NAME' created."
echo "Attach with: tmux attach -t $SESSION_NAME"