import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import inquirer
import argparse
import os

def load(name, cpu=4):
    
    data = pd.read_table(
        name,
        sep=":",
        names=["Thread", "Interval", "Latency"],
        
        skiprows=cpu+3,
    )

    print(f'Avg:\t{data["Latency"].mean()}')
    print(f'Std:\t{data["Latency"].std()}')
    print(f'95th:\t{data["Latency"].quantile(q=0.95)}')
    print(f'Max:\t{data["Latency"].max()}')
    return data

def vals(data):
    lat = data["Latency"]
    return {"Min": lat.min(), "Avg": lat.mean(), "Max": lat.max(), "Std": lat.std()}

colors = ['#3498db', '#e67e22']  # Bright blue, Orange
sns.set_palette(sns.color_palette(colors))

bins = 100

def save(plot, name, path):
    fig = plot.get_figure()
    if not os.path.isdir(path):
        os.mkdir(path)
    fig.savefig(f"{path}/{name}.png", dpi=600, bbox_inches='tight')

def draw_hist(data):
    plot = sns.histplot(data=data, 
                         x="Latency",
                         bins=bins,
                         #binrange=(0, 20000),
                         #log_scale=[False, True],  # AP: this triggers a bug on my machine
                         color=colors[1])
    plot.set_yscale("log")
    plot.set_xlabel("Latency (μs)")
    return plot

if __name__ == "__main__":


    """boards = ["beaglev_fire", "hifive_unmatched", "raspberrypi5_original_method"]
    kernels = ["realtime"]
    cpu = 4

    for board in boards:
        for kernel in kernels:
            target_path = f"targets/{board}/{kernel}"
            print(f'--- {board} - {kernel} ---')
            data = load(f"{target_path}/logs/cyclictest.log", cpu)
            plot = draw_hist(data)
            save(plot, f"{board}_{kernel}", "images")
            plot.clear()

    exit(0)"""

    

    
    questions = [
        inquirer.Text('target_name', message="Enter the target name", default="hifive_unmatched"),
        inquirer.Text('target_type', message="Enter the target type", default="stock"),
        inquirer.Text('cpu', message="Enter the number of CPUs", default="4"),
    ]
    answers = inquirer.prompt(questions)
    args = argparse.Namespace(**answers)
    args.cpu = int(args.cpu)

    target_path = f"targets/{args.target_name}/{args.target_type}"

    data = load(f"{target_path}/logs/cyclictest.log", args.cpu)
    plot = draw_hist(data)
    #plot.set_title(f"{args.target_name}\n{args.target_type}")
    save(plot, f"{args.target_name}_{args.target_type}", f"{target_path}/images")
    plt.clf()



