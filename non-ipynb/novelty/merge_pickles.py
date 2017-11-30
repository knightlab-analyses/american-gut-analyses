import pandas as pd
from os import listdir

fd = 'pickles/'
fps = ['%s%s' % (fd, f) for f in listdir(fd) if f.startswith('samples_to_select')]
 
full_data = pd.read_pickle(fps.pop())
for f in fps:
    data = pd.read_pickle(f)
    full_data = pd.concat([full_data, data], axis=0)

full_data.to_pickle('full_data.pickle')
