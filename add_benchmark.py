from __future__ import with_statement
from shutil import copyfile
import sys
import os
from glob import glob

# Repeat a benchmark multiple times in order to get a sense for the variability of the measurements.
REPEAT = 1

OUT_DIR = "grist_output"

SNAKEMAKE_FILE = str()
modified_rules = list()


if len(sys.argv) != 2:
    sys.exit("run: python add_benchmark.py <snakemake_file_path>")
else:
    SNAKEMAKE_FILE = sys.argv[1]

# Create a backup
SNAKEMAKE_DIR = os.path.dirname(SNAKEMAKE_FILE)
SNAKEMAKE_BASENAME = os.path.basename(SNAKEMAKE_FILE)

i = 1
while os.path.exists(f"BAK_{i}_{SNAKEMAKE_BASENAME}"):
    i += 1

BACKUP_SNAKEMAKE = os.path.join(SNAKEMAKE_DIR, f"BAK_{i}_{SNAKEMAKE_BASENAME}")

print(f"Renaming {SNAKEMAKE_FILE} to {BACKUP_SNAKEMAKE}")

os.rename(SNAKEMAKE_FILE, BACKUP_SNAKEMAKE)


try:
    with open(BACKUP_SNAKEMAKE, 'r') as SM, open(SNAKEMAKE_FILE, 'w') as E_SM:
        for line in SM:
            if line.startswith("rule"):
                rule_name = line.split()[1][:-1]
                E_SM.write(line)
                E_SM.write(
                    f'\tbenchmark:\n\t\trepeat("benchmarks/benchmark.{rule_name}.tsv", {REPEAT})\n'
                )
                modified_rules.append(rule_name)
            else:
                E_SM.write(line)

    print(f"Modified rules: {modified_rules}")


except FileNotFoundError:
    print("Snakemake file does not exist!", file=sys.stderr)
