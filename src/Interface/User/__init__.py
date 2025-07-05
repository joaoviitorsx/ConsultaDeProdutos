from .login import LoginPage
from .dashboard import DashboardPage
from .consultaFornecedor import ConsultaFornecedorPage
from .consultaProdutos import ConsultaProdutosPage
from .consultaRelatorio import ConsultaRelatorioPage

user_routes = {
    "login": LoginPage,
    "dashboard": DashboardPage,
    "consulta_fornecedor": ConsultaFornecedorPage,
    "consulta_produtos": ConsultaProdutosPage,
    "relatorios": ConsultaRelatorioPage,
}