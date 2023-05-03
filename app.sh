#!/bin/bash

set -euo pipefail

export LIMIT_GIB=1024 # 1TB is default non-billed limit on DigitalOcean
export INTERFACE=eth0
export TOKEN=5991497887:AAFXAUCGrhogt_ueavcgtq6GXN_Ftwu_KdM
export TG_CHAT_ID=-1001707197017

set -x

cd tg-vnstat-monitor-bot
# git pull # auto-update repo

python3.8 main.py
