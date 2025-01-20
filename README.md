# Projeto 001

## Overview

Projeto 001 is a web application designed to manage user authentication, data visualization, and administrative tasks. The application is built using Flask, SQLAlchemy, and other modern web technologies. It supports Google OAuth for user authentication and provides various functionalities for managing data, filters, and user permissions.

## Features

- User authentication via Google OAuth
- Data visualization using Folium maps
- Administrative functionalities for managing users, filters, and data
- Caching for improved performance
- Responsive design for desktop usage

## Project Structure

```
Projeto 001/
├── __pycache__/
├── .vscode/
│   └── settings.json
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── blueprints/
│   │   ├── __init__.py
│   │   └── bps.py
│   ├── cache/
│   │   ├── __init__.py
│   │   └── cache.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── AIController.py
│   │   ├── DadosController.py
│   │   ├── DatabaseController.py
│   │   ├── FiltroController.py
│   │   └── PerfilController.py
│   ├── ext/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── migrate.py
│   ├── mail/
│   │   ├── __init__.py
│   │   └── mail.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── tables.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── chamados.css
│   │   │   ├── flash.css
│   │   │   ├── index.css
│   │   │   ├── login.css
│   │   └── files/
│   │       ├── GeoJsonFile/
│   │       │   └── AREA_SIG_10052024_EPSG4326.geojson
│   ├── templates/
│   │   ├── blocked_page.html
│   │   ├── blocked_user.html
│   │   ├── create_dados.html
│   │   ├── create_filtros.html
│   │   ├── dados.html
│   │   ├── filtros.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── perfis.html
│   │   ├── permission.html
│   │   ├── select_dep.html
│   │   ├── user.html
│   │   ├── users.html
│   │   ├── view_dados.html
│   │   ├── view_filtros.html
│   │   ├── view_map_inv.html
│   │   └── view_user_lat.html
│   ├── ultils.py
├── cache/
│   └── cache_db_0.10.db.wal
├── config.py
├── db.sqlite
├── docker-compose.yml
├── Dockerfile
├── install.sh
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── 05884d22f5af_.py
│       ├── 03c8fa745c8f_.py
│       ├── 2b66bbf3ccf6_.py
│       ├── 30374c9cc0a3_.py
│       ├── 482158bff1ad_.py
│       ├── 5f1a2bd186d7_.py
│       ├── 72aaed25d335_.py
│       ├── 725af78da855_.py
│       ├── 73d78a4f6eb2_.py
│       ├── ab10a47afb4e_.py
│       ├── cf21a4f2575c_.py
│       ├── d2e206eff2bb_.py
│       ├── ddbb10bd2547_.py
│       ├── ef14b173511d_.py
│       └── f2d2e9ac397e_.py
├── nginx.conf
├── output/
│   └── db.sqlite
├── pandasai.log
├── requirements.txt
├── run_docker.bat
├── run.py
```

## Installation

### Prerequisites

- Python 3.8.10
- Docker
- Docker Compose

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/projeto001.git
    cd projeto001
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```sh
    flask db upgrade
    ```

4. Run the application:
    ```sh
    python run.py
    ```

5. Alternatively, you can use Docker to build and run the application:
    ```sh
    ./run_docker.bat
    ```

## Configuration

The application configuration is managed through the 

config.py

 file. You can set environment variables for sensitive information such as 

GOOGLE_CLIENT_ID

 and 

GOOGLE_CLIENT_SECRET

.

## Usage

### Authentication

Users can log in using their Google accounts. The authentication flow is handled by the 

auth.py

 module in the 

auth

 directory.

### Data Visualization

The application uses Folium to create interactive maps. The maps are generated based on the filters defined by the users. The 

DatabaseController.py

 and 

FiltroController.py

 modules handle the data fetching and filtering logic.

### Administrative Tasks

Admins can manage users, filters, and data through the web interface. The 

PerfilController.py

 module handles user permissions and roles.

## Caching

The application uses Flask-Caching to cache data and improve performance. The caching configuration is defined in the 

cache.py

 module.

## Deployment

The application can be deployed using Docker. The 

docker-compose.yml

 file defines the services and configurations needed to run the application in a containerized environment.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (

git commit -am 'Add new feature'

).
4. Push to the branch (

git push origin feature-branch

).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or feedback, please contact [yourname@domain.com](mailto:yourname@domain.com).