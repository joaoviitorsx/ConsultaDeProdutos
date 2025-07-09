import flet as ft

from src.Interface.User.login import LoginPage
from src.Interface.User.dashboard import DashboardPage
from src.Interface.User.consultaFornecedor import ConsultaFornecedorPage
from src.Interface.User.consultaProdutos import ConsultaProdutosPage
from src.Interface.User.consultaRelatorio import ConsultaRelatorioPage

from src.Components.adminLayout import AdminLayout

from src.Config import theme

def main(page: ft.Page):
    theme.set_theme("dark" if page.theme_mode == ft.ThemeMode.DARK else "light")
    page.window_icon = "images/icone.ico"

    def route_change(e):
        page.views.clear()
        rota = page.route
        print(f"Navegando para rota: {rota}")

        if rota in ["/", "/login"]:
            page.views.append(LoginPage(page))
        elif rota == "/dashboard":
            page.views.append(DashboardPage(page))
        elif rota == "/consulta_fornecedor":
            page.views.append(ConsultaFornecedorPage(page))
        elif rota == "/consulta_produtos":
            page.views.append(ConsultaProdutosPage(page))
        elif rota == "/relatorios":
            page.views.append(ConsultaRelatorioPage(page))
            
        #rota admin
        elif rota == "/admin_dashboard":
            page.views.append(AdminLayout(page))
        else:
            page.views.append(ft.View("/", controls=[ft.Text("Página não encontrada!")]))
        
        page.update()

    page.on_route_change = route_change

    page.go("/login")

ft.app(target=main, assets_dir="src/Assets")