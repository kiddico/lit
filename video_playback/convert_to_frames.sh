name=$(echo "$1" | awk -F"." '{print $1}')
mkdir "$name" >> /dev/null
ffmpeg -i "$1" -s 640x360 -r 24/1 "$name\\""$name""_f%03d.png"
