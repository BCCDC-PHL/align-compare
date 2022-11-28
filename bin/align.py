#!/usr/bin/env python3

import argparse
import json

import parasail


def parse_fasta(fasta_path):
    seq = {}
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                defline = line.strip().replace('>', '')
                seq_id = defline.split()[0]
                description = ' '.join(defline.split()[1:])
                seq['description'] = description
                seq['id'] = seq_id
            else:
                if 'sequence' in seq:
                    seq['sequence'] += line.strip()
                else:
                    seq['sequence'] = line.strip()

    return seq


def main(args):
    seq_1 = parse_fasta(args.seq_1)
    seq_1_length = len(seq_1['sequence'])

    seq_2 = parse_fasta(args.seq_2)
    seq_2_length = len(seq_2['sequence'])
    
    result = parasail.nw_trace(seq_1['sequence'], seq_2['sequence'], args.gap_open, args.gap_extend, parasail.dnafull)

    traceback = result.traceback

    print('>' + ' '.join([seq_1['id'], seq_1['description']]))
    print(traceback.query)
    print('>' + ' '.join([seq_2['id'], seq_1['description']]))
    print(traceback.ref)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seq-1')
    parser.add_argument('--seq-2')
    parser.add_argument('--gap-open', type=int, default=10)
    parser.add_argument('--gap-extend', type=int, default=1)
    args = parser.parse_args()

    main(args)
