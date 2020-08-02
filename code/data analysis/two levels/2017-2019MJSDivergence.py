import numpy as np
import sys
# import torch
import array
import math
import pandas as pd
# from d2lsource.GetMySQLConnection import GetMySQLConnection
from scipy.stats import entropy as H
def get_score_2017_2018_2020(text):
    index=text.index('Rating:###')
    index1=int(index)+len('Rating:###')
    str=text[index1:len(text)]
    index2=str.index(':')+index1

    return text[index1:index2]
def get_review_level_2017_2018_2020(text):
    index = text.index('Confidence:###')
    index1 = int(index) + len('Confidence:###')
    str = text[index1:len(text)]
    index2 = str.index(':') + index1

    return text[index1:index2]
def get_score_2019(text):
    return text[0:text.index(':')]
def get_review_level_2019(text):
    return text[0:text.index(':')]

def JSD(prob_distributions, weights, logbase=2):
    # left term: entropy of mixture
    wprobs = weights * prob_distributions
    mixture = wprobs.sum(axis=0)
    entropy_of_mixture = H(mixture, base=logbase)

    # right term: sum of entropies
    entropies = np.array([H(P_i, base=logbase) for P_i in prob_distributions])
    wentropies = weights * entropies
    # wentropies = np.dot(weights, entropies)
    sum_of_entropies = wentropies.sum()

    divergence = entropy_of_mixture - sum_of_entropies
    return(divergence)
import scipy.stats
def JS_divergence(p,q):
    M=(p+q)/2
    return 0.5*scipy.stats.entropy(p, M)+0.5*scipy.stats.entropy(q, M)
def get_dis(list1,list2):
    total=[]
    for line in list1:
        if line not in total:
            total.append(line)
    for line in list2:
        if line not in total:
            total.append(line)
    import numpy as np
    return_list1=np.zeros(len(total))
    return_list2=np.zeros(len(total))
    for line in list1:
        return_list1[total.index(line)]+=1
    for line in list2:
        return_list2[total.index(line)]+=1
    return return_list1/np.sum(return_list1),return_list2/np.sum(return_list2)

def get_review_level(text):
    if text=='Experience Assessment:###I do not know much about this area.':
        return '1'
    elif text=='Experience Assessment:###I have read many papers in this area.':
        return '2'
    elif text=='Experience Assessment:###I have published one or two papers in this area.':
        return '3'
    elif text=='Experience Assessment:###I have published in this field for several years.':
        return '4'
    else:
        print("error")
import math
def get_log(num):

    return float(math.log(num,2))


# connection=GetMySQLConnection('localhost' , 'root' , 'root' , 'openreviewuseddata',3307)
# original_data_2017=connection.selectDb("select  A,L,M from tp_2017conference")
# original_data_2018=connection.selectDb("select  A,L,M from tp_2018conference_final")
# original_data_2019=connection.selectDb("select  A,L,M from tp_2019conference_final")

import pandas as pd
import os
data_2017=pd.read_excel(os.path.abspath('../../../data/Data analysis/data/tp_2017conference.xlsx'),sheet_name='tp_2017conference')
data_2018=pd.read_excel(os.path.abspath('../../../data/Data analysis/data/tp_2018conference.xlsx'),sheet_name='tp_2018conference')
data_2019=pd.read_excel(os.path.abspath('../../../data/Data analysis/data/tp_2019conference.xlsx'),sheet_name='tp_2019conference')
original_data_2017=data_2017[['A','L','M']].values.tolist()
original_data_2018=data_2018[['title','confidence','rate']].values.tolist()
original_data_2019=data_2019[['title','Confidence','rate']].values.tolist()

# original_data_2020=data[['title','reviewer_level','paper_score']].values.tolist()


# print(len(title_2020))

situations_list=[
    [1,2],
    [1,3],
    [1,4],
    [1,5],
    [2,3],
    [2,4],
    [2,5],
    [3,4],
    [3,5],
    [4,5]
]




