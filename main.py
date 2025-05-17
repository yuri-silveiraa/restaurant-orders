from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
from models import Pedido
from configs.database import SessionLocal, create_tables
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
create_tables()

connections = []


@app.websocket("/ws/pedidos")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        db = SessionLocal()
        pedidos = db.query(Pedido).all()
        await websocket.send_json([serialize_pedido(p) for p in pedidos])
        db.close()

        while True:
            data = await websocket.receive_json()
            db = SessionLocal()
            pedido = Pedido(nome=data["nome"], item=data["item"], qtd=data["qtd"], estado="recebido", hora_recebido=datetime.utcnow())
            db.add(pedido)
            db.commit()
            db.refresh(pedido)
            db.close()
            await broadcast()
    except WebSocketDisconnect:
        connections.remove(websocket)


@app.post("/update")
async def update_pedido(req: Request):
    data = await req.json()
    db: Session = SessionLocal()
    pedido = db.query(Pedido).filter(Pedido.id == data["id"]).first()

    if pedido:
        pedido.estado = data["estado"]
        if data["estado"] == "preparando":
            pedido.hora_preparo = datetime.utcnow()
        elif data["estado"] == "finalizado":
            pedido.hora_finalizado = datetime.utcnow()
        db.commit()
    db.close()
    await broadcast()
    return {"ok": True}


@app.get("/", response_class=HTMLResponse)
async def get_cozinha():
    return open("static/cozinha.html").read()


@app.get("/cliente", response_class=HTMLResponse)
async def get_cliente():
    return open("static/cliente.html").read()


@app.get("/pedidos")
async def get_pedidos():
    db = SessionLocal()
    pedidos = db.query(Pedido).all()
    db.close()
    return [serialize_pedido(p) for p in pedidos]


def serialize_pedido(p):
    return {
        "id": p.id,
        "nome": p.nome,
        "item": p.item,
        "qtd": p.qtd,
        "estado": p.estado,
        "horaRecebido": p.hora_recebido.strftime("%H:%M:%S") if p.hora_recebido else "-",
        "horaPreparando": p.hora_preparo.strftime("%H:%M:%S") if p.hora_preparo else "-",
        "horaFinalizado": p.hora_finalizado.strftime("%H:%M:%S") if p.hora_finalizado else "-",
    }


async def broadcast():
    db = SessionLocal()
    pedidos = db.query(Pedido).all()
    data = [serialize_pedido(p) for p in pedidos]
    db.close()
    for conn in connections:
        await conn.send_json(data)
