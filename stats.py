import numpy as np

def assimetria(media, mediana, desvio_padrao):
    coef = (3 * (media - mediana)) / desvio_padrao

    if coef > -1 and coef < 1:
        return [coef, "Simetrica"]
    elif coef < -1:
        return [coef, "Negativo (ou a esquerda)"]
    elif coef > 1:
        return [coef, "Positivo (ou a direita)"]

def kurtosis(arr):
    #sintaxe
    #np.percentile(arr, 90) percentil 90 do arr
    p90 = np.percentile(arr, 90)
    p10 = np.percentile(arr, 10)
    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)

    curtose = round((q3 - q1)/ (2*(p90 - p10)), 3)
    if curtose < 0.263:
        return [curtose, "Leptocurtica"]
    if curtose == 0.263:
        return [curtose, "Mesocurtica"]
    else:
        return [curtose, "Platicurtica"]

v = np.array([])