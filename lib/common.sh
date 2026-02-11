#!/bin/bash
# lib/common.sh — Shared logging and utility functions
# All scripts source this file for consistent logging, error handling, and validation.
# Usage: source "$(dirname "${BASH_SOURCE[0]}")/../lib/common.sh"
# NOTE: This is a library file — sourcing scripts should set their own shell options.
# Recommended: set -euo pipefail in the sourcing script.

# === Colors (disabled if not a terminal) ===
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# === Logging ===

# Internal: write to log file
# Appends to $LOG_DIR/pipeline-YYYYMMDD.log
_log_to_file() {
    local level="$1"
    local message="$2"
    local log_dir="${LOG_DIR:-.}"
    local logfile="$log_dir/pipeline-$(date +%Y%m%d).log"

    mkdir -p "$log_dir"
    echo "$(date -Iseconds) [$level] $message" >> "$logfile"
}

log_info() {
    local message="$1"
    local timestamp
    timestamp="$(date -Iseconds)"
    echo -e "${GREEN}${timestamp} [INFO] ${message}${NC}"
    _log_to_file "INFO" "$message"
}

log_warn() {
    local message="$1"
    local timestamp
    timestamp="$(date -Iseconds)"
    echo -e "${YELLOW}${timestamp} [WARN] ${message}${NC}" >&2
    _log_to_file "WARN" "$message"
}

log_error() {
    local message="$1"
    local timestamp
    timestamp="$(date -Iseconds)"
    echo -e "${RED}${timestamp} [ERROR] ${message}${NC}" >&2
    _log_to_file "ERROR" "$message"
}

log_debug() {
    local message="$1"
    if [[ -z "${DEBUG:-}" ]]; then
        return 0
    fi
    local timestamp
    timestamp="$(date -Iseconds)"
    echo -e "${BLUE}${timestamp} [DEBUG] ${message}${NC}"
    _log_to_file "DEBUG" "$message"
}

# === Error handling ===

# Fatal error: log and exit
# Arguments:
#   $1 - error message
#   $2 - exit code (default: 1)
die() {
    local message="$1"
    local exit_code="${2:-1}"
    log_error "FATAL: $message"
    exit "$exit_code"
}

# === Dependency checking ===

# Verify a command is available
# Arguments:
#   $1 - command name
# Returns:
#   0 if found, 1 if missing
require_command() {
    local cmd="$1"
    if ! command -v "$cmd" >/dev/null 2>&1; then
        log_error "Required command not found: $cmd"
        return 1
    fi
    return 0
}
