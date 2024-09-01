# Vitreus

Projeto de TCC que consiste em receber um arquivo edf e predizer se o arquivo representa um exame de paciente com PNES ou SE 


# Mapa do projeto 

## App 
    pasta que contém os códigos do projeto 
        - config.py
            carrega o arquivo config.ini e inicia as variaveis de configuração para rodar o projeto 
        - edf_to_csv.py
            lê todos os edfs da pasta raw e transforma em xlsx (para otimizar espaço transformar em csv dps)
        - make_dataset.py
            lê todos os exames processados, aplica transformada de wavelet e cria 3 versões de dataset
        - make_prediction.py
            recebe um arquivo de exame teste , carrega o artefato do modelo e faz um predição 
        - train_svm.py
            treina o modelo com o dataset criado e cria um artefato do modelo para realizar futuras predições

## Data 
    pasta que contem os dados do projeto 
        - exams
            exames brutos e processados dos pascientes com pnes e se 
        - datasets
            lore impsun 
        - model.pkl 
            artefato para inferencia de exames 
        - test_exam
            exame de teste do modelo 

# Ordem de execução 

    1 - edf_to_csv.py
    2 - make_dataset.py
    3 - train_svm.py
    4 - make_prediction.py