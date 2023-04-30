"""
    das-hotkey-generator
    ~~~~~~~~~~~~~~~~~~~~

    If you came across this and have no idea what it is, read the article I
    wrote here: https://forums.bearbulltraders.com/topic/518-position-sizing
    on position sizing, and how I manage my risk.

    INTRO
    =====

    When I change my risk, it can be tedious entering new share values for
    every key. I wrote this generator to solve this problem, and I thought
    I would share it with anyone else that was interested.

    This generator only generates the hotkeys for the alpha keys used to enter
    your positions. If you want my full hotkey file that I use for my keyboard,
    you can download it here: http://bit.ly/das-trader-hotkeys

    If you are interested in the CLI version, it can be found here:
    https://gist.github.com/onosendi/11ae4c274e87425b02eb676928547960

    INSTRUCTIONS
    ============

    Overview of what we will be doing:
        - Backup your current hotkey file
        - Use this generator to generate hotkeys
        - Paste the generated hotkeys into a new hotkey file
        - Load the new hotkey file into DAS Trader

    BACKUP
    ******

    Before we go messing with our hotkey file, we should back it up in case
    something goes wrong. Navigate to your DAS install directory, which is
    "C:\DAS Trader Pro" by default.

    There are a few files in there named hotkey:
        - hotkey    this is an XML document
        - HotKey    this is an HTML document
        - Hotkey    this is an HTK document, the one we want

    Once you have located this file:
        1. Copy the file: right click and select "copy"
        2. Paste the file: press Ctrl+V
        3. Rename the newly created file "Hotkey - Copy" to "MyHotkeys"

    Note:
    We are going to be adding the new hotkeys to "MyHotkeys". The original
    "Hotkey" file you copied from will be your backup.

    GENERATING HOTKEYS
    ******************

    You will need to have Python3 installed in order to use this program.

    Generate hotkeys with $50 risk, using the SMRTL route:
        - $ /usr/bin/python3 das-hotkey-generator.py --risk 50 --route SMTRL
        - A bunch of lines will be printed out in your terminal. Copy them.

    UPDATE YOUR HOTKEY FILE
    ***********************

    Now we are going to paste the hotkeys we generated into your newly created
    "MyHotkeys" file. To do this, we need to open the file up in an editor:
        1. Right click "Myhotkeys" and select "Open with...", then
           select "Notepad"
        2. Paste the lines generated at the bottom of this file, then save it

    LOAD YOUR HOTKEYS INTO DAS
    **************************

    Now it is time to load your new hotkey file into DAS Trader:
        1. Open DAS
        2. From the menu bar, open your hotkey configuration by selecting
           "Setup", then "Hotkey"
        3. Click "Browse" at the bottom of the window, then open your newly
           created hotkey file "MyHotkeys"
        4. Click "Ok", and you are finished!

    DISCLAIMER
    ==========

    I accept no responsibility for misconfigured hotkey files. Always test your
    new configurations in a simulator before using them live.
"""
import os
import sys
import getopt


def usage():
    u_string = 'Usage: '
    u_string += os.path.basename(__file__)
    u_string += ' [-r RISK] [-o ROUTE] [-l LONG_KEY] [-s SHORT_KEY] [-i]'
    print(u_string)
    print('''\

Options:
    -r, --risk              amount you are willing to risk for each trade
    -l, --long-key          key(s) for long position (default: Ctrl+Shift)
    -o, --route             route your hotkeys will send orders through
    -s, --short-key         key(s) for short position (default: Alt+Shift)
    -i, --include-defaults  include default hotkeys
    -h, --help              show this help
''')


