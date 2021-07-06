import subprocess
import os

test_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(test_dir)
os.chdir(base_dir)

def run_cli(args):
    output = subprocess.run(args, capture_output=True)
    stdout = str(output.stdout).split("\\n")
    stderr = str(output.stderr).split("\\n")
    return stdout, stderr, output.returncode


def test_basic():
    # Check that the most basic test runs, with just imgdir and n_comp
    basic_test = [
        'python',
        'gaussquality/gaussquality_3D.py',
        '-d',
        'test/example_images/3D_/',
        '-n',
        '3'
    ]
    stdout, stderr, returncode = run_cli(basic_test)
    assert returncode == 0


def test_ncomp():
    # Check that error is thrown when n_components is not specified
    stdout, stderr, returncode = run_cli([
        'python',
        'gaussquality/gaussquality_3D.py'
        '-d',
        'test/example_images/3D_/',
    ])
    assert returncode != 0


