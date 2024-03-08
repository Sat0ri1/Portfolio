//Written by Pawel Grygielski and Michal Somala 18.01.23

nextflow.enable.dsl=2 

/*#############-IMPORTANT-#################

    Input sequences must be:
    -fetched into one file
    -in file, separated with <enter>
    -You can fetch the sequences with
     provided script "merge.sh in which
     you have to replace path with your's"

##########################################*/

/*
    Process responsible for clustalw2 alignment.
    Results will be placed in /wyniki/clustal_allignment directory
    NOTE: it requires clustalw2 to be installed
                                                        */
process clustalw2_allign {
    publishDir "wyniki/clustal_allignment", mode: "copy"

    input:
    path allignments

    output: 
    path("*")

    script:
    """
    clustalw2 -infile=sequences.txt -align -outfile=alseq.aln
    """
}
/*
    Process responsible for tcoffee alignment.
    Results will be placed in /wyniki/tcoffe directory
    NOTE: it requires T-coffee package to be installed
    Note: tcoffee alignment might take a lot of time
                                                        */
process tcoffee_allign {
    publishDir "wyniki/tcoffee", mode: "copy"

    input:
    path allignments_tcoffee

    output: 
    path("*")

    script:
    """
    t_coffee -infile=sequences.txt -outfile=theraphosidae_tcf.aln
    """
}
/*
    Process responsible for granting all rights to all users
    (refers to fetched sequences in file alseq.aln only)
                                                             */
process rights {
    input:
    path file

    output:
    val true
    """
    #!/usr/bin/bash
    
        chmod 777 alseq.aln
    """
}

/*
    Process responsible for reformating clustal alignment to 
    phylip format.
    This process will only start when clustal alignment process is over
    NOTE: it requires HMMER and easel packages to be installed
                                                             */                                                           
process clustal_to_phylip {
    publishDir "wyniki/phylips", mode: "copy"

    input:
    val ready
    path reformat

    output:
    path("*")

    script:
    """
    esl-reformat phylip $reformat > allignments_phylip.txt
    """
}
/*
    Process responsible for building NJ tree for alignment created by clustal.
    This process will only start when clustal alignment process is over
    NOTE: it requires clustalw2 to be installed
                                                                        */ 
process clustal_tree {
    publishDir "wyniki/clustal_tree", mode: "copy"

    input:
    val ready
    path spiders_tree

    output: 
    path("*")

    script:
    """
    clustalw2 -infile=alseq.aln -tree -outfile=TheraphosidaeNJ.tre
    """
}

    //Channels from paths, used in workflow to specify inputs for processes
spider_datasets_cl = Channel.fromPath("merged/sequences.txt")
reformat_datasets = Channel.fromPath("wyniki/clustal_allignment/alseq.aln")

/*
    workflow - task that needs to be performed to close the pipeline
    -rights process requires clustalw alignment, so it can only start
     running, when clustalw2_allign got to it's output,
    
    -clustal_to_phylip also requires clustalw alignment, but as there was
     a problem with reading the file, we will make it run only after rights
     finish to perform,
    
    -clustal_tree requires clustal alignment as well, so it can onlu start
    performing when clustalw2_allign is over. 
- 
                                                                                */
workflow{
    clustalw2_allign(spider_datasets_cl)
    tcoffee_allign(spider_datasets_cl)
    rights(clustalw2_allign.out)
    clustal_to_phylip(rights.out, reformat_datasets)
    clustal_tree(clustalw2_allign.out, reformat_datasets)
}


