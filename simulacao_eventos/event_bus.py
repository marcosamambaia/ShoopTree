# simulacao_eventos/event_bus.py

# O barramento de eventos (EventBus) é responsável por gerenciar
# os consumidores e distribuir os eventos publicados.
class EventBus:
    def __init__(self):
        # Lista de consumidores inscritos
        self.subscribers = []
        # Histórico de todos os eventos publicados
        self.historico = []

    def subscribe(self, subscriber):
        """Adiciona um consumidor à lista de inscritos"""
        self.subscribers.append(subscriber)

    def publish(self, evento):
        """Publica um evento para todos os consumidores"""
        self.historico.append(evento)
        for subscriber in self.subscribers:
            subscriber.handle(evento)


# Consumidor responsável por processar eventos de pagamento
class PagamentoConsumer:
    def handle(self, evento):
        if evento.get("tipo") == "COMPRA":
            # Aqui você pode integrar com o serviço de pagamentos
            print("PagamentoConsumer: processando pagamento ->", evento)


# Consumidor responsável por enviar notificações
class NotificacaoConsumer:
    def handle(self, evento):
        # Aqui você pode integrar com o serviço de notificações
        print("NotificacaoConsumer: enviando notificação ->", evento)
