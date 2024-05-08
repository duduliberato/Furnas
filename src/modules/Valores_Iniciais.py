from Headers import headers_turbinas, header_posicoes_turbinas, headers_baterias, header_posicoes_baterias
from types import SimpleNamespace


class Valores_Iniciais:
    # Definição de constantes que serão utilizadas como constantes no programa
    VALORES_INICIAIS = SimpleNamespace(

        # taxa de inflação em dólares corrigida  https://www.bls.gov/data/inflation_calculator.htm
        MULTIPLICADOR_INFLACAO_2012=1.6,
        MULTIPLICADOR_INFLACAO_2019=1.2,
        # Transformação de BTU/ft^3 (BTU sobre pé cubico) para MJ/m^3 (Megajoule sobre metro cúbico)
        # Encontrado em: https://www.eia.gov/energyexplained/units-and-calculators/energy-conversion-calculators.php
        METRO_CUBICO_PARA_PES=35.3,
        # Taxa de juros de 5% ao ano
        TAXA_DE_JUROS=0.1,
        # Considerando que o preço do pé cúbico do gás natural é 0,27051 USD
        # De acordo com: https://www.eia.gov/dnav/ng/hist/n3035us3A.htm
        PRECO_GAS_NATURAL=9.8,
        # Tempo para pagar o valor da turbina em 20 anos de 12 meses
        TEMPO_PAGAR_TURBINA=10 * 12,

        # Para a CCGT - modelo GE 7HA.01 Combined Cycle 1x1: https://www.ge.com/gas-power/products/gas-turbinas/7ha
        CCGT_POTENCIA=400,  # MW
        CCGT_CUSTO_TOTAL=1100,  # $/kW
        CCGT_CUSTO_OM=15 * 1000,  # US$/MW por ano
        CCGT_EFICIENCIA=0.6,  # 62.3%
        CCGT_TEMPO_HOT_START=100,  # Minutos
        CCGT_TEMPO_WARM_START=100,  # Minutos
        CCGT_TEMPO_COLD_START=100,  # Minutos
        CCGT_CUSTO_HOT_START=35,  # $/MW
        CCGT_CUSTO_WARM_START=55,  # $/MW
        CCGT_CUSTO_COLD_START=80,  # $/MW

        # Para a Aero GT - modelo GE LM600: https://www.ge.com/gas-power/products/gas-turbinas/lm6000
        AERO_POTENCIA=100,  # MW
        AERO_CUSTO_TOTAL=1200,  # $/kW
        AERO_CUSTO_OM=16.3 * 1000,  # US$/MW por ano
        AERO_EFICIENCIA=0.4,  # 40.8%
        AERO_TEMPO_HOT_START=2,  # Minutos
        AERO_TEMPO_WARM_START=4,  # Minutos
        AERO_TEMPO_COLD_START=5,  # Minutos
        AERO_CUSTO_HOT_START=20,  # $/MW
        AERO_CUSTO_WARM_START=25,  # $/MW
        AERO_CUSTO_COLD_START=30,  # $/MW

        # Para a Heavy Duty - modelo GE 7F.05: https://www.ge.com/gas-power/products/gas-turbinas/7f
        HEAVY_DUTY_POTENCIA=240,  # MW
        HEAVY_DUTY_CUSTO_TOTAL=700,  # $/kW
        HEAVY_DUTY_CUSTO_OM=7 * 1000,  # US$/MW por ano
        HEAVY_DUTY_EFICIENCIA=0.4,  # 38.5%
        HEAVY_DUTY_TEMPO_HOT_START=20,  # Minutos
        HEAVY_DUTY_TEMPO_WARM_START=25,  # Minutos
        HEAVY_DUTY_TEMPO_COLD_START=25,  # Minutos
        HEAVY_DUTY_CUSTO_HOT_START=35,  # $/MW
        HEAVY_DUTY_CUSTO_WARM_START=60,  # $/MW
        HEAVY_DUTY_CUSTO_COLD_START=75,  # $/MW

        # Fontes:
        # - https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2020.pdf
        # - https://www.ge.com/content/dam/gepower-new/global/en_US/downloads/gas-new-site/products/gas-turbinas/7ha-fact-sheet-product-specifications.pdf
        # - https://etn.global/wp-content/uploads/2018/09/Startup_time_reduction_for_Combined_Cycle_Power_Plants.pdf
        # - https://www.nrel.gov/docs/fy12osti/55433.pdf
    )

    VALORES_INICIAIS_BATERIAS = SimpleNamespace(
        # Dados do site da DOE
        CHUMBO_ACIDO_KW=2220,
        CHUMBO_ACIDO_VIDA_UTIL=2,
        CHUMBO_ACIDO_KWh=550,

        LI_ION_KW=1876,
        LI_ION_VIDA_UTIL=10,
        LI_ION_KWh=469,

        SODIO_ENXOFRE_KW=3626,
        SODIO_ENXOFRE_VIDA_UTIL=13.5,
        SODIO_ENXOFRE_KWh=907,

        FLUXO_OXIDACAO_KW=3430,
        FLUXO_OXIDACAO_VIDA_UTIL=15,
        FLUXO_OXIDACAO_KWh=858,

        SODIO_METAL_KW=3710,
        SODIO_METAL_VIDA_UTIL=12.5,
        SODIO_METAL_KWh=928,

        ZINCO_CATODO_KW=2202,
        ZINCO_CATODO_VIDA_UTIL=10,
        ZINCO_CATODO_KWh=551,

        ULTRACAPACITOR_KW=930,
        ULTRACAPACITOR_VIDA_UTIL=16,
        ULTRACAPACITOR_KWh=74480,
    )

    @staticmethod
    def valido(data, mode):
        if mode == "turbinas":
            return data in headers_turbinas
        elif mode == "baterias":
            return data in headers_baterias
        else:
            raise ValueError("Modo inválido!")

    @staticmethod
    def resgatar_valores_validos(mode):
        if mode == "turbinas":
            return headers_turbinas
        elif mode == "baterias":
            return headers_baterias
        else:
            raise ValueError("Modo inválido!")

    @staticmethod
    def resgatar_valores_validos_por_indice(key, mode):
        if mode == "turbinas":
            return headers_turbinas[key]
        elif mode == "baterias":
            return headers_baterias[key]
        else:
            raise ValueError("Modo inválido!")

    @staticmethod
    def resgatar_valores_validos_por_valor(value, mode):
        if mode == "turbinas":
            return list(headers_turbinas.keys())[list(headers_turbinas.values()).index(value)]
        elif mode == "baterias":
            return list(headers_baterias.keys())[list(headers_baterias.values()).index(value)]
        else:
            raise ValueError("Modo inválido!")

    @staticmethod
    def resgatar_valores_iniciais(mode):
        if mode == "turbinas":
            return Valores_Iniciais.VALORES_INICIAIS
        elif mode == "baterias":
            return Valores_Iniciais.VALORES_INICIAIS_BATERIAS
        else:
            raise ValueError("Modo inválido!")

    @staticmethod
    def resgatar_posicoes_header(mode):
        if mode == "turbinas":
            return header_posicoes_turbinas
        elif mode == "baterias":
            return header_posicoes_baterias
        else:
            raise ValueError("Modo inválido!")
