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
tempo_absorb = dados_excel['Tempo (min)']*dados_excel['Absorbância']
tempo_medio = np.trapz(tempo_absorb, tempo_real)/area_graf_real
temp_admens = tempo_real/tempo_medio
absorb_corrigida = (absorb/area_graf_real)*tempo_medio

print(np.trapz(absorb_corrigida, temp_admens))
print(tempo_medio)

#Encontrando o Valor de Péclet para o menor erro quadrático
min_error_list = []
Pe_list = []
Pe = 0
while Pe < 150:
    model = (((Pe + 1)/(4*np.pi*temp_admens**3))**0.5)*np.exp(-((Pe + 1)*(1-temp_admens)**2)/(4*temp_admens))
    min_error = ((absorb_corrigida - model)**2).sum()
    min_error_list.append(min_error)
    Pe_list.append(Pe)
    Pe = Pe + 0.1

ideal_Pe = 0
min_error = 0
for i in range(len(Pe_list)):
    if i == 0:
        ideal_Pe = Pe_list[0]
        min_error = min_error_list[0]
    elif min_error_list[i] < min_error_list[i - 1]:
        ideal_Pe = Pe_list[i]
        min_error = min_error_list[i]
print(ideal_Pe)

#Plotar gráfico de erro quadrático
plt.plot(Pe_list, min_error_list, color='blue')
plt.xlabel('Número de Péclet')
plt.ylabel('Soma da diferença quadrática')
plt.grid(True)
plt.show()

#Encontrando a função de modelagem axial pelo Péclet Ideal
Pe = ideal_Pe
model = (((Pe + 1)/(4*np.pi*temp_admens**3))**0.5)*np.exp(-((Pe + 1)*(1-temp_admens)**2)/(4*temp_admens))

plt.plot(temp_admens, absorb_corrigida, label='Experimental', color='blue')
plt.plot(temp_admens, model, label='Modelo Axial', color='orange')
plt.xlabel('Θ')
plt.ylabel('E(Θ)')
plt.title('Comparativo - Modelo de Dispersão Axial & Dados Experimentais \n Mínimo Quadráticos = ' + str(round(min_error,2)))
plt.grid(True)
plt.legend()
plt.show()