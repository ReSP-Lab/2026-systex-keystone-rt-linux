import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os

def load(name, cpu=4, start_skip = 0):
    
    data = pd.read_table(
        name,
        sep=":",
        names=["Thread", "Interval", "Latency"],
        
        skiprows=9,
    )

    if start_skip > 0:
        data = data.iloc[start_skip:]

    print(f'Avg:\t{data["Latency"].mean()}')
    print(f'Std:\t{data["Latency"].std()}')
    print(f'95th:\t{data["Latency"].quantile(q=0.95)}')
    print(f'Max:\t{data["Latency"].max()}')
    return data

def vals(data):
    lat = data["Latency"]
    return {"Min": lat.min(), "Avg": lat.mean(), "Max": lat.max(), "Std": lat.std()}

def plt_setup():
    plt.rcParams.update({
        'font.size': 16,           # Base font size
        'axes.labelsize': 18,      # Axis labels
        'axes.titlesize': 18,      # Title
        'xtick.labelsize': 16,     # X-axis tick labels
        'ytick.labelsize': 16,     # Y-axis tick labels
        'legend.fontsize': 16,     # Legend
        'figure.titlesize': 20     # Figure title
    })

def draw_single_hist(data, label=None, bins=100, colors = ['#3498db', '#e67e22'], unit='us', x_log = False):
    
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.set_palette(sns.color_palette(colors))

    # Convert based on unit
    data_plot = data.copy()

    if unit.lower() == 'ms':
        data_plot["Latency"] = data_plot["Latency"] / 1000
        unit_label = "Latency (ms)"
    else:  # default to microseconds
        unit_label = "Latency (μs)"

    if x_log:
        bin_edges = np.logspace(np.log10(data_plot["Latency"].min()), np.log10(data_plot["Latency"].max()), bins + 1)
    else:
        bin_edges = np.linspace(data_plot["Latency"].min(), data_plot["Latency"].max(), bins + 1)
    
    sns.histplot(data=data_plot, 
                 x="Latency",
                 bins=bin_edges,
                 color=colors[1],
                 label=label)
    
    ax.set_yscale("log")
    if x_log:
        ax.set_xscale("log")
    ax.set_xlabel(unit_label, fontsize=18)
    ax.set_ylabel("Count", fontsize=18)
    ax.legend(fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)

    return ax

