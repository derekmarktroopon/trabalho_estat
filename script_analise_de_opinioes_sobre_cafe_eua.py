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
import seaborn as sns
from scipy.stats import chi2_contingency as chi2_cont
from scipy.stats import chi2
import scipy.cluster.hierarchy as sch

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

#Pie chart das frequencias de ingestão de café por dia
contagem_frequencias_de_beber_cafe = tab_cafe.How_many_cups_of_coffee_do_you_typically_drink_per_day.value_counts()
frquencias_de_beber_pie_lab = ['2 copos por dia', '1 copo por dia', '3 copos por dia', '<1 copo por dia', '4 copos por dia', 'NA', '>4 copos por dia']
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
    percentage = (freq / total_responses) * 100
    plt.text(i, freq, f'{percentage:.1f}%', ha='center', va='bottom')
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
    percentage = (freq / total_responses) * 100
    plt.text(i, freq, f'{percentage:.1f}%', ha='center', va='bottom')
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
for i, freq in enumerate(frequencias_compra_de_cafe):
    percentage = (freq / total_responses) * 100
    plt.text(i, freq, f'{percentage:.1f}%', ha='center', va='bottom')
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
for i, freq in enumerate(frequencias_cpa_a_cafe):
    percentage = (freq / total_responses) * 100
    plt.text(i, freq, f'{percentage:.1f}%', ha='center', va='bottom')
plt.xticks(rotation=45)
plt.title('Que pessoas adicionam à sua café')

#%%

#As sabores preferidas pelos respontentes antes da aprovação de café


#Descrições pre-aprovação de preferiencias de sabores

#Pie chart das faixas de idade na amostra
contagem_pref_sab_pre_aprov = tab_cafe.Before_todays_tasting_which_of_the_following_best_described_what_kind_of_coffee_you_like.value_counts()
pref_sab_pre_aprov_lab = ['Frutado', 'Cacau', 'Corp Encorpado', 'Vibrante', 'Nozes', 'Doce', 'Caramelizada', 'Suculento', 'Forte', 'Floral', 'NA', 'Complexo', 'Leve']
plt.figure(figsize=(6,6))
plt.pie(contagem_pref_sab_pre_aprov, labels=[f'{label}\n({value})' for label, value in zip(pref_sab_pre_aprov_lab, contagem_pref_sab_pre_aprov)], autopct='%.1f%%')

plt.title('As sabores preferidas pelos respontentes antes da aprovação de café')
plt.tight_layout()  

#%%

#As intensidades de sabor preferidas pelos respontentes

contagem_pref_intens_sabor = tab_cafe.How_strong_do_you_like_your_coffee.value_counts()
pref_intens_sabor_lab = ['Relativamente Forte', 'Médio', 'Muito Forte', 'Relativamente Leve', 'NA', 'Fraca']
plt.figure(figsize=(6,6))
plt.pie(contagem_pref_intens_sabor, labels=[f'{label}\n({value})' for label, value in zip(pref_intens_sabor_lab, contagem_pref_intens_sabor)], autopct='%.1f%%')

plt.title('As intensidades de sabor preferidas pelos respontentes')
plt.tight_layout() 

#%%

#As Níves prefiridas de Torra de Café

contagem_pref_niv_torra = tab_cafe.What_roast_level_of_coffee_do_you_prefer.value_counts()
pref_niv_torra_lab = ['Torra Leve', 'Torra Médio', 'Torra Forte', 'NA', 'Nordico', 'Loiro', 'Italiano','Frances']
plt.figure(figsize=(6,6))
plt.pie(contagem_pref_niv_torra, labels=[f'{label}\n({value})' for label, value in zip(pref_niv_torra_lab, contagem_pref_niv_torra)], autopct='%.1f%%')

plt.title('As Níves prefiridas de Torra de Café')
plt.tight_layout() 

#%%

#COMPARAÇÕES - correlações entre dados diferentes

#%% 

#relação: idade - frequência de beber café

tab_rel_idade_freq_beber_cafe = pd.crosstab(tab_cafe['What_is_your_age'], tab_cafe['How_many_cups_of_coffee_do_you_typically_drink_per_day'], margins = True)

#Agora vou deletar os totais, pois vamos fazer isso manualmente depois
tab_rel_idade_freq_beber_cafe.drop(['All'], axis = 1, inplace = True)
tab_rel_idade_freq_beber_cafe.drop(['All'], axis = 0, inplace = True)

