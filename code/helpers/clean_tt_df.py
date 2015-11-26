import pandas as pd
import numpy as np
import re

from nltk import stopwords

def remove_punc_stopwords_lower(s):
    """
    INPUT: string
    OUTPUT: string

    removes stopwords from the string and lower-cases the string.
    """
    stop = stopwords.words('english')
    regex = r"\W+"
    return " ".join([i for i in re.split(regex, s.lower()) if i not in stop])

def fix_titles(df):
    """
    INPUT: pandas df
    OUTPUT: pandas df

    Applies remove_punc_stopwords_lower() to relevant O*NET features.
    """

    new_df = df.copy()
    new_df['T2 Example'] = new_df['T2 Example'].apply(lambda x: remove_punc_stopwords_lower(x))
    new_df['Commodity Title'] = new_df['Commodity Title'].apply(lambda x: remove_punc_stopwords_lower(x))
    return new_df

def add_group_codes(df):
    """
    INPUT: df
    OUTPUT: df

    Adds tech hierarchy codes as features in the df.
    """
    new_df = df.copy()
    new_df['segment_code'] = create_codes(new_df, group = 'Segment')
    new_df['class_code'] = create_codes(new_df, group = 'Class')
    new_df['family_code'] = create_codes(new_df, group = 'Family')
    return new_df

def add_group_titles(df, class_codes, family_codes, segment_codes):
    """
    INPUT: df, df, df, df
    OUTPUT: df

    Adds tech hierarchy titles as features in the df.
    """
    new_df = df.copy()
    add_class = new_df.merge(class_codes, how = 'left', on = 'class_code')
    add_family = add_class.merge(family_codes, how = 'left', on = 'family_code')
    final = add_family.merge(segment_codes, how = 'left', on = 'segment_code')
    return final

def full_clean(df, class_codes, family_codes, segment_codes):
    """
    INPUT: df, df, df, df
    OUTPUT: df

    Performs all the above cleaning functions in one pass.
    """
    new_df = df.copy()
    new_df = add_group_codes(fix_titles(new_df))
    new_df = add_group_titles(new_df, class_codes, family_codes, segment_codes)
    return new_df
