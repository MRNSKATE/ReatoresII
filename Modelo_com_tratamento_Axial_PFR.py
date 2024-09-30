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
#tempo_medio = np.trapz(tempo_absorb, tempo_real)/area_graf_real

tempo_medio = 0.8
min_error_list_tm = []
ideal_Pe_list = []
ideal_tm_list = []

# Construção de uma lista de erros em função do aumento do tm já sintetizando os melhores Pe
while tempo_medio < 1.5:
    temp_admens = tempo_real/tempo_medio
    absorb_corrigida = (absorb/area_graf_real)*tempo_medio

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
    min_error_list_tm.append(min_error)
    ideal_Pe_list.append(ideal_Pe)
    ideal_tm_list.append(tempo_medio)
    tempo_medio = tempo_medio + 0.01

# Verificando o menor erro e correlacionand ao Pe e o tm utilizado, já definindo-os
min_error_real = min_error_list_tm[0]
ideal_Pe = 0
ideal_tm = 0
for i in range(len(min_error_list_tm)):
    if min_error_list_tm[i] < min_error_real:
        min_error_real = min_error_list_tm[i]
        ideal_Pe = ideal_Pe_list[i]
        ideal_tm = ideal_tm_list[i]

print(ideal_Pe)
print(ideal_tm)

temp_admens = tempo_real/ideal_tm
absorb_corrigida = (absorb/area_graf_real)*ideal_tm

Pe = ideal_Pe
model = (((Pe + 1)/(4*np.pi*temp_admens**3))**0.5)*np.exp(-((Pe + 1)*(1-temp_admens)**2)/(4*temp_admens))

plt.plot(temp_admens, absorb_corrigida, label='Experimental', color='blue')
plt.plot(temp_admens, model, label='Modelo Axial', color='orange')
plt.xlabel('Θ')
plt.ylabel('E(Θ)')
plt.title('Comparativo - Modelo de Dispersão Axial & Dados Experimentais \n Mínimo Quadráticos = ' + str(round(min_error_real,2)))
plt.grid(True)
plt.legend()
plt.show()