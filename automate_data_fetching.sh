#!/usr/bin/sh

# -------------------------------------------------------
# 
# File: automate_data_fetching.sh
#
# Description: Automate Data fetching with a
# cron-job that fetches NPPES data every month
# and grabs the specific csv files.
#
# Developer: Randy Brown
# Developer Email: randybrown9812@gmail.com
# 
# Version 1.0
# Initialed Bash Script for this
#
# -------------------------------------------------------

MONTH=$(date +%B)
YEAR=$(date +%Y)

DATA_LINK="https://download.cms.gov/nppes/NPPES_Data_Dissemination_${MONTH}_${YEAR}_V2.zip"
DEST_ZIP="NPPES_Data_Dissemination_${MONTH}_${YEAR}_V2.zip"
DEST_FILE="npidata_pfile_20[0-9][0-9][0-9][0-9][0-9][0-9]-20[0-9][0-9][0-9][0-9][0-9][0-9].csv"
cd Original_data || exit

curl -o "$DEST_ZIP" "$DATA_LINK"

unzip "$DEST_ZIP" "$DEST_FILE"

rm "$DEST_ZIP"