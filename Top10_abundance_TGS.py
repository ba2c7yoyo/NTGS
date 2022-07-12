# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 13:12:48 2022
@author: ZHAOQI
"""
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

path = './'
file_name = 'fire_ant.opti_mcc_avg.shared'
file_name_taxa = 'fire_ant.opti_mcc.0.01.cons.taxonomy'
int_topN = 15 #決定TopN

def single_dict (sample_name, hierarchy)   :  
    a = 0
    target_dict = {}
    for each_abundance in sample_dict[sample_name]['counts'] :
        if int(each_abundance)!=0: #條數為0不計算
            key_otu_id = sample_dict['otu_id'][a] #找每一個otu代號
            value_hierarchy = taxa_dict[key_otu_id][hierarchy]#找到該otu代號的某一階層 0~6
            if value_hierarchy in target_dict.keys() :
                target_dict[value_hierarchy] += int(each_abundance)
            else :
                target_dict.update({
                    value_hierarchy : int(each_abundance)
                    })
        a+=1  
    return target_dict


sample_dict = {}
with open (path + file_name, 'r') as otu_abundances:
    otu_id = otu_abundances.readline().split('\t')[3:] #跳掉0, 1, 2
    otu_id[-1] = otu_id[-1].replace('\n','') #最後有換行符號
    for line in otu_abundances.readlines():                         
        sample_name = line.split('\t')[1] #取樣本名
        abundance = line.split('\t')[3:] #跳掉0, 1, 2
        abundance[-1] = abundance[-1].replace('\n','') #最後有換行符號
        sample_dict.update({
            sample_name : {
                "counts" : abundance
                }
            })
    sample_dict.update({ 
                "otu_id" : otu_id
            })
    

taxa_dict = {}
with open (path + file_name_taxa, 'r') as taxas :
    for line in taxas.readlines():
        otu_taxa_id = line.split('\t')[0] #otu代號
        taxa_dict.update({ otu_taxa_id : [] }) 
        
        tmps = line.split('\t')[2].split(';')
        if len(tmps)>5 :
            tmps[-2] =  tmps[-3].strip('g__') +' '+ tmps[-2].strip('s__5')
        for tmp in tmps :
            if tmp != '\n' :
                taxa_dict[otu_taxa_id].append(re.sub(r'\([^)]*\)','',tmp))  #階層
                
    # del taxa_dict['OTU']

'''輸入 START'''    
sample_name_counts = int(input("Sample_name_counts ?"))
sample_names = []
for i in range (sample_name_counts):
    sample_names.append(input("Sample Name (" + str(i+1) + "):"))
hierarchy = int(input("Hierarchy :"))
'''輸入 END''' 


'''取得綜合排名 START''' 
prerank_dict = {}
pre_plot_dict = {}
total_sample_counts = []
for sample_name in sample_names :
    tmp_dict = single_dict(sample_name,hierarchy)
    pre_plot_dict.update({
        sample_name : tmp_dict
        })
    X, Y = Counter(tmp_dict),Counter(prerank_dict)
    prerank_dict = dict (X+Y)
    
    total_sample_counts.append(sum(tmp_dict.values()))
    
rank_dict = {k: v for k, v in sorted(prerank_dict.items(), key=lambda item: item[1], reverse=True)}
'''取得綜合排名 END'''
 
'''取得Top10 START''' 
Top_10_array = []
a = 0
for key in rank_dict.keys() :
    if a >= int_topN :
        break
    else :
        Top_10_array.append(key)
        a+=1

# print(Top_10_array) 
'''取得Top10 END'''
    
'''準備圖要的格式 START''' 
# employees=["Rudra","Alok","Prince","Nayan","Reman"]
plot_dict = {}
for Top10 in Top_10_array :   #把前十名的物種秀出
    plot_dict.update({
        Top10 : []
        })
#把每一個物種的各豐富度秀出
a = 0
for each_sample_name in sample_names : #樣本

    for each_Top10_species in Top_10_array : #物種
        try :
            plot_dict[each_Top10_species].append(
                round(pre_plot_dict[each_sample_name][each_Top10_species]/total_sample_counts[a],2)
                )
            # plot_dict['Others'].append(
                
            #     )
        except :
            plot_dict[each_Top10_species].append(
                0
                )            
    a+=1
'''準備圖要的格式 END'''
'''增加Others START''' 
plot_dict.update({'Others' : []})        
for i in range(len(sample_names)) :
    total_abundance = 0
    # print(i)
    for each_Top10_species in Top_10_array :
        total_abundance += plot_dict[each_Top10_species][i]
    plot_dict['Others'].append(1-total_abundance)  
'''增加Others END'''     
    
df=pd.DataFrame(plot_dict,index=sample_names)
# custom_colors = "rgcbyrgcbyy"

df.plot(kind="bar",stacked=True,figsize=(10,8), colormap= 'tab20')
plt.legend(loc="upper left",bbox_to_anchor=(1.05, 1.0), fontsize="x-large")
# plt.legend(loc="upper left")

plt.show()
    
# '''畫圖拉 END''' 
# print(str(sample_name_counts) + "//" + str(hierarchy))
# print(sample_name)
# print(sample_dict)   
# print(taxa_dict)     
 