# Fazendo o teste Qui2
chi2_calculado_rel_idade_freq_beber_cafe, p, dof, expect = chi2_cont(tab_rel_idade_freq_beber_cafe)
chi2_tabelado_rel_idade_freq_beber_cafe = chi2.ppf(0.95, 4) # temos que considera 4 graus de liberdade

#Agora, fazendo o passo a passo para determinar a relação entre as categorias

#Definindo a matriz
n_tab_rel_idade_freq_beber_cafe = np.matrix(tab_rel_idade_freq_beber_cafe, dtype = float)

#Contando
cont_sum_row = n_tab_rel_idade_freq_beber_cafe.sum(axis=1)
cont_sum_col = n_tab_rel_idade_freq_beber_cafe.sum(axis=0)

#Criando a matriz de frequencia esperada
freq_abs_esperada = (np.multiply(cont_sum_row,
                                 cont_sum_col))/n_tab_rel_idade_freq_beber_cafe.sum()

#Obtendo a matriz residual
residuo_n_tab_rel_idade_freq_beber_cafe = n_tab_rel_idade_freq_beber_cafe - freq_abs_esperada

#Agora vamos fazer o calculo do chi2
chi2 = np.divide(np.square(residuo_n_tab_rel_idade_freq_beber_cafe), freq_abs_esperada).sum()

#Calculando a matriz dos residuos padronizados
residuo_padronizado_tab_rel_idade_freq_beber_cafe = residuo_n_tab_rel_idade_freq_beber_cafe / np.sqrt(freq_abs_esperada)

#Calculando a matriz dos residuos padronizados ajustados
residuo_padronizado_ajust_tab_rel_idade_freq_beber_cafe = np.divide(residuo_padronizado_tab_rel_idade_freq_beber_cafe,
                       np.sqrt(np.multiply(
                           (1-(cont_sum_col/n_tab_rel_idade_freq_beber_cafe.sum())),
                           (1-(cont_sum_row/n_tab_rel_idade_freq_beber_cafe.sum())))))

#Fazendo uma figura bonitinha para mostrar eses residuos
colunas = ['1 copo por dia', '2 copos por dia', '3 copos por dia', '4 copos por dia', '<1 copo por dia', '>4 copos por dia', 'NA']
linhas = ['18-24 anos', '25-34 anos', '35-44 anos', '45-54 anos', '55-64 anos', '<18 anos', '>65 anos', 'NA']
ax = sns.heatmap(residuo_padronizado_ajust_tab_rel_idade_freq_beber_cafe, annot=True, xticklabels=colunas, yticklabels=linhas)

#%%

#relação: idade - onde pessoas bebem café

#criando a tabela binária das idades

tab_bin_idades_2 = tab_cafe['What_is_your_age']

# Ensure tab_bin_locais_de_beber_cafe_2 is a DataFrame (if it's not already)

tab_bin_locais_de_beber_cafe_2 = tabela_contagem_locais_de_beber_cafe.astype(bool)

# Calculo das corelações 
result_locais_de_beber_cafe_2 = {}
for column in tab_bin_locais_de_beber_cafe_2:
    observed = pd.crosstab(tab_bin_locais_de_beber_cafe_2[column], tab_bin_idades_2)
    chi2, p, dof, expected = chi2_cont(observed)
    result_locais_de_beber_cafe_2[column] = {'Chi-square': chi2, 'p-value': p}

# Vetor das frequências esperadas
freqs = {}

# Teste Qui-quadrado
for column in tab_bin_locais_de_beber_cafe_2:
    observed = pd.crosstab(tab_bin_locais_de_beber_cafe_2[column], tab_bin_idades_2)
    chi2, p, dof, expected = chi2_cont(observed)
    freqs[column] = {'Observed': observed, 'Expected': expected}

# Calcular os resíduos e criar matrizes residuais
residual_matrices = {}
for column, data in freqs.items():
    observed = data['Observed']
    expected = data['Expected']
    residuals = observed - expected
    # Replace residuals for 'false' values with NaN
    residuals[~observed.astype(bool)] = np.nan
    residual_matrices[column] = residuals

# Criar mapa de calor
plt.figure(figsize=(35, 30))  
for i, (column, residuals) in enumerate(residual_matrices.items(), 1):
    plt.subplot(1, len(residual_matrices), i)
    sns.heatmap(residuals, annot=True, cmap='coolwarm', cbar=False, square=True, fmt=".2f")  # Specify format
    plt.title(f'Residuais para {rotulos_locais_de_beber_cafe[i-1]}')  # Use custom column labels
    plt.xlabel('Faixas de Idade')
    plt.ylabel('Respostas Binárias')
