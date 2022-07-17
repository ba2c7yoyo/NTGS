# NTGS
NTGS is a tool for NGS and TGS taxonomic composition result visualization. User only need to prepare the composition result (.csv) from EasyMAP (Qiime2, NGS) or Mothur (TGS) output file. This tool can plot the Top10 / Top20 in any taxonomic rank.

## 1-1 TopN abundance by NGS 
### Top10_abundance_NGS.py

- Import Package

```python
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
```
- Parameters

``` python
path = './fireant220710/'
#The folder path

file_name = 'level-7.csv'  
#NGS composition result in level-7 (.csv) after classifier analysis.

int_last_cloumn = -1 
#The number of column you want to ignore. (Because there are some group information in EasyMAP output.)
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

	```
And remember to comment this line :
	``` python
	df.plot(kind="bar",stacked=True,figsize=(10,8), cmap= 'tab20')
	```

	- Save the figure automatically
	Instead of copy the result on IDE plots window, you can uncomment this line to save the results automatically.
	 ``` python
	 plt.savefig( Target_PNG_name +'_Top' + str(TOPTOP) + '_' + level_legend[hierarchy] + '.png',dpi=150,bbox_inches ='tight')
	 ```

## 1-2 TopN abundance by TGS
### Top10_abundance_TGS.py

- Import Package

```python
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
```

- Parameters

```python
path = './'
#The folder path

file_name = 'fire_ant.opti_mcc.shared'  
#TGS composition result after classifier analysis.

file_name_taxa = 'fire_ant.opti_mcc.0.01.cons.taxonomy'
#TGS composition result after classifier analysis.

int_topN = 15 
#Range on Top2~20

```
- Input file 1 - TGS composition result (.shared)

![TGS_.shared](https://user-images.githubusercontent.com/81002817/179384401-4193b8c0-c73e-42c8-858d-ec78275fe759.png)

- Input file 2 - TGS composition result (.taxonomy)

![TGS_.taxonomy](https://user-images.githubusercontent.com/81002817/179384415-c3fb9aff-f343-43ac-8e13-8df3287761b6.png)

- Output figures
	- Top20 taxonomic result in Family level.

![TGS_Eg.1](https://user-images.githubusercontent.com/81002817/179384177-98f7b2dd-c0aa-4563-8df2-60cc8fd59932.png)