for situation in situations_list:
    MJS=[]
    sample_one = []
    sample_two = []
    total = []
    counter=0
    sum_total=0
    title_2017 = [original_data_2017[0][0]]
    for line in original_data_2017:
        if line[0] not in title_2017:
            title_2017.append(line[0])
    for line in title_2017:
        distribution_before_original_1 = []
        distribution_before_original_2 = []

        for single_data in original_data_2017:
            if line==single_data[0]:
                if int(get_review_level_2017_2018_2020(single_data[1]))==situation[0]:
                    distribution_before_original_1.append(int(get_score_2017_2018_2020(single_data[2])))
                elif int(get_review_level_2017_2018_2020(single_data[1]))==situation[1]:
                    distribution_before_original_2.append(int(get_score_2017_2018_2020(single_data[2])))
        if len(distribution_before_original_1)>0 and len(distribution_before_original_2)>0:
            counter+=1
            sum_total+=len(distribution_before_original_1)
            sum_total+=len(distribution_before_original_2)


            
            avg_1=np.mean([int(i) for i in distribution_before_original_1])
            avg_2=np.mean([int(i) for i in distribution_before_original_2])
            avg_total=np.mean([int(i) for i in distribution_before_original_1+distribution_before_original_2])
            # for line in distribution_before_original_1:
            MJS.append(avg_1 * get_log(avg_1 / avg_total))
            # for line in distribution_before_original_2:
            MJS.append(avg_2 * get_log(avg_2 / avg_total))
    title_2018 = [original_data_2018[0][0]]
    for line in original_data_2018:
        if line[0] not in title_2018:
            title_2018.append(line[0])
    for line in title_2018:
        distribution_before_original_1 = []
        distribution_before_original_2 = []

        for single_data in original_data_2018:
            if line == single_data[0]:
                if int(get_review_level_2017_2018_2020(single_data[1])) == situation[0]:
                    distribution_before_original_1.append(int(get_score_2017_2018_2020(single_data[2])))
                elif int(get_review_level_2017_2018_2020(single_data[1])) == situation[1]:
                    distribution_before_original_2.append(int(get_score_2017_2018_2020(single_data[2])))
        if len(distribution_before_original_1) > 0 and len(distribution_before_original_2) > 0:
            counter += 1
            sum_total += len(distribution_before_original_1)
            sum_total += len(distribution_before_original_2)
            avg_1 = np.mean([int(i) for i in distribution_before_original_1])
            avg_2 = np.mean([int(i) for i in distribution_before_original_2])
            avg_total = np.mean([int(i) for i in distribution_before_original_1 + distribution_before_original_2])
            # for line in distribution_before_original_1:
            MJS.append(avg_1 * get_log(avg_1 / avg_total))
            # for line in distribution_before_original_2:
            MJS.append(avg_2 * get_log(avg_2 / avg_total))

    title_2019 = [original_data_2019[0][0]]
    for line in original_data_2019:
        if line[0] not in title_2019:
            title_2019.append(line[0])
    for line in title_2019:
        distribution_before_original_1 = []
        distribution_before_original_2 = []

        for single_data in original_data_2019:
            if line == single_data[0]:
                if int(get_review_level_2019(single_data[1])) == situation[0]:
                    distribution_before_original_1.append(int(get_score_2019(single_data[2])))
                elif int(get_review_level_2019(single_data[1])) == situation[1]:
                    distribution_before_original_2.append(int(get_score_2019(single_data[2])))
        if len(distribution_before_original_1) > 0 and len(distribution_before_original_2) > 0:
            counter += 1
            sum_total += len(distribution_before_original_1)
            sum_total += len(distribution_before_original_2)
            avg_1 = np.mean([int(i) for i in distribution_before_original_1])
            avg_2 = np.mean([int(i) for i in distribution_before_original_2])
            avg_total = np.mean([int(i) for i in distribution_before_original_1 + distribution_before_original_2])
            # for line in distribution_before_original_1:
            MJS.append(avg_1 * get_log(avg_1 / avg_total))
            # for line in distribution_before_original_2:
            MJS.append(avg_2 * get_log(avg_2 / avg_total))
    # total.append([i for i in list(set(sample_one))])
    if len(MJS)>0:
        print(situation)
        print(np.sum(MJS)/(2*counter))
        print(counter)
        print(sum_total)
        print("###########")
    else:
        print(situation)
        print("not exists")
        print("###########")
























