# create function that for every occupation in base year, finds technologies that were introduced
import pandas as pd

def tech_introduced(year_start, year_finish):
	
	# file load syntax
	prefix_start, prefix_finish = map(lambda x: x[-2:], [year_start, year_finish])
	path_folder = '~/Google Drive/Oxford/DPhil/future_employment/data/databases/db'
	path_start = path_folder + prefix_start 
	path_finish = path_folder + prefix_finish

	# load files
	full_df_before = pd.read_table(path_start, delimiter = '\t')[[]]
	full_df_finish = pd.read_table(path_finish, delimiter = '\t')

	# subset files to technology
	full_df_before = full_df_before[full_df_before['T2 Type'] == 'Technology']
	full_df_finish = full_df_finish[full_df_finish['T2 Type'] == 'Technology']

	# limit later year occupations to those available in earlier year
	limited_occupations = df_before['O*NET-SOC Code'].unique()
	df_before = full_df_before[full_df_before['O*NET-SOC Code'].isin(limited_occupations)]
	df_finish = full_df_finish[full_df_finish['O*NET-SOC Code'].isin(limited_occupations)]

	# create new dataframe
	df_adoptions = pd.DataFrame(columns = df_before.columns)

	# find technologies that have emerged
	for occupation_code in limited_occupations:
		df_before_occ_tools = df_before[df_before['O*NET-SOC Code'] == occupation_code]
		df_finish_occ_tools = df_finish[df_finish['O*NET-SOC Code'] == occupation_code]
		adopted = df_finish_occ_tools[~df_finish_occ_tools['Commodity Code'].isin(df_before_occ_tools['Commodity Code'])]
		df_adoptions = pd.concat([df_adoptions, adopted])

	return df_adoptions