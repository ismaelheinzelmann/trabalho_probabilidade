import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import variation
from json import dump
from statistics import mode
from stats import kurtosis, assimetria


segmentos = {"1": "Auto-serviço", "2": "Mercado Frio", "3": "Mercado Tradicional"}
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

        output_data.append(
            {
                "segmento": i,
                "marca": marca.title(),
                "valor_central": {
                    "media": media,  # média aritmetica
                    "mediana": mediana,  # valor que divide a amostra ao meio (valor do meio se for impar, media dos valores centrais se for par )
                    "moda": mode(
                        marca_segmento_data
                    ),  # valores que mais aparecem (pode ser 1 ou mais, caso aparecam a mesma quantidade de vezes)
                },
                "dispercao": {
                    "desvio_padrao": desvio_padrao,  # raiz quadrada da variância
                    "erro_padrao": desvio_padrao
                    / np.size(
                        marca_segmento_data
                    ),  # desvio padrão dividido pelo tamanho da amostra
                    "coef_de_variacao": variation(marca_segmento_data),
                },
                "forma":{
                    "curtose": kurtosis(media, desvio_padrao, marca_segmento_data),
                    "simetria": assimetria(media, mediana, desvio_padrao),
                }
            }
        )

    for info in marcas_data:
        plt.hist(
            info["data"], bins="sturges", alpha=0.7, label=f"{info['marca'].title()}"
        )

    plt.title(
        f"Histograma {', '.join([x.title() for x in marcas])} | Segmento {segmentos[str(i)]}"
    )
    plt.legend(loc="upper right")
    plt.savefig(f"segmento_{i}_hist.png")
    plt.clf()

    arrs = [x["data"] for x in marcas_data]
    plt.title(
        f"BoxPlot {', '.join([x.title() for x in marcas])} | Segmento {canais[str(i)]}"
    )
    plt.boxplot(arrs, showmeans=True, labels=[x.title() for x in marcas])
    plt.savefig(f"segment_{i}_boxplot.png")
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

        output_data.append(
            {
                "canal": i,
                "marca": marca.title(),
                "valor_central": {
                    "media": media,  # média aritmetica
                    "mediana": mediana,  # valor que divide a amostra ao meio (valor do meio se for impar, media dos valores centrais se for par )
                    "moda": mode(
                        marca_canal_data
                    ),  # valores que mais aparecem (pode ser 1 ou mais, caso aparecam a mesma quantidade de vezes)
                },
                "dispercao": {
                    "desvio_padrao": desvio_padrao,  # raiz quadrada da variância
                    "erro_padrao": desvio_padrao
                    / np.size(
                        marca_canal_data
                    ),  # desvio padrão dividido pelo tamanho da amostra
                    "coef_de_variacao": variation(marca_canal_data),
                },
                "forma":{
                    "curtose": kurtosis(media, desvio_padrao, marca_canal_data),
                    "simetria": assimetria(media, mediana, desvio_padrao),
                }
            }
        )

    for info in marcas_data:
        plt.hist(
            info["data"], bins="sturges", alpha=0.7, label=f"{info['marca'].title()}"
        )

    plt.title(
        f"Histograma {', '.join([x.title() for x in marcas])} | Canal {canais[str(i)]}"
    )
    plt.legend(loc="upper right")
    plt.savefig(f"canal_{i}_hist.png")
    plt.clf()

    plt.title(
        f"BoxPlot {', '.join([x.title() for x in marcas])} | Canal {canais[str(i)]}"
    )
    arrs = [x["data"] for x in marcas_data]
    plt.boxplot(arrs, showmeans=True, labels=[x.title() for x in marcas])
    plt.savefig(f"canal_{i}_boxplot.png")
    plt.clf()


with open("TAREFA_PROB_OUTPUT.json", "w+") as fp:
    dump(output_data, fp)

