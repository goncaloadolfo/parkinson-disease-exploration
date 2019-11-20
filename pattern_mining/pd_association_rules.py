"""
Association rules for Parkinson Decease Data Set.
"""

# libs
from sklearn.feature_selection import f_classif

# own libs
from pattern_mining.pattern_mining_functions import *
from utils import print_return_variable
from data_exploration.multi_analysis_functions import put_away_vars


#####
# load data
data = pd.read_csv("../datasets/pd_speech_features.csv")
y = data.pop('class').values

#####
# remove high correlated variables
vars_to_remove = put_away_vars(data.corr(), 0.8)
col_names_to_remove = data.columns[vars_to_remove]
new_df = data.drop(columns=col_names_to_remove)

#####
# pattern mining parameters
print("\n### Pattern mining parameters")
k_features = print_return_variable("Number of features to select: ", 35)
selection_measure = print_return_variable("Feature selection function: ", f_classif)
discretize_function = print_return_variable("Discretize function: ", pd.cut)
bins = print_return_variable("Number of bins: ", 7)
disc_needless_cols = print_return_variable("Variables that doesnt need to be discretize: ", ['gender', 'class'])
min_supp = print_return_variable("Min support: ", 0.6)
fp_mining_args = [min_supp]
min_conf = print_return_variable("Min confidence: ", 0.9)
min_ant_items = print_return_variable("Min of items in antecedents itemset: ", 2)

#####
# extract association rules
selected_features, dummified_df, frequent_patterns, _, rules = pm_system(new_df, y, k_features, selection_measure,
                                                                         discretize_function, bins,
                                                                         disc_needless_cols, fp_mining_args,
                                                                         min_conf, min_ant_items)

#####
# results visualization
print("\n### Selected features")
print("Selected features: ", selected_features)
print("\n### Frequent patterns found (some)")
pretty_print_fsets(frequent_patterns, False, 5)
print("\n### Association rules found (some)")
pretty_print_rules(rules, ['confidence'], False, 10)

fsets_per_supp(dummified_df, np.arange(0.4, 1.001, 0.1))

#####
# exclusive rules between classes
rules_per_class = rules_per_target(dummified_df, y, 0.6, 0.9, 2)

print("#####\n")
print("# Exclusive association rules")
print("numbers of ars found for patients without parkinson decease:", rules_per_class[0].shape[0])
print("numbers of ars found for patients with parkinson decease:", rules_per_class[1].shape[0])

common_ars = rules_per_class[0].merge(rules_per_class[1], how='inner', on=['antecedents', 'consequents'])
