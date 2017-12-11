#!/bin/bash


target="/home/linaro/jobs"

rm -rf $target

mkdir $target

home="/media/linaro/MACVOLUME/working/*"

cp -rf $home $target

echo "Working Directory Updated..."