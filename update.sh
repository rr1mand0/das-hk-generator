#!/bin/bash
for i in 50 100 150 200 250 300;
do 
  python3 gen.py --account 25000 -o /Volumes/\[C\]\ Windows\ 11/DAS\ Trader\ Pro/hotkey-$i.htk $i
done