plt.show()



#%% 

#relação: idade - quais tipos de café são preferidas

tab_rel_idade_tipobeb_cafe = pd.crosstab(tab_cafe['What_is_your_age'], tab_cafe['What_is_your_favorite_coffee_drink'], margins = True)

#Agora vou deletar os totais, pois vamos fazer isso manualmente depois
tab_rel_idade_tipobeb_cafe.drop(['All'], axis = 1, inplace = True)
tab_rel_idade_tipobeb_cafe.drop(['All'], axis = 0, inplace = True)

# Fazendo o teste Qui2
chi2_calculado_rel_idade_tipobeb_cafe, p, dof, expect = chi2_cont(tab_rel_idade_tipobeb_cafe)

#Definindo a matriz
n_tab_rel_idade_tipobeb_cafe = np.matrix(tab_rel_idade_tipobeb_cafe, dtype = float)

#Contando
cont_sum_row_tipobeb_cafe = n_tab_rel_idade_tipobeb_cafe.sum(axis=1)
cont_sum_col_tipobeb_cafe = n_tab_rel_idade_tipobeb_cafe.sum(axis=0)

#Criando a matriz de frequencia esperada
freq_abs_esperada_tipobeb_cafe = (np.multiply(cont_sum_row_tipobeb_cafe,
                                 cont_sum_col_tipobeb_cafe))/n_tab_rel_idade_tipobeb_cafe.sum()

#Obtendo a matriz residual
residuo_n_tab_rel_idade_tipobeb_cafe = n_tab_rel_idade_tipobeb_cafe - freq_abs_esperada_tipobeb_cafe

#Agora vamos fazer o calculo do chi2
chi2_tipobeb_cafe = np.divide(np.square(residuo_n_tab_rel_idade_tipobeb_cafe), freq_abs_esperada_tipobeb_cafe).sum()

#Calculando a matriz dos residuos padronizados
residuo_padronizado_tab_rel_idade_tipobeb_cafe = residuo_n_tab_rel_idade_tipobeb_cafe / np.sqrt(freq_abs_esperada_tipobeb_cafe)

#Calculando a matriz dos residuos padronizados ajustados
residuo_padronizado_ajust_tab_rel_idade_tipobeb_cafe = np.divide(residuo_padronizado_tab_rel_idade_tipobeb_cafe,
                       np.sqrt(np.multiply(
                           (1-(cont_sum_col/n_tab_rel_idade_tipobeb_cafe.sum())),
                           (1-(cont_sum_row/n_tab_rel_idade_tipobeb_cafe.sum())))))

#Fazendo uma figura bonitinha para mostrar eses residuos
colunas = ['Americano', 'Bebida mista', 'Cappuccino', 'Cold Brew', 'Cortado', 'Espresso', 'Café gelado', 'Latte', 'Mocha', 'NA' , 'Outro', 'Pourover (Coado)', 'Café de Filtro' ]
linhas = ['18-24 anos', '25-34 anos', '35-44 anos', '45-54 anos', '55-64 anos', '<18 anos', '>65 anos', 'NA']
ax = sns.heatmap(residuo_padronizado_ajust_tab_rel_idade_tipobeb_cafe, annot=True, xticklabels=colunas, yticklabels=linhas)

#%%

#relação: idade - As durezas de café prefirídas

tab_rel_idade_forca_cafe = pd.crosstab(tab_cafe['What_is_your_age'], tab_cafe['How_strong_do_you_like_your_coffee'], margins = True)

#Agora vou deletar os totais, pois vamos fazer isso manualmente depois
tab_rel_idade_forca_cafe.drop(['All'], axis = 1, inplace = True)
tab_rel_idade_forca_cafe.drop(['All'], axis = 0, inplace = True)

# Fazendo o teste Qui2
chi2_calculado_rel_idade_tipobeb_cafe, p, dof, expect = chi2_cont(tab_rel_idade_tipobeb_cafe)
chi2_tabelado_rel_idade_tipobeb_cafe = chi2.ppf(0.95, 4) # temos que considera 4 graus de liberdade

#Agora, fazendo o passo a passo para determinar a relação entre as categorias

