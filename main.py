#!/usr/bin/env python
# coding: utf-8

# In[3]:


from ProcesarImagens import tratar_imagens, separar_letras, classificar_letras
from PrevisaoClasificatoria import clasificar_previsao
from TreinarModelo import treinar
import os
import pickle
import time    

step = 1

if step == 1:
    start = time.time()
    print('Iniciando passo 1')
    pasta_origem = 'images'
    pasta_destino = 'imgsTratadas'

    tratar_imagens(pasta_origem, pasta_destino)

    pasta_origem = 'imgsTratadas'
    pasta_destino = 'letras'

    separar_letras(pasta_origem, pasta_destino)

    # Criar um pasta para cada letra
    alfabeto = 'abcdefghijklmnopqrstuvwyxz'
    for letra in alfabeto:
        letra = letra.capitalize()
        try:
            os.mkdir(f'base_letras/{letra}')
        except:
            continue

    pasta_letras = 'letras' # diretorio que almacena as letras
    pasta_base = 'base_letras' # diretorio que contem uma pasta para cada letra
    
    classificar_letras(pasta_letras, pasta_base)
    end = time.time()
    print(f'Fim do passo 1. Tempo: {end-start}')

    
# Apos esta etapa debe ser analizada cada pasta em busca de erros e preferivelmente para igualar a quantidade de cada letra
# Sugerido 10 imagens de cada letra
# Nesse ponto nossos arquivos estão prontos para o primeiro treino do modelo
# Alterar a variavel step para 2 para continuar no proximo paso


if step == 2:
    
    pasta_base = 'base_letras' # Diretorio que contem uma pasta para cada letra
    
    modelo, lb = treinar(pasta_base)
    
    pasta_letras = 'letras' # Diretorio que contem as letras
   
    clasificar_previsao(pasta_letras, pasta_base, modelo, lb) # Amplia a base de letras 
    
# Após esse passo devem ser revisadas manualmente as pastas de cada letra para buscar erros na previsão do modelo
# A continuação o modelo sera novamente treinado com a nova e maior base de dados
# Para continuar alterar a variavel step para 3


if step == 3:
    print("Inicio do passo 3") 
    
    pasta_base = 'base_letras'
    
    modelo, lb = treinar(pasta_base) # Treino final do modelo
    
    modelo.save('modeloTreinado.hdf5') # Salvar o modelo 
    
    with open('tradutor.dat', 'wb') as tradutor:
        pickle.dump(lb, tradutor)
        
    print('Fin do passo 3')

