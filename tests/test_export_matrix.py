import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from matrices.export_matrix import ExportMatrix

@pytest.fixture(scope="module")
def hardcode_data():
    dados = {
        "Setor": [
            "AAProdução", 
            "ACVarejoRural", "AFIndustBenef", "AGIndustTransf", "AHAtacado", "AIVarejoUrbano",
            "BFIndustBenef", "BGIndustTransf", "BHAtacado", "BIVarejoUrbano", "CFIndustBenef", "CGIndustTransf",
            "CHAtacado", "CIVarejoUrbano", "Total"
            ],
        "Produção": [0]*15,
        "ACVarejoRural":     [0.676723, 0.000376, 0.000000, 0.000000, 0.000257, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.677356],
        "AFIndustBenef":     [0.167359, 0.175900, 0.000000, 0.000000, 0.002498, 0.004868, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.350625],
        "AGIndustTransf":    [0.000055, 0.000028, 0.000105, 0.000000, 0.000000, 0.000006, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000195],
        "AHAtacado":         [0.050208, 0.009095, 0.000040, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.059342],
        "AIVarejoUrbano":    [0.007316, 0.000982, 0.000328, 0.000000, 0.000000, 0.000000, 0.000744, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.009371],
        "AJConFinLocal":     [0.011758, 0.008002, 0.310155, 0.000195, 0.000028, 0.000952, 0.000000, 0.000000, 0.000204, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.331293],
        "BFIndustBenef":     [0.005856, 0.401013, 0.000086, 0.000000, 0.052061, 0.003721, 0.000000, 0.000000, 0.133817, 0.000532, 0.000000, 0.000000, 0.000000, 0.000000, 0.597087],
        "BGIndustTransf":    [0.000001, 0.000000, 0.000321, 0.000000, 0.004008, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.004330],
        "BHAtacado":         [0.070439, 0.062742, 0.000539, 0.000000, 0.000301, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.134022],
        "BIVarejoUrbano":    [0.000045, 0.000000, 0.000001, 0.000000, 0.000199, 0.000000, 0.014704, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.014950],
        "BJConFinEstadual":  [0.000002, 0.000000, 0.000042, 0.000000, 0.000000, 0.000000, 0.131392, 0.000001, 0.000000, 0.014418, 0.000000, 0.000000, 0.000000, 0.000000, 0.145855],
        "CFIndustBenef":     [0.010167, 0.003251, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.007765, 0.000000, 0.021183],
        "CGIndustTransf":    [0.000000, 0.000000, 0.000412, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000412],
        "CHAtacado":         [0.000071, 0.014247, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.014318],
        "CIVarejoUrbano":    [0.000000, 0.001856, 0.038503, 0.000000, 0.000000, 0.000000, 0.431780, 0.004008, 0.000000, 0.000000, 0.000000, 0.000000, 0.006553, 0.000000, 0.482700],
        "CJConFinNacional":  [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.018213, 0.000321, 0.000000, 0.000000, 0.021183, 0.000412, 0.000000, 0.482700, 0.522829],
        "Total":            [1.000000, 0.677492, 0.350532, 0.000195, 0.059353, 0.009547, 0.596833, 0.004330, 0.134022, 0.014950, 0.021183, 0.000412, 0.014318, 0.482700, 3.365868]
        }

    df_teste = pd.DataFrame(dados).set_index("Setor").round(3)

    dados = {
    "Produção": [0] * 15,
    "ACVarejoRural":     [0.804960, 0.681041, 0.000000, 0.000000, 1.127111, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.805013],
    "AFIndustBenef":     [1.482340, 1.361630, 0.000000, 0.000000, 1.463850, 3.007692, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.442438],
    "AGIndustTransf":    [4.332123, 1.801789, 4.431797, 0.000000, 0.000000, 2.767888, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 3.971571],
    "AHAtacado":         [0.789047, 0.672730, 9.658322, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.777137],
    "AIVarejoUrbano":    [1.494891, 1.846849, 4.386225, 0.000000, 0.000000, 0.000000, 1.916523, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.661870],
    "AJConFinLocal":     [1.641122, 1.321818, 2.396948, 62.580836, 9.658322, 4.577482, 0.000000, 0.000000, 2.333343, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 2.386220],
    "BFIndustBenef":     [1.278902, 0.830587, 1.194809, 0.000000, 1.108492, 3.998095, 0.000000, 0.000000, 1.796997, 1.404919, 0.000000, 0.000000, 0.000000, 0.000000, 1.095686],
    "BGIndustTransf":    [9.474704, 0.000000, 1.194809, 0.000000, 0.764678, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.799345],
    "BHAtacado":         [1.246107, 1.331268, 2.098102, 0.000000, 1.126070, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.289135],
    "BIVarejoUrbano":    [1.135048, 0.000000, 3.174959, 0.000000, 1.127111, 0.000000, 2.568840, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 2.534339],
    "BJConFinEstadual":  [3.151147, 0.000000, 2.173061, 0.000000, 0.000000, 0.000000, 2.883265, 12.155531, 0.000000, 3.369429, 0.000000, 0.000000, 0.000000, 0.000000, 2.932007],
    "CFIndustBenef":     [1.446094, 1.342817, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.735158, 0.000000, 1.536206],
    "CGIndustTransf":    [0.000000, 0.000000, 3.146331, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 3.146331],
    "CHAtacado":         [0.599472, 1.960897, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.954146],
    "CIVarejoUrbano":    [0.000000, 1.383915, 2.836885, 0.000000, 0.000000, 0.000000, 2.650035, 0.955847, 0.000000, 0.000000, 0.000000, 0.000000, 3.201179, 0.000000, 2.654951],
    "CJConFinNacional":  [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 2.616632, 1.194809, 0.000000, 0.000000, 2.288072, 3.883130, 0.000000, 3.529151, 3.427303],
    "Total":             [1.000000, 1.093860, 2.447401, 62.580836, 1.102719, 3.483208, 2.697427, 0.977163, 1.798224, 3.322280, 2.288072, 3.883130, 2.406144, 3.529151, 1.872773]
}

    index = [
    "AAProdução", 
    "ACVarejoRural", "AFIndustBenef", "AGIndustTransf", "AHAtacado",
    "AIVarejoUrbano", "BFIndustBenef", "BGIndustTransf", "BHAtacado", "BIVarejoUrbano",
    "CFIndustBenef", "CGIndustTransf", "CHAtacado", "CIVarejoUrbano", "Total"
    ]

    matriz_formacao_preco = pd.DataFrame(dados, index=index).round(3)

    quantidade_total = 697281.18     
    exportacao_USD = 23862.02 
    param_exportacao = {
    'BFIndustBenef': 0.795,
    'BGIndustTransf': 0.005,
    'CFIndustBenef': 0.196,
    'CGIndustTransf': 0.004
    }
    preco_implicito = 2.73
    preco = 2.09
    #cambio = 5.16
    default_export_value = 14.09

    df_fluxo_quantidade = df_teste * quantidade_total

    quantidade_exportada = {setor: (prop * exportacao_USD) / preco_implicito
                            for setor, prop in param_exportacao.items()}

    df_fluxo = df_fluxo_quantidade.copy()

    df_fluxo['ExportacaoRestoMundo'] = 0.0
    for setor, qty in quantidade_exportada.items():
        df_fluxo.at[setor, 'ExportacaoRestoMundo'] = qty
    df_fluxo['CJConFinNacional'] -= df_fluxo['ExportacaoRestoMundo']
    df_fluxo = df_fluxo[['CJConFinNacional', 'ExportacaoRestoMundo', 'Total']]

    precos_export = matriz_formacao_preco * preco
    precos_export['ExportacaoRestoMundo'] = default_export_value

    final_matrix = (precos_export * df_fluxo).round(2)
    final_matrix = final_matrix.loc[:'CIVarejoUrbano', :'ExportacaoRestoMundo'].copy()
    final_matrix['Total'] = final_matrix.sum(axis=1)

    return {
        'parameters': df_teste.reset_index(),
        'prices': matriz_formacao_preco.reset_index(),
        'fluxo_quantidade': df_fluxo_quantidade,
        'fluxo_ajustado': df_fluxo,
        'precos_export': precos_export,
        'final_matrix': final_matrix,
        'quantidade_exportada': quantidade_exportada,
        'quantidade_total': quantidade_total,
        'exportacao_USD': exportacao_USD,
        'param_exportacao': param_exportacao,
        'preco_implicito': preco_implicito,
        'preco': preco,
        'default_export_value': default_export_value
    }