#Definindo a matriz
n_tab_rel_idade_tipobeb_cafe = np.matrix(tab_rel_idade_tipobeb_cafe, dtype = float)

#Contando
cont_sum_row = n_tab_rel_idade_tipobeb_cafe.sum(axis=1)
cont_sum_col = n_tab_rel_idade_tipobeb_cafe.sum(axis=0)

#Criando a matriz de frequencia esperada
freq_abs_esperada = (np.multiply(cont_sum_row,
                                 cont_sum_col))/n_tab_rel_idade_tipobeb_cafe.sum()

#Obtendo a matriz residual
residuo_n_tab_rel_idade_tipobeb_cafe = n_tab_rel_idade_tipobeb_cafe - freq_abs_esperada

#Agora vamos fazer o calculo do chi2
chi2 = np.divide(np.square(residuo_n_tab_rel_idade_tipobeb_cafe), freq_abs_esperada).sum()

#Calculando a matriz dos residuos padronizados
residuo_padronizado_tab_rel_idade_tipobeb_cafe = residuo_n_tab_rel_idade_tipobeb_cafe  / np.sqrt(freq_abs_esperada)

#Calculando a matriz dos residuos padronizados ajustados
residuo_padronizado_ajust_tab_rel_idade_tipobeb_cafe  = np.divide(residuo_padronizado_tab_rel_idade_tipobeb_cafe ,
                       np.sqrt(np.multiply(
                           (1-(cont_sum_col/n_tab_rel_idade_tipobeb_cafe .sum())),
                           (1-(cont_sum_row/n_tab_rel_idade_tipobeb_cafe .sum())))))

#Fazendo uma figura bonitinha para mostrar eses residuos
colunas = ['Americano', 'Bebida mista', 'Cappuccino', 'Cold Brew', 'Cortado', 'Espresso', 'Café gelado', 'Latte', 'Mocha', 'NA' , 'Outro', 'Pourover (Coado)', 'Café de Filtro' ]
linhas = ['18-24 anos', '25-34 anos', '35-44 anos', '45-54 anos', '55-64 anos', '<18 anos', '>65 anos', 'NA']
ax = sns.heatmap(residuo_padronizado_ajust_tab_rel_idade_tipobeb_cafe, annot=True, xticklabels=colunas, yticklabels=linhas)


#relação: idade - dureza de café

tab_rel_idade_durez_caf = pd.crosstab(tab_cafe['What_is_your_age'], tab_cafe['How_strong_do_you_like_your_coffee'], margins = True)

#Agora vou deletar os totais, pois vamos fazer isso manualmente depois
tab_rel_idade_durez_caf.drop(['All'], axis = 1, inplace = True)
tab_rel_idade_durez_caf.drop(['All'], axis = 0, inplace = True)

# Fazendo o teste Qui2
chi2_calculado_rel_idade_durez_caf, p, dof, expect = chi2_cont(tab_rel_idade_durez_caf)

#Agora, fazendo o passo a passo para determinar a relação entre as categorias

#Definindo a matriz
n_tab_rel_idade_durez_caf = np.matrix(tab_rel_idade_durez_caf, dtype = float)

#Contando
cont_sum_row = n_tab_rel_idade_durez_caf.sum(axis=1)
cont_sum_col = n_tab_rel_idade_durez_caf.sum(axis=0)

#Criando a matriz de frequencia esperada
freq_abs_esperada_durez_caf = (np.multiply(cont_sum_row,
                                 cont_sum_col))/n_tab_rel_idade_durez_caf.sum()

#Obtendo a matriz residual
residuo_n_tab_rel_idade_durez_caf = n_tab_rel_idade_durez_caf - freq_abs_esperada_durez_caf

#Agora vamos fazer o calculo do chi2
chi2 = np.divide(np.square(residuo_n_tab_rel_idade_durez_caf), freq_abs_esperada_durez_caf).sum()

#Calculando a matriz dos residuos padronizados
residuo_padronizado_tab_rel_idade_durez_caf = residuo_n_tab_rel_idade_durez_caf / np.sqrt(freq_abs_esperada_durez_caf)

#Calculando a matriz dos residuos padronizados ajustados
residuo_padronizado_ajust_tab_rel_idade_durez_caf = np.divide(residuo_padronizado_tab_rel_idade_durez_caf,
                       np.sqrt(np.multiply(
                           (1-(cont_sum_col/n_tab_rel_idade_durez_caf.sum())),
                           (1-(cont_sum_row/n_tab_rel_idade_durez_caf.sum())))))

