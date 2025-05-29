from abc import ABC, abstractmethod
from typing import List

# Abstract Product
class Fornecedor(ABC):
    def __init__(self, nome: str, tags: List[str], contato: str, portfolio: str = None):
        self.nome = nome
        self.tags = tags
        self.contato = contato
        self.portfolio = portfolio
    
    @abstractmethod
    def exibir_info(self) -> str:
        pass
    
    @abstractmethod
    def calcular_preco(self) -> float:
        pass
    
    @abstractmethod
    def listar_servicos(self) -> List[str]:
        pass

# Concrete Products
class Pizzaria(Fornecedor):
    def exibir_info(self) -> str:
        return f"Pizzaria: {self.nome} - Contato: {self.contato}"
    
    def calcular_preco(self) -> float:
        # Lógica específica para cálculo de preço de pizzaria
        return 150.0 * len(self.tags)
    
    def listar_servicos(self) -> List[str]:
        return ["Pizza tradicional", "Pizza gourmet", "Esfihas", "Calzones"]

class Confeitaria(Fornecedor):
    def exibir_info(self) -> str:
        return f"Confeitaria: {self.nome} - Contato: {self.contato}"
    
    def calcular_preco(self) -> float:
        # Lógica específica para cálculo de preço de confeitaria
        return 200.0 * len(self.tags)
    
    def listar_servicos(self) -> List[str]:
        return ["Bolos", "Doces", "Salgados", "Coffee break"]

class Churrascaria(Fornecedor):
    def exibir_info(self) -> str:
        return f"Churrascaria: {self.nome} - Contato: {self.contato}"
    
    def calcular_preco(self) -> float:
        # Lógica específica para cálculo de preço de churrascaria
        return 300.0 * len(self.tags)
    
    def listar_servicos(self) -> List[str]:
        return ["Churrasco completo", "Espetos", "Buffet de carnes", "Acompanhamentos"]

# Abstract Factory
class FornecedorFactory(ABC):
    @abstractmethod
    def create_fornecedor(self, nome: str, tags: List[str], contato: str, portfolio: str = None) -> Fornecedor:
        pass

# Concrete Factories
class PizzariaFornecedorFactory(FornecedorFactory):
    def create_fornecedor(self, nome: str, tags: List[str], contato: str, portfolio: str = None) -> Fornecedor:
        return Pizzaria(nome, tags, contato, portfolio)

class ConfeitariaFornecedorFactory(FornecedorFactory):
    def create_fornecedor(self, nome: str, tags: List[str], contato: str, portfolio: str = None) -> Fornecedor:
        return Confeitaria(nome, tags, contato, portfolio)

class ChurrascariaFornecedorFactory(FornecedorFactory):
    def create_fornecedor(self, nome: str, tags: List[str], contato: str, portfolio: str = None) -> Fornecedor:
        return Churrascaria(nome, tags, contato, portfolio)

# Factory Provider - Simplifica a criação da fábrica correta
def get_fornecedor_factory(tipo: str) -> FornecedorFactory:
    factories = {
        "pizzaria": PizzariaFornecedorFactory(),
        "confeitaria": ConfeitariaFornecedorFactory(),
        "churrascaria": ChurrascariaFornecedorFactory()
    }
    
    factory = factories.get(tipo.lower())
    if not factory:
        raise ValueError(f"Tipo de fornecedor não suportado: {tipo}")
    
    return factory
