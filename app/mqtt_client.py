import paho.mqtt.client as mqtt
from sqlalchemy import select

# Função chamada quando o cliente recebe uma mensagem do servidor
def on_message(client, userdata, msg):
    from .models.user import User
    from . import db, create_app
    app = create_app()
    with app.app_context():
        print(f"Mensagem recebidas: {msg.topic} -> {msg.payload.decode('utf-8')}")
        statement = select(User).filter_by(tag=msg.payload.decode('utf-8'))
        user = db.session.execute(statement).scalars().first()
        print(f"user: {user.name}")
    #decodifica  a mensagem
    #ver de qual topico veio
    #dependendo ele verifica se tem no banco de dados tal usuario
    #envia outra mensagem pra liberar a porta

# Função chamada quando o cliente se conecta ao servidor
def on_connect(client, userdata, flags, rc):
    print("Conectado com o código de resultado "+str(rc))
    client.subscribe("/door_command/request")

def init_mqtt():

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.1.7", 1883, 60)
    client.loop_forever()
# Loop para manter a conexão

