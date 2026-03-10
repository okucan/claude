#!/bin/bash
# SSH Remote Connection Script
# Connects to the remote Ubuntu server using the PEM key

set -euo pipefail

KEY_FILE="${SSH_KEY_FILE:-myopenclaw.pem}"
REMOTE_USER="${REMOTE_USER:-ubuntu}"
REMOTE_HOST="${REMOTE_HOST:-23.23.211.5}"

usage() {
    echo "Usage: $0 [OPTIONS] [COMMAND]"
    echo ""
    echo "Options:"
    echo "  -i KEY_FILE    Path to PEM key file (default: $KEY_FILE)"
    echo "  -u USER        Remote user (default: $REMOTE_USER)"
    echo "  -h HOST        Remote host (default: $REMOTE_HOST)"
    echo "  --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                          # Interactive shell"
    echo "  $0 'ls -la /home/ubuntu'    # Run single command"
    echo "  $0 -i /path/to/key.pem      # Use specific key file"
    echo ""
    echo "Environment variables:"
    echo "  SSH_KEY_FILE   Path to PEM key (overrides default)"
    echo "  REMOTE_USER    Remote username (overrides default)"
    echo "  REMOTE_HOST    Remote host/IP (overrides default)"
}

# Parse arguments
COMMAND=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        -i) KEY_FILE="$2"; shift 2 ;;
        -u) REMOTE_USER="$2"; shift 2 ;;
        -h) REMOTE_HOST="$2"; shift 2 ;;
        --help) usage; exit 0 ;;
        *) COMMAND="$*"; break ;;
    esac
done

# Validate key file exists
if [[ ! -f "$KEY_FILE" ]]; then
    echo "Error: Key file '$KEY_FILE' not found." >&2
    echo "Set SSH_KEY_FILE env var or use -i flag to specify the key path." >&2
    exit 1
fi

# Ensure correct permissions on key file
chmod 600 "$KEY_FILE"

echo "Connecting to $REMOTE_USER@$REMOTE_HOST..."

if [[ -n "$COMMAND" ]]; then
    ssh -i "$KEY_FILE" \
        -o StrictHostKeyChecking=accept-new \
        -o ConnectTimeout=10 \
        "$REMOTE_USER@$REMOTE_HOST" \
        "$COMMAND"
else
    ssh -i "$KEY_FILE" \
        -o StrictHostKeyChecking=accept-new \
        -o ConnectTimeout=10 \
        "$REMOTE_USER@$REMOTE_HOST"
fi
