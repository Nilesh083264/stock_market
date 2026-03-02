from services.contract_hub import  load_or_build
from constants.constant import strike_ABS

print("loading contract hub dictionary")
hub_dict = load_or_build()       #hub_dict it is a source variable/ global variable
def ATM(index,spot):
    spot = float(spot)
    step_val = strike_ABS[index]["step"]
    atm = round(spot / step_val) * step_val
    return str(atm)


def get_instrument(index,atm):
    strike  = hub_dict[index][list(hub_dict[index].keys())[0]][atm]
    return strike



def get_instruments_list(index,last_atm):
    stack = get_instrument(index,last_atm)
    lst = [
        {"ExchangeSegment": strike_ABS[index]["Exchange"], "SecurityId": str(stack["CE"])},
        {"ExchangeSegment": strike_ABS[index]["Exchange"], "SecurityId": str(stack["PE"])}
    ]
    return lst