#Fazendo uma figura bonitinha para mostrar eses residuos
colunas = ['Médio', 'NA', 'Relativamente Leve', 'Relativamente Forte', 'Muito Forte', 'Fraca']
linhas = ['18-24 anos', '25-34 anos', '35-44 anos', '45-54 anos', '55-64 anos', '<18 anos', '>65 anos', 'NA']
ax = sns.heatmap(residuo_padronizado_ajust_tab_rel_idade_durez_caf, annot=True, xticklabels=colunas, yticklabels=linhas)

#%%

#relação: educação - quais tipos de café são preferidas


tab_rel_edu_tipobeb_cafe = pd.crosstab(tab_cafe['Education_Level'], tab_cafe['What_is_your_favorite_coffee_drink'], margins = True)

#Agora vou deletar os totais, pois vamos fazer isso manualmente depois
tab_rel_edu_tipobeb_cafe.drop(['All'], axis = 1, inplace = True)
tab_rel_edu_tipobeb_cafe.drop(['All'], axis = 0, inplace = True)

# Fazendo o teste Qui2
chi2_calculado_rel_edu_tipobeb_cafe, p, dof, expect = chi2_cont(tab_rel_edu_tipobeb_cafe)

#Agora, fazendo o passo a passo para determinar a relação entre as categorias

#Definindo a matriz
n_tab_rel_edu_tipobeb_cafe = np.matrix(tab_rel_edu_tipobeb_cafe, dtype = float)

#Contando
cont_sum_row = n_tab_rel_edu_tipobeb_cafe.sum(axis=1)
cont_sum_col = n_tab_rel_edu_tipobeb_cafe.sum(axis=0)

#Criando a matriz de frequencia esperada
freq_abs_esperada_durez_caf = (np.multiply(cont_sum_row,
                                 cont_sum_col))/n_tab_rel_edu_tipobeb_cafe.sum()

#Obtendo a matriz residual
residuo_n_tab_rel_edu_tipobeb_cafe = n_tab_rel_edu_tipobeb_cafe - freq_abs_esperada_durez_caf

#Agora vamos fazer o calculo do chi2
chi2 = np.divide(np.square(residuo_n_tab_rel_edu_tipobeb_cafe), freq_abs_esperada_durez_caf).sum()

#Calculando a matriz dos residuos padronizados
residuo_padronizado_tab_rel_edu_tipobeb_cafe = residuo_n_tab_rel_edu_tipobeb_cafe / np.sqrt(freq_abs_esperada_durez_caf)

#Calculando a matriz dos residuos padronizados ajustados
residuo_padronizado_ajust_tab_rel_edu_tipobeb_cafe = np.divide(residuo_padronizado_tab_rel_edu_tipobeb_cafe,
                       np.sqrt(np.multiply(
                           (1-(cont_sum_col/n_tab_rel_edu_tipobeb_cafe.sum())),
                           (1-(cont_sum_row/n_tab_rel_edu_tipobeb_cafe.sum())))))

#Fazendo uma figura bonitinha para mostrar eses residuos
colunas = ['Americano', 'Bebida mista', 'Cappuccino', 'Cold Brew', 'Cortado', 'Espresso', 'Café gelado', 'Latte', 'Mocha', 'NA' , 'Outro', 'Pourover (Coado)', 'Café de Filtro' ]
linhas = ['Bacharelado', 'Doturado', 'Ensino Médio Completo', 'Até Ensino Médio Incompleto', 'Mestrado','NA' , 'Associates Degree']
ax = sns.heatmap(residuo_padronizado_ajust_tab_rel_edu_tipobeb_cafe, annot=True, xticklabels=colunas, yticklabels=linhas)

#%%

#relação: educação - dureza de café

tab_rel_edu_durez_caf = pd.crosstab(tab_cafe['Education_Level'], tab_cafe['How_strong_do_you_like_your_coffee'], margins = True)

#Agora vou deletar os totais, pois vamos fazer isso manualmente depois
tab_rel_edu_durez_caf.drop(['All'], axis = 1, inplace = True)
tab_rel_edu_durez_caf.drop(['All'], axis = 0, inplace = True)

# Fazendo o teste Qui2
chi2_calculado_rel_edu_durez_caf, p, dof, expect = chi2_cont(tab_rel_edu_durez_caf)

