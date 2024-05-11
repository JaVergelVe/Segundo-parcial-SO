import threading
import time
import queue



sillas_ocupadas = 0  # Número de sillas ocupadas en la barbería
clientes_esperando = queue.Queue()  # Cola para mantener un registro de los clientes esperando
barbero_dormido = threading.Semaphore(0)  # Semáforo para controlar si el barbero está dormido
mutex_sillas = threading.Lock()  # Objeto de exclusión mutua para proteger acceso a sillas_ocupadas


def entrar_a_barberia(cliente_id):
    global sillas_ocupadas
    global barbero_dormido
    global mutex_sillas
    
    mutex_sillas.acquire()  # tenemos el lock del mutex para proteger la sección crítica
    if sillas_ocupadas < 3:  
        sillas_ocupadas += 1  # Ocupar  silla
        print(f"Cliente {cliente_id} se sienta. Sillas ocupadas: {sillas_ocupadas}")
        mutex_sillas.release()  # Liberamos el lock del mutex
        if sillas_ocupadas == 1:
            barbero_dormido.release()  # Despertamos al barbero si estaba dormido
        atender_cliente(cliente_id)  # El cliente espera a ser atendido
    else:
        print(f"Cliente {cliente_id} se va, todas las sillas están ocupadas.")
        mutex_sillas.release()  # liberar el lock del mutex , no hay sillas disponibles

def atender_cliente(cliente_id):
    global sillas_ocupadas
    global clientes_esperando
    global barbero_dormido
    global mutex_sillas
    
    print(f"Barbero atiende al cliente {cliente_id}.")
    time.sleep(2) 
    mutex_sillas.acquire()  # tenemos el lock del mutex para proteger la sección crítica
    sillas_ocupadas -= 1  # Liberamos una silla
    print(f"Barbero termina de atender al cliente {cliente_id}. Sillas ocupadas: {sillas_ocupadas}")
    if sillas_ocupadas == 0:
        barbero_dormido.acquire()  # El barbero deurme , no hay más clientes 
    mutex_sillas.release()  # liberaar el lock del mutex


def funcion_barbero():
    global clientes_esperando
    global barbero_dormido
    
    while True:
        barbero_dormido.acquire()  # eel barbero se duerme si no hay clientes esperando
        print("Barbero despierto.")
        if not clientes_esperando.empty():  # Si hay clientes esperando
            cliente_id = clientes_esperando.get()  # Obtenemos al siguiente cliente de la cola
            atender_cliente(cliente_id)


def funcion_cliente(cliente_id):
    entrar_a_barberia(cliente_id)  
    time.sleep(1) 

#hilo de barbero
hilo_barbero = threading.Thread(target=funcion_barbero)
hilo_barbero.start()  

# hilos de clientes
for i in range(10):
    hilo_cliente = threading.Thread(target=funcion_cliente, args=(i,))
    hilo_cliente.start()  # Iniciamos cada hilo de cliente
    time.sleep(0.5)  