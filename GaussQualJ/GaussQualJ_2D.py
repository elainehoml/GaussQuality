#@ String (visibility = MESSAGE, value = "<html><h1>GaussQual: Fitting Gaussian Mixture Models to grey values</h1><br><p>See github.com/elainehoml/GaussQual for more information.</p></html>", required = false) msg0
#@ String (visibility = MESSAGE, value = "<html><h3>The following parameters are required: </h3></html>", required = false) msg1
#@ String (label = "<html><b>Conda environment*</b></html>", value = "GMM", description = "conda environment in which to run the Python code") conda_env
#@ File (label = "<html><b>GaussQual directory*</b></html>", style = "directory") path
#@ File (label = "<html><b>Input 2D image*</b></html>", style = "file") img_filepath
#@ Integer (label = "<html><b>Number of Gaussians to fit*</b></html>") n_components
#@ String (visibility = MESSAGE, value = "<html><p> ......................................................................................................................................................... </p></html>", required = false) msg2
#@ String (visibility = MESSAGE, value = "<html><h3>The following parameters are optional: </h3></html>", required = false) msg3
#@ String (choices = {"No plots", "Histogram", "Image + Histogram", "Both"}, style="listBox", value = "Both") plots
#@ Float (label = "Mask percentage in xy", value = 100, style = "slider", min = 0, max = 100) mask_percentage
#@ Boolean (label = "Threshold image?", value = False) threshold
#@ Float (label = "<html>Threshold: Minimum grey value <br>(Ignored if threshold image is not checked) </html>", value=0) min_GV
#@ Float (label = "<html>Threshold: Maximum grey value <br>(Ignored if threshold image is not checked) </html>", value=255) max_GV
#@ Boolean (label = "<html>Show plots in separate interactive window<br>Please exit window to continue </html>", value = False) show_plots
#@ String (label = "Material names, separate by commas", value = "<None>") material_names
#@ Boolean (label = "Calculate SNR and CNR?", value = False, description = "Calculate SNR and CNR between feature and background material Gaussians") calc
#@ String (visibility = MESSAGE, value = "<html><h3>Background and feature Gaussians an have >1 value, separated by commas, e.g. 1,2.<br> Please ensure there are equal numbers of indices specified for background and feature. </h3></html>", required = false) msg4
#@ String (label = "<html>Background Gaussian index, <br>(Ignored if SNR and CNR is not calculated)</html>", value="<None>", description = "Can have >1 value, separated by commas, e.g. 1,2") background
#@ String (label = "<html>Feature Gaussian index, <br>(Ignored if SNR and CNR is not calculated)</html>", value = "<None>", description = "Can have >1 value, separated by commas, e.g. 1,2") feature

from java.lang import Runtime
from java.io import BufferedReader, InputStreamReader

# Set up parameters for python script to run here
script = "GaussQual/GaussQual_2D.py"

args = [
	'-f',
	'"{}"'.format(img_filepath),
	'-n',
	str(n_components),
	'-sss',
	'--mask_percentage',
	str(mask_percentage)]

def compile_cmd_str(args):
	return "cmd /k cd {} & conda activate {} & python {} {} & exit()".format(
		path,
		conda_env,
		script,
		' '.join(args))

def run_cmd_str(cmd_str):
	# Start a new process, run python script from cmd
	run = Runtime.getRuntime()
	print(cmd_str)
	proc = run.exec(cmd_str)
	
	# Collect output from stdout and stderr, print to console
	stdout_reader = BufferedReader(InputStreamReader(proc.getInputStream()))
	stderr_reader = BufferedReader(InputStreamReader(proc.getErrorStream()))

	return stdout_reader, stderr_reader

def print_output(output_reader):
	"""
	Prints output of stdout or stderr to console

	Parameters
	----------
	output_reader : BufferedReader object
		Reads either stdout or stderr
		
	Returns
	-------
	list
		List of all lines in output_reader as str
	"""
	output_list = []
	output_single = output_reader.readLine()
	while output_single != None: # while line in output_reader is not empty
		output_list.append(output_single) # append this line
		output_single = output_reader.readLine() # advance to next line of output_reader

	# print to console
	for line in output_list:
		print(line)
	print("\n")

	return output_list


def check_plots_input(plots, args):
	if plots == "Histogram":
		args.append('-p')
	if plots == "Image + Histogram":
		args.append('-pp')
	if plots == "Both":
		args.append('-ppp')

def check_threshold_input(threshold, args):
	if threshold == True:
		args.append('-t')
		args.append(str(min_GV))
		args.append(str(max_GV))

def check_material_names_input(material_names, args):
	if material_names != "<None>":
		args.append("--material_names")
		material_names_list = material_names.split(",")
		for material in material_names_list:
			args.append(str(material))

def check_calc(background, feature, calc, args):
	if calc == True:
		if background == "<None>":
			raise ValueError("Please input background Gaussian, or uncheck Calculate SNR and CNR")
		if feature == "<None>":
			raise ValueError("Please input feature Gaussian, or uncheck Calculate SNR and CNR")		
		args.append("-c")
		background_list = background.split(",")
		feature_list = feature.split(",")
		args.append("--background")
		for background in background_list:
			args.append(str(background))
		args.append("--feature")
		for feature in feature_list:
			args.append(str(feature))

# ------- MAIN ----------------------------------------------------------
check_plots_input(plots, args)
check_threshold_input(threshold, args)
if show_plots == True:
	args.append('--show_plots')
check_material_names_input(material_names, args)
check_calc(background, feature, calc, args)
cmd_str = compile_cmd_str(args)
stdout_reader, stderr_reader = run_cmd_str(cmd_str)

print("stdout: \n")
stdout = print_output(stdout_reader)

print("stderr: \n")
stderr = print_output(stderr_reader)


print("done")
