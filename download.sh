#!/usr/bin/env bash

# Download Noto Sans CJK KR
wget -P otf --no-check-certificate "https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKkr-hinted.zip"
unzip otf/NotoSansCJKkr-hinted.zip -d otf -x LICENSE_OFL.txt README

# Download Noto Serif CJK KR
wget -P otf --no-check-certificate "https://noto-website.storage.googleapis.com/pkgs/NotoSerifCJKkr-hinted.zip"
unzip otf/NotoSerifCJKkr-hinted.zip -d otf -x LICENSE_OFL.txt README

# Download D2Coding
wget -P otf --no-check-certificate "https://github.com/naver/d2codingfont/releases/download/VER1.21/D2Coding-1.2.zip"
unzip otf/D2Coding-1.2.zip -d otf
rm -r otf/__MACOSX

# Download Unicode data
wget -P data http://unicode.org/Public/UNIDATA/Blocks.txt
wget -P data http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/KSC/KSX1001.TXT