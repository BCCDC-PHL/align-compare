#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { parasail_nw_align } from './modules/align_compare.nf'

workflow {

  if (params.samplesheet_input != 'NO_FILE') {
    ch_fasta = Channel.fromPath(params.samplesheet_input).splitCsv(header: true).map{ it -> [it['ID'], it['SEQ1'], it['SEQ2']] }
  } else {
    ch_fasta_1 = Channel.fromPath(params.fasta_1_search_path).map{ it -> [it.getName().split('_')[0], it] }.unique{ it -> it[0] }
    ch_fasta_2 = Channel.fromPath(params.fasta_2_search_path).map{ it -> [it.getName().split('_')[0], it] }.unique{ it -> it[0] }
    ch_fasta = ch_fasta_1.join(ch_fasta_2)
  }

  main:
  
    parasail_nw_align(ch_fasta)
}
