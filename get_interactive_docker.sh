#!/bin/bash

APP_NAME=nscmr
APP_CONFIG_PATH=/app/nscmr/config

function usage()
{
    echo
    echo "Script to get an interactive shell with full access to app"
    echo "Usage:"
    echo "      get_interactive [mode | help]"
    echo "mode -> specify the app's running mode (dev, test or prod)"
    echo "help -> prints this text"
    echo
}

if [[ "$1" ]]; then
    case "$1" in
        dev)
            FILE=development.py
            ;;
        test)
            FILE=testing.py
            ;;
        prod)
            FILE=default.py
            ;;
        *)
            echo
            echo "Wrong usage"
            usage
            exit 1
            ;;
    esac
    APP_CONFIG_FILE="$APP_CONFIG_PATH/$FILE" ipython3 -i "$APP_NAME"/__init__.py
else
    usage
    exit 0
fi

