#!/bin/bash

LOG_FILE="/var/log/apache2/access.log"
BACKUP_DIR="/var/log/apache2/log_backup"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

mkdir -p "$BACKUP_DIR"
#copy the log to file with date
cp "$LOG_FILE" "$BACKUP_DIR/access.log.$TIMESTAMP"
#cleaning the original file
> "$LOG_FILE"

chown www-data:adm "$LOG_FILE"