DEFAULT_HOTKEYS = [
    'Space:HorizontalLine:HorizontalLine',
    'Ctrl+D:Duplicate window:DuplicateWindow',
    'F1:1 MIN CHART 1 day:MinuteChart 1 1d; ZoomFit',
    'F2:5 MIN CHART 1 day:MinuteChart 5 1d; ZoomFit',
    'F3:1H Chart 15 day:MinuteChart 15 1d; ZoomFit',
    'F4:DAILY CHART:DayChart 1d 1825d; ZoomFit',
    'F5:WEEKLY CHART:DayChart 1w 4y; ZoomFit',
    'F6:MONTHLY CHART 5 years:DayChart 1m 5y',
    'Shift+ESC:close all open positions (all orders must be cancelled'
    ' first):PANIC',

    'Shift+bkspace:Cancel all open orders of symbol in montage:CXL ALLSYMB',
    'Ctrl+PageUp:Long Sell'
    ' all:ROUTE=SMRTL;Price=Bid-0.05;Share=Pos;TIF=DAY+;SELL=Send',

    'Ctrl+Home:Long Sell'
    ' 1/2:ROUTE=SMRTL;Price=Bid-0.05;Share=Pos*0.5;TIF=DAY+;SELL=Send',

    'Ctrl+Insert:Long Sell'
    ' 1/4:ROUTE=SMRTL;Price=Bid-0.05;Share=Pos*0.25;TIF=DAY+;SELL=Send',

    'Alt+PageDown:Short Cover'
    ' all:ROUTE=SMRTL;Price=Ask+0.05;Share=Pos;TIF=DAY+;BUY=Send',

    'Alt+End:Short Cover'
    ' 1/2:ROUTE=SMRTL;Price=Ask+0.05;Share=Pos*0.5;TIF=DAY+;BUY=Send',

    'Alt+Delete:Short Cover'
    ' 1/4:ROUTE=SMRTL;Price=Ask+0.05;Share=Pos*0.25;TIF=DAY+;BUY=Send',

    'Ctrl+Shift+:Long N Shares:ROUTE=SMRTL;Price=Ask+0.05;TIF=DAY+;BUY=Send',
    'Alt+Shift+:Short N Shares:ROUTE=SMRTL;Price=Bid-0.05;TIF=DAY+;SELL=Send',
]

# Map keys to risk.
KEY_MAP = {
    5: 'Q',
    10: 'W',
    15: 'E',
    20: 'R',
    25: 'T',
    30: 'Y',
    35: 'U',
    40: 'I',
    45: 'O',
    50: 'P',
    55: 'A',
    60: 'S',
    65: 'D',
    70: 'F',
    75: 'G',
    80: 'H',
    85: 'J',
    90: 'K',
    95: 'L',
    100: 'Z',
    105: 'X',
    110: 'C',
    115: 'V',
    120: 'B',
    125: 'N',
    130: 'M',
}


def main():
    o_risk = 100
    o_long_key = 'Ctrl+Shift'
    o_route = 'SMRTL'
    o_short_key = 'Alt+Shift'
    o_default_hotkeys = False
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'o:l:r:s:ih',
            ['risk=', 'long-key=', 'route=', 'short-key=', 'default-hotkeys',
             'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for o, a in opts:
        if o == '-r' or o == '--risk':
            o_risk = int(a)
        elif o == '-l' or o == '--long-key':
            o_long_key = a
        elif o == '-o' or o == '--route':
            o_route = a
        elif o == '-s' or o == '--short-key':
            o_short_key = a
        elif o == '-i' or o == '--default-hotkeys':
            o_default_hotkeys = True
        elif o == '-h' or o == '--help':
            usage()
            sys.exit(0)
    result = []
    i = 0
    while i < 2:
        # First iteration is for the long side.
        if i == 0:
            side_key = o_long_key
            side_text = 'Long'
            l2 = 'Ask+'
            side_send = 'BUY'
        # Second iteration is for the short side.
        else:
            side_key = o_short_key
            side_text = 'Short'
            l2 = 'Bid-'
            side_send = 'SELL'
        # Iterate :var:`KEY_MAP` and build string.
        for k, v in KEY_MAP.items():
            dollar = k / 100
            string = ''
            string += '{}+{}:'.format(side_key, v)
            string += '{0} {1:.2f}:'.format(side_text, dollar)
            string += 'ROUTE={};'.format(o_route)
            string += 'Price={}0.05;'.format(l2)
            string += 'Share={};'.format(round(o_risk / dollar))
            string += 'TIF=DAY+;{}=Send'.format(side_send)
            result.append(string)
        i += 1
    if o_default_hotkeys:
        for hotkey in DEFAULT_HOTKEYS:
            result.append(hotkey)
    for line in result:
        print(line)


if __name__ == '__main__':
    main()
