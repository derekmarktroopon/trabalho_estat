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
plt.figure(figsize=(6,6))
plt.pie(contagem_idades, labels=[f'{label}\n({value})' for label, value in zip(idades_pie_lab, contagem_idades)], autopct='%.1f%%')

plt.title('Idades dos Respondentes')
plt.tight_layout()  


#%%

#Pie chart das frequencias de ingestão de café por dia
contagem_frequencias_de_beber_cafe = tab_cafe.How_many_cups_of_coffee_do_you_typically_drink_per_day.value_counts()
frquencias_de_beber_pie_lab = ['2 copos por dia', '1 copo por dia', '3 copos por dia', '<1 copo por dia', '4 copos por dia', 'NA', '>4 copos por dia',]
total_de_respostas = sum(contagem_frequencias_de_beber_cafe)
plt.figure(figsize=(6,6))
plt.pie(contagem_frequencias_de_beber_cafe, labels=[f'{label}\n({value})' for label, value in zip(frquencias_de_beber_pie_lab, contagem_frequencias_de_beber_cafe)], autopct='%.1f%%')

plt.title('Frequencia de Ingestão de Café')
plt.tight_layout()  

#%%
mapping_trocadevalores = {
    'NA': 0,
    'TRUE': 1,
    'True': 1,
    'FALSE': 0,
    'False': 0,
}

#%%
#Onde pessoas tendem ao beber café

#selecionando as colunas necessárias
colunas_para_contagem_locais_de_beber_cafe = [
    'Where_do_you_typically_drink_coffee_At_home',
    'Where_do_you_typically_drink_coffee_At_the_office',
    'Where_do_you_typically_drink_coffee_On_the_go',
    'Where_do_you_typically_drink_coffee_At_a_cafe',
    'Where do you typically drink coffee_None_of_these'
]
#montando numa própria tabela
tabela_contagem_locais_de_beber_cafe = tab_cafe[colunas_para_contagem_locais_de_beber_cafe].copy()
# Convertendo-a em dados binários
tabela_contagem_locais_de_beber_cafe.replace(mapping_trocadevalores, inplace=True)
# Obtendo dummies para as variáveis de local de consumo de café
df_tabela_contagem_locais_de_beber_cafe = pd.DataFrame(tabela_contagem_locais_de_beber_cafe)
frequencias_locais_de_beber_cafe = df_tabela_contagem_locais_de_beber_cafe.sum(axis=0)

#Criação do gráfico bar - respostas de multípula escolha
rotulos_locais_de_beber_cafe = [
    'Em casa',
    'No Trabalho',
    'Em movimento',
    'No cafeteria',
    'Nenhuma desses'
]
plt.figure(figsize=(10,4))
total_responses = row_count = tab_cafe.shape[0]
plt.bar(rotulos_locais_de_beber_cafe, frequencias_locais_de_beber_cafe)
for i, freq in enumerate(frequencias_locais_de_beber_cafe):
    percentage = (frequencias_locais_de_beber_cafe / total_responses) * 100
    plt.text(i, frequencias_locais_de_beber_cafe, f'{percentage:.1f}%', ha='center', va='bottom')
plt.title('Onde pessoas bebem café')

#%%

#Como pessoas preparem café 

#selecionando as colunas necessárias
colunas_para_contagem_preparacao_de_cafe = [
    'How_do_you_brew_coffee_at_home_Pour_over',
    'How_do_you_brew_coffee_at_home_French_press',
    'How_do_you_brew_coffee_at_home_Espresso',
    'How_do_you_brew_coffee_at_home_Coffee_brewing_machine',
    'How_do_you_brew_coffee_at_home_Pod_or_capsule_machine',
    'How_do_you_brew_coffee_at_home_Instant_coffee',
    'How_do_you_brew_coffee_at_home_Bean-to-cup_machine',
    'How_do_you_brew_coffee_at_home_Cold_brew',
    'How_do_you_brew_coffee_at_home_Coffee_extract',
    'How_do_you_brew_coffee_at_home_Other'
]
#montando numa própria tabela
tabela_contagem_preparacao_de_cafe = tab_cafe[colunas_para_contagem_preparacao_de_cafe].copy()
# Convertendo-a em dados binários
tabela_contagem_preparacao_de_cafe.replace(mapping_trocadevalores, inplace=True)
# Obtendo dummies para as variáveis de local de consumo de café
df_tabela_contagem_preparacao_de_cafe = pd.DataFrame(tabela_contagem_preparacao_de_cafe)
frequencias_preparacao_de_cafe = df_tabela_contagem_preparacao_de_cafe.sum(axis=0)

#Criação do gráfico bar - respostas de multípula escolha
rotulos_preparacao_cafe = [
    'Filtro',
    'Prensa Francesa',
    'Espresso',
    'Cafeteria Italiana',
    'Maquina de Capsula',
    'Café Instantânea',
    'Maquina Bean-to-Cup',
    'Cold Brew',
    'Extrato de Café',
    'Nenhuma desses'
]
plt.figure(figsize=(14,4))
total_responses = row_count = tab_cafe.shape[0]
plt.bar(rotulos_preparacao_cafe, frequencias_preparacao_de_cafe)
for i, freq in enumerate(frequencias_preparacao_de_cafe):
    percentage = (frequencias_preparacao_de_cafe / total_responses) * 100
    plt.text(i, frequencias_preparacao_de_cafe, f'{percentage:.1f}%', ha='center', va='bottom')
