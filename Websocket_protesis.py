import websocket

ws = websocket.WebSocket()
ws.connect("ws://192.168.137.224")
print("conectado al websocket server")

while True:
    str = input("Escribe algo: ")
    if str == "exit":
       break
    else: 
        ws.send(str)
        result = ws.recv()
        print("Recibido: " + result)
print("Finalizando conexion con el websocket")
ws.close()