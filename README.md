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

Implementación: Dentro del flujo de CI/CD (usando GitHub Actions, por ejemplo), se ha creado un paso que ejecuta la prueba de integración. esta prueba realiza una solicitud a la API y evalúa dos aspectos principales:

Código de Estado: Comprobamos que la API devuelva un código HTTP 200, indicando que la solicitud fue procesada exitosamente.
Contenido de Respuesta: Verificamos que el JSON de la respuesta contenga los datos válidos, lo que asegura que la API está realmente conectada a la base de datos y devolviendo datos reales.
Argumento: Esta prueba es fundamental, ya que cualquier fallo en ella indicaría problemas de conectividad o funcionalidad en la API, lo cual impactaría directamente en la experiencia del usuario final.

# el codigo se encontrara en la rama "master/devops/codigoAPI.py

3.2 Otras pruebas de Integración para Verificar el Funcionamiento del Sistema se puede verificar que la API esté sirviendo los datos, Estas podrían incluir:

Prueba de Disponibilidad de la Base de Datos: Verifica que la conexión a la base de datos esté activa y que las consultas se puedan realizar sin problemas y sin errores. Esta prueba puede lanzarse en CI/CD para validar que la base de datos esté respondiendo correctamente en cada despliegue realizado.

Prueba de Formato de Datos: Verifica que los datos devueltos por la API contengan el formato correcto. Esto es importante en casos en los que el cliente necesitara un JSON específico, asegurando la integración.

Prueba de Autenticación y Autorización (si aplica): Asegura que solo usuarios o aplicaciones autorizadas puedan acceder a los datos, reforzando la seguridad del sistema.

Implementación: Estas pruebas también pueden añadirse al flujo CI/CD para ejecutarse en cada despliegue o en periodos regulares.

3.3 Identificación de Puntos Críticos del Sistema (Fallo o Rendimiento)
Para garantizar la estabilidad del sistema, Aquí están algunos de ellos:

Latencia de Respuesta de la API: Si la API tarda demasiado en responder, la experiencia de usuario se verá afectada. Este problema puede ocurrir por problemas de rendimiento en la base de datos o en el propio entorno de la API.

Uso de Recursos en la Base de Datos: Un alto consumo de CPU o memoria en la base de datos podría llevar a caídas del sistema o lentitud en la respuesta. Este problema puede surgir cuando ocurren un alto volumen de consultas simultaneamente.

Cola de Mensajes en el Sistema Pub/Sub: Si la cola de mensajes se llena o tiene retrasos, podría haber problemas de entrega de datos a la base de datos, causando pérdida de información o retrasos en el procesamiento de datos.

Medición y Pruebas Sugeridas:

Latencia: Utilizar herramientas de monitoreo para medir el tiempo de respuesta de la API en tiempo real y simular múltiples solicitudes para ver si el sistema mantiene un tiempo de respuesta adecuado.

Rendimiento de la Base de Datos: Ejecutar pruebas de carga y monitorear el uso de CPU y memoria para asegurar que la base de datos pueda manejar la carga esperada.

Prueba de Saturación del Sistema Pub/Sub: Realizar pruebas de alta demanda para ver si la cola gestiona los datos correctamente bajo carga o presion.

3.4. Propuestas para Fortalecer el Sistema ante los Puntos Críticos Identificados
Para minimizar el impacto de los puntos críticos, es recomendable tomar algunas medidas adicionales:

Escalabilidad de la API: Implementar balanceo de carga en el endpoint de la API para repartir las solicitudes entrantes entre múltiples instancias de la función Lambda (o instancias EC2, si se utilizan). También podríamos configurar autoescalado para la función Lambda en función de la carga, asegurando que haya suficiente capacidad para manejar picos de tráfico.

Optimización de Consultas en la Base de Datos: Analizar las consultas SQL para optimizarlas y reducir la carga en la base de datos. Además, configurar índices en las tablas más consultadas para mejorar el rendimiento de búsqueda y acceso a los datos.

Gestión de Mensajes en Pub/Sub: Configurar alarmas en el sistema Pub/Sub para detectar cuellos de botella en la cola de mensajes. En caso de un aumento repentino en la ingesta de datos, podríamos ajustar la configuración para aumentar la capacidad de procesamiento de mensajes.

-------- o -----------------

Parte 4: Métricas y Monitoreo
4.1. Propuesta de Métricas Críticas para la Salud y Rendimiento del Sistema

Latencia de la API (Tiempo de Respuesta): Esta métrica mide el tiempo que toma la API para responder a una solicitud. Si la latencia es alta, puede ser una señal de que algo en la infraestructura (como la base de datos o el propio servidor) necesita optimización.

Tasa de Errores de la API: el porcentaje de solicitudes que terminan en error (por ejemplo, códigos de error HTTP como 500 o 404). Una tasa de errores alta puede indicar problemas serios en la API o en la conexión con la base de datos. 

Cantidad de Mensajes Procesados en Pub/Sub: Esta métrica muestra el número de mensajes que el sistema Pub/Sub procesa en un período determinado. Una baja en este número podría significar que hay un cuello de botella en el procesamiento de mensajes.

Estas tres métricas nos proporcionan una visión clara de la velocidad y fiabilidad del sistema desde la ingesta de datos hasta la exposición en la API.

4.2. Herramienta de Visualización y Métricas Mostradas
Herramienta de Visualización: Grafana o AWS CloudWatch (si estamos en el entorno de AWS) serían buenas opciones. Estas herramientas ofrecen tableros personalizables donde podemos ver todas las métricas en tiempo real y configurar alarmas si alguna métrica supera un umbral peligroso.

Métricas en el Tablero:

Gráfica de Latencia de la API: Nos mostraría la evolución del tiempo de respuesta de la API en intervalos de tiempo. Si vemos un aumento en la latencia, podríamos investigar problemas en la base de datos o en el servidor.

Panel de Tasa de Errores de la API: Este panel mostraría el porcentaje de errores de API en tiempo real. Esto nos ayuda a reaccionar rápidamente en caso de fallas inesperadas en el sistema.

Historial de Procesamiento de Mensajes en Pub/Sub: Nos muestra el número de mensajes procesados en cada período (hora, día). Nos permite ver si el sistema está cumpliendo con la ingesta de datos esperada o si existen retrasos.

Estas métricas visualizadas en un tablero centralizado nos permiten entender rápidamente la salud general del sistema, como ajustar la infraestructura o agregar más capacidad.

4.3. Implementación en la Nube y Recolección de Métricas
Implementación General:

Utilizamos AWS CloudWatch o Google Cloud Monitoring para configurar las métricas y alarmas, en función de los servicios que el sistema esté usando. Estas herramientas permiten monitorear servicios como bases de datos, servidores y funciones serverless (como Lambda).
Recolección de Métricas: Las métricas como latencia de la API y tasa de errores se recolectan automáticamente con AWS CloudWatch cuando la API está configurada en un entorno de Amazon API Gateway. Para Pub/Sub, Google Cloud Monitoring recopila métricas de cantidad de mensajes y latencia en el procesamiento.

Código de Ejemplo para AWS Lambda con CloudWatch:

# el codigo se encontrara en la rama "master/devops/

El código simula el registro de la latencia de la API en AWS CloudWatch, ayudándonos a monitorear los tiempos de respuesta.



