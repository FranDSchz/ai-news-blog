# AI News Blog 🤖📰

¡Bienvenido a AI News Blog! Una aplicación web full-stack desarrollada con Django que funciona como un portal de noticias centralizado sobre los últimos avances en Inteligencia Artificial.

Este proyecto fue desarrollado como el trabajo final para el programa "Informatorio Chaco", aplicando los principios del desarrollo backend, la arquitectura MTV y la gestión de bases de datos.

### Demo Visual

`![Demo del Proyecto](URL)` Pendiente

---

## 🚀 Features Principales

* **Gestión de Contenido (CRUD):** Los administradores y autores pueden crear, editar y eliminar noticias.
* **Sistema de Usuarios:** Registro, inicio de sesión y perfiles de usuario personalizados.
* **Comentarios Interactivos:** Los usuarios registrados pueden comentar en las noticias, fomentando la discusión.
* **Categorización y Búsqueda:** Las noticias están organizadas por categorías y los usuarios pueden usar una barra de búsqueda para encontrar artículos de su interés.
* **Panel de Administración:** Interfaz de administración para gestionar usuarios, noticias, categorías y comentarios.

---

## 🛠️ Stack Tecnológico

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## ⚙️ Instalación y Uso Local

Para ejecutar este proyecto en tu propia máquina, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/FranDSchz/ai-news-blog.git
    cd ai-news-blog
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplica las migraciones:**
    ```bash
    python ai_news_config/manage.py migrate
    ```

5.  **Crea un superusuario para acceder al admin:**
    ```bash
    python ai_news_config/manage.py createsuperuser
    ```

6.  **Ejecuta el servidor de desarrollo:**
    ```bash
    python ai_news_config/manage.py runserver
    ```

¡Listo! Abre tu navegador y ve a `http://127.0.0.1:8000` para ver la aplicación funcionando.

---
## 💡 Desafíos y Aprendizajes

Uno de los principales desafíos de este proyecto fue diseñar la estructura de los modelos y las relaciones en la base de datos para que fueran escalables. Implementar el sistema de comentarios anidados y la gestión de perfiles de usuario me permitió profundizar en el ORM de Django y en cómo manejar la lógica de negocio compleja en las vistas.