def draw_dual_hist(data1, data2, label1="Dataset 1", label2="Dataset 2", bins=100, colors = ['#3498db', '#e67e22'], unit='us', x_log = False):

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.set_palette(sns.color_palette(colors))

    # Convert based on unit
    data1_plot = data1.copy()
    data2_plot = data2.copy()

    if unit.lower() == 'ms':
        data1_plot["Latency"] = data1_plot["Latency"] / 1000
        data2_plot["Latency"] = data2_plot["Latency"] / 1000
        unit_label = "Latency (ms)"
    else:  # default to microseconds
        unit_label = "Latency (μs)"

    combined_min = min(data1_plot["Latency"].min(), data2_plot["Latency"].min())
    combined_max = max(data1_plot["Latency"].max(), data2_plot["Latency"].max())

    if x_log:
        bin_edges = np.logspace(np.log10(combined_min), np.log10(combined_max), bins + 1)
    else:
        bin_edges = np.linspace(combined_min, combined_max, bins + 1)
    
    # Plot first histogram
    sns.histplot(data=data1_plot,
                 x="Latency",
                 bins=bin_edges,
                 color=colors[0],
                 label=label1,
                 ax=ax)
    
    # Plot second histogram on the same axes
    sns.histplot(data=data2_plot,
                 x="Latency",
                 bins=bin_edges,
                 color=colors[1] if len(colors) > 1 else 'orange',
                 label=label2,
                 alpha=0.6,
                 ax=ax)
    
    
    ax.set_yscale("log")
    if x_log:
        ax.set_xscale("log")
    ax.set_xlabel(unit_label, fontsize=18)
    ax.set_ylabel("Count", fontsize=18)
    ax.legend(fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    
    return ax

def draw_hist(datas, labels=None, alphas=None, bins=100, colors = ['#3498db', '#e67e22', "#22e62c"], unit='us', x_log = False):
    plt.rcParams.update({
        'font.size': 16,           # Base font size
        'axes.labelsize': 18,      # Axis labels
        'axes.titlesize': 18,      # Title
        'xtick.labelsize': 16,     # X-axis tick labels
        'ytick.labelsize': 16,     # Y-axis tick labels
        'legend.fontsize': 16,     # Legend
        'figure.titlesize': 20     # Figure title
    })
    

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.set_palette(sns.color_palette(colors))

    datas_plot = []

    for i, data in enumerate(datas):
        data_temp = data.copy()
        if unit.lower() == 'ms':
            data_temp["Latency"] = data_temp["Latency"] / 1000
        datas_plot.append(data_temp)

    if unit.lower() == 'ms':
        unit_label = "Latency (ms)"
    else:  # default to microseconds
        unit_label = "Latency (μs)"
        

    combined_min = min(datas_plot[i]["Latency"].min() for i in range(len(datas_plot)))
    combined_max = max(datas_plot[i]["Latency"].max() for i in range(len(datas_plot)))

    if x_log:
        bin_edges = np.logspace(np.log10(combined_min), np.log10(combined_max), bins + 1)
    else:
        bin_edges = np.linspace(combined_min, combined_max, bins + 1)

    if alphas == None:
        alphas = [0.8 for _ in range(len(datas))]

    if labels == None:
        labels = [f"dataset_{i}" for i in range(len(datas))]

    for i in range(len(datas)):

        sns.histplot(data=datas_plot[i],
                    x="Latency",
                    bins=bin_edges,
                    color=colors[i],
                    label=labels[i],
                    alpha=alphas[i],
                    ax=ax)
    
    
    ax.set_yscale("log")
    if x_log:
        ax.set_xscale("log")
    ax.set_xlabel(unit_label, fontsize=18)
    ax.set_ylabel("Count", fontsize=18)
    ax.legend(fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    
    return ax

def save(ax, name, path):
    fig = ax.get_figure()
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)  # Better than mkdir
    fig.savefig(f"{path}/{name}.png", dpi=1200, bbox_inches='tight')

if __name__ == "__main__":

    x_log = True
    figure_dir = "results/figures"

    # Hifive Unmtached
    print(f'--- Linux ---')
    print(" stock")
    data_hifive_unmatched_stock = load(f"results/hifive_unmatched/stock/hifive_unmatched_stock_cyclictest.log", cpu=4, start_skip=1000)
    print(" realtime")
    data_hifive_unmatched_rt = load(f"results/hifive_unmatched/realtime/hifive_unmatched_realtime_cyclictest.log", cpu=4, start_skip=1000)

    ax = draw_hist(datas=[data_hifive_unmatched_stock, data_hifive_unmatched_rt], labels= [f"stock",f"preempt-rt"], bins=50, unit='us', x_log=x_log)
    save(ax, f"linux_stock_vs_realtime", figure_dir)
    ax.clear()


    # Keystone mixted
    print(f'--- keystone Mixted ---')
    print(" stock")
    data_keystone_mixted_stock = load(f"results/keystone_mixted/stock/keystone_mixted_stock_cyclictest.log", cpu=4, start_skip=1000)
    print(" realtime")
    data_keystone_mixted_rt = load(f"results/keystone_mixted/realtime/keystone_mixted_realtime_cyclictest.log", cpu=4, start_skip=1000)

    ax = draw_hist(datas=[data_keystone_mixted_stock, data_keystone_mixted_rt], labels=[f"stock", f"preempt-rt"], bins=50, unit='us', x_log=x_log)
    save(ax, f"keystone_mixted_stock_vs_realtime", figure_dir)
    ax.clear()

    ax = draw_hist(datas=[data_hifive_unmatched_rt, data_keystone_mixted_rt], labels=[f"w/o keystone", f"w/ keystone"], bins=50, unit='us', x_log=x_log)
    save(ax, f"realtime_linux_vs_keystone_mixted", figure_dir)
    ax.clear()

    # Keystone hybrid
    print(f'--- keystone Hybrid ---')
    print(" stock")
    data_keystone_hybrid_1_stock = load(f"results/keystone_hybrid/stock/keystone_hybrid_stock_1_cyclictest.log", cpu=1, start_skip=0)
    print(" realtime 1th")
    data_keystone_hybrid_1_rt = load(f"results/keystone_hybrid/realtime/keystone_hybrid_realtime_1_cyclictest.log", cpu=1, start_skip=0)
    print(" realtime 2th")
    data_keystone_hybrid_2_rt = load(f"results/keystone_hybrid/realtime/keystone_hybrid_realtime_2_cyclictest.log", cpu=2, start_skip=0)

    ax = draw_hist(datas=[data_keystone_hybrid_1_stock, data_keystone_hybrid_1_rt], labels=[f"stock", f"preempt-rt"], bins=50, unit='ms', x_log=x_log)
    save(ax, f"keystone_hybrid_stock_vs_realtime_1t", figure_dir)
    ax.clear()

    ax = draw_hist(datas=[data_keystone_hybrid_1_rt, data_keystone_hybrid_2_rt], labels=[f"preempt-rt (1th)", f"preempt-rt (2 th)"], bins=50, unit='ms', x_log=x_log)
    save(ax, f"keystone_hybrid_realtime_1t_vs_2t", figure_dir)
    ax.clear()

    ax = draw_hist(datas=[data_keystone_mixted_stock, data_keystone_hybrid_1_stock], labels=[f"Linux process", f"Keystone enclave"], bins=50, unit='ms', x_log=x_log)
    save(ax, f"keystone_stock_mixted_vs_hybrid", figure_dir)
    ax.clear()

    ax = draw_hist(datas=[data_keystone_mixted_rt, data_keystone_hybrid_1_rt], labels=[f"Linux process", f"Keystone enclave"], bins=50, unit='ms', x_log=x_log)
    save(ax, f"keystone_realtime_mixted_vs_hybrid", figure_dir)
    ax.clear()

    

    exit(0)