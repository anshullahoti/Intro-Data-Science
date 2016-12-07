##########################################################################################################
# TABLE OF CONTENTS
#
# MODULES / SETUP
# BASIC TOOLS
# ANNUAL GLOBAL TEMPERATURES


##########################################################################################################
# MODULES / SETUP

import numpy as np
import pandas as pd

from tkinter import Tk
from tkinter import filedialog as fd

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


##########################################################################################################
# BASIC TOOLS


def open_file():
	root = Tk().withdraw()
	filename = fd.askopenfilename()
	return filename

def create_dataframe():
	filename = open_file()
	return pd.read_csv(filename, parse_dates=['dt'])


##########################################################################################################
# ANNUAL GLOBAL TEMPERATURES

def get_avg_temperatures(dataframe, start_year, end_year):

	df = dataframe.copy()

	# extract year from feature 'dt'
	df['dt'] = df['dt'].apply(lambda x: x.year)

	# extract observations of specified year range
	data = df[(df['dt']>=start_year) & (df['dt']<=end_year)]

	# return numpy array of average temperatures
	return data.groupby(['dt']).mean()['AverageTemperature'].values

def get_uncertainty(dataframe, start_year, end_year):

	df = dataframe.copy()

	# extract year from feature 'dt'
	df['dt'] = df['dt'].apply(lambda x: x.year)

	# extract observations of specified year range
	data = df[(df['dt']>=start_year) & (df['dt']<=end_year)]

	# return numpy array of average temperature uncertainties
	return data.groupby(['dt']).mean()['AverageTemperatureUncertainty'].values


def plot_avg_global_temperatures(dataframe, start_year, end_year):

	# extract corresponding dates and temperatures 
	dates = np.arange(start_year, end_year + 1)
	temps = get_avg_temperatures(dataframe, start_year, end_year)

	# plot data
	plt.figure(figsize=(12, 6))
	plt.scatter(dates, temps, c=temps, s=150, alpha=0.6, edgecolors='none', cmap='viridis')
	plt.xlim([start_year - 5, end_year + 5])
	plt.grid(True)
	plt.title("Average Global Temperatures [" + str(start_year) + ", " + str(end_year) + "]")
	plt.xlabel("Year")
	plt.ylabel("Temperature (Celsius)")
	plt.show()


def plot_uncertainty(dataframe, start_year, end_year):

	# extract corresponding dates, temperatures, and uncertainties 
	dates = np.arange(start_year, end_year + 1)
	temps = get_avg_temperatures(dataframe, start_year, end_year)
	uncertainty = get_uncertainty(dataframe, start_year, end_year)


	# plot data
	plt.figure(figsize=(12, 6))
	plt.plot(dates, (temps + uncertainty), c='purple', label='Average Uncertainty Field')
	plt.plot(dates, (temps - uncertainty), c='purple')
	plt.fill_between(dates, (temps + uncertainty), (temps - uncertainty), facecolor='mediumpurple')
	plt.plot(dates, temps, linewidth=3, label='Average Temperature')
	plt.xlim([start_year - 5, end_year + 5])
	plt.grid(True)
	plt.legend(loc='best')
	plt.title("Average Global Temperatures and Uncertainty Field [" + str(start_year) + ", " + str(end_year) + "]")
	plt.xlabel("Year")
	plt.ylabel("Temperature (Celsius)")
	plt.show()
	