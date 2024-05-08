# Importações necessárias para o funcionamento do formulário e manipulação de dados
from types import SimpleNamespace

import pandas as pd
from Gerenciador_Constantes import Constantes
from IPython.display import clear_output, display
from ipywidgets import HTML, Button, Dropdown, HBox, Layout, VBox


class Formulario_Furnas:

    def __init__(self, mode='turbinas', is_colab=True):
        # Inicialização das constantes e dos widgets do formulário
        sources = {}
        if mode == "turbinas":
            sources = {
                "Multiplicadores de inflação": "https://www.bls.gov/data/inflation_calculator.htm",
                "Conversão de pés cúbicos para metros cúbicos": "https://www.eia.gov/energyexplained/units-and-calculators/energy-conversion-calculators.php",
                "Preço de gás natural": "https://www.eia.gov/dnav/ng/hist/n3035us3A.htm",
                "Dados sobre CCGT": "https://www.ge.com/gas-power/products/gas-turbinas/7ha",
                "Dados sobre AeroGT": "https://www.ge.com/gas-power/products/gas-turbinas/lm6000",
                "Dados sobre Heavy Duty": "https://www.ge.com/gas-power/products/gas-turbinas/7f",
                "Dados sobre custos de partida": "https://www.nrel.gov/docs/fy12osti/55433.pdf",
            }
        elif mode == "baterias":
            sources = {
                "Custos das baterias": "https://www.energy.gov/",
            }

        self.is_colab = is_colab
        self.sources = sources
        self.consts = Constantes(mode)
        self.inicializar_widgets()
        self.configurar_observadores()

    def inicializar_widgets(self):
        # Criação dos widgets do formulário
        self.dropdown = Dropdown(
            options=['Usar Dados Padrão', 'Usar Dados Personalizados'],
            description='Escolha:',
            disabled=False,
        )
        self.criar_widgets_dados()
        self.botao_enviar = Button(
            description='Enviar', layout=Layout(width='200px', height='50px', margin='20px 10px 10px 475px'))
        self.botao_exportar_csv = Button(
            description='Exportar CSV', layout=Layout(margin='10px 10px 10px 420px'))
        self.botao_carregar_csv = Button(
            description='Carregar CSV', layout=Layout(margin='10px'))

    def configurar_observadores(self):
        # Configuração dos observadores de eventos para os widgets
        self.dropdown.observe(self.manipulador_evento_dropdown, names='value')
        self.botao_enviar.on_click(self.manipulador_evento_botao_enviar)
        self.botao_exportar_csv.on_click(self.manipulador_evento_baixar_csv)
        self.botao_carregar_csv.on_click(self.manipulador_evento_carregar_csv)

    def criar_widgets_dados(self):
        # Método placeholder para criação de widgets específicos de dados
        widgets = self.consts.resgatar_widgets()

    def exibir_formulario(self):
        # Exibe o widget dropdown do formulário
        display(self.dropdown)
        self.exibir_fontes()
        self.atualizar_valores()

    def exibir_fontes(self):
        # Widgets para os itens em self.sources
        widgets_para_exibir = [
            HTML(value=f'<h3 style="margin:0 padding:0">Fontes:</h3>')]
        for chave, valor in self.sources.items():
            chave_widget = HTML(value=f'<strong>{chave}:</strong>')
            valor_widget = HTML(
                value=f'<a href="{valor}" style="color: #b8c730" target="_blank">{valor}</a>')
            widgets_para_exibir.append(HBox([chave_widget, valor_widget]))

        # Exibe todos os widgets de uma vez usando VBox para um layout vertical
        display(VBox(widgets_para_exibir))

    def manipulador_evento_dropdown(self, change):
        # Lida com mudanças no valor selecionado do dropdown, reiniciando a exibição
        clear_output(wait=True)
        display(self.dropdown)
        if change.new == 'Usar Dados Personalizados':
            self.exibir_formulario_dados_personalizados()
        else:
            self.exibir_fontes()
            self.consts = Constantes()

    def formulario_namespace(self, namespace):
        # Método para criar um formulário baseado em SimpleNamespace, organizando os widgets em linhas
        widgets = vars(namespace)
        rows = []
        dict_iterator = iter(widgets.items())
        last_element = None

        while True:
            try:
                key1, element1 = next(dict_iterator)

                if "header" in key1.lower():
                    rows.append([element1])
                    continue
                try:
                    key2, element2 = next(dict_iterator)
                    if "header" in key2.lower():
                        rows.append([element1])
                        rows.append([element2])
                        continue

                    rows.append([element1, element2])
                except StopIteration:
                    last_element = element1  # Salva o último elemento se não houver par para ele
                    break
            except StopIteration:
                break

        if last_element is not None:
            rows.append([last_element])

        rows.append([self.botao_enviar])
        form = VBox([HBox([element for element in row]) for row in rows])
        return form

    def exibir_formulario_dados_personalizados(self):
        # Método para exibir o formulário de dados personalizados, incluindo botões de exportar e carregar CSV
        display(self.formulario_namespace(self.consts.resgatar_widgets()))
        display(HBox([self.botao_exportar_csv, self.botao_carregar_csv]))

    def atualizar_valores(self):
        # Atualiza os valores baseando-se nas entradas do usuário ou dados padrão
        self.consts.set_valores()

    def manipulador_evento_botao_enviar(self, _):
        # Manipulador de evento para o botão de enviar, atualizando os valores
        try:
            self.atualizar_valores()
            display(HTML(value="<h3>Valores atualizados com sucesso!</h3>"))
        except Exception as e:
            print(f"Erro ao atualizar valores: {e}")

    def recuperar_valores(self):
        # Retorna os valores atualizados do formulário
        values = self.consts.resgatar_valores()
        values_dict = vars(values)

        filtered_values = {
            k: v for k, v in values_dict.items() if "header" not in k.lower()}

        return SimpleNamespace(**filtered_values)

    def manipulador_evento_baixar_csv(self, _):
        # Manipulador de evento para o botão de exportar para CSV

        if self.is_colab:
            try:
                from google.colab import files  # type: ignore
                valores = self.recuperar_valores()

                # Conversão de SimpleNamespace para dicionário, se necessário
                if isinstance(valores, SimpleNamespace):
                    valores_dict = vars(valores)
                else:
                    valores_dict = valores

                # Criação de DataFrame e exportação para CSV
                df = pd.DataFrame([valores_dict])

                df.to_csv('dados.csv', index=False)

                files.download('dados.csv')
                print("CSV exportado com sucesso!")
            except Exception as e:
                print(f"Erro ao exportar csv: {e}")

        else:
            try:
                valores = self.recuperar_valores()

                # Conversão de SimpleNamespace para dicionário, se necessário
                if isinstance(valores, SimpleNamespace):
                    valores_dict = vars(valores)
                else:
                    valores_dict = valores

                # Criação de DataFrame e exportação para CSV
                df = pd.DataFrame([valores_dict])

                df.to_csv('dados.csv', index=False)

                print("CSV exportado com sucesso!")
            except Exception as e:
                print(f"Erro ao exportar csv: {e}")

    def exibir_formulario_dados_personalizados_e_dropdown(self):
        # Exibe o dropdown e o formulário de dados personalizados
        display(self.dropdown)
        self.exibir_formulario_dados_personalizados()

    def manipulador_evento_carregar_csv(self, _):
        # Manipulador de evento para o botão de carregar CSV
        if self.is_colab:
            from google.colab import files  # type: ignore
            clear_output(wait=True)
            self.exibir_formulario_dados_personalizados_e_dropdown()
            uploaded = files.upload()
            for fn in uploaded.keys():
                try:
                    df = pd.read_csv(fn)
                    valores = SimpleNamespace(
                        **df.to_dict(orient='records')[0])
                    self.consts.set_valores_personalizados(valores)
                    msg1 = "CSV carregado com sucesso!"
                    msg2 = "Não esqueça de clicar em 'Enviar' para atualizar os valores"
                except Exception as e:
                    msg1 = "Erro ao carregar csv: verifique os dados inseridos!"
                    msg2 = f"Erro: {e}"
                finally:
                    # Após o carregamento (bem-sucedido ou não), atualize a interface do usuário
                    clear_output(wait=True)
                    self.exibir_formulario_dados_personalizados_e_dropdown()
                    print(msg1)
                    print(msg2)
        else:
            try:
                df = pd.read_csv('dados.csv')
                valores = SimpleNamespace(**df.to_dict(orient='records')[0])
                self.consts.set_valores_personalizados(valores)
                msg1 = "CSV carregado com sucesso!"
                msg2 = "Não esqueça de clicar em 'Enviar' para atualizar os valores"
            except FileNotFoundError:
                msg1 = "Arquivo não encontrado!"
                msg2 = "Por favor, exporte um arquivo CSV e tente novamente"
            except Exception as e:
                msg1 = "Erro ao carregar csv: verifique os dados inseridos!"
                msg2 = f"Erro: {e}"
            finally:
                # Após o carregamento (bem-sucedido ou não), atualize a interface do usuário
                clear_output(wait=False)
                self.exibir_formulario_dados_personalizados_e_dropdown()
                print(msg1)
                print(msg2)


# Execução principal do script, caso este arquivo seja o ponto de entrada
if __name__ == "__main__":
    formulario = Formulario_Furnas()
    formulario.exibir_formulario()
    formulario.recuperar_valores()
