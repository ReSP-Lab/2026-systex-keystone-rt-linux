import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.colors as mcolors

def load(name, start_skip = 0, skiprows=9):
    
    data = pd.read_table(
        name,
        sep=":",
        names=["Thread", "Interval", "Latency"],
        
        skiprows=skiprows,
    )

    if start_skip > 0:
        data = data.iloc[start_skip:]

    print(f"Data loaded: {name}")

    print(f'\tN:\t{len(data["Latency"])}')
    print(f'\tAvg:\t{data["Latency"].mean()}')
    print(f'\tStd:\t{data["Latency"].std()}')
    print(f'\t95th:\t{data["Latency"].quantile(q=0.95)}')
    print(f'\tMax:\t{data["Latency"].max()}')
    return data


def draw_hist(datas, labels=None, alphas=None, alpha=0.8, bins=50, unit='us', x_log = True, bin_edges=None, grayscale=False):
    # Extract data, colors, hatches from dicts
    data_list = [d['data'] for d in datas]
    colors = [d['color'] for d in datas]

    plt.rcParams.update({
        'font.size': 20,           # Base font size
        'axes.labelsize': 22,      # Axis labels
        'axes.titlesize': 22,      # Title
        'xtick.labelsize': 20,     # X-axis tick labels
        'ytick.labelsize': 20,     # Y-axis tick labels
        'legend.fontsize': 20,     # Legend
        'figure.titlesize': 24     # Figure title
    })

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.set_palette(sns.color_palette(colors))

    datas_plot = []

    for i, data in enumerate(data_list):
        data_temp = data.copy()
        if unit.lower() == 'ms':
            data_temp["Latency"] = data_temp["Latency"] / 1000
        datas_plot.append(data_temp)

    if unit.lower() == 'ms':
        unit_label = "Latency (ms)"
    else:  # default to microseconds
        unit_label = "Latency (μs)"
        
    min_sample_size = min(len(datas_plot[i]["Latency"]) for i in range(len(datas_plot)))     
    combined_min = min(datas_plot[i]["Latency"].min() for i in range(len(datas_plot)))
    combined_max = max(datas_plot[i]["Latency"].max() for i in range(len(datas_plot)))

    if bin_edges is None:
        if x_log:
            bin_edges = np.logspace(np.log10(combined_min), np.log10(combined_max), bins + 1)
        else:
            bin_edges = np.linspace(combined_min, combined_max, bins + 1)

    if alphas is None:
        alphas = [1.0 if i==0 else alpha for i in range(len(datas))]

    if labels == None:
        labels = [f"dataset_{i}" for i in range(len(datas))]

    if grayscale:
        # Convert colors to grayscale equivalents
        gray_colors = []
        for c in colors:
            rgb = mcolors.to_rgb(c)
            # Use luminance formula for grayscale
            gray = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            gray_colors.append((gray, gray, gray))
        colors = gray_colors

    for i in range(len(datas)):
        normalization_factor = len(datas_plot[i]["Latency"]) / min_sample_size
        
        counts, _ = np.histogram(datas_plot[i]["Latency"], bins=bin_edges)
        normalized_counts = counts / normalization_factor
        
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_width = bin_edges[1:] - bin_edges[:-1]
        ax.bar(
            bin_centers,
            normalized_counts,
            width=bin_width, 
            color=colors[i],
            label=labels[i],
            alpha=alphas[i]
        )
    
    ax.set_yscale("log")
    if x_log:
        ax.set_xscale("log")
    ax.set_xlabel(unit_label, fontsize=22)
    ax.set_ylabel("Count", fontsize=22)
    if len(datas) > 1:
        ax.legend(fontsize=20)


    ax.tick_params(axis='both', which='major', labelsize=18)
    
    return ax

def save(ax, name, path):
    fig = ax.get_figure()
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    fig.savefig(f"{path}/{name}.png", dpi=1200, bbox_inches='tight')
    print(f"Figure saved: {name}.png")

