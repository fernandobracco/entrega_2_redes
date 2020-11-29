import asyncio
import json
import logging
import websockets

logging.basicConfig()

STATE = {"value": 0}

USERS = []

async def echo(websocket, path):
    try:
        await websocket.send("Bem vindo ao chat. Digite seu nome para acessar o chat.")
        async for message in websocket:
            message = message.strip('"')
            existingUser, repeatedUser, privateMessage = False, False, False
            """Laco para verificar se remetente já existe e, se não existir, verificar se nome escolhido é repetido"""
            for user in USERS:
                if websocket == user[0]:
                    existingUser = True
                    messageUser = user[1]
                if message == user[1]: 
                    repeatedUser = True 
                    
            if existingUser:
                """Laco para verificar se mensagem é privada e, se não for, enviar a todos exceto o remetente"""
                for user in USERS:
                    if (" para " + user[1]) in message and user[1] != messageUser:
                        privateMessage = True
                        await user[0].send("Mensagem privada de " + messageUser + " : " + message[:-6-len(user[1])])
                        break
                if not privateMessage:
                    await asyncio.wait([user[0].send(messageUser + " : " + message) for user in USERS if user[1] != messageUser])       
            elif repeatedUser:
                await websocket.send("Usuário escolhido já existente. Digite outro nome para acessar o chat.")
            else:
                await register(websocket,message)
    finally:
        await unregister(websocket)

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user[0].send(message) for user in USERS])

async def register(websocket,message):
    if message not in USERS:
        await websocket.send("Nome alterado com sucesso para " + message)
        if USERS: 
            await asyncio.wait([user[0].send("Usuário " + message + " entrou na sala.") for user in USERS])
        USERS.append([websocket,message])
        await notify_users()


async def unregister(websocket):
    for user in USERS:
        if websocket == user[0]:
            USERS.remove([user[0],user[1]])
            userName = user[1]
            await asyncio.wait([user[0].send("Usuário " + userName + " saiu da sala.") for user in USERS])
            break
    await notify_users()

start_server = websockets.serve(echo, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()