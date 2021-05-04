import os

from pathlib import Path


ARRAY_HEADER = """#!/bin/bash
#SBATCH --account={account}
#SBATCH --time={time}
#SBATCH --job-name={job_name}
#SBATCH --output={job_name}_%A_array%a__%j.out
#SBATCH --array=0-{N}
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task={cpus}
#SBATCH --mem-per-cpu={cpu_memory}G
#SBATCH --mail-user={email}
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL"""

ARRAY_SCRIPT = """
PROJECT=$HOME/projects/{account}/{user}/error-consistency

module load python/{python}
cd $SLURM_TMPDIR
tar -xf $PROJECT/venv.tar .venv
source .venv/bin/activate
PYTHON=$(which python)

# virtualenv --no-download .venv
# source .venv/bin/activate
# pip install --no-index --upgrade pip
# pip install --no-index -r $PROJECT/requirements.txt

commands=(
{}
)
eval ${{commands["$SLURM_ARRAY_TASK_ID"]}}
"""

FIELD_DEFAULTS = {
    "account": os.environ.get("SLURM_ACCOUNT"),
    "user": Path(os.environ.get("HOME")).name,
    "project": None,
    "time": "00:01:00:00",  # 1 hour
    "job_name": "cc_job",
    "cpus": 1,
    "cpu_memory": 8,
    "python": "3.8.2"
}