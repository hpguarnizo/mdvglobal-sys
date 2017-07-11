# BaseProject
Componentes bases para iniciar un proyecto

# Archivos necesarios:

- Docker
- Docker-compose
- Heroku
- Heroku-container
- Git

# 1 - Variables de entorno
    - Abrir archivo env_base
    - Cambiar las variables de entorno
        DJANGO_SETTINGS_MODULE= .dev para desarrollo o .production para produccion
        DJANGO_SECRET_KEY= entra en el siguiente link y genera un secret key http://www.miniwebtool.com/django-secret-key-generator/
         
        #Crea un email de google para usar en desarrollo
        GOOGLE_ANALYTICS_PROPERTY_ID=crear cuenta en google analytics y obtener id
        SERVER_EMAIL=email de google
        DEFAULT_EMAIL_FROM=email de google
        EMAIL_HOST_USER=email de google
        EMAIL_HOST_PASSWORD=contraseña del email de google

        #Los emails de produccion es por si contamos con un servidor de emails como Gsuite

        #Crear cuenta de facebook developers, crear una API de facebook,en la seccion Configuracion>>Basica>>URL del sitio poner https://nombreapp.herokuapp.com/
        #en Revision de la Aplicacion>>Tu aplicacion debe ser publica y  Revision de la Aplicacion>>Elementos aprobados>>Permisos de inicio de sesion>>Debe 
        #estar el email         
        SOCIAL_AUTH_FACEBOOK_KEY=crear cuenta en facebook developers, crear una api, llenarlo con el <Identificador de la aplicación>
        SOCIAL_AUTH_FACEBOOK_SECRET=llenarlo con la <Clave secreta de la aplicación>
        
        #Crear una cuenta en twitter, Ir a Twitter Application Management, crear una app de twitter, en settings>>Aplications Details>>Callback URL  
        #poner https://nombreapp.herokuapp.com/ y Allow this application to be used to Sign in with Twitter debe estar tildado. 
        #En Permissions>>Access>>Read and Write>>Debe estar tildado y 
        #Permissions>>Additional Permissions>>Request email addresses from users>>Debe estar tildado
        SOCIAL_AUTH_TWITTER_KEY=Keys and Access Tokens>>Application Settings>>Consumer Key (API Key)                         
        SOCIAL_AUTH_TWITTER_SECRET=Keys and Access Tokens>>Application Settings>>Consumer Secret (API Secret)   
        
        #Con la cuenta de google, entrar a Google API Console, en Biblioteca>>API sociales>>Google+ Api>>habilitarla , en Credentials>>Create credentials>>OAuth
        #client ID>> Restrictions>>Authorized JavaScript origins>>https://nombreapp.herokuapp.com y https://www.tudominio.com(si lo tienes),
        #y en Authorized redirect URIs>>https://nombreapp.herokuapp.com/complete/google-oauth2/ y https://www.tudominio.com/complete/google-oauth2/
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=Client ID   
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=Client secret 

        #Crear una cuenta en mercado pago, ir a https://www.mercadopago.com/mla/account/credentials(o buscar la pagina de las credenciales de tu cuenta), y en
        #Checkout personalizado, usar las credenciales de Modo Sandbox para desarrollo y  Modo Producción para produccion. Recuerda que deberas completar mas
        #datos para usarla en produccion.   
        PUBLIC_KEY_MP=Public key
        ACCESS_TOKEN_MP=Access token

        #Crear una cuenta en amazon web services, cuando pida el numero ponerlo en Argentina con +5493513000000. Luego vas a Services>>Storage>>S3>>Create bucket>>
        #Aclaracion: el bucket_name es unico, la region debe ser la mas cercana a su posicion para evitar costos adicionales.
        #En la lista de buckets entrar al que creamos luego ir a Permissions>>CORS configuration y verificar que esta como #sigue
        
            <!-- Sample policy -->
            <CORSConfiguration>
	            <CORSRule>
		            <AllowedOrigin>*</AllowedOrigin>
                    <AllowedMethod>POST</AllowedMethod>
                    <MaxAgeSeconds>3000</MaxAgeSeconds>
                    <AllowedHeader>Authorization</AllowedHeader>
	            </CORSRule>
            </CORSConfiguration> 
        
        #Para obtener el AWS_SECRET_ACCESS_KEY y el AWS_ACCESS_KEY_ID ir a Services>>Security, Identity & Compliance>>IAM>>Groups
    	#Crear un nuevo grupo: Step 1 : Group Name (el nombre que quieres),Step 2 : Attach Policy (Debes agregar los permisos de AmazonDMSRedshiftS3Role,AmazonS3FullAccess,AdministratorAccess, AmazonS3ReadOnlyAccess)
    	#Crear un usuario, con el nombre que quieres, Access type:Programmatic access, en la siguiente etapa debeas agregar al nuevo usuario al grupo creado anteriormente para que tenga los permisos del grupo, este usuario nos dara el access key id y el secret access key.
    	#Por ultmo aqui http://docs.aws.amazon.com/general/latest/gr/rande.html, buscamosla region depende de donde decidimos iban a alojarse las imagenes o archivos.           
        AWS_SECRET_ACCESS_KEY=9999999
        AWS_ACCESS_KEY_ID=99999999
        AWS_STORAGE_BUCKET_NAME=name_bucket
        S3DIRECT_REGION=us-west-2
                
    -Guardar archivo con el nombre ".env", este archivo no debera subirse a github por problemas de seguridad.

# 2 - Configurar web>>settings>>production
    - ALLOWED_HOSTS = ['www.tudominio.com',]
    - SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/ruta/relativa/ "
    - S3DIRECT_DESTINATIONS = esta descomentado para subir imagenes necesario para la foto de perfil, se puede descomentar para subir pdf o videos.

# 3 - Modificar web/home/context_processors.py
    - Metodo company debe devolver el nombre de su compañia
    
# 4 - Modificar templates de Home
    - index.html - Etiquetas meta
    - home_index.html
    - home_support.html - Si desea agregar algun soporte ademas de tecnico y comercial
    - home_terms_and_privacity.html - revisar y cambiar los terminos y condiciones

# 5 - Modificar fixtures de Home
    - Agregar si va a haber algun soporte ademas de tecnico y comercial

# 6 - Modificar emails de Home
    - Revisar el texto de los emails y la estructura 

# 7 - Modificar views de Home
    - view:Support Si se agrego algun soporte crear el metodo que envia el email en emails.py y poner el condicional en la vista para enviar ese email 
    - view:SignupTrialView modificar la cantidad de dias de prueba luego del comentario #Client premium for 14 days

# 8 - Modificar templates de Pay
    - Revisar todos los textos incluyendo los email

# 9 - Modificar views Pay
    - view:buy_my_item Este metodo realiza el pago en pesos de la moneda local de la cuenta de Mercado Pago, transaction_amount es donde debe ir el precio, 
    -                  dentro de if payment['response']['status'] == 'approved': se ejecuta la logica cuando el pago fue aprobado

# 10 - Modificar templates de blog
    - blog_post_atraer.html es un ejemplo de un post del blog creado
    - blog_about.html esta un ejemplo de presentacion de la compañia
    - blog.html inicio del blog donde aparecen todos los post
    -
           
     
# Instrucciones antes de iniciar (en la raiz del proyecto):

- sudo docker-compose build
- sudo docker-compose run web python manage.py createsuperuser
- sudo docker-compose up
- Acceder al navegador e ingresar a la direccion localhost:8080 o 0.0.0.0:8080 
  (Si no accede, entrar al archivo docker-compose y cambiar en la seccion ports del servicio
 web a "8080:8080" o "8080"). 

