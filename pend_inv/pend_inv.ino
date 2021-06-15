/**********************************************/
/* Ejemplo llamada a la funcion read_dis(x,y) */
/* la funcion read_ang()                      */
/**********************************************/

#include "pend_inv_lib.h"

#define PIN_TRIG 4
#define PIN_ECHO 5

void setup() {
    pinMode(PIN_TRIG, OUTPUT);
    pinMode(PIN_ECHO, INPUT);
    // incializacion de comunicacion serie a 9600bps
    Serial.begin(9600);
    // espero 10ms para q se inicialice el puerto
    delay(10);                    
}
void loop() {
    float angulo, distancia;
/*    angulo = read_ang();
    // imprimo valor del ANGULO puerto serie 
    Serial.println("Ángulo:" + String(angulo,2)); */
    distancia = read_dis(PIN_TRIG,PIN_ECHO);
    // imprimo valor de la distancia en el puerto serie
    Serial.println(distancia);
}
/**********************************************/

/**********************************************/
/* Ejemplo llamada a la funcion:              */
/* vel_mot(X, Y, ENXY, D, SENTIDO)            */
/**********************************************/
/*
#include "pend_inv_lib.h"

#define PIN_IN1 6
#define PIN_IN2 7
#define PIN_ENA 5

void setup() {
    pinMode(PIN_IN1, OUTPUT);
    pinMode(PIN_IN2, OUTPUT);
    pinMode(PIN_ENA, OUTPUT);
    // incializacion de comunicacion serie a 9600 bps
    Serial.begin(9600);
    // espero 10ms para q se inicialice el puerto
    delay(10);                    
}
void loop(){
    int vel, D = 0.5;
    vel = vel_mot(PIN_IN1, PIN_IN2, PIN_ENA, D, "CW");
    if (vel == 1)
        Serial.println("El motor está girando en sentido horario y v = v_N(50%)");
    else if (vel == 0)
        Serial.println("Error en Duty Cycle");
    else
        Serial.println("Error en Sentido de Giro");
    delay(5000);
    D = 0;
    vel = vel_mot(PIN_IN1, PIN_IN2, PIN_ENA, D, "CW");
    delay(2000);
    D = 0.5;
    vel = vel_mot(PIN_IN1, PIN_IN2, PIN_ENA, D, "CCW");
    if (vel == 1)
        Serial.println("El motor está girando en sentido anti-horario y v = v_N(50%)");
    else if (vel == 0)
        Serial.println("Error en Duty Cycle");
    else
        Serial.println("Error en Sentido de Giro");
    delay(5000);
    D = 0;
    vel = vel_mot(PIN_IN1, PIN_IN2, PIN_ENA, D, "CW");
} */
/**********************************************/
