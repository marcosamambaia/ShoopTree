from typing import List

# Evento genérico
class Evento:
    def __init__(self, tipo: str, dados: dict):
        self.tipo = tipo
        self.dados = dados

# Interface para observadores
class Observer:
    def notificar(self, evento: Evento):
        raise NotImplementedError

# Sujeito que dispara eventos
class Subject:
    def __init__(self):
        self.observers: List[Observer] = []

    def adicionar_observer(self, observer: Observer):
        self.observers.append(observer)

    def remover_observer(self, observer: Observer):
        self.observers.remove(observer)

    def disparar_evento(self, evento: Evento):
        for obs in self.observers:
            obs.notificar(evento)

# Observadores concretos
class PagamentoService(Observer):
    def notificar(self, evento: Evento):
        if evento.tipo == "COMPRA_REALIZADA":
            print(f"[Pagamento] Processando pagamento da compra {evento.dados}")

class NotificacaoService(Observer):
    def notificar(self, evento: Evento):
        if evento.tipo == "PAGAMENTO_CONFIRMADO":
            print(f"[Notificação] Enviando confirmação ao cliente: {evento.dados}")

# Simulação
if __name__ == "__main__":
    sistema = Subject()

    pagamento = PagamentoService()
    notificacao = NotificacaoService()

    sistema.adicionar_observer(pagamento)
    sistema.adicionar_observer(notificacao)

    # Compra gera evento
    compra_evento = Evento("COMPRA_REALIZADA", {"produto": "Notebook", "valor": 3500})
    sistema.disparar_evento(compra_evento)

    # Pagamento confirmado gera outro evento
    pagamento_evento = Evento("PAGAMENTO_CONFIRMADO", {"status": "sucesso", "valor": 3500})
    sistema.disparar_evento(pagamento_evento)
