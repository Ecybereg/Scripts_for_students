#!/bin/bash

#© Copyright Erel Regev
#This script extract the NTLM challenge from a PCAP file for further cracking.

HOME=$(pwd)
pcap=$1

NTLMCRACK() {
    n=100

    mkdir -p $HOME/NTLM/hash
    cd $HOME/NTLM/hash

    tshark -r $HOME/$pcap -2 -R 'ntlmssp' -T fields -e ntlmssp.ntlmserverchallenge -e tcp.ack_raw \
    | awk NF | awk '{print $1"#"$2}' | awk -F'#' '{print $1"::"$2}' | awk 'length >= 16' \
    > "a.lst"

    if [ -s "a.lst" ]; then
        for i in $(cat "a.lst"); do
            s=$(echo "$i" | awk -F:: '{print $2}')
            c=$(echo "$i" | awk -F:: '{print $1}')
            
            tshark -r $HOME/$pcap -2 -R "ntlmssp" -Y "tcp.seq_raw == $s" -T fields \
            -e ntlmssp.auth.username -e ntlmssp.auth.domain -e ntlmssp.ntlmv2_response.ntproofstr \
            -e ntlmssp.ntlmv2_response \
            | awk NF | awk '{print $1"#"$2"#"$3"#"$4"#"$5"#"$6}' | awk -F'#' '{print $1"::"$2":L:"$3":"$4":"$5":"$6}' \
            > "b$n.lst"

            cat "b$n.lst" | sed 's/:L:/:'$c':/g' > "c$n.lst"
            r=$(cat "c$n.lst" | awk -F: '{print $5}')
            cat "c$n.lst" | sed -e 's/'$r'/L:/g' | sed 's/:L::L:/:L:/g' > "d$n.lst"
            cat "d$n.lst" | sed 's/:L:/:'$r':/g' > "e$n.lst"
            cat "e$n.lst" | rev | cut -c3- | rev > "crackme_$n.log"
            ((n++))
        done

        rm *.lst
        for fcr in $(ls $HOME/NTLM/hash/crackme*.log); do
            if [ -s "$fcr" ]; then
                cat "$fcr"
            else
                echo "An error occurred while collecting the information."
            fi
        done
    fi
}

NTLMCRACK
