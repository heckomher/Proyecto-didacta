# Guía de Despliegue en Google Cloud Platform (GCP)

Esta guía te ayudará a desplegar tu aplicación (Django Backend + React Frontend + MySQL) en Google Cloud Platform.

## Prerrequisitos
1.  **Cuenta de Google Cloud**: Asegúrate de tener una cuenta activa con facturación habilitada.
2.  **Google Cloud SDK**: Instala `gcloud` CLI en tu máquina.
    - [Instrucciones de instalación](https://cloud.google.com/sdk/docs/install)
3.  **Docker**: Asegúrate de tener Docker corriendo.

## Paso 1: Configurar el Proyecto en GCP

1.  **Crear un nuevo proyecto** (o usar uno existente):
    ```bash
    gcloud projects create didacta-cloud --name="Didacta Project"
    gcloud config set project didacta-cloud
    ```

2.  **Habilitar servicios necesarios**:
    ```bash
    gcloud services enable run.googleapis.com sqladmin.googleapis.com cloudbuild.googleapis.com
    ```

## Paso 2: Configurar Base de Datos (Cloud SQL)

1.  **Crear instancia de MySQL**:
    ```bash
    gcloud sql instances create didacta-db-instance \
        --database-version=MYSQL_8_0 \
        --cpu=1 \
        --memory=3840MiB \
        --region=us-central1
    ```
    *(Esto puede tardar unos minutos)*

2.  **Configurar contraseña de root**:
    ```bash
    gcloud sql users set-password root \
        --host=% \
        --instance=didacta-db-instance \
        --password=TU_PASSWORD_SEGURA
    ```

3.  **Crear la base de datos**:
    ```bash
    gcloud sql databases create didacta_db --instance=didacta-db-instance
    ```

## Paso 3: Desplegar Backend (Cloud Run)

1.  **Construir y subir la imagen**:
    ```bash
    gcloud builds submit --tag gcr.io/didacta-cloud/backend ./backend
    ```

2.  **Desplegar en Cloud Run**:
    *Reemplaza `TU_PASSWORD_SEGURA` y `PROJECT_ID` con tus valores.*
    ```bash
    gcloud run deploy didacta-backend \
        --image gcr.io/didacta-cloud/backend \
        --region us-central1 \
        --platform managed \
        --allow-unauthenticated \
        --add-cloudsql-instances didacta-cloud:us-central1:didacta-db-instance \
        --set-env-vars DB_HOST=/cloudsql/didacta-cloud:us-central1:didacta-db-instance \
        --set-env-vars DB_NAME=didacta_db \
        --set-env-vars DB_USER=root \
        --set-env-vars DB_PASSWORD=TU_PASSWORD_SEGURA \
        --set-env-vars MONGO_URI="TU_URI_DE_MONGODB_ATLAS" \
        --set-env-vars DJANGO_SUPERUSER_USERNAME=admin \
        --set-env-vars DJANGO_SUPERUSER_PASSWORD=adminpass \
        --set-env-vars DJANGO_SUPERUSER_EMAIL=admin@example.com
    ```
    *Nota: `didacta-cloud:us-central1:didacta-db-instance` es el "Connection Name" de tu instancia SQL.*

3.  **Ejecutar Migraciones**:
    *Cloud Run no persiste datos, pero para correr migraciones puedes usar un "Job" o ejecutarlo temporalmente:*
    La forma más rápida es conectar desde tu máquina local usando Cloud SQL Proxy, o crear un Job en Cloud Run.
    
    *Opción Cloud Run Jobs (Recomendado):*
    ```bash
    gcloud run jobs create migrate \
        --image gcr.io/didacta-cloud/backend \
        --region us-central1 \
        --set-env-vars ... (mismas variables de arriba) ... \
        --command python,manage.py,migrate
    
    gcloud run jobs execute migrate --region us-central1
    ```

## Paso 4: Desplegar Frontend (Cloud Run)

1.  **Obtener URL del Backend**:
    Copia la URL que te dio el comando anterior (ej. `https://didacta-backend-xyz.a.run.app`).

2.  **Construir y subir imagen**:
    *(El build de Docker usará la variable VITE_API_URL para "quemarla" en el build de React)*
    ```bash
    gcloud builds submit --tag gcr.io/didacta-cloud/frontend ./frontend \
        --substitutions=_VITE_API_URL="https://didacta-backend-xyz.a.run.app"
    ```
    *Nota: Cloud Build necesita configuración extra para pasar argumentos de build a Docker. Si esto falla, construye localmente y sube:*
    ```bash
    # Opción alternativa (Local Build)
    cd frontend
    docker build --build-arg VITE_API_URL=https://didacta-backend-xyz.a.run.app -t gcr.io/didacta-cloud/frontend .
    docker push gcr.io/didacta-cloud/frontend
    ```

3.  **Desplegar**:
    ```bash
    gcloud run deploy didacta-frontend \
        --image gcr.io/didacta-cloud/frontend \
        --region us-central1 \
        --allow-unauthenticated
    ```

## ¡Listo!
Tu aplicación estará disponible en la URL que te entregue el último comando.
