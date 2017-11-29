import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from time import gmtime, strftime

full_data = pd.read_pickle('full_data.pickle')
sns.set_context("paper")
sns.set_style("darkgrid")
plt.figure(figsize=(13, 7))
pp = sns.pointplot(data=full_data, y="uniques", x='samples_to_select', hue="max_occurrences",
                   dodge=True)

pp.set(xlabel='Samples', ylabel='Occurrences', title= 'Rare sOTU')
tmp = pp.set_xticklabels(pp.get_xticklabels(), rotation=90)
pp.set_ylim(0,)

fig = pp.get_figure()
fig.savefig("novelty_%s.png" % strftime("%y%m%d_%H%M%S", gmtime()))
