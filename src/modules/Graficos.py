import os
from IPython.display import display, HTML
from ipywidgets import Button
import plotly.graph_objects as go
import time


class Gerador_Grafico_Furnas:
    def __init__(self, nome_arquivo="grafico"):
        self.nome_arquivo = nome_arquivo

    def grafico_interativo_linha(self, x, y, nome_eixo_x, nome_eixo_y, titulo="", nome_legenda=""):
        """
        Cria um gráfico de linha interativo utilizando Plotly.

        :param x: Vetor com os valores do eixo x.
        :param y: Vetor com os valores do eixo y.
        :param nome_eixo_x: Nome para ser exibido no eixo x do gráfico.
        :param nome_eixo_y: Nome para ser exibido no eixo y do gráfico.
        :param titulo: Título opcional do gráfico.
        :param nome_legenda: Nome opcional para a legenda da linha.
        :return: Objeto de figura Plotly contendo o gráfico de linha.
        """
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=nome_legenda))

        fig.update_layout(
            title=titulo,
            xaxis_title=nome_eixo_x,
            yaxis_title=nome_eixo_y,
            legend_title="Legenda"
        )

        fig.show(config={'displaylogo': False})
        self.fig = fig

    def grafico_interativo_multiplas_linhas(self, x, y, nome_eixo_x, nome_eixo_y, titulo="", nome_legenda=[]):
        """
        Cria um gráfico interativo com múltiplas linhas utilizando Plotly.

        :param x: Vetor com os valores do eixo x, comum a todas as linhas.
        :param y: Matriz com os valores do eixo y para cada linha.
        :param nome_eixo_x: Nome para ser exibido no eixo x do gráfico.
        :param nome_eixo_y: Nome para ser exibido no eixo y do gráfico.
        :param titulo: Título opcional do gráfico.
        :param nome_legenda: Lista com os nomes das legendas para cada linha.
        :return: Objeto de figura Plotly contendo o gráfico com múltiplas linhas.
        """
        fig = go.Figure()
        for i in range(len(y)):
            legenda = nome_legenda[i] if i < len(
                nome_legenda) else f"Série {i+1}"
            fig.add_trace(go.Scatter(x=x, y=y[i], mode='lines', name=legenda))

        fig.update_layout(
            title=titulo,
            xaxis_title=nome_eixo_x,
            yaxis_title=nome_eixo_y,
            legend_title="",
            margin=dict(l=10, r=10, t=80, b=10),
            title_x=0.5,
            # Ajuste da legenda para não sobrepor o gráfico
            legend=dict(
                font=dict(size=12),
                orientation="h",
                x=0.5,
                y=1.0,
                xanchor='center',
                yanchor='bottom',
            )
        )

        fig.show(config={'displaylogo': False})
        self.fig = fig

    def exportar_para_pdf(self):
        """
        Exporta um gráfico para um arquivo PDF.

        :param fig: Objeto de figura Plotly que será exportado.
        :param nome_arquivo: Nome do arquivo PDF para salvar o gráfico.
        """
        if not os.path.exists("imagens"):
            os.mkdir("imagens")
        self.fig.write_image(f"imagens/{self.nome_arquivo}")

    def botao_exportar_pdf(self, isColab=False):
        """
        Cria e exibe um botão no Jupyter para exportar um gráfico como PDF.

        :param fig: Objeto de figura Plotly que será exportado.
        :param nome_arquivo: Nome do arquivo PDF para salvar o gráfico.
        """

        botao = Button(description="Exportar para PDF")
        botao.on_click(self._criar_handler_botao(
            self.fig, self.nome_arquivo, isColab))
        display(botao)

    def _criar_handler_botao(self, fig, nome_arquivo, isColab):
        """
        Cria um handler para um evento de clique de botão que exporta um gráfico para PDF.

        :param fig: Objeto de figura Plotly que será exportado.
        :param nome_arquivo: Nome do arquivo PDF para salvar o gráfico.
        :return: Função que será chamada quando o botão for clicado.
        """
        def ao_clicar_no_botao(_):
            # Verifica se o diretório 'imagens/' existe, se não, cria
            if not os.path.exists('imagens'):
                os.makedirs('imagens')

            try:
                # Caminho completo do arquivo
                arquivo_completo = f'imagens/{nome_arquivo}.pdf'

                # Gráfico temporário para corrigir bug
                figTemp = go.Figure(go.Scatter(
                    x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16]))
                figTemp.write_image(arquivo_completo)
                # Aguarda 2 segundos para garantir que o bug suma
                time.sleep(2)

                fig.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),  # Ajusta a margem
                    title=None,  # Remove o título do gráfico
                )

                # Exporta a figura como PDF
                fig.write_image(arquivo_completo)

                # Inicia o download do arquivo
                self._download_file(arquivo_completo, isColab)
            except Exception as e:
                print(f"Não foi possível baixar o arquivo: {e}")

        return ao_clicar_no_botao

    def _download_file(self, file_path, isColab):
        """
        Inicia o download de um arquivo no Jupyter Notebook.

        :param file_path: Caminho do arquivo a ser baixado.
        """
        if isColab:
            try:
                from google.colab import files  # type: ignore
                files.download(file_path)
            except:
                print("Ocorreu um erro ao baixar o arquivo PDF...")
        else:
            from IPython.display import FileLink
            html = "<p>Arquivo gerado com sucesso!</p>"

            display(HTML(html))
            display(FileLink(file_path))


if __name__ == "__main__":
    # Exemplo de uso da classe
    gerador = Gerador_Grafico_Furnas("meu_grafico")
    x = [1, 2, 3, 4]
    gerador.grafico_interativo_multiplas_linhas(
        x, [[1, 2, 3, 4], [20, 21, 22, 23], [20, 21, 22, 23], [20, 21, 22, 23]
            ], "Eixo X", "Eixo Y",
    )
    gerador.botao_exportar_pdf()
