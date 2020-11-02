# Plataforma Phishing

# modulos
## webphishingApi (/api/)
Modulo utilizado paraa todas las comunicaciones de los hoooks (maquinas que hacen phishing) y la plaataforma central. Esta recibe los resultados de los correos enviados, personas que hicieron click, etc etc etc.

## webphishingAuth (/auth/)
Maneja todo lo que es permisos, autenticacion, modelos de usuarios y clientes (nuestro cliente).

## webphishingBase
El proyecto base de django

## webphishingClient (/client/)
Contiene toda la informacion con respecto a los resultados de los ejercicios y sus campañas para cada cliente. Aca tambien se lleva registro de los colaboradores de cada cliente y su historial de phishing.

## webphishingCore (/admin/)
Manejo base de la plataforma

## webphishingManagement (/management/)
Administracion del sistema