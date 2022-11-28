#!/usr/bin/env python3

import argparse
import json


def parse_fasta(fasta_path):
    seqs = []
    with open(fasta_path, 'r') as f:
        current_seq = None
        for line in f:
            if line.startswith('>'):
                if current_seq is not None:
                    seqs.append(current_seq)
                    current_seq = {}
                current_seq = {}
                defline = line.strip().replace('>', '')
                seq_id = defline.split()[0]
                description = ' '.join(defline.split()[1:])
                current_seq['description'] = description
                current_seq['id'] = seq_id
            else:
                if 'sequence' in current_seq:
                    current_seq['sequence'] += line.strip()
                else:
                    current_seq['sequence'] = line.strip()

        seqs.append(current_seq)

    return seqs


def main(args):
    seqs = parse_fasta(args.alignment)

    seq_1 = seqs[0]['sequence']
    seq_2 = seqs[1]['sequence']

    assert len(seq_1) == len(seq_2)

    alignment_length = len(seq_1)
    num_identical_positions = 0
    num_aligned_positions = 0
    for i in range(alignment_length):
        if seq_1[i] == '-' or seq_2[i] == '-':
            continue
        if seq_1[i] == seq_2[i]:
            num_identical_positions += 1
            num_aligned_positions += 1
        else:
            num_aligned_positions += 1

    percent_identity = num_identical_positions / num_aligned_positions * 100.0

    output_fieldnames = [
        'seq_1',
        'seq_2',
        'seq_1_length',
        'seq_2_length',
        'aligned_length',
        'percent_identity_of_aligned_segments',
    ]

    print(','.join(output_fieldnames))
    print(','.join([seqs[0]['id'], seqs[1]['id'], str(len(seq_1)), str(len(seq_2)), str(num_aligned_positions), "{:.2f}".format(percent_identity)]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('alignment')
    args = parser.parse_args()

    main(args)
