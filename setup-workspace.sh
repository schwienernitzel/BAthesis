#!/bin/bash

# Set required variables
rm -rf documents/setup.txt
touch documents/setup.txt
LOG="documents/setup.txt"

# Initiate setup process
echo -e "\033[33mSetting up workspace...\033[0m"
echo ""
sleep 1

# Check API-Key
if [ -z "$APIKEY" ]; then
    echo -e "\033[91mERROR: The Google API-Key has not been declared!!!\033[0m" >&2
    exit 1
else
    echo -e "\033[33mGoogle API-Key: Done!\033[0m"
fi

# Install required packages
{
    sudo apt-get install python3 python3-pip
} > $LOG 2>&1

echo -e "\033[33mPackage installation: Done!\033[0m"

# Install required modules
{
sudo pip3 install torch torchvision torchaudio tensorflow transformers numba==0.56.4 bertopic HanTa langid google-api-python-client nltk matplotlib
} > $LOG 2>&1

echo -e "\033[33mModule installation: Done!\033[0m"
echo ""
sleep 1

# Done
echo -e "\033[33mSetup completed: Logfile: '$LOG'\033[0m"
