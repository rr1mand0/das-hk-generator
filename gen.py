from jinja2 import Environment, FileSystemLoader
import argparse

WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'

parser = argparse.ArgumentParser()
parser.add_argument('risk', type=int, help='default amount to risk($)')
parser.add_argument('--account', type=int, default=25000, help='Account size($25000)')
parser.add_argument('--template', '-T', type=str, default="default.htk.j2", help='default template file')
parser.add_argument('--output', '-o', type=str, default='/dev/stdout', help='Output file')
args = parser.parse_args()

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template(args.template)

content = template.render(
        risk=args.risk,
        account=args.account
    )

# c = []

# for line in content.split('\n'):
#     c.append(line.strip())
#     c.append('\r\n')
    
with open(args.output, 'w') as fh:
    fh.write(content) #"".join(c))
