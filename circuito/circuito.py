from .abstract_circuito import CircuitoBase
import pandas as pd
import warnings


class Circuito(CircuitoBase):
    """
    Classe que abriga um conjunto de métodos para verificar o estado dos circuitos e suas
    as condições de fechamento do circuito

    
    * Lembre-se a classe é uma própria estrutura de dados * 
    * organizar sistÊmicamente a realidade em que os dados estão inseridos 
    * inserindo-os em planos mais amplos; 
    Atributos
    ---------
    _dic_input : dict
        Dicionário com id_circuito como chave e classe circuito como valor

        dict= [
                {
                    idlancamento1: Lancamento()
                    },
                {   idlancamento2: Lancamento()
                    },
                ] 

        self._idcircuito = SHA(seed) #cada id só pode ser gerado uma vez; 
        get & setter para id_circuito: retrieve and modify the id_circuito

        
        dict = {
            id_circuito : {
                id_lancamento : { 
                                {id_lancamento : classe_lancamento},
                }
                
        }

        #get_idcircuito()
        #setter_idcircuito() 

    Métodos
    -------
    visualize_state(**kwargs)
        Visualiza a quantidade de circuitos existentes e seus estados;

    """

    

    #! A média é calculada em função das relações entre entre par de setores;
    #! Serão 2 métodos:
        # Construção de médias parciais no momento de um lançamento?
        # Ajuste final da média no momento em que os circuitos são de fato
        #fechados; 
    

        
        
            
        
        
        
        
    

