from flask_mqtt import Mqtt
import time
from .queries import *
import random
from flask import current_app
from flask_mail import Mail, Message

mqtt = Mqtt()
topic_request = "/door_command/request"
topic_response = "/door_command/response"
topic_send_info = "/door/info"
topic_notify_error = "/weird_activity"
global_uuid = 0  

def init_mqtt(app):
    mqtt.init_app(app)
    mail = Mail(app)

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Conectado ao broker MQTT com sucesso')
            client.subscribe(topic_request, qos=2)
            client.subscribe(topic_send_info, qos=2)
            client.subscribe(topic_notify_error, qos=2)
        else:
            print(f'Falha ao conectar ao broker MQTT, código: {rc}')

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, msg):
        with app.app_context():
            global global_uuid
            if msg.retain:
                return
            time.sleep(1)

            message = msg.payload.decode('utf-8', errors='ignore')
            print(f"message: {message}")
            if msg.topic == topic_notify_error:
                parts = msg.payload.decode('utf-8', errors='ignore').split(':')
                if len(parts) == 2:
                    compartment = parts[0]
                    locker_name = parts[1]
                print(f"Possível arrombamento no compartimento {message}")
                users_admins = get_admins()
                
                msg = Message(
                    'Security alert',  sender='smart.lockers.notification@gmail.com',
                    recipients = users_admins
                )
                msg.body = f"Possible invasion in compartment {compartment}. \nLocker name: {locker_name}"
                
                with app.app_context():
                    mail.send(msg)
    
                    return "E-mail enviado com sucesso!"
                
            if msg.topic == topic_request:
                parts = msg.payload.decode('utf-8', errors='ignore').split(':')
                if len(parts) == 3:
                    tag = parts[0]
                    locker_name = parts[1]
                    num_compartments = parts[2]

                    print(f"Mensagem recebida: {msg.topic} -> {msg.payload.decode('utf-8', errors='ignore')}")
                    try:
                        num_compartments = int(num_compartments)
                    except ValueError:
                        print("Erro: número de compartimentos inválido")
                        return
                    locker = get_locker(locker_name)
                    if locker is None:
                        set_locker(locker_name)

                    locker_obj = get_locker(locker_name)

                    for i in range(1, num_compartments+1):
                        if check_compartment_by_num(i, locker_obj.id) is None:
                            set_compartment(locker_obj.id, i)
                    
                    user = get_user_by_tag(tag)
                    if(user is None):
                        print(f"Tag não cadastrada: {tag}")
                        buffer = ':'.join(['0' , locker_name, tag])
                        client.publish(topic_response, payload=buffer, qos=2)

                        return
                    compartment_usage = get_compartment_usage(user)
                    if compartment_usage is not None:
                        print(f"user: {user.name} is using a compartment already, user is removing objects")
                        compartment = get_compartment_by_id(compartment_usage.compartment_id)
                        buffer = ':'.join([str(compartment.number) , locker_name, tag,'remove'])
                        client.publish(topic_response, payload=buffer, qos=2)
                    else:
                        print(f"user: {user.name} isn't using a compartment, user is keeping objects")

                        available_numbers = get_available_compartments(get_locker(locker_name).id)

                        if available_numbers:
                            chosen_number = random.choice(available_numbers)
                            print(f"Chosen number: {chosen_number}")
                            buffer = ':'.join([str(chosen_number) , locker_name, tag, 'store'])
                            client.publish(topic_response, payload=buffer, qos=2)
                        else:
                            buffer = ':'.join([str(-1) , locker_name, tag])
                            client.publish(topic_response, payload=buffer, qos=2)
                            print("No available compartments")

                else:
                    return 
            elif msg.topic == topic_send_info:

                parts = msg.payload.decode('utf-8', errors='ignore').split(':')
                if len(parts) == 5:
                    time1 = parts[0]
                    time2 = parts[1]
                    tag = parts[2]
                    num_compartment = parts[3]
                    locker_name = parts[4]

                    try:
                        num_compartment = int(num_compartment)
                    except ValueError:
                        print("Erro: número do compartimento inválido")
                        return
                    locker = get_locker(locker_name)
                    if locker is None:
                        print("Erro: Nome do locker inválido")
                        return
                    user = get_user_by_tag(tag)
                    if(user is None):
                        print(f"Tag não cadastrada: {tag}")
                        return
                    compartment_usage = get_compartment_usage(user)
                    if compartment_usage is None:
                        set_compartment_usage(time1, time2, user.id, locker.id, num_compartment)
                    else:
                        set_locker_schedule(time1, time2, user.id, locker.id, num_compartment)

                    print(f"Mensagem recebida: {msg.topic} -> {msg.payload.decode('utf-8', errors='ignore')}")

    @mqtt.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print('Desconectado do broker MQTT')

    @mqtt.on_subscribe()
    def handle_subscribe(client, userdata, mid, granted_qos):
        print('Assinatura MQTT realizada')
    