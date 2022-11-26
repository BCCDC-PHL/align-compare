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


def print_traceback_attributes(traceback):
    print(traceback.query)
    print(traceback.comp)
    print(traceback.ref)



def main(args):
    seq_1 = parse_fasta(args.seq_1)

    seq_2 = parse_fasta(args.seq_2)
    
    result = parasail.nw_trace(seq_1['sequence'], seq_2['sequence'], args.gap_open, args.gap_extend, parasail.dnafull)

    traceback = result.traceback

    with open(args.alignment_output, 'w') as f:
        print('>' + ' '.join([seq_1['id'], seq_1['description']]), file=f)
        print(traceback.query, file=f)
        print('>' + ' '.join([seq_2['id'], seq_1['description']]), file=f)
        print(traceback.ref, file=f)

    assert len(traceback.query) == len(traceback.ref)

    alignment_length = len(traceback.ref)
    num_identical_positions = 0
    for i in range(alignment_length):
        if traceback.query[i] == traceback.ref[i]:
            num_identical_positions += 1

    percent_identity = num_identical_positions / alignment_length * 100.0

    output_fieldnames = [
        'seq_1',
        'seq_2',
        'percent_identity',
    ]

    if args.identity_output is not None:
        with open(args.identity_output, 'w') as f:
            print(','.join(output_fieldnames), file=f)
            print(','.join([seq_1['id'], seq_2['id'], "{:.2f}".format(percent_identity)]), file=f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seq-1')
    parser.add_argument('--seq-2')
    parser.add_argument('--gap-open', type=int, default=10)
    parser.add_argument('--gap-extend', type=int, default=1)
    parser.add_argument('--alignment-output')
    parser.add_argument('--identity-output')
    args = parser.parse_args()

    main(args)
