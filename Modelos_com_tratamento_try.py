import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# Leia o arquivo Excel
dados_excel = pd.read_excel('Resultados DTR_python.xlsx', sheet_name='PFR')

#Definindo as colunas utilizadas para a análise de dados
tempo_real = dados_excel['Tempo (min)']
absorb = dados_excel['Absorbância']

#Padronização da curva de absorbância para Área = 1
area_graf_real = np.trapz(absorb, tempo_real)
absorb_corrigida = (absorb/area_graf_real)

print(np.trapz(absorb_corrigida, tempo_real))

#Encontrando o Valor de Péclet para o menor erro quadrático
min_error_list = []
Pe_list = []
tm_list = []
tm = 0.3
while tm < 1.5:
    Pe = 20  
    min_error_tm_i_list = []
    while Pe < 150:
        model = (1/tm)*(((Pe + 1)/(4*np.pi*(tempo_real/tm)**3))**0.5)*np.exp(-((Pe + 1)*(1-(tempo_real/tm))**2)/(4*(tempo_real/tm)))
        min_error = ((absorb_corrigida - model)**2).sum()
        min_error_tm_i_list.append(min_error)
        Pe_list.append(Pe)
        Pe = Pe + 0.1
    min_error_list.append(min_error_tm_i_list)
    tm_list.append(tm)
    tm = tm + 0.1
print(min_error_list)

ideal_Pe = 0
ideal_tm = 0
min_error = min_error_list[0][0]

for i, row in enumerate(min_error_list):
    # Itere sobre cada elemento da linha
    for j, item in enumerate(row):
        # Atualize o valor mínimo e o índice mínimo se o elemento atual for menor
        if item < min_error:
            min_error = item
            ideal_Pe = Pe_list[i]
            ideal_tm = Pe_list[j]
print(ideal_Pe)
print(min_error)

#Plotar gráfico de erro quadrático
plt.plot(Pe_list, min_error_list, color='blue')
plt.xlabel('Número de Péclet')
plt.ylabel('Soma da diferença quadrática')
plt.grid(True)
plt.show()

#Encontrando a função de modelagem axial pelo Péclet Ideal
Pe = ideal_Pe
tm = ideal_tm
model = (1/tm)*(((Pe + 1)/(4*np.pi*(tempo_real/tm)**3))**0.5)*np.exp(-((Pe + 1)*(1-(tempo_real/tm))**2)/(4*(tempo_real/tm)))

plt.plot(tempo_real, absorb_corrigida, label='Experimental', color='blue')
plt.plot(tempo_real, model, label='Modelo Axial', color='orange')
plt.xlabel('Θ')
plt.ylabel('E(Θ)')
plt.title('Comparativo - Modelo de Dispersão Axial & Dados Experimentais \n Mínimo Quadráticos = ' + str(round(min_error,2)))
plt.grid(True)
plt.legend()
plt.show()