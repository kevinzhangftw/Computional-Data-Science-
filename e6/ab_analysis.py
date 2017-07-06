import pandas as pd
import numpy as np
import sys
from scipy import stats

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)

def getOdduid(uid):
    if (uid % 2 == 1):
        return True
    else:
        return False

def getEvenuid(uid):
    if (uid % 2 == 0):
        return True
    else:
        return False

def getnonzeros(search_count):
    if search_count != 0:
        return True
    else:
        return False

def main():
    searchdata_file = sys.argv[1]
    searches = pd.read_json(searchdata_file, orient='records', lines=True)
    newoption = searches[searches['uid'].apply(getOdduid)]
    oldoption = searches[searches['uid'].apply(getEvenuid)]
    newoptioninstr = newoption[newoption['is_instructor']]
    oldoptioninstr = oldoption[oldoption['is_instructor']]
    
    utestMoreSearchs = stats.mannwhitneyu(newoption['search_count'], oldoption['search_count'])
    utestMoreInstrSearchs = stats.mannwhitneyu(newoptioninstr['search_count'], oldoptioninstr['search_count'])

    newoptionNo0s= newoption[newoption['search_count'].apply(getnonzeros)]
    oldoptionNo0s= oldoption[oldoption['search_count'].apply(getnonzeros)]    
    contingency = [[len(newoptionNo0s), len(oldoptionNo0s)], 
                   [len(newoption) - len(newoptionNo0s), len(oldoption) - len(oldoptionNo0s)]]
    chi2, p, dof, expected = stats.chi2_contingency(contingency)

    newinstroptionNo0s= newoptioninstr[newoptioninstr['search_count'].apply(getnonzeros)]
    oldinstroptionNo0s= oldoptioninstr[oldoptioninstr['search_count'].apply(getnonzeros)]
    contingencyinstr = [[len(newinstroptionNo0s), len(oldinstroptionNo0s)], 
                   [len(newoptioninstr) - len(newinstroptionNo0s), len(newoptioninstr) - len(oldinstroptionNo0s)]]
    chi2i, pi, dofi, expectedi = stats.chi2_contingency(contingencyinstr)


    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=p,
        more_searches_p=utestMoreSearchs.pvalue,
        more_instr_p=pi,
        more_instr_searches_p=utestMoreInstrSearchs.pvalue,
    ))


if __name__ == '__main__':
    main()