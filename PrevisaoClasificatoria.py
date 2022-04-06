# Expandindo a base de letras com a previsão do modelo
    # Nesse passo a nosa inteligencia vai prever o valor de novas imagens, e colocar na pasta correspondente.
    # Depois faremos uma limpeza manual, realocando as imagens que o modelo separou e colocando-as na pasta certa.
        # Nesse paso o modelo teria feito o maior trabalho
    
from keras.models import load_model
from helpers import resize_to_fit
import os
import numpy as np
import cv2 as cv
from imutils import paths


def clasificar_previsao(pasta_letras, pasta_base, modelo, lb):
    '''
    (path/string, path/string, IA model, LabelBinarizer()) --> None
    Usando o modelo, clasifica o restante das letras. Analiza as letras e copia para a pasta correspondente.
    Argumentos:
        pasta_letras: Diretorio que contem as letras sem clasificar.
        pasta_base: Diretorio que contem uma pasta para cada letra.
        modelo: Modelo treinado.
        lb: Tradutor do modelo.
    Retorno: None
    '''

    lista_imagens = list(paths.list_images(pasta_letras))

    #modelo = load_model('modeloTreinado.hdf5')

    #with open('rotulos_model.dat', 'rb') as tradutor:
    #    lb = pickle.load(tradutor)

    num_imagem = 1000 # numero alto para não interferir com as imagens crianadas anteriormente

    for rotaImagem in lista_imagens:
        imLetra = cv.imread(rotaImagem)
        imLetraBase = imLetra
        imLetra = cv.cvtColor(imLetra, cv.COLOR_BGR2GRAY)

        imLetra = resize_to_fit(imLetra, 20, 20) # Padronizar a imagem para 20px * 20px
        imLetra = np.expand_dims(imLetra, axis=2) # Adicionar uma terceira dimensão a imagem
        imLetra = np.expand_dims(imLetra, axis=0) # Adicionar uma quarta dimensão na poscição 0

        imLetra = np.array(imLetra, dtype='float') / 255 # Padronozar entre 0 e 1

        letra_prevista = modelo.predict(imLetra)
        letra_prevista = lb.inverse_transform(letra_prevista)[0]

        caminho = f'{pasta_base}/{letra_prevista}/{num_imagem}.png'
        cv.imwrite(caminho, imLetraBase)
        num_imagem +=1

