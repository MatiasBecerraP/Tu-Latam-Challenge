Desafío Técnico DevSecOps/SRE

Parte 1: Infraestructura y IaC:

1.1 La infraestructura se ha dividido en tres componentes principales:

Esquema Pub/Sub para Ingesta de Datos: Se utilizo Amazon Simple Notification Service (AmazonSNS) y Amazon Simple Queue Service o "Amazon SQS" en AWS para gestionar la ingesta de datos en tiempo real. SNS actuará como un "publicador" que recibe los mensajes, y SQS como la "suscripción" que este encolara los mensajes para su posterior procesamiento. Esto asegurara una entrega confiable y escalable de los datos.

La Base de Datos: Se ha seleccionado Amazon Relational Databases "Amazon RDS" con PostgreSQL, es ideal para almacenamiento y procesamiento de grandes volúmenes de datos, ya que esto permite consultas rápidas y almacenamiento optimizado para la analítica.

Endpoint HTTP para Exposición de Datos: Utilizamos AWS API Gateway junto con una función AWS Lambda que actuará como la API. La API permitirá el acceso a los datos almacenados, exponiéndolos a través de un endpoint HTTP.

1.2 Despliegue de la Infraestructura con Terraform (opcional)
Terraform se utiliza para crear y configurar estos recursos en AWS de manera automatizada. Este enfoque IaC facilita la consistencia, replicación y escalabilidad de la infraestructura.

Código de Ejemplo en Terraform:

Para crear los componentes mencionados (SNS, SQS, RDS y API Gateway), hemos utilizado Terraform. Cada recurso está declarado en archivos de configuración de Terraform. Por ejemplo:

El tópico SNS y la cola SQS se declaran como recursos para el sistema de Pub/Sub.
La base de datos PostgreSQL se configura con los parámetros necesarios para almacenamiento y consultas.
El API Gateway y Lambda se crean y configuran para exponer los datos de la base de datos.
Este proceso incluye tres pasos clave:

"Inicialización de Terraform (terraform init) para preparar el entorno de trabajo".

"Verificación del Plan (terraform plan) para confirmar los cambios antes del despliegue".

"Aplicación del Plan (terraform apply) para crear los recursos en AWS".

# el codigo se encontrara en la rama "master/devops/

----------- o ----------

Parte 2: Aplicación y Flujo CI/CD
2.1 API HTTP para Exponer los Datos
Para el endpoint HTTP, creamos una función Lambda en Python. Esta función se conecta a la base de datos PostgreSQL, se realiza una consulta a los datos y devuelve el resultado en formato JSON.
# el codigo se encontrara en la rama "master/devops/codigopython2.1"

Asegúrarse de que los datos y el servidor de la API cumplan con requisitos de seguridad.

Paso 2.2: Desplegar la API HTTP en la nube mediante CI/CD
Para automatizar el despliegue de esta API, hemos configurado "GitHub Action" como pipeline de CI/CD. Cada vez que se realiza un cambio en el repositorio, GitHub Actions ejecuta el flujo, actualizando automáticamente la función Lambda en AWS. Esto asegura que los despliegues sean consistentes y ágiles.

# el codigo se encontrara en la rama "master/devops/pipeline2.2"








