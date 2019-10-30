awk '/avg/' ./log.txt | awk '{print $3}' > avg.txt
awk '/avg/' ./log.txt | awk -F ":" '{print $1}' > epochs.txt
paste -d " " epochs.txt avg.txt > epochavg.txt
rm epochs.txt avg.txt
