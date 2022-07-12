# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 13:12:48 2022
@author: ZHAOQI
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
'''Tips:
    1.注意如果是Top20 會改成TOP19 因為顏色關係20與21會撞色
    2.分組情況最後幾行要處理-1,-2,-3,-4之類，倒數幾個要從這裡調整
    這檔案會一次自動出七個階層
    3.Colormap 客製化在259行
'''
path = './fireant220710/'
file_name = 'level-7.csv'  
int_last_cloumn = -1 #倒數幾個要從這裡調整

def single_dict (sample_names)   :  
    sum_sample_abundance = []
    a = 0
    for each_sample in sample_names:
        if a == 0 : #因為第一次沒有陣列要跟他相加
            # sum_sample_abundance = np.add( sample_dict[each_sample]['counts'], sum_sample_abundance )#得到abundance list
            sum_sample_abundance = sample_dict[each_sample]['counts']
        else : 
            sum_sample_abundance = [a + b for a, b in zip(sample_dict[each_sample]['counts'], sum_sample_abundance)]
        a+=1    
    return sum_sample_abundance

sample_dict = {}
#taxa_array = otu_id
with open (path + file_name, 'r') as otu_abundances:
    otu_id = otu_abundances.readline().split(',')[1:int_last_cloumn] #跳掉1, 倒數幾個要從這裡調整
    otu_id[-1] = otu_id[-1].replace('\n','') #最後有換行符號
    for line in otu_abundances.readlines():                         
        sample_name = line.split(',')[0] #取樣本名
        abundance = line.split(',')[1:int_last_cloumn] #跳掉1，倒數幾個要從這裡調整
        abundance[-1] = abundance[-1].replace('\n','') #最後有換行符號
        abundance = [int(float(x)) for x in abundance] #把元素內的字串變成int
        sample_dict.update({
            sample_name : {
                "counts" : abundance
                }
            })
# sample_dict
# {'1': {'counts': [0, 0, 14, 90, 0, 0, 0, 746, 44]}
taxa_dict = {}
a = 0
strip1 = 'D_'
strip2 = '__'
for otu in otu_id:
    
    tmp_levels = otu.split(';')
    taxa_dict.update({
    'OTU' + str(a) : []
    })
    b = 0 
    for tmp_level in tmp_levels :
        
        if b == 6 : #處理種層級D5+D6合併
            # taxa_dict['OTU' + str(a)].append(taxa_dict['OTU' + str(a)][5] + ' ' + tmp_level.strip(strip1 + str(b) + strip2) )
            try:
                taxa_dict['OTU' + str(a)].append(taxa_dict['OTU' + str(a)][5] + ' ' + tmp_level.split('__')[1])
            except :
                taxa_dict['OTU' + str(a)].append(taxa_dict['OTU' + str(a)][5] + ' ' + tmp_level.strip(strip1 + str(b) + strip2) )
                
            # taxa_dict['OTU' + str(a)].append(tmp_level)
        else :
            try:
            # taxa_dict['OTU' + str(a)].append(tmp_level.strip(strip1 + str(b) + strip2) )
                taxa_dict['OTU' + str(a)].append(tmp_level.split('__')[1] )
            except:
                taxa_dict['OTU' + str(a)].append(tmp_level.strip(strip1 + str(b) + strip2) )
                
            # taxa_dict['OTU' + str(a)].append(tmp_level)
        b+=1
    a += 1
# taxa_dict
# 'OTU1': ['D_0__Bacteria',
# 'D_1__Actinobacteria',
# 'D_2__Actinobacteria',
# 'D_3__Bifidobacteriales',
# 'D_4__Bifidobacteriaceae',
# 'D_5__Bifidobacterium',
# 'D_6__uncultured bacterium'],
    
    
'''輸入 START'''    
try:
    sample_name_counts = int(input("Sample_name_counts ?"))
    sample_names = []
    for i in range (sample_name_counts):
        sample_names.append(input("Sample Name (" + str(i+1) + "):"))
except :
    sample_name_counts = 5
    sample_names = []
    for i in range(5) :
        sample_names.append(str(i+1))
    
# hierarchy = int(input("Hierarchy :"))
hierarchys = [0,1,2,3,4,5,6]   #自動跑出0~6
Target_PNG_name = input("File name?")
TOPTOP = int(input("Top?"))
if TOPTOP == 20:
    TOPTOP = 19
