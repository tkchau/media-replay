for dest in $(< /home/beowulf/list.txt); do
    scp -P 5242 /home/beowulf/autostart.sh   beowulf@$dest:~  
done

