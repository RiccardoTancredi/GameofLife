import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

folder_name = 'data/'
all_dim = [[i, i] for i in [15, 18]] # ToDo
all_seed = [123, 124] # ToDo
all_native = [40, 50] # ToDo
graph = False
iterations = 100 # ToDo
x = list(range(iterations))      # This is useful when decomposing the dataframe

patterns = ['block', 'bee_hive', 'loaf', 'boat', 'tub', 'blinker', 'toad', 'beacon', 'pulsar', 'glider']
others = ['heat', 'occupancy']
columns = ['block', 'bee_hive', 'loaf', 'boat', 'tub', 'blinker', 'toad', 'beacon', 'pulsar', 'glider', 'heat', 'occupancy']

# Analysis of occupancies and heats

tuples = [(str(dim), str(j)) for dim in all_dim for j in all_native]
index = pd.MultiIndex.from_tuples(tuples, names=['dimension', 'native'])
all_freq = []
for dim in all_dim:
    for native in all_native:
        df = pd.DataFrame(columns=columns)
        for seed in all_seed:
            file_name = folder_name+str(dim[0])+"_"+str(dim[1])+"/"+str(native)+"_"+str(seed)+'.csv'
            df_tmp = pd.read_csv(file_name, sep=';', skiprows=[0], names=columns, header=None)
            for col in df_tmp.columns:
                df_tmp[col] = df_tmp[col].apply(lambda x: ast.literal_eval(str(x)))
            df = pd.concat([df, df_tmp], ignore_index=True)
        
        # Analysis of occupancies and heats
        n = len(all_seed)
        df_per_native = df[others]
        df_res = pd.DataFrame([((lambda z: df_per_native.loc[z:df.shape[0]:iterations])(z)).mean() for z in x])     # In this way we average on same time for different seeds
        frequencies = []
        for col in patterns:
            df_frequencies = df[col]
            df_frequencies = df_frequencies[df_frequencies != 0]
            if df_frequencies.shape[0] != 0:
                freq = len(df_frequencies.sum())
                frequencies.append(freq)
            else:
                frequencies.append(0)
        
        all_freq.append(frequencies)

        if graph:
            plt.title(f"dim = {dim}, native = {native}")
            plt.plot(df_res['occupancy'], label=f'mean occupancy')
            plt.plot(df_res['heat'], label=f'mean heat')
            plt.xlabel('Time')
            plt.ylabel('Data')
            plt.legend(loc='best')
            plt.grid()
            plt.show()

df_final = pd.DataFrame(all_freq, index=index, columns=patterns)/len(all_seed)/iterations
print(df_final)
for col in patterns:
    ax = df_final[col].unstack(level=0).plot(kind='bar', subplots=True, title=[col, col], figsize=(9, 7), xlabel='Natives', ylabel='Relative Frequencies')#, layout=(2, 2))
    plt.tight_layout()
    plt.show()