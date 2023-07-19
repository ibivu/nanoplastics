#!/usr/bin/python3

### Plot Panta data
### To run: python3 plot_meltingscan.py 20211216_NanoPET_asyn/melting-scan.csv melting-scan_py

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sys import argv

# Colormaps
blues = plt.get_cmap('Blues_r')
oranges = plt.get_cmap('Oranges_r')
greens = plt.get_cmap('Greens_r')

def read_data(f_in):
	""" Read input data from melting-scan file, in csv format """
	
	df = pd.read_table(f_in, sep=';', index_col=0, header=0)
	
	return(df)


def plot_ratio(df, samples, colors, f_out, show_legend=True):
	""" Plot the 350/330 nm ratio for each capillary """
	# Select columns
	cols_sel = [colname for colname in df.columns if colname.startswith('Ratio 350 nm')]
	
	df_sub = df.loc[:, cols_sel]
	df_sub.columns = samples
	df_sub[df_sub.index.name] = df_sub.index
	
	# Create plot
	fig, ax = plt.subplots(figsize=(10,6))
	if show_legend:
		for idx in range(len(df_sub.columns) - 1):
			df_sub.plot.scatter(x=df_sub.index.name, y=df_sub.columns[idx], fontsize=20, s=2, ax=ax, color=colors[idx], label=samples[idx])
		#ax.legend(loc='center left', bbox_to_anchor=(1, .5), fontsize=16)
		ax.legend(fontsize=16)
	else:
		for idx in range(len(df_sub.columns) - 1):
			df_sub.plot.scatter(x=df_sub.index.name, y=df_sub.columns[idx], fontsize=20, s=2, ax=ax, color=colors[idx])
	ax.set_ylim((0, 2))
	ax.set_xlabel('Time (min)', fontsize=24)
	ax.set_ylabel('Ratio 350nm/330nm', fontsize=24)
	plt.savefig(f_out + '_ratio.png', bbox_inches='tight', transparent=True)
	plt.close()
	
	
	
def plot_turbidity(df, samples, colors, f_out, show_legend=True):
	""" Plot turbidity for each capillary """
	
	# Select columns
	cols_sel = [colname for colname in df.columns if colname.startswith('Turbidity')]
	
	df_sub = df.loc[:, cols_sel]
	df_sub.columns = samples
	df_sub[df_sub.index.name] = df_sub.index
	
	# Create plot
	fig, ax = plt.subplots(figsize=(10,6))
	if show_legend:
		for idx in range(len(df_sub.columns) - 1):
			df_sub.plot.scatter(x=df_sub.index.name, y=df_sub.columns[idx], fontsize=20, s=2, ax=ax, color=colors[idx], label=samples[idx])
		ax.legend(fontsize=12)
	else:
		for idx in range(len(df_sub.columns) - 1):
			df_sub.plot.scatter(x=df_sub.index.name, y=df_sub.columns[idx], fontsize=20, s=2, ax=ax, color=colors[idx])
	ax.set_ylim((80, 110))
	ax.set_xlabel('Time (min)', fontsize=24)
	ax.set_ylabel('Turbidity (mAU)', fontsize=24)
	plt.savefig(f_out + '_turbidity.png', transparent=True)
	plt.close()
	
	
	
def plot_radius(df, samples, colors, f_out, show_legend=True):
	""" Plot the cumulant radius for each capillary """
	
	# Select columns
	cols_sel = [colname for colname in df.columns if colname.startswith('Cumulant Radius')]
	
	df_sub = df.loc[:, cols_sel]
	df_sub.columns = samples
	df_sub[df_sub.index.name] = df_sub.index
	
	# Create plot
	fig, ax = plt.subplots(figsize=(10,6))
	if show_legend:
		for idx in range(len(df_sub.columns) - 1):
			df_sub.plot.scatter(x=df_sub.index.name, y=df_sub.columns[idx], logy=True, fontsize=20, s=2, ax=ax, color=colors[idx], label=samples[idx])
		ax.legend(fontsize=12)
	else:
		for idx in range(len(df_sub.columns) - 1):
			df_sub.plot.scatter(x=df_sub.index.name, y=df_sub.columns[idx], logy=True, fontsize=20, s=2, ax=ax, color=colors[idx])
	ax.set_ylim((1, 5000))
	ax.set_xlabel('Time (min)', fontsize=24)
	ax.set_ylabel('Cumulant radius (nm)', fontsize=24)
	plt.savefig(f_out + '_radius.png', transparent=True, bbox_inches='tight')
	plt.close()



def main():
	
	### Parse input arguments
	f_in = argv[1]
	f_out = argv[2]
	
	try:
		if argv[3] == 'y' or 'Y' or 'yes' or 'YES' or 'Yes' or 1 or 'TRUE' or 'true' or 'True' or 'T' or 't':
			show_legend = True
		elif argv[3] == 'n' or 'N' or 'no' or 'NO' or 'No' or 0 or 'FALSE' or 'false' or 'False' or 'F' or 'f':
			show_legend = False
		else:
			print('Error: show_legend needs to be a boolean (yes/no/true/false/0/1, caps allowed)')
			exit(-1)
	except:
		# if no input for show_legend is provided, default to True
		show_legend = True

	# Sample labels for legend
	samples = [r'$\alpha$-syn 100$\mu$M', r'$\alpha$-syn 50$\mu$M', r'$\alpha$-syn 10$\mu$M', 'nanoPET', r'nanoPET + $\alpha$-syn 100$\mu$M', r'nanoPET + $\alpha$-syn 50$\mu$M', r'nanoPET + $\alpha$-syn 10$\mu$M']
	colors = [greens(0), greens(.3), greens(.6), oranges(0), blues(0), blues(.3), blues(.6)]
	
	### Read input data
	df = read_data(f_in)
	
	### Create plots
	plot_radius(df, samples, f_out)
	plot_turbidity(df, samples, f_out)
	plot_ratio(df, samples, f_out)
	
	
if __name__ == '__main__':
	main()