import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter, OrderedDict
from nltk.corpus import stopwords
import re

from automation_mapping import *
from automating_tech_helpers import *
from machines_helpers import *
from ai_tech_helpers import *

## LOAD DATA
def load_data():
    unspsc = pd.read_table('../data/onet_tools_technology/UNSPSC Reference.txt') # occupation code database
    tt6 = pd.read_csv('../data/db06/Tools_and_Technology.csv') # tools & tech 2006
    tt9 = pd.read_csv('../data/db09/Tools and Technology.csv') # tools & tech 2009
    tt15 = pd.read_table('../data/db15/Tools and Technology.txt') # tools & tech 2015
    occ_ref = pd.read_table('../data/db15/helpers/occ_codes/occupation_reference.csv')

    ## add occupation titles to tt15
    tt15 = tt15.merge(occ_ref, how = 'left', on = ['O*NET-SOC Code'])

    ## add the missing grouping: family
    # tt15['Segment Code'] = create_codes(tt15, group = 'Segment')
    # tt15['Class Code'] = create_codes(tt15, group = 'Class')
    # tt15['Family Code'] = create_codes(tt15, group = 'Family')
    # tt15.columns = ['O*NET-SOC Code',
    #  'T2 Type',
    #  'T2 Example',
    #  'Commodity Code',
    #  'Commodity Title',
    #  'O*NET-SOC Title',
    #  'Segment Code',
    #  'Class Code',
    #  'Family Code']

    return None

# removing stopwords and punctuation for ease of use
def remove_punc_stopwords_lower(s):
    stop = stopwords.words('english')
    regex = r"\W+"
    return " ".join([i for i in re.split(regex, s.lower()) if i not in stop])

def fix_titles(df):
    new_df = df.copy()
    new_df['Commodity Title'] = new_df['Commodity Title'].apply(lambda x: remove_punc_stopwords_lower(x))
    return new_df

# add occupation major, minor, and broad groups. Major > minor > broad in "generalization"
def get_groupings(df, group):
    zeroes = 3
    if group == "broad":
        add = 1
    elif group == "minor":
        add = 3
    elif group == "major":
        add = 4
    column = df['O*NET-SOC Code'].apply(lambda x: x[:-(zeroes + add)] + add*'0')
    return column

def assign_groupings(df):
    new_df = df.copy()
    for group in ['broad', 'minor', 'major']:
        new_df[group+"_group"] = get_groupings(new_df, group)
    return new_df

def add_group_titles(df):
    add_broad = df.merge(broad_groups, how = 'left', on = 'broad_group')
    add_minor = add_broad.merge(minor_groups, how = 'left', on = 'minor_group')
    add_major = add_minor.merge(major_groups, how = 'left', on = 'major_group')
    return add_major

def add_group_info(df):
    occ_ref = add_group_titles(occ_ref)
    just_titles = occ_ref[['O*NET-SOC Code', 'broad_title', 'minor_title', 'major_title']]
    return df.merge(just_titles, how = 'left', on = 'O*NET-SOC Code')

# Information on adopting companies
def get_adopting_companies(now, old):
    columns = ['O*NET-SOC Code', 'O*NET-SOC Title', 'Commodity Code', 'Commodity Title', 'T2 Example']
    def just_tech_title(df):
        return df[columns]
    tech_now = just_tech_title(now)
    tech_old = just_tech_title(old)
    master_df = pd.DataFrame(columns = now.columns)
    for occ in tech_now['O*NET-SOC Code'].unique():
        new_group_tech = set(tech_now[tech_now['O*NET-SOC Code'] == occ]['Commodity Code'].unique())
        old_group_tech = set(tech_old[tech_old['O*NET-SOC Code'] == occ]['Commodity Code'].unique())
        adopted_tech = list(new_group_tech - old_group_tech)
        adopted_tech_df = tech_now[(tech_now['Commodity Code'].isin(adopted_tech)) & (tech_now['O*NET-SOC Code'] == occ)]
        master_df = master_df.append(adopted_tech_df)
    return master_df

all_adoptions = get_adopting_companies(tt15, tt9)
