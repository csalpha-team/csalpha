from .abstract_launcher import LauncherBase
import warnings
from typing import Any
import time
import hashlib

class Launcher(LauncherBase):
    """
    Class that implements data collection for launching a given circuit.
    The data to be collected is strictly associated with the output seen from Netz.

    Attributes
    ----------
    _dic_input : dict
        Dictionary that stores the input data for launching a given circuit.
        The data is stored in a dictionary to facilitate data collection and verification.

    Methods
    -------
    input_data(**kwargs)
        Method that receives the input data for launching a given circuit.
        The data is stored in the _dic_input dictionary.

    remove_data(*args)
        Method that removes the input data for launching a given circuit.
        The data is removed from the _dic_input dictionary.

    check_data()
        Method to check the current status of the launch data,
        returning the list of filled and/or unfilled data.
    """

    def __init__(self, launcher_id='auto') -> None:
        self.launcher_id = self._generate_launcher_id(launcher_id=launcher_id) # Consider how to automatically generate this ID

        self._dic_input = {
            "nomeAgenteVenda": None,
            "localDoAgenteQueVende": None,
            "tipoAgenteQueVende": None,
            "setorDoAgenteQueVendeI": None,
            "setorDoAgenteQueVendeII": None,
            "setorDoAgenteQueVendeIII": None,
            "nomeAgenteCompra": None,
            "localDoAgenteQueCompra": None,
            "tipoAgenteQueCompra": None,
            "setorDoAgenteQueCompraI": None,
            "setorDoAgenteQueCompraII": None,
            "setorDoAgenteQueCompraIII": None,
            "produto": None,
            "unidade": None,
            "quantidade": None,
            "precoPesquisa": None,
            "precoAgenteNoCircuito": None,
            "precoSetorAlfaNaTabela": None,
            "precoBaseDoValor": None,
            "valor": None,
            "numeroDeAgentesVendaNoLancamento": None,
            "numeroDeAgentesCompraNoLancamento": None,
        }
    
    def input_data(self, **kwargs) -> None:
        """
        Method that receives the input data for launching a given circuit.
        The data is stored in the _dic_input dictionary.

        The input data must be associated with a key in the dictionary,
        otherwise a warning will be returned and the data will not be stored.

        The filled field can only be updated once. If the field is already filled,
        the data will not be updated. To update the field, it is necessary to remove
        the data and insert it again.

        Parameters
        ----------
        kwargs : dict
            Dictionary with the input data for launching a given circuit.
            The data is stored in the _dic_input dictionary.
        """
        for key, value in kwargs.items():
            if key in self._dic_input.keys():
                if not self._dic_input[key]:
                    self._dic_input[key] = value
                else:
                    continue
            else:
                warnings.warn(f"Key {key} not found in the dictionary", UserWarning)


    def remove_data(self, *args):
        """
        Method that removes the input data for launching a given circuit.
        The data is removed from the _dic_input dictionary.
        
        Parameters
        ----------
        args : tuple
            Tuple with the input data for launching a given circuit.
            The data is removed from the _dic_input dictionary.
        """
        for key in args:
            if key in self._dic_input.keys():
                    self._dic_input[key] = None
            else:
                continue


    def check_data(self) -> dict:
        """
        Method to check the current status of the launch data,
        returning the list of filled and/or unfilled data.

        Returns
        -------
        dict
            Dictionary with the list of filled and/or unfilled data.
        """
        return self._dic_input
    
    def _generate_launcher_id(self, launcher_id: Any='auto') -> str:
        """
        Generates a unique ID for the launch.

        Parameters
        ----------
        launcher_id : Any
            ID of the launch. If 'auto', a unique ID will be automatically generated.

        Returns
        -------
        str
            Unique ID of the launch.
        """
        if launcher_id == 'auto':
            seed = str(time.time()) + "1ePcWuuN"
            id_ = hashlib.sha1(seed.encode()).hexdigest()[:10]
        else:
            id_ = str(seed)

        return id_