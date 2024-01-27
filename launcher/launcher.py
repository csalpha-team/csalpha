from abstract_launcher import LauncherBase
import warnings

class Launcher(LauncherBase):
    def __init__(self) -> None:
        self._dic_input = {
            "NomeAgenteVenda": None,
            "LocalDoAgenteQueVende": None,
            "TipoAgenteQueVende": None,
            "SetorDoAgenteQueVendeI": None,
            "SetorDoAgenteQueVendeII": None,
            "SetorDoAgenteQueVendeIII": None,
            "NomeAgenteCompra": None,
            "LocalDoAgenteQueCompra": None,
            "TipoAgenteQueCompra": None,
            "SetorDoAgenteQueCompraI": None,
            "SetorDoAgenteQueCompraII": None,
            "SetorDoAgenteQueCompraIII": None,
            "Produto": None,
            "Unidade": None,
            "Quantidade": None,
            "PrecoPesquisa": None,
            "PrecoAgenteNoCircuito": None,
            "PrecoSetorAlfaNaTabela": None,
            "PrecoBaseDoValor": None,
            "Valor": None,
            "NumeroDeAgentesVendaNoLancamento": None,
            "NumeroDeAgentesCompraNoLancamento": None,
            "NumeroDoCircuito": None,
            "NumeroDoLancamento": None,
            "SituacaoCircuito": None,
            "SituacaoLancamento": None,
        
        }
    
    def input_data(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._dic_input.keys():
                if not self._dic_input[key]:
                    self._dic_input[key] = value
                else:
                    continue

            else:
                warnings.warn(f"Key {key} not found in the dictionary", UserWarning)


    def remove_data(self, *args):
        for key in args:
            if key in self._dic_input.keys():
                    self._dic_input[key] = None
            else:
                continue


    def check_data(self) -> str:
        return self._dic_input