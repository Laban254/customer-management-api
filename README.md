![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3F729B?style=for-the-badge&logo=django&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![Ansible](https://img.shields.io/badge/Ansible-ED4B2A?style=for-the-badge&logo=ansible&logoColor=white)  ![AWS EC2](https://img.shields.io/badge/Amazon%20AWS%20EC2-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white) ![pytest](https://img.shields.io/badge/pytest-000000?style=for-the-badge&logo=pytest&logoColor=white) ![Shell](https://img.shields.io/badge/Shell-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)

[![codecov](https://codecov.io/github/Laban254/customer-management-api/graph/badge.svg?token=573LW1DYQJ)](https://codecov.io/github/Laban254/customer-management-api)

----------
# 📱 Django REST API with Google OAuth2 Authentication and SMS Notifications 🚀

A Django REST API for efficiently managing customers and orders, featuring OpenID Connect authentication, SMS notifications for order updates, comprehensive unit testing, and seamless CI/CD integration.



## 📑 Table of Contents

-   🎯 [Features](#features)
-   🛠️ [Technologies](#technologies)
-   🗂 [Database Schema](#database-schema)
-   📦 [Installation](#installation)
-   📡 [Endpoints](#endpoints)
-   📊 [Swagger UI](#swagger-ui)
-   📖 [Usage](#usage)
-   🧪 [Testing](#testing)
-   📜 [Logging Setup](#logging-setup)
-   🌐 [Nginx Configuration](#nginx-configuration)
-   ⚙️ [CI/CD Setup](#cicd-setup)
-   🔄 [CI/CD Configuration](#cicd-configuration)
-   🚀 [Deployment](#deployment)
-   📜 [License](#license)

----------

## 🎯 Features

-   🔐 **Google OAuth2 Login**: Users can authenticate using their Google accounts.
-   👥 **Customer Management**: Easily manage customer records.
-   📦 **Order Management**: Track and manage orders.
-   📲 **SMS Notifications**:  Send notifications via SMS API *(Africa's Talking)* when orders are created.

----------

## 🛠 Technologies

-   **Framework**: Django 🦄
-   **API**: Django REST Framework ⚙️
-   **Database**: PostgreSQL 🗄
-   **Containerization**: Docker 🐳
-   **CI/CD**: GitHub Actions 🔄
-   **Provisioning**: Ansible 📜
-   **Code Coverage**: Codecov 📊

----------

## 🗂 Database Schema

Below is the database schema for the project, showing the relationships between the `User`, `Customer`, and `Order` tables:


🗂 **Database Schema**

Below is the database schema for the project, showing the relationships between the `User`, `Customer`, and `Order` tables.
![Database Schema](./docs/images/db%20schema.png)

----------
## 📦 Installation

### Prerequisites

-   🐳 **Docker**:  Ensure that Docker is installed and running on your machine. For installation instructions, visit the [Docker installation guide](https://docs.docker.com/engine/install/).

----------

### 📝 Steps

1.  **Clone the Repository**:
    

    
    `git clone https://github.com/Laban254/customer-management-api.git`
    `cd customer-management-api` 
    
2.  **Create Environment Variables**: 
		Create a `.env` file in the project root and add the necessary variables:
    

    `GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret
    DATABASE_URL=your_database_url
    AFRICAS_TALKING_USERNAME=your_africas_talking_username
    AFRICAS_TALKING_API_KEY=your_africas_talking_api_key
    DEBUG=False
    ALLOWED_HOSTS=your_allowed_hosts` 
    
3.  **Run the Application with Docker**:
    

    `docker-compose up --build` 
    
4.  **Run Database Migrations**:
    

    
    `docker-compose exec web python manage.py migrate` 
    
5.  **Create a Superuser (Optional)**:
    

    
    `docker-compose exec web python manage.py createsuperuser` 
    
6.  **Access the Application**: Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

----------

## 📡Endpoints

-   `GET /auth/google/login/` - Initiates the Google OAuth2 login flow.
-   `GET /auth/google/callback/` - Handles the Google OAuth2 callback and exchanges the authorization code for tokens.
-   `POST /auth/token/refresh/`- Refreshes the access token using the refresh token.
-   `POST /auth/token/`- Exchanges credentials for a new access token..
-   `GET /api/customers/` - Retrieves the list of customers associated with the authenticated user.
-   `POST /api/customers/` - Creates a new customer associated with the authenticated user.
-   `GET /api/orders/` - Retrieves the list of orders associated with the authenticated user.
-   `POST /api/orders/` - Creates a new order and sends an SMS notification.
----------

## 📊  Swagger UI

The application provides a Swagger UI for API documentation. You can access it at:

-   **Swagger UI:** http://localhost:8000/swagger-ui/
-   **ReDoc:** http://localhost:8000/redoc/

----------

## 📖Usage

Follow these steps to se the application:

1.  **Initiate Google Login**: 
	To start the Google login process, open your web browser and navigate to the following URL:
     `GET /auth/google/login/` 
    This action will redirect you to Google’s authentication page, where you can log in with your Google account.
    
2.  **Authenticate**: Log in using your Google account. After authentication, you will be redirected to the callback URL with an authorization code.
    
4.  **Access Token**: The response will include both an access token and a refresh token. The access token is used to authorize requests to secured endpoints, while the refresh token can be used to obtain a new access token when the current one expires.
    
5.  **Authorize Requests**:
    
    -   To use the access token in Swagger UI, locate the endpoints requiring authentication (e.g., **/api/customers/**, **/api/orders/**) and click "Authorize".
    -   Enter the access token in the "Value" field and click "Authorize".
6.  **Using Other Tools**: You can also leverage the access token with tools like Postman to access the secured endpoints.

----------
    
## 🧪 Testing

Ensure everything works as expected by running the tests defined within your Django application. To execute tests and check code coverage, run:


`pytest --cov=your_app_name` 

Ensure that your test environment is properly configured and that the database is available.

----------

### 📜 Logging Setup

The Django application is configured to log messages to both the console and a log file. The logging configuration is defined in the `settings.py` file.

📝 Logs will be written to **myAppLogs.log**, and console logs will be visible in the Docker logs.

----------


### 🌐 Nginx Configuration

Nginx is configured to serve the Django application and handle static files. The Nginx configuration file is located at **nginx/nginx.conf**.

 📂 Access logs are stored in **/var/log/nginx/mydjangoapp_access.log**.  
⚠️ Error logs are stored in **/var/log/nginx/mydjangoapp_error.log**.

----------

# ⚙️  CI/CD Setup

#### 🌱 Initial Setup

To configure your AWS EC2 instance, follow these steps:

1.  **Configure AWS EC2**:
    -   Ensure your EC2 instance is running.
    -   Update the Ansible inventory file located at `ansible/inventory/hosts.ini` with your server's IP address.
    -   Modify the Ansible playbook at `ansible/playbooks/initialSetup.yml` as necessary to suit your configuration.
2.  **Trigger the Initial Setup Workflow**:
    -   In GitHub Actions, trigger the [**`initial-setup.yml`**](./github/workflows/initial-setup.yml) workflow to automatically configure your EC2 instance.  

#### 🔄  CI/CD Configuration

-   **Continuous Integration (CI)**: Managed through GitHub Actions, this automatically runs tests for every pull request using the [**`ci.yml`**](./github/workflows/ci.yml) workflow to ensure code quality.
    
-   **Continuous Deployment (CD)**: A separate workflow, [**`cd.yml`**](./github/workflows/cd.yml) is responsible for deploying your application whenever changes are pushed to the specified branch.
    
-   **Repository Secrets**: Set up the following GitHub secrets to enable seamless CI/CD operations: [.env.sample](.env.sample)
    
    -   `AFRICAS_TALKING_API_KEY`
    -   `AFRICAS_TALKING_USERNAME`
    -   `ANSIBLE_USER`
    -   `CODECOV_TOKEN`
    -   `DATABASE_URL`
    -   `EC2_PRIVATE_KEY`
    -   `EC2_USER`
    -   `GOOGLE_CLIENT_ID`
    -   `GOOGLE_CLIENT_SECRET`
    -   `SERVER_IP`








----------
## 🚀 Deployment

The application is automatically deployed to your server through the  [**`cd.yml`**](./github/workflows/cd.yml) workflow upon pushing changes to the specified branch.

----------
## 📜 License

This project is licensed under the MIT License.

----------