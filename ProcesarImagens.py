import os
import cv2 as cv
from PIL import Image
from imutils import paths


def tratar_imagens(pasta_origem, pasta_destino=None):
    '''
    (path/string, path/string) --> None
    Processa as imagens limpando o ruido.
    Argumentos:
        pasta_origem: (Obrigatorio) Nome da pasta que contem as imagens para processar
        pasta_destino: (Opcional) Nome da pasta onde serão guardadas as imagens processadas. Se não for informada,
            a pasta de destino sera a mesma de origem, substituindo as imagens originais pelas imagens processadas
    Retorno: None
        O retorno da função são as imagens tratadas na pasta de destino
    '''
    if pasta_destino == None:
        pasta_destino = pasta_origem
    
    lista_imagens = os.listdir(pasta_origem)
    
    for nmImagem in lista_imagens:
        imagem = cv.imread(f'{pasta_origem}/{nmImagem}')

        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        _, imagem = cv.threshold(imagem, 127, 255, cv.THRESH_TRUNC or cv.THRESH_OTSU)   
        cv.imwrite(f'{pasta_origem}/{nmImagem}', imagem)

        imagem = Image.open(f'{pasta_origem}/{nmImagem}')
        imagem = imagem.convert("P")                   
        imagem2 = Image.new("P", imagem.size, (255, 255, 255))

        for x in range(imagem.size[1]):
            for y in range(imagem.size[0]):
                pixel = imagem.getpixel((y, x))
                if pixel < 127:
                    imagem2.putpixel((y, x), (0, 0, 0))
                else:
                    imagem2.putpixel((y, x), (255, 255, 255))

        imagem2.save(f'{pasta_destino}/{nmImagem}')
        
        
def separar_letras(pasta_origem, pasta_destino):
    '''
    (path/string, path/string) --> None
    Procesa as imagens para obter as letras.
    Argumentos:
        pasta_origem: Caminho da pasta que contem as imagens a ser processadas
        pasta_destino: Caminho da pasta onde serão guardadas as letras
    Retorno: None
        Na pasta_destino são guardadas as imagens das letreas
        Na pasta de destino cria uma pasta de nome "rec" onde almacena as imagens da pasta de origem 
        com um contorno para cada letra
        '''
    pasta_rec = os.path.join(pasta_destino, 'rec')

    if not os.path.exists(pasta_rec):
        os.mkdir(pasta_rec)

    lista_imagens = paths.list_images(pasta_origem)

    for rotaImagem in lista_imagens:
        imagem = cv.imread(rotaImagem)
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        _, imagem_inv = cv.threshold(imagem, 0, 255, cv.THRESH_BINARY_INV)

        # buscar os contornos da letra
        contornos, _ = cv.findContours(imagem_inv, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        area_letras = []
        for contorno in contornos:
            (x, y, l, a) = cv.boundingRect(contorno)
            area = cv.contourArea(contorno)
            if area > 220:
                area_letras.append((x, y, l, a))

        if len(area_letras) != 5:
            continue

        imagem_final = cv.merge([imagem] * 3)
        i = 1
        for retangulo in area_letras:
            x, y, l, a = retangulo
            letra  = imagem[y-2:y+a+2, x-2:x+l+2]
            nmImagem = rotaImagem.split(os.sep)[-1].replace('.png', '')
            try:
                cv.imwrite(f'{pasta_destino}/{nmImagem}{i}.png', letra)
            except:
                continue
            i += 1
            cv.rectangle(imagem_final, (x-2, y-2), ( x+l+2, y+a+2), (0,255,0), 1)

        cv.imwrite(f'{pasta_rec}/{nmImagem}.png', imagem_final)
        

def classificar_letras(pasta_letras, pasta_base):
    '''
    (path/string, path/string) --> None
    Classificação semi-automatica das imagens de letras. Mostra na tela uma imagem; o ususario debe digitar a letra
    correspondente a imagem. A função ira guardar a imagem na pasta da letra digitada.
    Argumentos:
        pasta_letras: Caminho da pasta que contem as imagens das letras
        pasta_base: Caminho da pasta que contem o diretorio com uma pasta para cada letra
    Retorno = None
        O retorno é guardar cada letra na pasta correspondente
        '''

    lista = os.listdir(pasta_letras)[0:500]

    tecla = 0
    for i, nm_imagem in enumerate(lista):
        im_letra = cv.imread(f'{pasta_letras}/{nm_imagem}')

        try:
            cv.imshow('letra', im_letra)
        except:
            continue

        tecla = cv.waitKey()
        while tecla == 0:
            time.sleep(1)
        if tecla != 0:
            if tecla == 27:        
                cv.destroyAllWindows()
                break
            elif tecla == 42:
                cv.destroyAllWindows()
                continue
            else:
                pasta = chr(tecla).capitalize()
                cv.imwrite(f'{pasta_base}/{pasta}/{i}.png', im_letra)
                cv.destroyAllWindows()
    cv.destroyAllWindows()
    
    # Listar e printar a quantidade de letras de cada uma
    lista = os.listdir(pasta_base)
    for pasta in lista:
        lista_imagens = os.listdir(f'{pasta_base}/{pasta}')
        print(f'Pasta {pasta} = {len(lista_imagens)} imagens')
        
        
        
if __name__ == '__main__':
    
    pasta_origem = 'imagens'
    pasta_destino = 'imgsTratadas'

    tratar_imagens(pasta_origem, pasta_destino)

    pasta_origem = pasta_destino
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
            
    # Clasificação inicial semi-automatica:
        # Esse programa exibe a imagem de uma letra. Debe ser digitada a letra da imagen no teclado. 
        # O programa almacena a letra na pasta correspondente.
            # Use '*' para ignorar a letra (por não reconhecer, ou achar que é suficinete to tipo). 
            # Use 'ESC' para terminar o programa      
            
    pasta_letras = 'letras' # caminho da pasta que contem as letras separadas
    pasta_base = 'base_letras' # caminho da pasta onde foi criado um pasta para cada letra

    lista = os.listdir(pasta_letras)[0:500]

    tecla = 0
    for i, nm_imagem in enumerate(lista):
        im_letra = cv.imread(f'{pasta_letras}/{nm_imagem}') 
        cv.imshow('letra', im_letra)
        tecla = cv.waitKey()
        while tecla == 0:
            time.sleep(1)
        if tecla != 0:
            if tecla == 27:        
                cv.destroyAllWindows()
                break
            elif tecla == 42:
                cv.destroyAllWindows()
                continue
            else:
                pasta = chr(tecla).capitalize()
                cv.imwrite(f'{pasta_base}/{pasta}/{i}.png', im_letra)
                cv.destroyAllWindows()
    cv.destroyAllWindows()
    
    # Listar e printar a quantidade de letras de cada uma
    lista = os.listdir(pasta_base)
    for pasta in lista:
        lista_imagens = os.listdir(f'{pasta_base}/{pasta}')
        print(f'Pasta {pasta} = {len(lista_imagens)} imagens')
        
        
# Apos esta etapa debe ser analizada cada pasta em busca de erros e preferivelmente para igualar a quantidade de cada letra
# Sugerido 10 imagens de cada letra
# Nesse ponto nossos arquivos estão prontos para o primeiro treino do modelo

