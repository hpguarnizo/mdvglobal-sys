# MDV Global
Pagina de www.mdvglobal.org, posee un eccomerce de libros digitales, audios y documentos; una seccion de convocatorias pagas y gratuitas con posibilidad de emitir online su transmicion, contenido con distintos tipos de suscripciones, un landing page, donaciones y pagos con MercadoPago.

Diagrama de clases
https://cacoo.com/diagrams/AsGZwbcaH3R3EVHr#EE9F1

Estructura del sitio
El sitio esta desarrollado en python 3.5 con Django 1.11 cuenta con las siguientes apps:
- accounts: Aqui esta todo lo referido al usuario
- blog: aqui solo se encuentra el registro del los suscriptos al newsletter de la pagina
- contenido: aqui se encuentra lo relacionado a los recursos subidos al sitio ya sea video audio o pdf relacionado a la suscripcion
- donacion: aqui se encuentra todo lo relacionado a las donaciones realizadas  y la configuracion de las mismas
- evento: aqui se encuentra lo referido a las convocatorias y entradas a cada una
- home: aqui se encuentra todo lo relacionado al login, el landing page y algunas paginas auxiliares
- pay: este es el modulo de pago, procesa todas las transacciones de mercado pago
- tienda: aqui se encuentra todo lo relacionado al eccomerce de libros audios y videos

Arquitectura del sitio
Se encuentra en el archivo docker-compose

Correr el sitio en desarrollo:
Se debe tener instalado docker, y se debera crear un archivo .env en la carpeta de inicio con las variables de entorno contenidas en el sitio de heroku o similar al archivo env_base de este repositorio
# docker-compose up
# docker-compose up
Ctrl-c
# docker-compose run web python manage.py loaddata cotenido categorias estados tipoevento motive plan tienda
# docker-compose run web python manage.py cities_light
# docker-compose run web python manage.py createsuperuser

Correr el sitio en produccion:
Se debera tener instalado heroku-cli y heroku-container, luego se debera setear la app de heroku y despues
# sudo heroku container:push web
Luego debera agregarse el addon de base de datos en heroku
# sudo heroku run python manage.py migrate
# sudo heroku run python manage.py loaddata cotenido categorias estados tipoevento motive plan tienda
# sudo heroku run python manage.py createsuperuser
# sudo heroku run python manage.py cities_light
Ademas deberan llenarse las variables de AWS con el bucket creado para la aplicacion, estas variables se encuentra en heroku





