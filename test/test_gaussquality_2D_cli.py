import subprocess
import os
import numpy as np
import pytest
import datetime

test_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(test_dir)
os.chdir(base_dir)

def run_cli(args):
    output = subprocess.run(args, capture_output=True)
    stdout = str(output.stdout).split("\\n")
    stderr = str(output.stderr).split("\\n")
    return stdout, stderr, output.returncode


def test_basic():
    # Check that the most basic test runs, with just a filepath and n_components
    basic_test = [
    'python',
    'gaussquality/gaussquality_2D.py',
    '-f',
    'test/example_images/3D_/3D_00.tif',
    '-n',
    '3']
    stdout, stderr, returncode = run_cli(basic_test)
    assert returncode == 0


def test_ncomp():
    # Check that error is thrown when n_components is not specified
    stdout, stderr, returncode = run_cli([
        'python',
        'gaussquality/gaussquality_2D.py'
        '-f',
        'test/example_images/3D_/3D_00.tif',
    ])
    assert returncode != 0


def test_mask_percentage():
    # Check that mask percentage is applied correctly
    stdout, stderr, returncode = run_cli([
        'python',
        'gaussquality/gaussquality_2D.py',
        '-f',
        'test/example_images/3D_/3D_00.tif',
        '-n',
        '3',
        '--mask_percentage',
        '20'
    ])
    fullsize_x, fullsize_y = stdout[1].split(" = ")[1][1:-3].split(", ")
    masked_x, masked_y = stdout[2].split(" = ")[1][1:-3].split(", ")
    assert ((int(masked_x) / int(fullsize_x)) == pytest.approx(0.2, rel=0.05)) and ((int(masked_y) / int(fullsize_y)) == pytest.approx(0.2, rel=0.05))


def test_threshold():
    # Check that threshold is applied correctly
    stdout, stderr, returncode = run_cli([
    'python',
    'gaussquality/gaussquality_2D.py',
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


def test_save_results():
    # Check that all results are saved
    stdout, stderr, returncode = run_cli([
    'python',
    'gaussquality/gaussquality_2D.py',
    '-f',
    'test/example_images/3D_/3D_00.tif',
    '-n',
    '3',
    '-ppp',
    '-sss'
    ])    
    today = datetime.date.today().strftime("%Y%m%d")
    histo_filename = "test/example_images/3D_/results/3D_00_histogram_{}.png".format(today)
    img_and_histo_filename = "test/example_images/3D_/results/3D_00_img_and_histogram_{}.png".format(today)
    input_filename = "test/example_images/3D_/results/3D_00_{}_input.json".format(today)
    results_filename = "test/example_images/3D_/results/3D_00_{}_GMM_results.json".format(today)
    check_files = [histo_filename, img_and_histo_filename, input_filename, results_filename]
    store_results = True
    for files in check_files:
        if os.path.isfile(files) == False:
            store_results = False
            print("{} was not saved".format(files))
    assert store_results == True


def test_Gaussians_specified():
    # Check that if SNR and CNR are calculated, Gaussians are specified
    stdout, stderr, returncode = run_cli([
    'python',
    'gaussquality/gaussqualityity_2D.py',
    '-f',
    'test/example_images/3D_/3D_00.tif',
    '-n',
    '3',
    '-c',
    ])
    assert returncode != 0
