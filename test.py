import cnc_tools

job = cnc_tools.read_yml('./yaml/cutoff-job.yaml')
program = cnc_tools.cutoff(job)
print( program )
