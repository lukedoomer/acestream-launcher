# Acestream Launcher
Acestream Launcher allows you to open Acestream links with a Media Player of your choice
This is a fork of Acestream Launcher which does not start Acestream Engine by itself instead connect to a specified network socket.
This fork also remove desktop notification and its dependency.

## Dependencies
    python, python-psutil, python-pexpect, acestream-engine

## Usage
    acestream-launcher URL [--player PLAYER] [--engine IP:PORT]

## Positional arguments
    URL               The acestream url to play

## Optional arguments
    -h, --help                  Show this help message and exit
    --player PLAYER             The media player to use (default: vlc)
    --engine IP:PORT   The acestream engine executable to use (default: localhost:62062)

## Installation
Arch Linux: [AUR Package](https://aur.archlinux.org/packages/acestream-launcher)
