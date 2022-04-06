import cv2 as cv
import os
import numpy as np
import pickle
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from helpers import resize_to_fit

def treinar(pastaBase):
    '''
    (path/string) --> ia model, labelBinarizer
    Treina o modelo com deep learning para identificar as letras
    Argumentos:
        pastaBase: Caminho da pasta que contem os directorios de cada letra 
    Retorno:
        modelo: modelo treinado
        lb: tradutor de respostas de modelo
    '''
    dados = []
    rotulos = []

    imagens = paths.list_images(pastaBase)
    for arquivo in imagens:
        rotulo = arquivo.split(os.path.sep)[-2]
        imagem = cv.imread(arquivo)
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        imagem = resize_to_fit(imagem, 20, 20) # Padronizar a imagem para 20px * 20px

        imagem = np.expand_dims(imagem, axis=2) # Adicionando uma terceira dimensão a imagem

        rotulos.append(rotulo)
        dados.append(imagem)

    dados = np.array(dados, dtype='float') / 255 # Padronozar entre 0 e 1
    rotulos = np.array(rotulos)

    # Separar os dados
    (x_train, x_test, y_train, y_test) = train_test_split(dados, rotulos, test_size=0.25, random_state=0)

    # Tratar os rotulos (são letras)
    lb = LabelBinarizer().fit(y_train)
    y_train = lb.transform(y_train)
    y_test = lb.transform(y_test)

    # criar modelo
    modelo = Sequential()

    # adicionar camadas
    modelo.add(Conv2D(20, (5,5), padding='same', input_shape=(20, 20, 1), activation='relu'))
    modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2)))

    modelo.add(Conv2D(50, (5,5), padding='same', activation='relu'))
    modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2)))

    modelo.add(Flatten())
    modelo.add(Dense(500, activation='relu'))

    modelo.add(Dense(26, activation='softmax'))

    # compilar as camadas
    modelo.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # treinar 
    modelo.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=26, epochs=10, verbose=1)
    
#     Salvar o LabelBinarizer (tradutor)
#     with open('rotulos_model.dat', 'wb') as arquivo:
#         pickle.dump(lb, arquivo)

#     salvar o modelo em um arquivo
#     modelo.save('modeloTreinado.hdf5')

    return modelo, lb

