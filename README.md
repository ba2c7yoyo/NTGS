# NTGS
NTGS is a tool for NGS and TGS taxonomic composition result visualization. User only need to prepare the composition result (.csv) from EasyMAP (Qiime2, NGS) or Mothur (TGS) output file. This tool can plot the Top10 / Top20 in any taxonomic rank.

## 1-1 TopN abundance by NGS 
### TopN_abundance_NGS.py

- Import / Install Package

```bash
pip install pandas matplotlib
```
- Parameters

``` python
path = './examples/'
#The folder path

file_name = 'level-7.csv'  
#NGS composition result in level-7 (.csv) after classifier analysis.

int_last_cloumn = -4 
#The number of column you want to ignore. (Because there are some group information in EasyMAP output.)
```
- Example name list

```bash
1
2
3
4
5
6
7
8
9
10
H_J
H_J_01_03
H_J_07_09
H_J_13_15
H_J_19_21
H_J_P
H_J_P_01_03
H_J_P_07_09
H_J_P_13_15
H_J_P_19_21
HFD
HFD_01_03
HFD_07_09
HFD_13_15
HFD_19_21
ND
ND_01_03
ND_07_09
ND_13_15
ND_19_21
```
- Taxonomic Hierarchy

```
1 : Kingdom
2 : Phylum
3 : Class
4 : Order
5 : Family
6 : Genus
7 : Specices
```

- Input file - NGS composition result (.csv)
In this example, you can set the ```int_last_cloumn = -4```, because there are 4 columns about the group and sample information, not taxonomic abundance.

![Input file](https://user-images.githubusercontent.com/81002817/179383739-ac797212-2376-4688-b992-cdb32e53ede1.png "Input file")

- Output figures

	- Top10 taxonomic result in Order level.
![Example1](https://user-images.githubusercontent.com/81002817/179384383-3ddad4d7-29e0-4727-9e25-0a7d132298c8.png)

	- Top20 taxonomic result in Family level with customize color bar.
![Example2](https://user-images.githubusercontent.com/81002817/179384367-efb9bed5-0d86-4462-91f8-9fe713c99103.png)

- Advanced parameters
	- Config the color bar
	If you would like to customize each bacteria color bar, just uncomment these codes to edit it. The camp array length is up to select Top10/Top20.
	``` python
	cmap = ListedColormap(["#D0D0D0", "#ff9694", "#2ca02c", "#ffbb78","#D0D0D0",
                            "#c7c7c7","#ff7f0e","#D0D0D0","#D0D0D0","#dada8b",
                            "#D0D0D0","#7f7f7f","#D0D0D0","#D0D0D0","#D0D0D0",
                            "#D0D0D0","#D0D0D0","#9edae5","#e274c1","#D0D0D0",
                            ])
	df.plot(kind="bar",stacked=True,figsize=(10,8), cmap= cmap)
	
	#df.plot(kind="bar",stacked=True,figsize=(10,8), cmap= 'tab20')
	#Remember to comment this line.

	```

	- Save the figure automatically
	Instead of copy the result on IDE plots window, you can uncomment this line to save the results automatically.
	
	 ``` python
	 plt.savefig( Target_PNG_name +'_Top' + str(TOPTOP) + '_' + level_legend[hierarchy] + '.png',dpi=150,bbox_inches ='tight')
	 ```

## 1-2 TopN abundance by TGS
### TopN_abundance_TGS.py

- Import / Install Package

```bash
pip re collections pandas matplotlib
```

- Parameters

```python
path = './examples/'
#The folder path

file_name = 'opti_mcc.shared'  
#TGS composition result after classifier analysis.

file_name_taxa = 'opti_mcc.0.01.cons.taxonomy'
#TGS composition result after classifier analysis.

int_topN = 15 
#Range on Top2~20

```

- Example name list

```bash
Dax_1
Dax_2
Dax_3
Guan_1
Guan_2
Guan_3
H50_1
Hua_1
Hua_2
Hua_3
San_1
Zhu_1
Zhu_2
Zhu_3
Z
D
H
G
```

- Taxonomic Hierarchy

```
0 : Kingdom
1 : Phylum
2 : Class
3 : Order
4 : Family
5 : Genus
6 : Specices
```

- Input file 1 - TGS composition result (.shared)

![TGS_.shared](https://user-images.githubusercontent.com/81002817/179384401-4193b8c0-c73e-42c8-858d-ec78275fe759.png)

- Input file 2 - TGS composition result (.taxonomy)

![TGS_.taxonomy](https://user-images.githubusercontent.com/81002817/179384415-c3fb9aff-f343-43ac-8e13-8df3287761b6.png)

- Output figures
	- Top20 taxonomic result in Family level.

![TGS_Eg.1](https://user-images.githubusercontent.com/81002817/179384177-98f7b2dd-c0aa-4563-8df2-60cc8fd59932.png)

