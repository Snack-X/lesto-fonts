#!/usr/bin/env bash

VERSION="1.00"

# Build Lesto
LESTO_FAMILY_SANS=(Thin Light DemiLight Regular Medium Bold Black)
LESTO_FAMILY_SERIF=(ExtraLight Light Regular Medium SemiBold Bold Black)

for WEIGHT in "${LESTO_FAMILY_SANS[@]}"
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

for WEIGHT in "${LESTO_FAMILY_SERIF[@]}"
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

# Build D2Coding
for EXT in ttf woff woff2
do
  python3 build.py "otf/D2Coding.ttf" "d2coding-light.cfg" \
  "gen/D2CodingLightKR-Regular.$EXT" --subfamily="Regular" --version="$VERSION"
  python3 build.py "otf/D2CodingBold.ttf" "d2coding-light.cfg" \
  "gen/D2CodingLightKR-Bold.$EXT" --subfamily="Bold" --version="$VERSION"
done