import pandas as pd
import hashlib
import time
from typing import Any

class Table(TableBase):
    """
    Class that presents consolidated data via circuit.

    This is the last level of interface with the user. The table is a composition of circuits.

    Attributes:
        id_table (str): Unique ID for the table.
        _dict_table (dict): Dictionary storing circuits by their IDs.
        _dataframe_table (pd.DataFrame): DataFrame to store the consolidated data via circuits.

    Methods:
        insert_circuit(circuit: Circuit) -> None:
            Inserts a circuit into the table.
        
        remove_circuit(circuit_remove: Any) -> None:
            Removes a circuit from the table by its instance or ID.

        show_table(format: str = 'standard') -> Any:
            Shows the table in the specified format, either 'standard' or 'pandas'.
        
        _generate_id_table(id_tabela: Any = 'auto') -> str:
            Generates a unique ID for the table using SHA-1.
    """

    def __init__(self):
        self.id_table: str = self._generate_id_table()
        self._dict_table: dict = {}
        self._dataframe_table: pd.DataFrame = pd.DataFrame()

    def insert_circuit(self, circuit: Circuit) -> None:
        """
        Inserts a circuit into the table.

        Args:
            circuit (Circuit): The circuit to be inserted.
        """
        self._dict_table.update({circuit.circuit_id: circuit})

    def remove_circuit(self, circuit_remove: Any) -> None:
        """
        Removes a circuit from the table.

        Args:
            circuit_remove (Any): The circuit to be removed, either by instance or ID.
        
        Raises:
            KeyError: If the circuit is not found.
        """
        if isinstance(circuit_remove, Circuit):
            circuit_id = circuit_remove.circuit_id
        else:
            circuit_id = circuit_remove

        try:
            self._dict_table.pop(circuit_id)
        except KeyError as e:
            print("Circuit not found.", e)

    def show_table(self, format: str = 'standard') -> Any:
        """
        Shows the table in the specified format.

        Args:
            format (str): The format to show the table. Must be either 'pandas' or 'standard'.

        Returns:
            Any: The table in the specified format.
        """
        if format == 'standard':
            _dic_show = {}
            for k, v in self._dict_table.items():
                _dic_show.update({k: v.get_launches()})
            return _dic_show
        elif format == 'pandas':
            app_list = []

            for k, v in self._dict_table.items():
                if v.is_closed():
                    app_list.append(v.show_dataframe_circuit())
                else:
                    v.circuit_closed(True)
                    app_list.append(v.show_dataframe_circuit())

            return pd.concat(app_list)

    def _generate_id_table(self, id_tabela: Any = 'auto') -> str:
        """
        Generates a unique ID for the table using SHA-1.

        Args:
            id_tabela (Any): Defines the table ID. If "auto", the ID will be generated from SHA-1 hash. By default, "auto".

        Returns:
            str: Unique ID generated for the table.
        """
        if id_tabela == 'auto':
            seed = str(time.time()) + "36NOYMrLnmlextec"
            id_ = hashlib.sha1(seed.encode()).hexdigest()[:10]
        else:
            id_ = str(id_tabela)

        return id_
