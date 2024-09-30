# -*- coding: utf-8 -*-
"""tlbo_01.ipynb

Automatically generated by Colab.

Original file is located at
    
"""

# .........................................................................
# Algoritmo TLBO (Optimización basada en Enseñanza-Aprendizaje)
# minimiza la benchmark function Rastrigin
# .........................................................................
import numpy as np  # Importa la biblioteca NumPy para operaciones numéricas
import matplotlib.pyplot as plt  # Importa Matplotlib para la creación de gráficos

# Función de Rastrigin: función de prueba comun para algoritmos de optimización
def rastrigin(posicion):
    A = 10  # Constante de la función Rastrigin
    suma = 0  # Inicializa la suma
    for xi in posicion:  # Itera sobre cada valor en la posición
        suma += xi**2 - A * np.cos(2 * np.pi * xi)  # Suma los términos de la función Rastrigin
    return A * len(posicion) + suma  # Retorna el valor de la función Rastrigin

# Parametros de TLBO: parámetros para el algoritmo TLBO
nVar = 2  # Número de variables de decisión (dimensionalidad)
TamanoVar = [nVar]  # Tamaño de la variable (vector)
LimiteMin = -5.12  # Límite inferior de las variables
LimiteMax = 5.12  # Límite superior de las variables
MaxIter = 80  # Número máximo de iteraciones
TamanoPoblacion = 50  # Tamaño de la población

# Inicialización: inicialización de la población
poblacion = np.random.uniform(LimiteMin, LimiteMax, (TamanoPoblacion, nVar))  # Genera la población inicial aleatoria
MejorSolucion = None  # Inicializa la mejor solución como None
MejoresCostos = []  # Lista para almacenar los mejores costos en cada iteración

# Bucle principal del algoritmo TLBO
for iteracion in range(MaxIter):
    # Calcular la media de la población
    Media = np.mean(poblacion, axis=0)  # Media de la población para cada variable

    # Seleccionar al profesor: selecciona el mejor individuo como "Profesor"
    aptitudes = np.zeros(TamanoPoblacion)  # Inicializa un array para las aptitudes
    for indice, individuo in enumerate(poblacion):  # Itera sobre cada individuo en la población
        aptitudes[indice] = rastrigin(individuo)  # Calcula el fitness de cada individuo

    IndiceProfesor = np.argmin(aptitudes)  # Índice del individuo con mejor fitness
    Profesor = poblacion[IndiceProfesor]  # Selecciona al profesor (el mejor individuo)

    # Fase del Profesor: fase de aprendizaje del profesor
    for i in range(TamanoPoblacion):
        TF = np.random.randint(1, 3)  # Factor de enseñanza, aleatorio entre 1 y 2
        nueva_posicion = poblacion[i] + np.random.uniform(size=TamanoVar) * (Profesor - TF * Media)  # Calcula nueva posición
        nueva_posicion = np.clip(nueva_posicion, LimiteMin, LimiteMax)  # Asegura que la nueva posición esté dentro de los límites

        if rastrigin(nueva_posicion) < aptitudes[i]:  # Si la nueva posición mejora el fitness
            poblacion[i] = nueva_posicion  # Actualiza la posición del individuo

    # Fase del Alumno: fase de aprendizaje entre alumnos
    for i in range(TamanoPoblacion):
        j = np.random.choice([k for k in range(TamanoPoblacion) if k != i])  # Selecciona un individuo diferente al actual
        paso = poblacion[i] - poblacion[j]  # Calcula el paso de aprendizaje
        if rastrigin(poblacion[j]) < aptitudes[i]:  # Si el otro individuo tiene mejor fitness
            paso = -paso  # Invierte la dirección del paso
            #poblacion[i] = poblacion[i] - poblacion[j]
        #else:
            #poblacion[i] = poblacion[j] - poblacion[i]
        nueva_posicion = poblacion[i] + np.random.uniform(size=TamanoVar) * paso  # Calcula nueva posición
        nueva_posicion = np.clip(nueva_posicion, LimiteMin, LimiteMax)  # Asegura que la nueva posición esté dentro de los límites

        if rastrigin(nueva_posicion) < aptitudes[i]:  # Si la nueva posición mejora el fitness
            poblacion[i] = nueva_posicion  # Actualiza la posición del individuo

    # Actualizar la Mejor Solución encontrada
    MejorAptitud = np.inf  # Inicializa la mejor aptitud como infinito
    for individuo in poblacion:  # Itera sobre cada individuo en la población
        aptitud = rastrigin(individuo)  # Calcula el fitness del individuo
        if aptitud < MejorAptitud:  # Si el fitness actual es mejor
            MejorAptitud = aptitud  # Actualiza la mejor aptitud
            MejorSolucion = individuo  # Actualiza la mejor solución encontrada

    MejoresCostos.append(MejorAptitud)  # Almacena el mejor costo (fitness) de la iteración

    # Mostrar Información de la Iteración
    print(f'Iteración {iteracion + 1}: Mejor Costo = {MejoresCostos[-1]:.4f}')  # Imprime el mejor costo en la iteración actual

# Gráfica de la Curva de Convergencia
plt.figure()  # Crea una nueva figura
plt.plot(MejoresCostos, label='TLBO', linewidth=2)  # Grafica los mejores costos a lo largo de las iteraciones
plt.xlabel('Iteración')  # Etiqueta del eje X
plt.ylabel('Mejor Costo (Aptitud)')  # Etiqueta del eje Y
plt.title('Curva de Convergencia (TLBO)')  # Título del gráfico
plt.grid(True)  # Activa la cuadrícula
plt.legend()  # Muestra la leyenda
plt.show()  # Muestra el gráfico

# Diagrama de Caja del Fitness de la Población Final
plt.figure()  # Crea una nueva figura
aptitudes_finales = []  # Inicializa la lista de aptitudes finales
for individuo in poblacion:  # Itera sobre cada individuo en la población final
    aptitudes_finales.append(rastrigin(individuo))  # Calcula el fitness de la población final

plt.boxplot(aptitudes_finales)  # Crea un diagrama de caja para el fitness final
plt.title('Distribución del Fitness de la Población Final (TLBO)')  # Título del gráfico
plt.ylabel('Aptitud')  # Etiqueta del eje Y
plt.grid(True)  # Activa la cuadrícula
plt.show()  # Muestra el gráfico