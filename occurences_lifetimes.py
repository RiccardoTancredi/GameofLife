import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
from scipy.optimize import curve_fit
import matplotlib as mpl
from matplotlib import cm

# Logistic regression of populations
def f2(x, K, r):
    x0 = df_res['occupancy'].iloc[0]
    return (K*x0*np.exp(r*x))/(K+x0*(np.exp(x*r)-1))

f2v = np.vectorize(f2)

def consecutive(data, stepsize=1):    
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

pattern_period = {"block" : 1, "bee_hive" : 1, "loaf" : 1, "boat" : 1, "ship" : 1, "tub" : 1, "pond" : 1, "blinker" : 1, "toad" : 2, "beacon" : 2, "glider":4}


folder_name = 'data/'
all_dim = [[i, i] for i in [15, 20, 25, 30, 35, 40]]
all_seed = list(range(100, 200)) 
native = 37.5 
all_native = [native]
graph = True
iterations = 500
list_iterations = list(range(iterations))      # This is useful when decomposing the dataframe

patterns = ['block', 'bee_hive', 'loaf', 'boat', 'ship', 'tub', 'pond', 'blinker', 'toad', 'beacon', 'glider']
others = ['heat', 'occupancy']
columns = patterns + others

# Analysis of occupancies and heats

# tuples = [(str(dim), str(native)) for dim in all_dim]
# index = pd.MultiIndex.from_tuples(tuples, names=['dimension', 'natives'])
index = [(str(dim)) for dim in all_dim]
all_freq, all_lives = [], []
K, r, K_err, r_err = [], [], [], []
for dim in all_dim:
    df = pd.DataFrame(columns=columns)
    for seed in all_seed:
        file_name = folder_name+str(dim[0])+"_"+str(dim[1])+"/"+str(seed)+'.csv'
        df_tmp = pd.read_csv(file_name, sep=';', skiprows=[0], names=columns, header=None)
        for col in df_tmp.columns:
            df_tmp[col] = df_tmp[col].apply(lambda x: ast.literal_eval(str(x)))
        df = pd.concat([df, df_tmp], ignore_index=True)
    
    # Analysis of occupancies and heats
    n = len(all_seed)
    df_per_native = df[others]
    df_res = pd.DataFrame([((lambda z: df_per_native.loc[z:df.shape[0]:iterations])(z)).mean() for z in list_iterations])     # In this way we average on same time for different seeds
    if graph:
        popt, pcov = curve_fit(f2, list_iterations, df_res['occupancy'])
        print(f"We get K = {popt[0]}, with error = {np.sqrt(pcov[0][0])}")
        K.append(popt[0])
        K_err.append(np.sqrt(pcov[0][0]))
        print(f"We get r = {popt[1]}, with error = {np.sqrt(pcov[1][1])}")
        r.append(popt[1])
        r_err.append(np.sqrt(pcov[1][1]))
        plt.rcParams['text.usetex'] = True
        plt.title(f"dim = {dim}")
        plt.plot(df_res['occupancy'], label=r'$\langle$Occupancy$\rangle$', color='tab:blue')
        plt.plot(list_iterations[1:], df_res['heat'].iloc[1:], label=r'$\langle$Heat$\rangle$', ls='--', alpha=0.8, color='tab:orange')
        plt.plot(f2v(list_iterations, popt[0], popt[1]), label='Fit', color='tab:cyan')
        plt.xlabel('Time')
        plt.ylabel(r'$\langle$ f(t) $\rangle$')
        plt.legend(loc='best')
        plt.grid()
        plt.tight_layout()
        plt.savefig('plots/'+str(dim[0])+"_"+str(dim[1])+'.png', bbox_inches='tight', dpi=300)
        plt.show()
        print("Plot Saved!")
    
    # Analysis of frequencies 
    frequencies, lives = [], []
    for col in patterns:
        keep_track = []
        df_frequencies = df[col]
        df_frequencies = df_frequencies[df_frequencies != 0].dropna()
        freq = 0
        for i in range(df_frequencies.shape[0]):
            element = df_frequencies.iloc[i]
            
            for sub_element in element:
                freq += 1
                chir, rot, x, y = sub_element
                keep_track.append([x, y, chir, rot, df_frequencies.index[i]])      
        df_keep_track = pd.DataFrame(keep_track, columns=['x', 'y', 'chir', 'rot', 'time'])
        
        unique_lists_in_items = df_keep_track.groupby(['x', 'y', 'chir'])['time'].apply(consecutive, stepsize=pattern_period[col])  # .to_numpy()
        freq_live = 0
        life = []
        # Analysis of average lives
        for k in range(len(unique_lists_in_items)):
            tmp = unique_lists_in_items.iloc[k]
            freq_live += len(tmp)
            for j in range(len(tmp)):
                life.append(len(tmp[j]))
                    
        frequencies.append(freq)
        lives.append(sum(life)/freq_live)

    all_freq.append(frequencies)
    all_lives.append(lives)
    print(f"Dimension: {dim}")

