Configuración Inicial del Proveedor

# Configurar el proveedor de AWS
provider "aws" {
  region = "us-west-2"
}

1. Esquema Pub/Sub
Amazon SNS y SQS para la ingesta de datos

# Crear un tópico de SNS para recibir mensajes de ingesta
resource "aws_sns_topic" "ingesta_topic" {
  name = "ingesta_topic"
}

# Crear una cola SQS para almacenar mensajes de ingesta
resource "aws_sqs_queue" "ingesta_queue" {
  name = "ingesta_queue"
}

# Crear una suscripción que conecte SNS con SQS
resource "aws_sns_topic_subscription" "sns_to_sqs" {
  topic_arn = aws_sns_topic.ingesta_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.ingesta_queue.arn
}


2. Base de Datos de Analítica
Amazon RDS para PostgreSQL

# Base de datos PostgreSQL
resource "aws_db_instance" "analytica_db" {
  allocated_storage    = 20
  engine               = "postgres"
  instance_class       = "db.t2.micro"
  name                 = "analytica_db"
  username             = "admin"
  password             = "password123" 
  parameter_group_name = "default.postgres12"
  skip_final_snapshot  = true
}

3. API HTTP para Exposición de Datos
AWS API Gateway y Lambda

# Crear una función Lambda para la API
resource "aws_lambda_function" "data_api" {
  function_name = "data_api_handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.8"
  filename      = "lambda_function_payload.zip"
}

# Crear API Gateway para exponer la función Lambda
resource "aws_api_gateway_rest_api" "data_api_gateway" {
  name        = "Data API"
  description = "API para exponer datos desde la base de datos"
}

# Configurar integración de API Gateway con Lambda
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.data_api_gateway.id
  resource_id             = aws_api_gateway_rest_api.data_api_gateway.root_resource_id
  http_method             = "GET"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.data_api.invoke_arn
}

