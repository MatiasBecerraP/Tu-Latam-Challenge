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

# el codigo se encontrara en la rama "master/devops/terraform.hcl y terraformbash.bash

----------- o ----------

Parte 2: Aplicación y Flujo CI/CD
2.1 API HTTP para Exponer los Datos
Para el endpoint HTTP, creamos una función Lambda en Python. Esta función se conecta a la base de datos PostgreSQL, se realiza una consulta a los datos y devuelve el resultado en formato JSON.
# el codigo se encontrara en la rama "master/devops/codigopython2.1.py"

Asegúrarse de que los datos y el servidor de la API cumplan con requisitos de seguridad.

Paso 2.2: Desplegar la API HTTP en la nube mediante CI/CD
Para automatizar el despliegue de esta API, hemos configurado "GitHub Action" como pipeline de CI/CD. Cada vez que se realiza un cambio en el repositorio, GitHub Actions ejecuta el flujo, actualizando automáticamente la función Lambda en AWS. Esto asegura que los despliegues sean consistentes y ágiles.

# el codigo se encontrara en la rama "master/devops/pipeline2.2.yaml"

paso 2.3: Ingesta Opcional (Pub/Sub)

Conecta el servicio Pub/Sub (como AWS SQS) a una función que procese los mensajes y los guarde en la base de datos.

paso 2.4: Diagrama de Arquitectura
El Pub/Sub recibe datos.
Los datos ingresan a la base y luego se leen a través del API.

# El diagrama en formato png se encontrara en la rama "master/devops/"

El diagrama de arquitectura se encontara lo mas simplificado posible en el flujo de datos del sistema:

Pub/Sub recibe los datos y los ingresa en la base de datos.
Base de Datos Analítica almacena los datos.
API HTTP esto lee los datos en la base de datos y los expone a los clientes mediante solicitudes GET.

------- o --------

Parte 3: Pruebas de Integración y Puntos Críticos de Calidad
1. Implementación de Prueba de Integración en CI/CD para Verificar la API
Propósito: Esta prueba tiene como objetivo asegurarnos de que la API esté funcionando correctamente y sea capaz de recuperar los datos de la base de datos cuando se le envía una solicitud GET. Es crucial porque permite confirmar que tanto la API como la base de datos están comunicándose sin problemas.

Implementación: Dentro del flujo de CI/CD (usando GitHub Actions, por ejemplo), hemos creado un paso que ejecuta esta prueba de integración. La prueba realiza una solicitud a la API y evalúa dos aspectos principales:

Código de Estado: Comprobamos que la API devuelva un código HTTP 200, indicando que la solicitud fue procesada exitosamente.
Contenido de Respuesta: Verificamos que el JSON de respuesta contenga datos válidos, lo que asegura que la API está realmente conectada a la base de datos y devolviendo datos reales.
Argumento: Esta prueba es fundamental, ya que cualquier fallo en ella indicaría problemas de conectividad o funcionalidad en la API, lo cual impactaría directamente en la experiencia del usuario final.

# el codigo se encontrara en la rama "master/devops/