@pytest.fixture(scope="module")
def export_matrix(hardcode_data):
    return ExportMatrix(
        df_parameters=hardcode_data['parameters'],
        df_prices=hardcode_data['prices'],
        total_quantity=hardcode_data['quantidade_total'],
        export_usd=hardcode_data['exportacao_USD'],
        export_proportions=hardcode_data['param_exportacao'],
        implicit_price=hardcode_data['preco_implicito'],
        export_price=hardcode_data['preco'],
        default_export_value=hardcode_data['default_export_value']
    )

def test_calculate_quantity_flow(export_matrix, hardcode_data):
    result = export_matrix.calculate_quantity_flow()
    expected = hardcode_data['fluxo_quantidade']
    assert_frame_equal(result, expected, check_exact=False, rtol=1e-5, check_like=True)

def test_calculate_exported_quantity(export_matrix, hardcode_data):
    result = export_matrix.calculate_exported_quantity()
    expected = hardcode_data['quantidade_exportada']
    assert result == pytest.approx(expected, rel=1e-5)

def test_adjust_quantity_flow(export_matrix, hardcode_data):
    fluxo = export_matrix.calculate_quantity_flow()
    quantidade_exportada = export_matrix.calculate_exported_quantity()
    result = export_matrix.adjust_quantity_flow(
        fluxo, quantidade_exportada,
        export_column_name='ExportacaoRestoMundo',
        adjust_column='CJConFinNacional'
    )
    expected = hardcode_data['fluxo_ajustado']
    assert_frame_equal(result, expected, check_exact=False, rtol=1e-5, check_like=True)

def test_adjust_export_prices(export_matrix, hardcode_data):
    result = export_matrix.adjust_export_prices(
        sectors=list(hardcode_data['param_exportacao']),
        export_column_name='ExportacaoRestoMundo'
    )
    expected = hardcode_data['precos_export']
    assert_frame_equal(result, expected, check_exact=False, rtol=1e-5, check_like=True)

def test_calculate_final_export_matrix(export_matrix, hardcode_data):
    fluxo_adj = export_matrix.adjust_quantity_flow(
        export_matrix.calculate_quantity_flow(),
        export_matrix.calculate_exported_quantity(),
        export_column_name='ExportacaoRestoMundo',
        adjust_column='CJConFinNacional'
    )
    precos_adj = export_matrix.adjust_export_prices(
        sectors=list(hardcode_data['param_exportacao']),
        export_column_name='ExportacaoRestoMundo'
    )
    result = export_matrix.calculate_final_export_matrix(
        fluxo_adj,
        precos_adj,
        final_row='CIVarejoUrbano',
        final_column='ExportacaoRestoMundo'
    )
    expected = hardcode_data['final_matrix']
    assert_frame_equal(result, expected, check_exact=False, rtol=1e-5, check_like=True)
