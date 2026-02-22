#!/usr/bin/env bash

declare -A dirs

br="book"
dirs["ch01-boing"]="${br}/boing-master"

for key in ${!dirs[@]}; do
    src=${dirs[${key}]}
    target=${key}
    cp -av ${src}/{images,music,sounds} ${target}/
done
