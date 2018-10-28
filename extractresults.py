import matplotlib as mpl
mpl.use('Agg')
import argparse
import os, json, pickle, yaml
import numpy
import hashlib
import tabulate

from ann_benchmarks import results
from ann_benchmarks.algorithms.definitions import get_algorithm_name
from ann_benchmarks.datasets import get_dataset
from ann_benchmarks.plotting.utils  import  compute_metrics, compute_all_metrics

import xlsxwriter
import re


def convert_color(color):
    r, g, b, a = color
    return "rgba(%(r)d, %(g)d, %(b)d, %(a)d)" % {
            "r" : r * 255, "g" : g * 255,  "b" : b * 255 , "a" : a}

def convert_linestyle(ls):
    new_ls = {}
    for algo in ls.keys():
        algostyle = ls[algo]
        new_ls[algo] = (convert_color(algostyle[0]), convert_color(algostyle[1]),
                algostyle[2], point_styles[algostyle[3]])
    return new_ls

def get_run_desc(properties):
    return "%(dataset)s_%(count)d_%(distance)s" % properties

def get_dataset_from_desc(desc):
    return desc.split("_")[0]

def get_count_from_desc(desc):
    return desc.split("_")[1]

def get_distance_from_desc(desc):
    return desc.split("_")[2]

def get_dataset_label(desc):
    return get_dataset_from_desc(desc) + " (k = " + get_count_from_desc(desc) + ")"


def create_xls(result):
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()
    array_items = [['algorithm', 'dataset', 'type', 'macchina', 'docker_image',
                'commit', 'date of commit', 'k-nn', 'epsilon',
                'largeepsilon', 'rel', 'qps', 'build',
                'candidates', 'indexsize', 'queryssize',
                 'dataset_items', 'float_tree']]

    info_ = str(result)
    temp_ = re.split(r'(:\s{)|(}\)],\s)' , info_)    
    algorithm_ = temp_[0]
    algorithm_ = algorithm_[2:len(algorithm_)-1]
    split_by_dataset = temp_[1:]
    for dataset_test in split_by_dataset:
        try:
           dataset_ = re.findall('^\'.{1,50}\:\s', dataset_test)[0]
        except:
           continue
        dataset_ = dataset_[1:len(dataset_)-3]
        split_by_test = re.split('[(]\'[\w]*\',', dataset_test)[1:]

        for test_ in split_by_test:
            items_ = []
            items_.append(algorithm_) #1.algorithm
            items_.append(dataset_) #2.dataset

            type_ = re.findall(r'type=.*,metric', test_)[0]
            type_ = type_[5:len(type_)-7]
            items_.append(type_) #3.type
            float_tree = "float tree" in test_

            #campi vuoti (commit, image-id...)
            items_.append('') #machine
            items_.append('') #image
            items_.append('') #commit
            items_.append('') #date

            test_ = test_.split("k-nn")[1]
            results_ = re.findall(r'(?:\d+[.]?\d+|\sinf\,)', test_)
            print("xx results",results)
            for val in results_ :
                items_.append(val) #?
            # for missing
            for qq in range(len(results_),7):
                items_.append("")

            #campi vuoto (data_items)
            items_.append('') 
            items_.append("TRUE" if float_tree else "FALSE")

    for row in range(0, len(array_items)):
        for col in range(0,len(array_items[0])):
             try:
                worksheet.write(row, col, array_items[row][col])
             except:
                continue
    workbook.close()
    print("file result.xlsx created")

def load_all_results():
    """Read all result files and compute all metrics"""
    all_runs_by_dataset = {'batch' : {}, 'non-batch': {}}
    all_runs_by_algorithm = {'batch' : {}, 'non-batch' : {}}
    cached_true_dist = []
    old_sdn = None
    for properties, f in results.load_all_results():
        sdn = get_run_desc(properties)
        if sdn != old_sdn:
            dataset = get_dataset(properties["dataset"])
            cached_true_dist = list(dataset["distances"])
            old_sdn = sdn
        algo = properties["algo"]
        ms = compute_all_metrics(cached_true_dist, f, properties)
        algo_ds = get_dataset_label(sdn)
        idx = "non-batch"
        if properties["batch_mode"]:
            idx = "batch"
        all_runs_by_algorithm[idx].setdefault(algo, {}).setdefault(algo_ds, []).append(ms)
        all_runs_by_dataset[idx].setdefault(sdn, {}).setdefault(algo, []).append(ms)

    return (all_runs_by_dataset, all_runs_by_algorithm)

if __name__ == "__main__":
	import pprint
	runs_by_ds, runs_by_algo = load_all_results()
	pprint.pprint(runs_by_algo)
        #    print(k,"\n",tabulate.tabulate(v))
	create_xls(runs_by_algo);