df_final = pd.DataFrame(all_freq, index=index, columns=patterns)
df_final.index.name = 'dimension'
print(df_final)

df_lives = pd.DataFrame(all_lives, index=index, columns=patterns)
df_lives.index.name = 'dimension'
print(df_lives)

rows = [df_final.iloc[i].sum() for i in range(len(all_dim))]
df_final2 = df_final/np.array(rows).reshape(len(rows), -1)
print(df_final2)

print(df_final2.to_markdown())

to = np.array([df_final2['block'].values, df_final2['blinker'].values, df_final2['bee_hive'].values, df_final2['loaf'].values, df_final2['boat'].values, df_final2['tub'].values, df_final2['pond'].values, df_final2['ship'].values, df_final2['toad'].values, df_final2['beacon'].values])

df_print = pd.DataFrame(data=to.T, columns=['block', 'blinker', 'bee_hive', 'loaf', 'boat', 'tub', 'pond', 'ship', 'toad', 'beacon'])

df_print = pd.DataFrame(to.T, index=index, columns=['block', 'blinker', 'bee_hive', 'loaf', 'boat', 'tub', 'pond', 'ship', 'toad', 'beacon'])
df_print.index.name = 'dimension'

print(df_print.to_markdown())
# df_print.mean(axis=0)

subpat = ['block', 'blinker', 'bee_hive', 'loaf', 'boat', 'tub', 'pond', 'ship', 'toad', 'beacon']

fig, ax = plt.subplots(ncols=5, nrows=2, figsize=(25, 14))
my_colors = [(x/10.0, x/20.0, 0.4) for x in range(df_final2.shape[1]-1)]
my_cmap = cm.get_cmap('viridis')
rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
labels = [str(dim) for dim in all_dim]
for j in range(2):
    for i in range(5):
        offset = (i+1)*(j+1)*25
        ax[j, i].bar(df_print.index, df_print[subpat[i+5*j]], label='Dimensions', color=my_cmap(i+5*j+offset)) #(0.2, 0.4, 0.6, 0.6)
        ax[j, i].set_title(subpat[i+5*j])
        ax[j, i].xaxis.set_ticks(list(range(6)))
        ax[j, i].set_xticklabels(labels)
plt.tight_layout()
plt.savefig('plots/'+"all_all"+'.png', bbox_inches='tight', dpi=300)
plt.show()

K = np.array(K)
K_err = np.array(K_err)
r = np.array(r)
r_err = np.array(r_err)
a = 1+r
x_star = r/(r+1)
# x_star*K*np.array([225, 400, 325, 900, 1225, 1600])


# How K scales with dimensions
mpl.style.use('default')
x_lab = [str(i) for i in all_dim]
def f(x, a, b, c):
    return a*x**2+b*x+c
f1 = np.vectorize(f)
popt2, pcov2 = curve_fit(f, [15, 20, 25, 30, 35, 40], K)
x = [15, 20, 25, 30, 35, 40]
plt.scatter(x_lab, K, label='K', color='xkcd:azure')
plt.errorbar(x_lab, K, K_err, fmt='|', capsize=15, ecolor='c')
x_f = np.linspace(start=15, stop=40, num=100)
x = np.linspace(start=0, stop=5, num=100)
plt.plot(x, f1(x_f, popt2[0], popt2[1], popt2[2]), label='Fit', color='xkcd:sky blue')
# plt.xticks(ticks=x_lab)
plt.ylabel('K')
plt.xlabel('Dimension')
plt.legend()
plt.grid(True)
plt.savefig('plots/'+"K"+'.png', dpi=300)
plt.show()