plt.xticks(rotation=45)
plt.title('Como pessoas preparam a sua café')

#%%


#Onde pessoas comprama a sua café 

#selecionando as colunas necessárias
colunas_para_contagem_compra_de_cafe = [
    'On_the_go_where_do_you_typically_purchase_coffee_National_chain',
    'On_the_go_where_do_you_typically_purchase_coffee_Local_cafe',
    'On_the_go_where_do_you_typically_purchase_coffee_Drive_thru',
    'On_the_go_where_do_you_typically_purchase_coffee_Specialty_coffee_shop',
    'On_the_go_where_do_you_typically_purchase_coffee__Deli_or_supermarket',
    'On_the_go_where_do_you_typically_purchase_coffee_Other',
]
#montando numa própria tabela
tabela_contagem_compra_de_cafe = tab_cafe[colunas_para_contagem_compra_de_cafe].copy()
# Convertendo-a em dados binários
tabela_contagem_compra_de_cafe.replace(mapping_trocadevalores, inplace=True)
# Obtendo dummies para as variáveis de local de consumo de café
df_tabela_contagem_compra_de_cafe = pd.DataFrame(tabela_contagem_compra_de_cafe)
frequencias_compra_de_cafe = df_tabela_contagem_compra_de_cafe.sum(axis=0)

#Criação do gráfico bar - respostas de multípula escolha
rotulos_compra_de_cafe = [
    'Marca Nacional',
    'Cafeteria local',
    'Drive-thru',
    'Loja de cafés especiais',
    'Supermercado',
    'Nenhuma desses'
]
plt.figure(figsize=(10,4))
total_responses = row_count = tab_cafe.shape[0]
plt.bar(rotulos_compra_de_cafe, frequencias_compra_de_cafe)
for i in range(len(rotulos_compra_de_cafe)):
    percentage = (frequencias_compra_de_cafe[i] / total_responses) * 100
    plt.text(i, frequencias_compra_de_cafe[i], f'{percentage:.1f}%', ha='center', va='bottom')
plt.xticks(rotation=45)
plt.title('Onde pessoas compram a sua café')

#%%

#Pie chart das bebidas de café preferídas
contagem_bebidas_preferidas = tab_cafe.What_is_your_favorite_coffee_drink.value_counts()
bebidas_preferidas_pie_lab = ['Pourover (Coado)', 'Latte', 'Café de Filtro', 'Cappuccino', 'Espresso', 'Cortado', 'Americano', 'Café gelado', 'Mocha', 'Outro', 'Cold Brew', 'NA', 'Bebida mista']
total_de_respostas = sum(contagem_bebidas_preferidas)
plt.figure(figsize=(6,6))
plt.pie(contagem_bebidas_preferidas, labels=[f'{label}\n({value})' for label, value in zip(bebidas_preferidas_pie_lab, contagem_bebidas_preferidas)], autopct='%.1f%%')

plt.title('As bebidas de Café preferidas pelos respondentes')
plt.tight_layout()  

#%%

#Que pessoas adicionam à sua café 

#selecionando as colunas necessárias
colunas_para_contagem_cpa_a_cafe = [
    'Do_you_usually_add_anything_to_your_coffee_No-just_black',
    'Do_you_usually_add_anything_to_your_coffee_Milk_dairy_alternative_or_coffee_creamer',
    'Do_you_usually_add_anything_to_your_coffee_Sugar_or_sweetener',
    'Do_you_usually_add_anything_to_your_coffee_Flavor_syrup',
    'Do_you_usually_add_anything_to_your_coffee_Other'
]
#montando numa própria tabela
tabela_contagem_cpa_a_cafe = tab_cafe[colunas_para_contagem_cpa_a_cafe].copy()
# Convertendo-a em dados binários
tabela_contagem_cpa_a_cafe.replace(mapping_trocadevalores, inplace=True)
# Obtendo dummies para as variáveis de local de consumo de café
df_tabela_contagem_cpa_a_cafe = pd.DataFrame(tabela_contagem_cpa_a_cafe)
frequencias_cpa_a_cafe = df_tabela_contagem_cpa_a_cafe.sum(axis=0)

#Criação do gráfico bar - respostas de multípula escolha
rotulos_cpa_a_cafe = [
    'Nada',
    'Lacticínio ou substituto',
    'Açucar/Adoçante atificicial',
    'Xarope Saborizado',
    'Outro'
]
plt.figure(figsize=(8,4))
total_responses = row_count = tab_cafe.shape[0]
plt.bar(rotulos_cpa_a_cafe, frequencias_cpa_a_cafe)
for i in range(len(rotulos_cpa_a_cafe)):
    percentage = (frequencias_cpa_a_cafe[i] / total_responses) * 100
    plt.text(i, frequencias_cpa_a_cafe[i], f'{percentage:.1f}%', ha='center', va='bottom')
plt.xticks(rotation=45)
plt.title('Que pessoas adicionam à sua café')





