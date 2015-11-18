import pandas as pd

from automating_tech_helpers import *
from unspsc_helpers import *

## translate automating_tech (classes) into codes
def map_group_to_code(map_list, group = 'Class'):
    """
    Turns raw UNSPSC data into a list of the codes of just the groupings you
    care about (like automating technology, for example).
    """
    title = group + ' Title'
    code = group + ' Code'
    groups = unspsc.groupby(title)[[title, code]].head()
    codes = groups.drop_duplicates().reset_index(drop = True)
    return codes[codes[title].isin(map_list)].reset_index(drop = True)

## convert existing commodity codes to grouping codes
def create_codes(df, group = 'Class'):
    if group == 'Class':
        zeroes = 2
    elif group == 'Family':
        zeroes = 4
    elif group == 'Segment':
        zeroes = 6
    def convert_to_code(num, zeroes):
        s = str(num)
        s = s[:-zeroes] + zeroes*"0"
        return int(s)
    return df['Commodity Code'].apply(lambda x: convert_to_code(x, zeroes))

## check if commodity code is in the "group" code
def has_automation_property(df, group_codes, group = 'Class'):
    """
    Checks if a commodity code is in the "group" (family/class/etc.) code
    list of automating/influential technologies.

    Returns a boolean vector.
    """
    code = group + ' Code'
    return df[code].isin(group_codes)

def add_group_automation(df, group_list, group = 'Class', outcome_title = 'automatable'):
    """
    """
    new_df = df.copy()
    code = group + ' Code'
    group_codes = map_group_to_code(group_list, group)[code]
    code_title = group + " Code"
    new_df[code_title] = create_codes(new_df, group)
    new_df[outcome_title] = has_automation_property(new_df, group_codes, group)
    return new_df


def get_innovative_occupations(df_old, df_new, outcome_class):
    subset = df_new[df_new[subset_class] == True]
    occupation_dict = {}
    for occupation in df_new['O*NET-SOC Title'].unique():
        new_tech = df_new[df_new['O*NET-SOC Title'] == occupation]['Commodity Title'].unique()
        old_tech = df_old[df_old['O*NET-SOC Title'] == occupation]['Commodity Title'].unique()
        occupation_dict[occupation] = [i for i in new_tech if i not in old_tech]
    return occupation_dict
