import numpy as np

def assimetria(media, mediana, desvio_padrao):
    coef = (3 * (media - mediana)) / desvio_padrao

    if coef > -1 and coef < 1:
        return "Simetrica"
    elif coef < -1:
        return "Negativo (ou a esquerda)"
    else:
        return "Positivo (ou a direita)"

def kurtosis(media, desvio_padrao, arr):
    size = np.size(arr)
    #create an empty list to store the values of the array
    kurtosis = []
    #loop through the array
    for i in arr:
        #calculate the kurtosis for each value in the array
        kurtosis.append(((i - media) / desvio_padrao) ** 4)
    #return the sum of the kurtosis list divided by the size of the array
    return sum(kurtosis) / size