from jinja2 import Environment, FileSystemLoader
import argparse

WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'

FUTURES_FACTOR = {
    'ES': 50,
    'MES': 5,
    'NQ': 20,
    'MNQ': 2
}

parser = argparse.ArgumentParser()
parser.add_argument('risk', type=int, help='default amount to risk($)')
parser.add_argument('--account', type=int, default=25000, help='Account size($25000)')
parser.add_argument('--template', '-T', type=str, default="default.htk.j2", help='default template file')
parser.add_argument('--output', '-o', type=str, default='/dev/stdout', help='Output file')
parser.add_argument('--npt', '-n', type=int, default=3, help='Number of profit targets')
parser.add_argument('--nhk', '-k', type=int, default=6, help='Number of hotkey targets')
parser.add_argument('--pto', '-O', type=float, default=0.20, help='Profit target offset')
parser.add_argument('--futures', choices=['ES', 'MES', 'NQ', 'MNQ'], default=None, help='Futures type')
args = parser.parse_args()

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template(args.template)


if args.futures is not None:
    args.risk = (int)(args.risk/FUTURES_FACTOR[args.futures])

content = template.render(
        risk=args.risk,
        account=args.account,
        npt=args.npt,
        pto=args.pto,
        nhk=args.nhk,
        future=FUTURES_FACTOR.get(args.futures, 1)
    )

dos = content.replace('\n', '\r\n')
    
with open(args.output, 'w') as fh:
    fh.write(dos)
