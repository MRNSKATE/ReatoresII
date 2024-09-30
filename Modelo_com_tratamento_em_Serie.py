import pandas as pd
import numpy as np
import math
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
ideal_N_list = []
ideal_tm_list = []

# Construção de uma lista de erros em função do aumento do tm já sintetizando os melhores Pe
while tempo_medio < 1.5:
    temp_admens = tempo_real/tempo_medio
    absorb_corrigida = (absorb/area_graf_real)*tempo_medio

    print(tempo_medio)

    #Encontrando o Valor de Péclet para o menor erro quadrático
    min_error_list = []
    N_list = []
    N = 1
    while N < 30:
        model = ((N*(N*temp_admens)**(N -1))/(math.factorial(N - 1)))*np.exp(-N*temp_admens)
        min_error = ((absorb_corrigida - model)**2).sum()
        min_error_list.append(min_error)
        N_list.append(N)
        N = N + 1

    ideal_N = 0
    min_error = 0
    for i in range(len(N_list)):
        if i == 0:
            ideal_N = N_list[0]
            min_error = min_error_list[0]
        elif min_error_list[i] < min_error_list[i - 1]:
            ideal_N = N_list[i]
            min_error = min_error_list[i]
    min_error_list_tm.append(min_error)
    ideal_N_list.append(ideal_N)
    ideal_tm_list.append(tempo_medio)
    tempo_medio = tempo_medio + 0.01

# Verificando o menor erro e correlacionand ao Pe e o tm utilizado, já definindo-os
min_error_real = min_error_list_tm[0]
ideal_N = 0
ideal_tm = 0
for i in range(len(min_error_list_tm)):
    if min_error_list_tm[i] < min_error_real:
        min_error_real = min_error_list_tm[i]
        ideal_N = ideal_N_list[i]
        ideal_tm = ideal_tm_list[i]

print(ideal_N)
print(ideal_tm)

temp_admens = tempo_real/ideal_tm
absorb_corrigida = (absorb/area_graf_real)*ideal_tm

'''#Plotar gráfico de erro quadrático
plt.plot(Pe_list, min_error_list, color='blue')
plt.xlabel('Número de Péclet')
plt.ylabel('Soma da diferença quadrática')
plt.grid(True)
plt.show()'''

#Encontrando a função de modelagem axial pelo Péclet Ideal
N = ideal_N
model = ((N*(N*temp_admens)**(N -1))/(math.factorial(N - 1)))*np.exp(-N*temp_admens)

plt.plot(temp_admens, absorb_corrigida, label='Experimental', color='blue')
plt.plot(temp_admens, model, label='Modelo de Tanques em Série', color='orange')
plt.xlabel('Θ')
plt.ylabel('E(Θ)')
plt.title('Comparativo - Modelo de Tanques em Série & Dados Experimentais \n Mínimo Quadrático = ' + str(round(min_error_real,2)))
plt.grid(True)
plt.legend()
plt.show()