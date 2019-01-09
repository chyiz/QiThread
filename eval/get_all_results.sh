find $1 -name stats.txt -exec cat {} \;| awk '!a[$0]++'
