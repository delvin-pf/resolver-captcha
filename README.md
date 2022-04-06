# resolver-captcha
 Criar e usar um modelo de IA para resolver captchas de texto

Nesse projeto criamos, treinamos e usamos um modelo de inteligencia artificial para reconhecer letras em imagens de captchas.

Utilidade
A quebra de captcha pode ser util quando precisamos fazer Web Scrapping e encontramos uma trava por meio de captcha de texto. 

Como usar
Para iniciar deve ser criada uma pasta com imagens em formato .png dos captchas que deseja resolver. 

Arquivos do projeto:

main.py: esta dividido em tres passos:
    Paso 1: Tratamento de imagens.
        - Haverá uma clasificação semi-automatica. Sera mostrado a imagem de uma letra, deve digitar no teclado a letra correspondente (Mais info, ProcessarImagens.py)
        - Como resultado desse passo, havera uma nova pasta na raiz do arquivo main.py, e uma pasta chamada 'base_letras' contendo uma pasta para cada letra.
        - Deve ser feita uma revisão manual para verificar as pasta de cada letra (quatidade e exatitud)
    Paso 2: Treino inicial do modelo e previsão clasificatoria
        - Usando o modelo de IA, clasificara o restante das letras não clasificadas anteriormente.
        - Após o passo deve ser feita uma nova revisão manual para corrigir erros da IA
    Paso 3: Treino final, salvar o modelo e o tradutor
         - Com uma base de letras maior, sera treinada a IA novamente.

ProcessarImagens.py contem funcões relacionadas com a limpeza das imagens, separação de letras e clasificação semi-automatica de letras

TreinarModelo.py contem a função de treinamento do nosso modelo

PrevisaoClasificatoria.py contem a função que usara o modelo para o clasificar as letras no passo 2

helpers.py contem uma função usada para processar imagens (arquivo externo)

ResolverCaptcha.py contem a função que faz uso do modelo de IA ja plenamente treinado para resolver captchas.
