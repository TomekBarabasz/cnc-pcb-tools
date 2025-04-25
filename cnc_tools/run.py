import argparse
from sys import argv
from pathlib import Path
from cutoff import cutoff
from utils import read_yml

if __name__ == '__main__':
    Cmds = {'cutoff' : cutoff}
    if len(argv) < 2:
        print('available tools :', ','.join(Cmds.keys()))
        exit(1)
    cmd = argv[1]
    parser = argparse.ArgumentParser(description="file format converter")
    parser.add_argument("job", type=Path, help='input file')
    parser.add_argument("--output","-o",type=Path, help="output file")
    Args = parser.parse_args(argv[2:])
    job = read_yml(Args.job)    
    program = Cmds[cmd](job)

    with open(Args.output,'w') as f:
        for c in program:
            f.write(c+'\n')