'''輸入 END'''
for hierarchy in hierarchys :
    '''取得綜合排名 START''' 
    total_each_sample_counts = []
    prerank_dict = {}
    sum_sample_abundance = single_dict(sample_names)
    a = -1
    for each_sum_sample_abundance in sum_sample_abundance :
        a += 1
        target_hierarchy_name = taxa_dict['OTU' + str(a)][hierarchy]#找到taxa_dict中指定階層的名稱
        if each_sum_sample_abundance == 0 : #總和0就不要紀錄了
            prerank_dict.update({
            target_hierarchy_name : 0
            })
        else :
            # target_hierarchy_name = taxa_dict['OTU' + str(a)][hierarchy] 
            if target_hierarchy_name in prerank_dict.keys() :
                prerank_dict[target_hierarchy_name] += each_sum_sample_abundance
            else:
                prerank_dict.update({
                    target_hierarchy_name : each_sum_sample_abundance
                    })
    
        # total_sample_counts.append(sum(tmp_dict.values()))
        
    rank_dict = {k: v for k, v in sorted(prerank_dict.items(), key=lambda item: item[1], reverse=True)}
    if 'Unassigned' in rank_dict.keys():
        del rank_dict['Unassigned']
        
    if '__' in rank_dict.keys():
        del rank_dict['__']
        
    if '' in rank_dict.keys(): 
        del rank_dict['']
        
    if ' ' in rank_dict.keys(): 
        del rank_dict[' ']    
        
    if 'uncultured bacterium uncultured bacterium' in rank_dict.keys(): 
        del rank_dict['uncultured bacterium uncultured bacterium']   
        
    if 'uncultured' in rank_dict.keys(): 
        del rank_dict['uncultured']   
        
    if 'uncultured uncultured bacterium' in rank_dict.keys(): 
        del rank_dict['uncultured uncultured bacterium']   
         
    if 'uncultured bacterium' in rank_dict.keys(): 
        del rank_dict['uncultured bacterium']   
    
    
    # rank_dict = 
    # {'D_5__Bacteroides': 1548, 'D_5__Enterorhabdus': 139, 'D_5__Adlercreutzia': 14}
    
    for sample_name in sample_names : 
        a = 0
        for each_sample_abundance in sample_dict[sample_name]['counts'] :
            a += int(each_sample_abundance)
        total_each_sample_counts.append(a) #取得每個樣本總條數
        
        
        # pre_plot_dict.update({    #
        #     sample_name : tmp_dict
        #     })   
    # total_each_sample_counts 
    # [894, 859]
        
    '''取得綜合排名 END'''
    
    
    '''取得Top10 START''' 
    Top_10_array = []
    a = 0
    for key in rank_dict.keys() :
        if a >= TOPTOP :    #決定TOP多少
            break
        else :
            Top_10_array.append(key)
            a+=1
    # print(Top_10_array) 
    # ['D_5__Bacteroides', 'D_5__Enterorhabdus', 'D_5__Adlercreutzia']
    '''取得Top10 END'''
    
    '''抓Sample Top10 data START'''
    tmp_top10_otu_id = []
    for each_otu in taxa_dict : #把每個OTU抓出來
        for each_top10_array in Top_10_array :      
            if each_top10_array in taxa_dict[each_otu][hierarchy] : #看看這個階層裡面有沒有這傢伙
                tmp_top10_otu_id.append(each_otu.strip('OTU')) #如果有就記錄到tmp_top10_otu_id
            # 接下來要把他的key拿去丟sample_dict
    pre_plot_dict = {}
    for each_sample_name in sample_names :
        pre_plot_dict.update({
            each_sample_name : {}
            })
    for each_sample_name in sample_names : #一個一個SAMPLE跳進去
        for each_tmp_top10_otu_id in tmp_top10_otu_id : #一個一個符合的OTU編號進來 tmp_top10_otu_id = ['9','13','25','41','54']
            bacteria_name = taxa_dict['OTU'+ each_tmp_top10_otu_id][hierarchy]
            try:
            # if bacteria_name in pre_plot_dict[each_sample_name] : #如果這樣本裡面已經有了
                pre_plot_dict[each_sample_name][bacteria_name] += sample_dict[each_sample_name]['counts'][int(each_tmp_top10_otu_id)]
            except :
                pre_plot_dict[each_sample_name].update({
                     bacteria_name : sample_dict[each_sample_name]['counts'][int(each_tmp_top10_otu_id)] 
                     })
        
    '''抓Sample Top10 data END'''
    
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
                    round((pre_plot_dict[each_sample_name][each_Top10_species]/total_each_sample_counts[a])*100,4)
                    )
                # plot_dict['Others'].append(
                    
                #     )
            except :
                plot_dict[each_Top10_species].append(
                    0
                    )            
        a+=1
        
    # pre_plot_dict = 
    # {'Dax_1': {'Dyella koreensis': 4763, 'Bartonella apis': 2699}}
    '''準備圖要的格式 END'''
    '''增加Others START''' 
    plot_dict.update({'Others' : []})        
    for i in range(len(sample_names)) :
        total_abundance = 0
        # print(i)
        for each_Top10_species in Top_10_array :
            total_abundance += plot_dict[each_Top10_species][i]
        if 100-total_abundance <0 :
            plot_dict['Others'].append(0)  
        else :
            plot_dict['Others'].append(100-total_abundance)  
        
    '''增加Others END'''     
        
    df=pd.DataFrame(plot_dict,index=sample_names)
    # custom_colors = "rgcbyrgcbyy"
    cmap = ListedColormap(["#D0D0D0", "#ff9694", "#2ca02c", "#ffbb78","#D0D0D0",
                            "#c7c7c7","#ff7f0e","#D0D0D0","#D0D0D0","#dada8b",
                            "#D0D0D0","#7f7f7f","#D0D0D0","#D0D0D0","#D0D0D0",
                            "#D0D0D0","#D0D0D0","#9edae5","#e274c1","#D0D0D0",
                            ])
    # df.plot(kind="bar",stacked=True,figsize=(10,8), cmap= 'tab20')
    df.plot(kind="bar",stacked=True,figsize=(10,8), cmap= cmap)
    level_legend = ['Kingdom01',
                    'Phylum02',
                    'Class03',
                    'Order04',
                    'Family05',
                    'Genus06',
                    'Species07']
    plt.legend(loc="upper left",bbox_to_anchor=(1.05, 1.0), fontsize="x-large",title=level_legend[hierarchy],title_fontsize=16)
    plt.xlabel('Sample Name')
    plt.ylabel('Abundance (%)')
    
    # plt.legend(loc="upper left")
    Target_PNG_name = './' + Target_PNG_name
    # plt.savefig( Target_PNG_name +'_Top' + str(TOPTOP) + '_' + level_legend[hierarchy] + '.png' ,dpi=150,bbox_inches ='tight')
    plt.show()