if __name__ == "__main__":

    # Global parameters
    result_dir = "results"
    figure_dir = f"{result_dir}/figures"
    colors = [ "#163F5F", "#4793CA", "#C56824", "#FFCB9F", "#572F37", "#CC6D6F", "#38736B", "#B6DDD8"]

    # Loading data
    print("--- Loading data ---")

    ## Hifive Unmtached
    data_hifive_unmatched_stock = {'data':load(f"{result_dir}/hifive_unmatched/stock/hifive_unmatched_stock_cyclictest.log", start_skip=1000), "color":colors[0]}
    data_hifive_unmatched_rt = {'data':load(f"{result_dir}/hifive_unmatched/realtime/hifive_unmatched_realtime_cyclictest.log", start_skip=1000), "color":colors[1]}
    
    ## Keystone mixted
    data_keystone_mixted_stock = {'data':load(f"{result_dir}/keystone_mixted/stock/keystone_mixted_stock_cyclictest.log", start_skip=1000), "color":colors[2]}
    data_keystone_mixted_rt = {'data':load(f"{result_dir}/keystone_mixted/realtime/keystone_mixted_realtime_cyclictest.log", start_skip=1000), "color":colors[3]}

    ## Enclave startup
    data_keystone_enclave_startup = {'data':load(f"{result_dir}/enclave-startup.log", start_skip=0,skiprows=0), "color":"#477E3E"}

    ## Keystone hybrid
    data_keystone_hybrid_1_stock = {'data':load(f"{result_dir}/keystone_hybrid/stock/keystone_hybrid_stock_1_cyclictest.log", start_skip=0), "color":colors[4]}
    data_keystone_hybrid_1_rt = {'data':load(f"{result_dir}/keystone_hybrid/realtime/keystone_hybrid_realtime_1_cyclictest.log", start_skip=0), "color":colors[5]}
    data_keystone_hybrid_2_stock = {'data':load(f"{result_dir}/keystone_hybrid/stock/keystone_hybrid_stock_2_cyclictest.log", start_skip=0), "color":colors[6]}
    data_keystone_hybrid_2_rt = {'data':load(f"{result_dir}/keystone_hybrid/realtime/keystone_hybrid_realtime_2_cyclictest.log", start_skip=0), "color":colors[7]}
   
    # Generating graph
    print("--- Generating Graphs ---")

    ax = draw_hist(datas=[data_hifive_unmatched_stock, data_hifive_unmatched_rt], labels= [f"stock",f"preempt-rt"])
    save(ax, f"linux_stock_vs_realtime_normalized", figure_dir) 
    
    ax = draw_hist(datas=[data_keystone_mixted_stock, data_keystone_mixted_rt], labels=[f"stock", f"preempt-rt"])
    save(ax, f"keystone_mixted_stock_vs_realtime_normalized", figure_dir)

    ax = draw_hist(datas=[data_hifive_unmatched_rt, data_keystone_mixted_rt], labels=[f"w/o keystone", f"w/ keystone"])
    save(ax, f"realtime_linux_vs_keystone_mixted_normalized", figure_dir)

    ax = draw_hist(datas=[data_hifive_unmatched_stock, data_keystone_mixted_stock], labels=[f"w/o keystone", f"w/ keystone"])
    save(ax, f"stock_linux_vs_keystone_mixted_normalized", figure_dir)
    
    ax = draw_hist(datas=[data_keystone_enclave_startup], labels=[f"startup"], bin_edges=np.logspace(np.log10(740000), np.log10(790000), 51))
    save(ax, f"keystone_enclave_startup", figure_dir)

    ax = draw_hist(datas=[data_keystone_hybrid_1_stock, data_keystone_hybrid_1_rt], labels=[f"stock", f"preempt-rt"])
    save(ax, f"keystone_hybrid_stock_vs_realtime_1t_normalized", figure_dir)

    ax = draw_hist(datas=[data_keystone_hybrid_2_stock, data_keystone_hybrid_2_rt], labels=[f"stock", f"preempt-rt"])
    save(ax, f"keystone_hybrid_stock_vs_realtime_2t_normalized", figure_dir)

    ax = draw_hist(datas=[data_keystone_hybrid_1_rt, data_keystone_hybrid_2_rt], labels=[f"1 thread", f"2 threads"])
    save(ax, f"keystone_hybrid_realtime_1t_vs_2t_normalized", figure_dir)

    ax = draw_hist(datas=[data_keystone_hybrid_1_stock, data_keystone_hybrid_2_stock], labels=[f"1 thread", f"2 threads"])
    save(ax, f"keystone_hybrid_stock_1t_vs_2t_normalized", figure_dir)
    
    ax = draw_hist(datas=[data_keystone_mixted_stock, data_keystone_hybrid_1_stock], labels=[f"Linux process", f"Keystone enclave"], alpha=1.0)
    save(ax, f"keystone_stock_mixted_vs_hybrid_normalized", figure_dir)

    ax = draw_hist(datas=[data_keystone_mixted_rt, data_keystone_hybrid_1_rt], labels=[f"Linux process", f"Keystone enclave"], alphas=[0.8, 0.8])
    save(ax, f"keystone_realtime_mixted_vs_hybrid_normalized", figure_dir)

    exit(0)
