import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

def consecutive(data, stepsize=1):    
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)


folder_name = 'data/'
all_dim = [[i, i] for i in [15, 20, 25, 30, 35, 40]]
all_seed = list(range(100, 200)) 
native = 37.5 
all_native = [native]
graph = False
iterations = 500
list_iterations = list(range(iterations))      # This is useful when decomposing the dataframe

patterns = ['block', 'bee_hive', 'loaf', 'boat', 'ship', 'tub', 'pond', 'blinker', 'toad', 'beacon', 'glider']
others = ['heat', 'occupancy']
columns = patterns + others

# Analysis of occupancies and heats

tuples = [(str(dim), str(j)) for dim in all_dim for j in all_native]
index = pd.MultiIndex.from_tuples(tuples, names=['dimension', 'native'])
all_freq = []
for dim in all_dim:
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
    df_res = pd.DataFrame([((lambda z: df_per_native.loc[z:df.shape[0]:iterations])(z)).mean() for z in list_iterations])     # In this way we average on same time for different seeds
    frequencies = []
    for col in patterns:
        keep_track = []
        df_frequencies = df[col]
        df_frequencies = df_frequencies[df_frequencies != 0]
        
        for i in range(df_frequencies.shape[0]):
            element = df_frequencies.iloc[i]
            
            for sub_element in element:
                chir, rot, x, y = sub_element
                keep_track.append([dim[0]*x+y, df_frequencies.index[i]])
            
        df_keep_track = pd.DataFrame(keep_track, columns=['xy', 'time'])
        unique_lists_in_items = df_keep_track.groupby(['xy'])['time'].apply(consecutive).to_numpy()
        freq = 0
        for k in range(unique_lists_in_items.shape[0]):
            freq += len(unique_lists_in_items[k])
        # print(unique_lists_in_items)
        # arr_unique = set(unique_lists_in_items)
        # for var in arr_unique:
        #     filtered = consecutive(df_keep_track[df_keep_track['xy'] == var]['time'], stepsize=pattern_period[col])
        frequencies.append(freq)

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

df_final = pd.DataFrame(all_freq, index=index, columns=patterns)#/len(all_seed)/iterations
print(df_final)