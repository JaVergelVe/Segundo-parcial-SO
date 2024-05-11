package main

import (
	"fmt"
	"sync"
	"time"
)

var (
	sillasOcupadas   = 0            // Número de sillas ocupadas en la barbería
	mutexSillas      sync.Mutex     // Mutex para proteger acceso a sillasOcupadas
	barberoDormido   = make(chan bool, 1) // Canal para controlar si el barbero está dormido
	clientesEsperando = make(chan int, 3) // Canal para mantener un registro de los clientes esperando
)

func entrarABarberia(clienteID int) {
	mutexSillas.Lock()
	if sillasOcupadas < 3 {
		sillasOcupadas++
		fmt.Printf("Cliente %d se sienta. Sillas ocupadas: %d\n", clienteID, sillasOcupadas)
		mutexSillas.Unlock()
		barberoDormido <- false // Despierta al barbero si está dormido
		atenderCliente(clienteID)
	} else {
		fmt.Printf("Cliente %d se va, todas las sillas están ocupadas.\n", clienteID)
		mutexSillas.Unlock()
	}
}

func atenderCliente(clienteID int) {
	fmt.Printf("Barbero atiende al cliente %d.\n", clienteID)
	time.Sleep(2 * time.Second)
	mutexSillas.Lock()
	sillasOcupadas--
	fmt.Printf("Barbero termina de atender al cliente %d. Sillas ocupadas: %d\n", clienteID, sillasOcupadas)
	if sillasOcupadas == 0 {
		<-barberoDormido // El barbero duerme si no hay más clientes
	}
	mutexSillas.Unlock()
}

func barbero() {
	for {
		_, ok := <-barberoDormido
		if ok {
			fmt.Println("Barbero despierto.")
			select {
			case clienteID := <-clientesEsperando:
				atenderCliente(clienteID)
			default:
				fmt.Println("El barbero duerme.")
				<-barberoDormido // El barbero vuelve a dormir si no hay clientes esperando
			}
		}
	}
}

func cliente(clienteID int) {
	entrarABarberia(clienteID)
	time.Sleep(1 * time.Second)
}

func main() {
	go barbero()

	for i := 0; i < 10; i++ {
		go cliente(i)
		time.Sleep(500 * time.Millisecond)
	}

	time.Sleep(10 * time.Second) // Tiempo suficiente para que se completen las operaciones
}
