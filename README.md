# snakemake-profiler

This is just a WIP repo for profiling memory and time of any snakemake file. The plan is to write a Python script that injects the `benchmark` directive into all the Snakemake file rules. There will be options to run the file directly `snakemake-profiler snakemake ...` Or write a new snakemake file with the injected directive. There might be an option to set the number of runs per benchmark.
