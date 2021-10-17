import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

#Funciones de separación de entrenamiento, validación y prueba.
def particionar(entradas,salidas,porcentaje_entrenamiento, porcentaje_validacion, porcentaje_prueba):
  temp_size = porcentaje_validacion + porcentaje_prueba
  x_train, x_temp, y_train, y_temp = train_test_split(entradas,salidas,test_size=temp_size)
  if(porcentaje_validacion > 0):
    test_size = porcentaje_prueba/temp_size
    x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size=test_size)
  else:
    return [x_train, None, x_temp, y_train, None, y_temp]
  return [x_train, x_val, x_temp, y_train, y_val, y_temp]

#Funciones de separación de datasets con K-Fold (el usuario debe poner el K, si K = 1 debe generar un Leave-One-Out Cross Validation).
def kfold(k):
  kfold = KFold(k,True,random_seed=48)
  return kfold

#Funciones de evaluación con matriz de confusión.
def conf_matrix(y_esperados, y_predichos):
  matrix = confusion_matrix(y_esperados, y_predichos)
  return matrix

#Funciones de obtención de Precisión (Accuracy), Sensibilidad y Especificidad.
def conf_matrix(y_esperados, y_predichos): 
  matrix = confusion_matrix(y_esperados, y_predichos)
  return matrix 

def parameters(matrix):
  (TP, FN, FP, TN) = np.ravel(matrix, order = 'C')
  return TP, FN, FP, TN

def accuracy(TP, FN, FP, TN):  #exactitud
  a = (TP + TN)/(TP+TN+FP+FN)
  return a

def sensitivity(TP, FN, FP, TN): #sensibilidad
  s = TP/(TP +FN)
  return s

def specificity(TP, FN, FP, TN): #especificidad
  sp = TN/(TN + FP)
  return sp

def precision(TP, FN, FP, TN): #precisión
  p = TP/(TP+FP)
  return p

#Funciones que comparen dos clasificadores:
#Obtengas precisión, sensibilidad y especificidad del clasificador 1
#Obtengas precisión, sensibilidad y especificidad del clasificador 2
def comparison(matrix1, matrix2): #la función toma dos matrices de confusión
  TP, FN, FP, TN = parameters(matrix1)
  TP2, FN2, FP2, TN2 = parameters(matrix2)

  #valores para la matriz del modelo 1
  a1 = accuracy(TP, FN, FP, TN)
  s1 = sensitivity(TP, FN, FP, TN)
  sp1 = specificity(TP, FN, FP, TN)
  p1 = precision(TP, FN, FP, TN)
  
  print("Modelo 1:") 
  print(f"Exactitud: {a1}") 
  print(f"Sensibilidad: {s1}") 
  print(f"Especificidad: {sp1}") 
  print(f"Precisión: {p1}") 
  
  print("\n") 

  print("Modelo 2:") 
  print(f"Exactitud: {a2}") 
  print(f"Sensibilidad: {s2}") 
  print(f"Especificidad: {sp2}") 
  print(f"Precisión: {p2}") 
  
  print("\n") 
  
  #valores para la matriz del modelo 2
  a2 = accuracy(TP2, FN2, FP2, TN2)
  s2 = sensitivity(TP2, FN2, FP2, TN2)
  sp2 = specificity(TP2, FN2, FP2, TN2)
  p2 = precision(TP2, FN2, FP2, TN2)
  
  #comparacion entre parámetros
  if a1 > a2: #exactitud
    print("El clasificador 1 es mejor que el clasificador 2 en términos de exactitud \n")
  else:
    print("El clasificador 2 es mejor que el clasificador 2 en términos de exactitud \n")

  if s1 > s2: #sensibilidad
    print("El clasificador 1 es mejor que el clasificador 2 en términos de sensibilidad \n")
  else:
    print("El clasificador 2 es mejor que el clasificador 2 en términos de sensibilidad \n")

  if sp1 > sp2: #especificidad
    print("El clasificador 1 es mejor que el clasificador 2 en términos de especificidad \n")
  else:
    print("El clasificador 2 es mejor que el clasificador 2 en términos de especificidad \n") 

  if p1 > p2: #precisión
    print("El clasificador 1 es mejor que el clasificador 2 en términos de precisión \n")
  else:
    print("El clasificador 2 es mejor que el clasificador 2 en términos de precisión \n")

#Funciones de evaluación multiclase.



#función de mapa de correlaciones
def mapa():
    df = pd.read_csv("https://raw.githubusercontent.com/maggiesam/BEDU-DataScience/main/Datasets/dataframe-junto.csv")
    correlation_mat = df.corr()
    fig = plt.figure(figsize=(10,10))
    sns.heatmap(correlation_mat, annot = True)
    plt.show()


#función de regresion
def regresion_lineal(planta=0, grado=1, meses=False, n_mes=1,  prueba=0.2, semilla=50):

    #carga los datos directamente del repositorio
    df = pd.read_csv("https://raw.githubusercontent.com/maggiesam/BEDU-DataScience/main/Datasets/dataframe-junto.csv")

    #diferencia entre las plantas
    lista=["maiz","frijol","trigo"]
    producto = df[df["producto"] == lista[planta]]

    #añade una columna de porcentaje de cosecha
    producto["porcentaje"] = producto["Cosechada_ha"]*100/producto["Sembrada_ha"]

    #activa el mes que queremos explorar
    if meses:
        producto = producto[producto["Mes"] == n_mes]

    #elimina las columnas no relevantes para la regresion
    nuevo = producto.drop(["producto", "ENTIDAD", "Año", "Mes", "Tipo_sequia", "Unnamed: 0", "perdida_ha", "Cosechada_ha"], axis=1)
    nuevo = nuevo.reset_index(drop=True)
    X = nuevo.drop("porcentaje",axis=1)
    Y = nuevo["porcentaje"]

    #selecciona los tamaños de entrenamiento y prueba
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = prueba, random_state=semilla)

    #regresión lineal
    if grado == 1:
      print("función de regresion lineal de "+lista[planta])
      lin_model = LinearRegression()
      lin_model.fit(X_train, Y_train)
      y_train_predict = lin_model.predict(X_train)
      MSE = mean_squared_error(Y_train,y_train_predict)
      print("Entrenamiento: MSE ="+str(MSE))

      y_test_predict = lin_model.predict(X_test)
      MSE = (mean_squared_error(Y_test, y_test_predict))
      print("Pruebas: MSE ="+str(MSE))
      df_predicciones = pd.DataFrame({'valor_real':Y_test, 'prediccion':y_test_predict})
      df_predicciones = df_predicciones.reset_index(drop = True)
      return df_predicciones, lin_model

    #regresión polinomica
    if grado >= 2:
        print("función de regresion polinomica de grado " + str(grado) + " de " + lista[planta])
        poly_model = LinearRegression()
        poly = PolynomialFeatures(degree=grado)

        Xpolytrain = poly.fit_transform(X_train)
        Xpolytest = poly.fit_transform(X_test)

        poly_model.fit(Xpolytrain, Y_train)
        y_train_predict = poly_model.predict(Xpolytrain)

        MSE = mean_squared_error(Y_train,y_train_predict)
        print("Entrenamiento: MSE ="+str(MSE))

        y_test_predict = poly_model.predict(Xpolytest)
        MSE = (mean_squared_error(Y_test, y_test_predict))
        print("Pruebas: MSE ="+str(MSE))

        df_predicciones = pd.DataFrame({'valor_real':Y_test, 'prediccion':y_test_predict})
        df_predicciones = df_predicciones.reset_index(drop = True)
        df_predicciones.head(10)
        return df_predicciones, poly_model
