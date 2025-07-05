import flet as ft
from datetime import datetime

def ConsultaRelatorioPage(page: ft.Page):
    # Mês e ano atuais
    ano_atual = datetime.now().year
    anos = [str(ano_atual - i) for i in range(2, -1, -1)]
    meses = [
        "01 - Janeiro", "02 - Fevereiro", "03 - Março", "04 - Abril", "05 - Maio", "06 - Junho",
        "07 - Julho", "08 - Agosto", "09 - Setembro", "10 - Outubro", "11 - Novembro", "12 - Dezembro"
    ]

    # Filtros
    combo_mes = ft.Dropdown(
        label="Mês",
        options=[ft.dropdown.Option(m) for m in meses],
        width=150,
        border_radius=8,
        filled=True,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLACK),
        focused_border_color=ft.colors.RED,
        border_color=ft.colors.RED
    )

    combo_ano = ft.Dropdown(
        label="Ano",
        options=[ft.dropdown.Option(a) for a in anos],
        width=100,
        border_radius=8,
        filled=True,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLACK),
        focused_border_color=ft.colors.RED,
        border_color=ft.colors.RED
    )

    def gerar_pdf(e):
        page.snack_bar = ft.SnackBar(ft.Text("PDF gerado com sucesso! (mock)"), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    botao_pdf = ft.ElevatedButton(
        text="Gerar PDF",
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
            overlay_color=ft.colors.with_opacity(0.1, ft.colors.RED),
            padding=20,
            text_style=ft.TextStyle(weight="bold")
        ),
        on_click=gerar_pdf
    )

    filtros = ft.Row(
        [combo_mes, combo_ano, botao_pdf],
        alignment=ft.MainAxisAlignment.START,
        spacing=20
    )

    # Mock da tabela
    colunas = [
        ft.DataColumn(ft.Text("Data")),
        ft.DataColumn(ft.Text("Fornecedor")),
        ft.DataColumn(ft.Text("Produto")),
        ft.DataColumn(ft.Text("Código")),
        ft.DataColumn(ft.Text("Valor Base")),
        ft.DataColumn(ft.Text("Alíquota")),
        ft.DataColumn(ft.Text("Adicional")),
        ft.DataColumn(ft.Text("Total")),
        ft.DataColumn(ft.Text("Valor Final"))
    ]

    linhas = [
        ft.DataRow(cells=[
            ft.DataCell(ft.Text("01/07/2025")),
            ft.DataCell(ft.Text("Fornecedor Alpha")),
            ft.DataCell(ft.Text("Produto A")),
            ft.DataCell(ft.Text("123456")),
            ft.DataCell(ft.Text("R$ 100,00")),
            ft.DataCell(ft.Text("12%")),
            ft.DataCell(ft.Text("5%")),
            ft.DataCell(ft.Text("R$ 17,00")),
            ft.DataCell(ft.Text("R$ 117,00"))
        ]),
        ft.DataRow(cells=[
            ft.DataCell(ft.Text("03/07/2025")),
            ft.DataCell(ft.Text("Fornecedor Beta")),
            ft.DataCell(ft.Text("Produto B")),
            ft.DataCell(ft.Text("789012")),
            ft.DataCell(ft.Text("R$ 200,00")),
            ft.DataCell(ft.Text("10%")),
            ft.DataCell(ft.Text("2%")),
            ft.DataCell(ft.Text("R$ 24,00")),
            ft.DataCell(ft.Text("R$ 224,00"))
        ])
    ]

    tabela = ft.DataTable(
        columns=colunas,
        rows=linhas,
        heading_row_color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
        data_row_color=ft.colors.with_opacity(0.05, ft.colors.BLACK),
        divider_thickness=0.5,
        border_radius=10,
        column_spacing=12
    )

    voltar = ft.OutlinedButton("Voltar", icon=ft.icons.ARROW_BACK, on_click=lambda e: page.go("/dashboard"))

    page.scroll = ft.ScrollMode.AUTO
    page.title = "Consulta de Relatórios"
    page.add(
        ft.Column([
            ft.Text("Histórico de Consultas", size=22, weight="bold"),
            filtros,
            tabela,
            voltar
        ],
        spacing=25)
    )