#Agora, fazendo o passo a passo para determinar a relação entre as categorias

#Definindo a matriz
n_tab_rel_edu_durez_caf = np.matrix(tab_rel_edu_durez_caf, dtype = float)

#Contando
cont_sum_row = n_tab_rel_edu_durez_caf.sum(axis=1)
cont_sum_col = n_tab_rel_edu_durez_caf.sum(axis=0)

#Criando a matriz de frequencia esperada
freq_abs_esperada_durez_caf = (np.multiply(cont_sum_row,
                                 cont_sum_col))/n_tab_rel_edu_durez_caf.sum()

#Obtendo a matriz residual
residuo_n_tab_rel_edu_durez_caf = n_tab_rel_edu_durez_caf - freq_abs_esperada_durez_caf

#Agora vamos fazer o calculo do chi2
chi2 = np.divide(np.square(residuo_n_tab_rel_edu_durez_caf), freq_abs_esperada_durez_caf).sum()

#Calculando a matriz dos residuos padronizados
residuo_padronizado_tab_rel_edu_durez_caf = residuo_n_tab_rel_edu_durez_caf / np.sqrt(freq_abs_esperada_durez_caf)

#Calculando a matriz dos residuos padronizados ajustados
residuo_padronizado_ajust_tab_rel_edu_durez_caf = np.divide(residuo_padronizado_tab_rel_edu_durez_caf,
                       np.sqrt(np.multiply(
                           (1-(cont_sum_col/n_tab_rel_edu_durez_caf.sum())),
                           (1-(cont_sum_row/n_tab_rel_edu_durez_caf.sum())))))

#Fazendo uma figura bonitinha para mostrar eses residuos
colunas = ['Médio', 'NA', 'Relativamente Leve', 'Relativamente Forte', 'Muito Forte', 'Fraca']
linhas = ['Bacharelado', 'Doturado', 'Ensino Médio Completo', 'Até Ensino Médio Incompleto', 'Mestrado','NA' , 'Associates Degree']
ax = sns.heatmap(residuo_padronizado_ajust_tab_rel_edu_durez_caf, annot=True, xticklabels=colunas, yticklabels=linhas)

#%%

#Calcula das distâncias entre as preferências cafeterias entre pessoas de educação diferente

#combinando as tabelas dos aspetos diferentes de café usado para esse calculo (sabor e intensidade)

tabela_edu_caf_comb = pd.merge(tab_rel_edu_durez_caf, tab_rel_edu_tipobeb_cafe, on='Education_Level', how='outer')
#tirada de qualquer valor não-numerico restante
tabela_edu_caf_comb_semnome = tabela_edu_caf_comb.select_dtypes(include='number')

Education_Level_list = ['Bacharelado', 'Doturado', 'Ensino Médio Completo', 'Até Ensino Médio Incompleto', 'Mestrado','NA' , 'Associates Degree']

plt.figure(figsize=(10, 5)) 
dendrograma_edu_caf_comb = sch.dendrogram(sch.linkage(tabela_edu_caf_comb_semnome, method = 'single', metric = 'euclidean'), labels = Education_Level_list)
plt.title('Relação das Preferências de acordo com Nível de Educação', fontsize=20
          )
plt.xlabel('Nível de Escolaridade', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Dist Euclidiana', fontsize=16)
plt.show()

#%%

#Calcula das distâncias entre as preferências cafeterias entre pessoas de idade diferente

#combinando as tabelas dos aspetos diferentes de café usado para esse calculo (sabor e intensidade)

tabela_edu_caf_comb = pd.merge(tab_rel_idade_durez_caf, tab_rel_idade_tipobeb_cafe, on='What_is_your_age', how='outer')
#tirada de qualquer valor não-numerico restante
tabela_edu_caf_comb_semnome = tabela_edu_caf_comb.select_dtypes(include='number')

age_list = ['18-24 anos', '25-34 anos', '35-44 anos', '45-54 anos', '55-64 anos', '<18 anos', '>65 anos', 'NA']

plt.figure(figsize=(10, 5)) 
dendrograma_edu_caf_comb = sch.dendrogram(sch.linkage(tabela_edu_caf_comb_semnome, method = 'single', metric = 'euclidean'), labels = age_list)
plt.title('Relação das Preferências de acordo com Idades diferentes', fontsize=20
          )
plt.xlabel('Faixas de Idade', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Dist Euclidiana', fontsize=16)
plt.show()


