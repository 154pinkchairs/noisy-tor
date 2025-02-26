#!/bin/sh
while getopts "c:q:" opt; do
    case $opt in
        c)
            sed -i 's/\"user_agents\": \[.*\]/\"user_agents\": \[\]/g' config.json
            ;;
        q)
            sed -i 's/^Mozilla/\"Mozilla/g' "$2"
            sed -i 's/[0-9]\"$/&\"/g' "$2"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done

