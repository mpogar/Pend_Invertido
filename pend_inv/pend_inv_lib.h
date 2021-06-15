/**********************************************/
/*               SONAR HC - SR04              */
/* Calculo distancia en m sensor ultrasonico  */
/*        Velocidad del SONIDO = 343m/s       */
/* 343m/s * 1/1.000.000s/us = 1/2.915,45m/us  */
/* Distancia(m) = Tiempo(us) * 1/5.830,9m/us  */
/**********************************************/

// Obtiene la distancia en m (0.02-4.00), si falla regresa -1
float read_dis(int p_trig, int p_echo){     
    float val;
    //para generar un pulso limpio ponemos triger a LOW 5us
    digitalWrite(p_trig, LOW);  
    delayMicroseconds(5);
    //generamos Trigger (disparo) de 10us   
    digitalWrite(p_trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(p_trig, LOW);   
    val = pulseIn(p_echo, HIGH);
    val = val / 5830.90;
    if (val >= 0.02 and val <= 4.00)
        return val;
    else 
        return -1;  
}

/**********************************************/
/*       ENCODER ROTATORIO INCREMENTAL        */
/* Atención: debemos conectar los pines A y B */
/* del ENCODER a los pines 2 y 3 del ARDUINO  */
/* pues son los dos pines q admiten interrup. */
/**********************************************/

/* int PIN_A = 2;
int PIN_B = 3; */
#define PIN_A 2
#define PIN_B 3

// defino variable global ("volatile") posicion con valor inicial 0 pues es 
// usada en read_ang y las ISRs (ai0 y ai1)
// esta variable se incrementará o decrementar dependiendo de la rotación 
// del encoder
volatile float posicion = 0;

void ai0() {
    // ai0 is activated if PIN_A is going from LOW to HIGH
    // Check pin PIN_B to determine the direction
    if(digitalRead(PIN_B)==LOW) {
        posicion++;
    }
    else {
        posicion--;
    }
}
void ai1() {
    // ai0 is activated if PIN_B is going from LOW to HIGH
    // Check with pin PIN_A to determine the direction
    if(digitalRead(PIN_A)==LOW) {
        posicion--;
    }
    else {
        posicion++;
    }
}
float read_ang() {
    // defino la variable anterior la cual almacena el valor anterior de posicion
    // static: modificador para indicar que una variable debe mantener su
    // valor entre llamados de la función.	
    static float anterior = 0;
    static bool inicio = true;
    if (inicio) {
        // internal pullup input pin 2
        pinMode(PIN_A, INPUT_PULLUP);  
        // internal pullup input pin 3
        pinMode(PIN_B, INPUT_PULLUP);
        inicio = false;        
    } 
    float ang;
    // INTERRUPCIÓN:
    // attachInterrupt(digitalPinToInterrupt(pin), ISR, modo)
    // modo = LOW, RISING, CHANGE, FALLING, HIGH (modelos DUE, ZERO, MKR1000)
    // interrupcion sobre pin = PIN_DT con funcion ISR = encoder y modo = LOW 
    // A rising pulse from encodenren activated ai0(). 
    attachInterrupt(digitalPinToInterrupt(PIN_A), ai0, RISING);
    // B rising pulse from encodenren activated ai1(). 
    attachInterrupt(digitalPinToInterrupt(PIN_B), ai1, RISING);
    // Send the value of posicion
    if (posicion != anterior) {
        // asigna a anterior el valor actualizado de posicion
        anterior = posicion;
    }        
    // mapping degree into pulse
    ang = map(anterior, 0.00, 1200.00, 0.00, 360.00);
    return (ang);        
}

/**********************************************/
/*    CONTROL VELOCIDAD MOTOR CC CON L298N    */
/*          ENA IN1 IN2     MOTOR A
/*           0   x   x         -              */
/*           1   0   1        CW              */
/*           1   1   0        CCW             */
/*          ENB IN3 IN4     MOTOR B
/*           0   x   x         -              */
/*           1   0   1        CW              */
/*           1   1   0        CCW             */
/*  ENA y ENB --> deben conectarse a PINES de */
/*  SALIDA PWM (p_enable).                    */
/*  IN1, IN2, IN3 e IN4 --> deben conectarse  */
/*  a PINES de SALIDA (p_inX, p_inY).         */
/**********************************************/

// Hace girar al motor a determinada velocidad y en un sentido determinado,
// si todo va bien devuelve un 1
int vel_mot(int p_inX, int p_inY, int p_enable, int duty_cycle, String sentido){     
    if (0 <= duty_cycle <= 1) {
        // mapeo duty_cycle en pulsos
        duty_cycle = map(duty_cycle, 0, 1, 0, 255);
        analogWrite(p_enable, duty_cycle);
        if (sentido == "CW"){
            digitalWrite(p_inX, LOW);	// IN1 o IN3 en 0
            digitalWrite(p_inY, HIGH);	// IN2 o IN4 en 1
        } 
        else if (sentido == "CCW"){
            digitalWrite(p_inX, HIGH);	// IN1 o IN3 en 0
            digitalWrite(p_inY, HIGH);	// IN2 o IN4 en 1
        }
        else
            return (-1); 
    }
    else
        return (0);
    return (1);      
}