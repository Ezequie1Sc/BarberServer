# 💈 API de Barbería - Sistema de Reservaciones

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-orange.svg)
![Flask-RESTX](https://img.shields.io/badge/Flask--RESTX-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Arquitectura](https://img.shields.io/badge/Arquitectura-MVC-purple)
![Swagger](https://img.shields.io/badge/Swagger-UI-brightgreen.svg)

API RESTful profesional para la gestión de una barbería con sistema de reservaciones, control de usuarios y auditoría de accesos. Desarrollada con Flask y PostgreSQL siguiendo una arquitectura por capas (MVC) para garantizar escalabilidad y mantenibilidad.

## 📋 Características

### 👥 Gestión de Usuarios
- Registro y autenticación de usuarios
- Control de accesos con auditoría
- Perfiles personalizados

### 📅 Sistema de Reservaciones
- Creación de citas para servicios de barbería
- Validación de disponibilidad horaria
- Gestión de estados (Pendiente, Confirmada, Cancelada, Completada)
- Reservas para terceros

### 🔐 Auditoría y Seguridad
- Registro de todos los intentos de login
- Seguimiento de IPs y user agents
- Reportes de accesos exitosos/fallidos

### 🏗️ Arquitectura Profesional
- Separación en capas (Models, Routes, Services)
- Documentación automática con Swagger UI
- Validaciones centralizadas
- Manejo de logs y errores

## 🛠️ Stack Tecnológico

<div align="center">
  
![Tecnologías](https://skillicons.dev/icons?i=python,flask,postgres,git,github,vscode)

</div>

### Backend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.8+ | Lenguaje de programación base |
| **Flask** | 2.0+ | Framework web principal |
| **Flask-RESTX** | 1.0+ | API RESTful con Swagger automático |
| **Flask-SQLAlchemy** | 3.0+ | ORM para base de datos |
| **PostgreSQL** | 13+ | Base de datos relacional |
| **Flask-CORS** | 4.0+ | Habilitar CORS para frontend |
| **Python-dotenv** | 1.0+ | Gestión de variables de entorno |

## 📁 Estructura del Proyecto (MVC)
