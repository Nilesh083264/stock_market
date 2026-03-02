from services.dhan_service import DhanConfig,DhanApiClient, CallStrategy,PutStrategy, StraddleService


def get_straddle_service():
    config = DhanConfig()
    client = DhanApiClient(config)

    call_strategy = CallStrategy(client)
    put_strategy = PutStrategy(client)

    return StraddleService(call_strategy, put_strategy)