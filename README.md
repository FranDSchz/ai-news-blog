# **Proyecto Final: Blog de Noticias sobre IA**

Este repositorio contiene el código fuente para el proyecto final de la cursada: una aplicación web de noticias sobre Inteligencia Artificial desarrollada con Django. El objetivo es crear un blog funcional que permita a distintos tipos de usuarios interactuar con el contenido.

## **🚀 Herramientas y Organización**

Nuestra gestión del proyecto se centraliza en Trello. Es nuestra **única fuente de verdad** para saber qué hay que hacer, quién lo está haciendo y qué se ha completado.

  * **Enlace al tablero:**  Cada miembro del equipo recibio al mismo mail con el cual se registrarion en el info la invitacion para unirse al tablero.

### **¿Cómo usamos Trello?**

El tablero está organizado en un flujo Kanban simple. Todas las tareas nacen en `Backlog` y se mueven hacia la derecha.

1.  **Elige una tarea de la columna `To Do`**. Las tareas con mayor prioridad estarán más arriba.
2.  **¡MUY IMPORTANTE\!** Antes de empezar, **lee la descripción completa de la tarjeta y revisa la checklist**. Ahí están los detalles y los requisitos de lo que hay que hacer.
3.  **Asígnate a la tarjeta** para que todos sepan que estás trabajando en ella.
4.  **Mueve la tarjeta a la columna `Doing`**. Nadie más debería trabajar en esa tarea.
5.  Una vez que hayas terminado y probado tu código, **mueve la tarjeta a `Done`**.

-----

## **💻 Flujo de Trabajo con Git y GitHub**

Para evitar conflictos y mantener el código ordenado, seguiremos un flujo de trabajo basado en ramas. **Nadie debe subir cambios directamente a la rama `main`**.

La idea principal es **integrar los cambios constantemente**. No esperes a tener una funcionalidad gigante terminada para subirla. Haz cambios pequeños y frecuentes.

### **Proceso para trabajar en una nueva tarea:**

1.  Asegúrate de tener la última versión del proyecto:
    ```bash
    git checkout main
    git pull
    ```
2.  Crea una nueva rama para tu tarea. El nombre debe ser descriptivo, usando el formato `feature/nombre-tarea`.
    ```bash
    # Ejemplo si tu tarea es crear el modelo de Post
    git checkout -b feature/modelo-post
    ```
3.  Ahora sí, ¡a programar\! Haz todos los cambios que necesites en tu rama.
4.  Cuando hagas un avance significativo, guarda tus cambios con un commit:
    ```bash
    git add .
    git commit -m "feat: Se crea el modelo Post con sus atributos"
    ```
5.  Sube tu rama a GitHub para tener una copia de seguridad y para luego integrarla:
    ```bash
    git push origin feature/modelo-post
    ```
6.  Cuando la tarea esté terminada, ve a GitHub y abre un **Pull Request (PR)** desde tu rama hacia `main`. Asigna a otro miembro del equipo para que revise tu código. Una vez aprobado, se podrá fusionar con la rama principal.

-----

## **📂 Estructura del Proyecto**


```markdown
/ai_news_config/
├── apps/               # Contenedor para todas nuestras aplicaciones de Django
│   ├── noticias/       # App para posts, categorías, comentarios
│   └── usuarios/       # App para perfiles, registro, login
├── ai_news_config/     # Carpeta de configuración del proyecto
│   ├── settings/       # Settings separados por entorno
│   │   ├── base.py     # Configuración común
│   │   ├── local.py    # Configuración para desarrollo
│   │   └── production.py # Configuración para el servidor final
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py         # Archivo de URLs principal
│   └── wsgi.py
│
├── media/              # Para archivos subidos por los usuarios (ej: fotos de posts)
├── static/             # Archivos estáticos (CSS, JS, imágenes del diseño)
│   ├── css/
│   ├── img/
│   └── js/
│
├── templates/          # Carpeta ÚNICA para todas las plantillas HTML
│   ├── noticias/
│   │   ├── home.html
│   │   └── post_detail.html
│   │   └── ...
│   ├── usuarios/
│   │   └── login.html
│   │   └── ...
│   └── base.html       # La plantilla principal de la que heredan todas las demás
│
├── .gitignore
├── db.sqlite3          # La base de datos
├── manage.py
├── README.md
└── requirements.txt
```
-----

## **🛠️ Cómo Levantar el Proyecto en Local**

Sigue estos pasos para tener el proyecto corriendo en tu computadora:

1.  **Clonar el Repositorio:**

    ```bash
    git clone https://github.com/FranDSchz/ai-news-blog.git
    cd ai-news-blog
    ```

2.  **Crear y Activar el Entorno Virtual:**
    Un entorno virtual (`env`) aísla las dependencias de nuestro proyecto.

    ```bash
    # Crear el entorno
    python -m venv .news-venv

    # Activarlo (Windows)
    .\.news-venv\Scripts\activate

    # Activarlo (macOS/Linux)
    source .news-venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    Esto instalará Django y cualquier otra librería que necesitemos.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar Migraciones:**
    Esto crea la base de datos (`db.sqlite3`) y las tablas según nuestros modelos.
    Primero nos aseguramos de estar parados en la carpeta del proyecto `ai_news_config`, si estamos en `ai-news-blog/` entonces:
    ```bash
    cd ai_news_config
    ```
    Ahora si podemos aplicar las migraciones.
    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```

6.  **Crear un Superusuario:**
    Necesitarás un usuario para acceder al panel de administrador (`/admin`).

    ```bash
    python manage.py createsuperuser
    ```

7.  **Levantar el Servidor:**
    ¡Listo\! Con esto, el proyecto estará corriendo.

    ```bash
    python manage.py runserver
    ```

    Ahora puedes abrir tu navegador y visitar **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** para ver la aplicación.
