import subprocess
import os

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
