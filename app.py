import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import variation
from json import dump
from statistics import mode
from stats import kurtosis, assimetria


segmentos = {"1": "Auto-serviço",
             "2": "Mercado Frio", "3": "Mercado Tradicional"}
canais = {
    "1": "Hipermercados com no mínimo 10 caixas",
    "2": "Depósito de bebidas multimarcas",
    "3": "Bares e Lanchonetes",
    "4": "Restaurantes, Churrascarias e Pizzarias",
    "5": "Padarias e Confeitarias",
    "6": "Lojas de conveniência",
    "7": "Mercados com 3 a 4 caixas",
    "8": "Minimercados com 1 a 2 caixas",
}
# Produto;Estabelecimento;Cidade;segmento;Canal;Bairro;Marca;Valor
csv_data = []
output_data = []

with open("DADOS_SC_PROB.csv", "r") as input_data:
    for line in input_data:
        spl = line.split(";")
        spl[-1] = spl[-1].replace("\n", "").replace(",", ".")

        # (segmento, marca, valor)
        csv_data.append((int(spl[3]), int(spl[4]), spl[-2], float(spl[-1])))

marcas = set()
for data in csv_data:
    marcas.add(data[-2].lower())

# Por Segmento
for i in range(1, 4):
    segmento_data = list(filter(lambda d: d[0] == i, csv_data))

    marcas_data = []
    for marca in marcas:
        marca_segmento_data = np.array([], dtype=np.float64)
        for data in segmento_data:
            if data[2].lower() == marca:
                marca_segmento_data = np.append(marca_segmento_data, data[-1])

        marcas_data.append({"marca": marca, "data": marca_segmento_data})

        desvio_padrao = marca_segmento_data.std()
        mediana = np.median(marca_segmento_data)
        media = marca_segmento_data.mean()
        curtose = kurtosis(marca_segmento_data)
        simetria = assimetria(media, mediana, desvio_padrao)

        output_data.append(
            {
                "segmento": i,
                "marca": marca.title(),
                "n_amostral": marca_segmento_data.size,
                "media": media,  # média aritmetica
                # valor que divide a amostra ao meio (valor do meio se for impar, media dos valores centrais se for par )
                "mediana": mediana,
                "moda": mode(
                    marca_segmento_data
                ),  # valores que mais aparecem (pode ser 1 ou mais, caso aparecam a mesma quantidade de vezes)
                "desvio_padrao": desvio_padrao,  # raiz quadrada da variância
                "erro_padrao": desvio_padrao
                / np.size(
                    marca_segmento_data
                ),  # desvio padrão dividido pelo tamanho da amostra
                "coef_de_variacao": variation(marca_segmento_data),
                "coef_curtose": curtose[0],
                "classificacao_curtose": curtose[1],
                "coef_simetria": simetria[0],
                "classificacao_simetria": simetria[1]
            }
        )

    #initial plot
    fig = plt.figure(figsize=(10, 7))
    plt.title(
        f"Histograma e Boxplot{', '.join([x.title() for x in marcas])} | {segmentos[str(i)]}")
    plt.axis('off')
    #end initial plot

    #histogram plot
    fig.add_subplot(1, 2, 1)
    for info in marcas_data:
        plt.hist(
            info["data"], bins="sturges", alpha=0.7, label=f"{info['marca'].title()}"
        )
    plt.legend(loc="upper right")
    #end histogram plot

    #boxplot plot
    fig.add_subplot(1, 2, 2)
    arrs = [x["data"] for x in marcas_data]
    plt.boxplot(arrs, showmeans=True, labels=[x.title() for x in marcas])
    #end boxplot plot
    
    plt.savefig(f"segmento_{i}.png")
    plt.clf()

# Por canal
for i in range(1, 9):
    canal_data = list(filter(lambda d: d[1] == i, csv_data))
    marcas_data = []
    for marca in marcas:
        marca_canal_data = np.array([], dtype=np.float64)
        for data in canal_data:
            if data[2].lower() == marca:
                marca_canal_data = np.append(marca_canal_data, data[-1])

        marcas_data.append({"marca": marca, "data": marca_canal_data})

        desvio_padrao = marca_canal_data.std()
        mediana = np.median(marca_canal_data)
        media = marca_canal_data.mean()
        curtose = kurtosis(marca_canal_data)
        simetria = assimetria(media, mediana, desvio_padrao)
        output_data.append(
            {
                "canal": i,
                "marca": marca.title(),
                "n_amostral": marca_canal_data.size,
                "media": media,  # média aritmetica
                # valor que divide a amostra ao meio (valor do meio se for impar, media dos valores centrais se for par )
                "mediana": mediana,
                "moda": mode(
                    marca_canal_data
                ),  # valores que mais aparecem (pode ser 1 ou mais, caso aparecam a mesma quantidade de vezes)
                "desvio_padrao": desvio_padrao,  # raiz quadrada da variância
                "erro_padrao": desvio_padrao
                / np.size(
                    marca_canal_data
                ),  # desvio padrão dividido pelo tamanho da amostra
                "coef_de_variacao": variation(marca_canal_data),
                "coef_curtose": curtose[0],
                "classificacao_curtose": curtose[1],
                "coef_simetria": simetria[0],
                "classificacao_simetria": simetria[1],
            }
        )

    fig = plt.figure(figsize=(10, 7))
    plt.title(
        f"Histograma e Boxplot{', '.join([x.title() for x in marcas])} | {canais[str(i)]}")
    plt.axis('off')

    fig.add_subplot(1, 2, 1)
    for info in marcas_data:
        plt.hist(
            info["data"], bins="sturges", alpha=0.7, label=f"{info['marca'].title()}"
        )
    plt.legend(loc="upper right")
    fig.add_subplot(1, 2, 2)
    arrs = [x["data"] for x in marcas_data]
    plt.boxplot(arrs, showmeans=True, labels=[x.title() for x in marcas])
    plt.savefig(f"canal_{i}.png")
    plt.clf()


with open("TAREFA_PROB_OUTPUT.json", "w+") as fp:
    dump(output_data, fp)

with open("TAREFA_DADOS_OUTPUT.txt", "w+") as fp:
    for data in output_data:
        for k, v in data.items():
            if isinstance(v, float):
                fp.write(f"{str(k).title().replace('_', ' ')} : {v:.3f}\n")
            else:
                fp.write(f"{str(k).title().replace('_', ' ')} : {v}\n")
        fp.write("\n")
