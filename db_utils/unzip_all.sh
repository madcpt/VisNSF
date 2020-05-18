#! /bin/bash
save_path=$1
file_list=$(ls "$save_path")
for file in $file_list
do
 unzip "$save_path/$file" -d "$save_path/${file:0:4}/"
# echo "$save_path/${file:0:(4)}/"
done