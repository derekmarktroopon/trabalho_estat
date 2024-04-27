# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:23:23 2024

@author: Dbm + Dv
"""

#%%

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as seab

#%%

#definição do caminho do usuário do computador
user_directory = os.path.expanduser("~")
#definição da pasta nos dowloads
if 'Downloads' in user_directory: 
    user_directory = user_directory
else: 
    user_directory = os.path.join(user_directory, 'Downloads', 'trabalho_estat')
os.chdir(user_directory)
#definição do path do arquivo excel
tab_cafe= pd.read_excel("GACTT_RESULTS_ANONYMIZED_v2.xlsx") 

# Preenchindo valores faltantes com "NA"
tab_cafe.fillna("NA", inplace=True)

#Deletando variaveis que não entrarao na analise
tab_cafe.drop(['Submission_ID'],axis=1,inplace=True)

#%%

#Pie chart das faixas de idade na amostra
contagem_idades = tab_cafe.What_is_your_age.value_counts()
idades_pie_lab = ['25-34 anos', '35-44 anos', '18-24 anos', '45-54 anos', '55-64 anos', '>65 anos', 'NA', '<18 anos']
plt.pie(contagem_idades, labels = idades_pie_lab, autopct='%.1f%%')

plt.title('Idades dos Respondentes')
plt.tight_layout()  


#%%

#Pie chart das frequencias de ingestão de café por dia
contagem_frequencias_de_beber_cafe = tab_cafe.How_many_cups_of_coffee_do_you_typically_drink_per_day.value_counts()
frquencias_de_beber_pie_lab = ['2 copos por dia', '1 copo por dia', '3 copos por dia', '<1 copo por dia', '4 copos por dia', 'NA', '>4 copos por dia',]
plt.pie(contagem_frequencias_de_beber_cafe, labels = frquencias_de_beber_pie_lab, autopct='%.1f%%')

plt.title('Frequencia de Ingestão de Café')
plt.tight_layout()  

#%%