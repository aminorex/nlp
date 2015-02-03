#/bin/bash
cat $1 | awk '{if(NF==10) {print $2" "$4" "$7-1" " $8 } else {print}}' > $2
