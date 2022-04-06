from keras.models import load_model
from helpers import resize_to_fit
import numpy as np
import pickle
from imutils import paths
import cv2 as cv
import time
from procesarImagens import tratar_imagens

def resolver_captcha(pasta_captcha):
    '''
    (path/string) --> list
    Resolve o captcha a partir de uuma imagen.
    Argumentos:
        pasta_captcha: pasta que contem os capcha a ser resolvidos
    Retorno: 
        lista_prev = lista com as previsões dos captchas'''
    
    
    with open('tradutor.dat', 'rb') as tradutor:
        lb = pickle.load(tradutor)
        
    modelo = load_model('modeloTreinado.hdf5')
    
    tratar_imagens(pasta_captcha)
    
    arquivos = list(paths.list_images(pasta_captcha))
    
    lista_prev = []
    
    for caminho_im in arquivos:
        # ler imagem
        imagem = cv.imread(caminho_im)
        #tratar imagem
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        _, imagem_inv = cv.threshold(imagem, 0, 255, cv.THRESH_BINARY_INV) # inverter a imagem para o proximo paso
         
        contornos, _ = cv.findContours(imagem_inv, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        area_letras = []
        for contorno in contornos:
            (x, y, l, a) = cv.boundingRect(contorno)
            area = cv.contourArea(contorno)
            if area > 220:
                area_letras.append((x, y, l, a))

        area_letras = sorted(area_letras, key=lambda x: x[0])
        
        previsao = []
        for area in area_letras:
            x, y, l, a = area
            imLetra  = imagem[y-2:y+a+2, x-2:x+l+2]
            # tratamento imagem da letra
            imLetra = resize_to_fit(imLetra, 20, 20) # Padronizar a imagem para 20px * 20px
            imLetra = np.expand_dims(imLetra, axis=2) # Adicionando uma terceira dimensão á imagem
            imLetra = np.expand_dims(imLetra, axis=0) # Adicionando uma primeira dimensão á imagem (total: 4)
            
            #imLetra = np.array(imLetra, dtype='float') / 255 # Padronozar entre 0 e 1

            letra_prevista = modelo.predict(imLetra)
            letra_prevista = lb.inverse_transform(letra_prevista)[0]
            previsao.append(letra_prevista)
        
        texto_previsao = ''.join(previsao)
        
        lista_prev.append(texto_previsao)
        
    return lista_prev


if __name__ == '__main__':
    lista = resolver_captcha('teste')
    print(lista)

