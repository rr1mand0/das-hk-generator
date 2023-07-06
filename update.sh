#!/bin/bash
for i in 50 100 150 200 250 300 350 400 450 500;
do 
  python3 gen.py --account 25000 -o /Volumes/\[C\]\ Windows\ 11/DAS\ Trader\ Pro/hotkeys/hotkey-$i.htk $i
done

python3 gen.py --account 25000 --future MES -o /Volumes/\[C\]\ Windows\ 11/DAS\ Trader\ Pro/hotkeys/hotkey-MES-125.htk 125
python3 gen.py --account 25000 --future ES -o /Volumes/\[C\]\ Windows\ 11/DAS\ Trader\ Pro/hotkeys/hotkey-ES-250.htk 250

python3 gen.py --account 25000 --future MNQ -o /Volumes/\[C\]\ Windows\ 11/DAS\ Trader\ Pro/hotkeys/hotkey-MNQ-20.htk 20
python3 gen.py --account 25000 --future NQ -o /Volumes/\[C\]\ Windows\ 11/DAS\ Trader\ Pro/hotkeys/hotkey-NQ-200.htk 200