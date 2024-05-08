from types import SimpleNamespace
from ipywidgets import FloatText, Layout, HTML
from Valores_Iniciais import Valores_Iniciais


# Importações necessárias para definir os widgets e manipular namespaces


def criar_widget(description, value, disabled=False, widget_style={'description_width': '325px'}, widget_layout=Layout(width='auto', margin='5px')):
    """
    Cria e retorna um widget FloatText para entrada de dados numéricos.

    :param description: Descrição do widget (aparece ao lado do campo de entrada).
    :param value: Valor inicial do widget.
    :param disabled: Define se o widget está desativado.
    :param widget_style: Estilo CSS do widget.
    :param widget_layout: Layout CSS do widget.
    :return: Instância do widget FloatText configurado.
    """
    return FloatText(description=description,
                     title=description,
                     label=description,
                     value=value,
                     disabled=disabled,
                     style=widget_style,
                     layout=widget_layout)


def criar_header(t):
    """
    Cria e retorna um widget HTML para exibir um cabeçalho.

    :param t: Texto do cabeçalho.
    """
    return HTML(f"<h2 style='color: #D5B60A; margin-left: 20%; width: 20rem;'>{t}</h2>")


def calcular_combustivel(Turbine_Power, efficiency):
    """
    Calcula o volume de combustível necessário com base na potência da turbina e sua eficiência.

    :param Turbine_Power: Potência da turbina.
    :param efficiency: Eficiência da turbina.
    :return: Volume de combustível necessário.
    """
    Volume = Turbine_Power / efficiency
    return Volume


def map_simple_namespace(a, f):
    """
    Aplica uma função a cada valor dentro de um SimpleNamespace e retorna um novo SimpleNamespace com os resultados.

    :param a: SimpleNamespace original.
    :param f: Função a ser aplicada a cada valor.
    :return: Novo SimpleNamespace com valores modificados.
    """
    # Converte o SimpleNamespace em dicionário
    a_dict = vars(a)
    # Aplica a função f a cada valor do dicionário
    b_dict = {k: f(v) for k, v in a_dict.items()}
    # Converte o dicionário modificado de volta para SimpleNamespace
    b = SimpleNamespace(**b_dict)
    return b


class Constantes:
    """
    Classe para gerenciar constantes e valores do formulário, incluindo a criação de widgets correspondentes.

    As fontes para os dados incluem publicações da EIA, GE, ETN, e NREL.
    """

    def __init__(self, mode):
        self.VALIDO = Valores_Iniciais.resgatar_valores_validos(mode)
        self.INICIAL = Valores_Iniciais.resgatar_valores_iniciais(mode)

        def converter_para_widget(a):
            """
            Converte um SimpleNamespace em um conjunto de widgets, baseando-se nas chaves válidas.

            :param a: SimpleNamespace contendo os valores a serem convertidos em widgets.
            :return: SimpleNamespace contendo os widgets.
            """
            # Converte o SimpleNamespace em dicionário
            a_dict = vars(a)
            try:
                # Cria um dicionário de widgets usando criar_widget para cada valor
                count = 0
                headers = Valores_Iniciais.resgatar_posicoes_header(mode)
                b_dict = {}
                for k, v in a_dict.items():
                    if count in headers:
                        b_dict["header" +
                               str(count)] = criar_header(self.VALIDO["header" + str(count)])
                    if k in self.VALIDO.keys():
                        b_dict[k] = criar_widget(self.VALIDO[k], v)
                    count += 1

                b = SimpleNamespace(**b_dict)
                return b
            except Exception as e:
                print("Valor inválido de variável. Verifique os dados inseridos!", e)
                return a

        # Inicialização dos valores padrão
        self.values = Valores_Iniciais.resgatar_valores_iniciais(mode)

        # Conversão dos valores para widgets
        self.widget_constants = converter_para_widget(self.values)

    def resgatar_widgets(self):
        """
        Retorna os widgets correspondentes às constantes.
        """
        return self.widget_constants

    def set_valores(self):
        """
        Atualiza os valores das constantes com base nos valores inseridos nos widgets.
        """
        novo_namespace = map_simple_namespace(
            self.widget_constants, lambda x: x.value)
        self.values = novo_namespace

    def set_valores_personalizados(self, values):
        """
        Define valores personalizados, garantindo que as chaves sejam válidas.
        """
        try:
            for key, _ in vars(values).items():
                if key not in self.VALIDO.keys():
                    raise ValueError("Chave inválida!", key)

            values = self.editar_valores(values)
            self.widget_constants = self.converter_para_widget(values)
        except Exception as e:
            raise ValueError("Erro ao atualizar valores personalizados: ", e)

    def resgatar_valores(self):
        """
        Retorna os valores atualizados das constantes.
        """
        return self.values

    def editar_valores(self, new_values: SimpleNamespace, initial_values=None):
        """
        Adiciona campos faltantes com valores padrão e atualiza os valores das constantes com base nos valores inseridos.
        """
        if initial_values is None:
            initial_values = self.INICIAL

        new_values_pacthed = SimpleNamespace()
        try:
            for key, value in vars(initial_values).items():
                if key not in vars(new_values).keys():
                    print(f"Chave {key} não encontrada. Usando valor padrão.")
                    setattr(new_values_pacthed, key, value)
                else:
                    setattr(new_values_pacthed, key, getattr(new_values, key))

            return new_values_pacthed

        except Exception as e:
            raise ValueError("Erro ao atualizar valores personalizados: ", e)


# Bloco de execução principal para testar a classe Constantes
if __name__ == "__main__":
    c = Constantes("baterias")
    c.set_valores()
    print(c.resgatar_valores())
