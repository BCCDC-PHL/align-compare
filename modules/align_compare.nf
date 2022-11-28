process mafft {
    tag { sample_id }

    publishDir "${params.outdir}/${sample_id}", pattern: "${sample_id}.aln.fa", mode: 'copy'

    input:
    tuple val(sample_id), path(seq_1), path(seq_2)

    output:
    tuple val(sample_id), path("${sample_id}.aln.fa")

    script:
    // Convert multi-line fasta to single line
    awk_string = '/^>/ {printf("\\n%s\\n", $0); next; } { printf("%s", $0); }  END { printf("\\n"); }'
    """
    align.py \
      --thread ${task.cpus} \
      --preservecase \
      --add \
      ${seq_1} \
      ${seq_2} \
      > ${sample_id}.multi_line.aln.fa

    awk '${awk_string}' ${sample_id}.multi_line.aln.fa > ${sample_id}.aln.fa
    """
}

process parasail_nw_align {
    tag { sample_id }

    publishDir "${params.outdir}/${sample_id}", pattern: "${sample_id}.aln.fa", mode: 'copy'
    publishDir "${params.outdir}/${sample_id}", pattern: "${sample_id}_alignment_identity.csv", mode: 'copy'

    input:
    tuple val(sample_id), path(seq_1), path(seq_2)

    output:
    tuple val(sample_id), path("${sample_id}.aln.fa"), emit: alignment
    tuple val(sample_id), path("${sample_id}_alignment_identity.csv"), emit: identity

    script:
    """
    align.py \
      --seq-1 ${seq_1} \
      --seq-2 ${seq_2} \
      --gap-open ${params.gap_open_penalty} \
      --gap-extend ${params.gap_extend_penalty} \
      > ${sample_id}.aln.fa

    calculate_identity.py ${sample_id}.aln.fa > ${sample_id}_alignment_identity.csv
    """
}


