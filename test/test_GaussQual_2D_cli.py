import subprocess
import os
import numpy as np
from pytest import approx

test_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(test_dir)
os.chdir(base_dir)

def run_GaussQual_2D(args):
    output = subprocess.run(args, capture_output=True)
    stdout = str(output.stdout).split("\\n")
    stderr = str(output.stderr).split("\\n")
    return stdout, stderr, output.returncode


def test_basic():
    # Check that the most basic test runs, with just a filepath and n_components
    basic_test = [
    'python',
    'GaussQual/GaussQual_2D.py',
    '-f',
    'test/example_images/3D_/3D_00.tif',
    '-n',
    '3']
    stdout, stderr, returncode = run_GaussQual_2D(basic_test)
    assert returncode == 0


def test_ncomp():
    # Check that error is thrown when n_components is not specified
    stdout, stderr, returncode = run_GaussQual_2D([
        'python',
        'GaussQual/GaussQual_2D.py'
        '-f',
        'test/example_images/3D_/3D_00.tif',
    ])
    assert returncode != 0


def test_mask_percentage():
    # Check that mask percentage is applied correctly
    stdout, stderr, returncode = run_GaussQual_2D([
        'python',
        'GaussQual/GaussQual_2D.py',
        '-f',
        'test/example_images/3D_/3D_00.tif',
        '-n',
        '3',
        '--mask_percentage',
        '20'
    ])
    fullsize_x, fullsize_y = stdout[1].split(" = ")[1][1:-3].split(", ")
    masked_x, masked_y = stdout[2].split(" = ")[1][1:-3].split(", ")
    assert ((int(masked_x) / int(fullsize_x)) == approx(0.2, rel=0.05)) and ((int(masked_y) / int(fullsize_y)) == approx(0.2, rel=0.05))


def test_threshold():
    # Check that threshold is applied correctly
    stdout, stderr, returncode = run_GaussQual_2D([
    'python',
    'GaussQual/GaussQual_2D.py',
    '-f',
    'test/example_images/3D_/3D_00.tif',
    '-n',
    '3',
    '-t',
    '5',
    '100'
    ])
    min_gv, max_gv = stdout[3].split(" = ")[1].split("-")
    assert (int(min_gv) == 5) and (int(max_gv[:-2]) == 100)

