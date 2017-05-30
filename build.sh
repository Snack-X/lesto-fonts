#!/usr/bin/env bash

VERSION="1.00"

FAMILY_SANS=(Thin Light DemiLight Regular Medium Bold Black)
FAMILY_SERIF=(ExtraLight Light Regular Medium SemiBold Bold Black)

for WEIGHT in "${FAMILY_SANS[@]}"
do
  for EXT in ttf woff woff2
  do
    python3 build.py \
      "otf/NotoSansCJKkr-$WEIGHT.otf" \
      "lesto-kr.cfg" \
      "gen/LestoSansKR-$WEIGHT.$EXT" \
      --type="Sans" --subfamily="$WEIGHT" --version="$VERSION"
  done
done

for WEIGHT in "${FAMILY_SERIF[@]}"
do
  for EXT in ttf woff woff2
  do
    python3 build.py \
      "otf/NotoSerifCJKkr-$WEIGHT.otf" \
      "lesto-kr.cfg" \
      "gen/LestoSerifKR-$WEIGHT.$EXT" \
      --type="Sans" --subfamily="$WEIGHT" --version="$VERSION"
  done
done
