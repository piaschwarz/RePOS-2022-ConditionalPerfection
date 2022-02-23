import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import logit
from scipy import stats
from statsmodels.formula.api import logit

if __name__ == '__main__':
    dataframe = pd.read_csv("pilotData_selected.csv", usecols=['item_type', 'item_answer_type', 'response'])
    #print(dataframe)

    # select only rows with the text items
    df = dataframe[dataframe['item_type'] == 'test']
    #print(df)

    # make column 'focus' where all when-q questions get value of 1 (focus) and what-if quations get 0 (non-focus)
    df['focus'] = np.where(df['item_answer_type'] == 'whenq', 1, 0)
    # make column Conditional Perfection which has value 1 when it arises (i.e. the response was 'Nein')
    df['CP'] = np.where(df['response'] == 'Nein', 1, 0)
    res_df = df.copy(deep=True)
    print(df)

    # TODO: sanity checks of data with plotting

    # fit model on data with (focus is independent variable):
    logit_mod = logit("CP ~ focus", res_df).fit()
    print("In the output, ‘Iterations‘ refer to the number of times the model iterates over the data, \n"
          "trying to optimize the model. By default, the maximum number of iterations performed is 35, \n"
          "after which the optimization fails.")
    print(logit_mod.summary())

    print('--- P-Values ----------------')
    print('p-values: ', logit_mod.pvalues)

    print('--- Odds Ratios and 95% Confidence Interval: ----------------')
    odds_ratios = pd.DataFrame(
        {
            "OR": np.exp(logit_mod.params),
            "Lower CI": np.exp(logit_mod.conf_int()[0]),
            "Upper CI": np.exp(logit_mod.conf_int()[1]),
        }
    )
    print(odds_ratios)