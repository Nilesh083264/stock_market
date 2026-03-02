import asyncio

lst = []

async def start_producer():
    global lst
    i = 0
    while True:
        lst.append(i)
        print("Produced:", lst)
        i += 1

        if len(lst) > 10:
            lst = []

        await asyncio.sleep(1)

def get_latest_tick():
    return lst