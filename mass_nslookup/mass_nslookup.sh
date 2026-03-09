#!/bin/bash

# Colors
YELLOW="\e[33m"
CYAN="\e[36m"
GREEN="\e[32m"
RED="\e[31m"
RESET="\e[0m"

domains=()

# Prompt user (yellow)
echo -e "${YELLOW}Insert domains (one per line).${RESET}"
echo -e "${YELLOW}Press Ctrl+D when finished.${RESET}"
echo

# Read domains until Ctrl+D
while read -r domain
do
    [ -z "$domain" ] && continue
    domains+=("$domain")
done < /dev/tty

# Table header
echo ""
printf "+%-26s-+-%-16s+\n" "--------------------------" "----------------"
printf "| ${YELLOW}%-25s${RESET} | ${YELLOW}%-15s${RESET} |\n" "DOMAIN" "IP"
printf "+%-26s-+-%-16s+\n" "--------------------------" "----------------"

# Resolve and print results
for domain in "${domains[@]}"
do
    ip=$(nslookup "$domain" 2>/dev/null | awk '/^Address: / {print $2}' | tail -n1)

    if [ -z "$ip" ]; then
        ip="-"
        printf "| %-25s | ${RED}%-15s${RESET} |\n" "$domain" "$ip"
    else
        printf "| %-25s | ${GREEN}%-15s${RESET} |\n" "$domain" "$ip"
    fi
done

printf "+%-26s-+-%-16s+\n" "--------------------------" "----------------"