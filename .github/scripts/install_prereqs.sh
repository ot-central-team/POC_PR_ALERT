#!/bin/bash
set -e

echo "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
else
    echo "Python 3 is already installed."
fi

echo "Checking for GitHub CLI (gh)..."
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI not found. Installing..."
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y gh
else
    echo "GitHub CLI is already installed."
fi

echo "Prerequisites check complete."
