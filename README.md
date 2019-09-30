# ocr2tei

## Installation (Linux)

### Docker 

Make sure that you have Docker and docker-compose installed on your system

On Arch based systems this can be achieved by:
```
sudo pacman -S docker docker-compose
```

#####  Building the image and starting the container

Run the following command in the directory containing the Dockerfile and docker-compose.yaml
```
docker-compose up
```

The service should now be reachable under localhost:8000

If you run into any errors, run the following command while the container is still running and then restart the container
```
docker-compose run web python manage.py makemigrations todo
```

### Native Django

#### Setup PostgreSQL Database

* Install PostgreSQL on your system
* Initialize a database with the credentials from the file *ocr2tei/ocr2tei/settings.py*

```
sudo su - postgres
# psql
```
Within psql execute the following commands:

```postgresql
CREATE USER [USER NAME]
CREATE DATABASE [DB NAME]
GRANT ALL PRIVILEGES ON DATABASE [DB NAME] TO [DB USER]
```

#### Install a virtual environment

```
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

##### Start Django

*optional*
```
python manage.py migrate
```

__required__
```
python manage.py runserver
```

The service should now be reachable under localhost:8000

# Usage

To use all features of the webapp it's required to create a user and be logged in.

It's possible to create an account within the web interface. This account doesn't possess admin privileges but 
in the current version there aren't any rights restriction for a non-admin account.

To create a superuser/admin account run the following command(s):

##### Docker
The containers have to be up and running for this to work.
```
docker exec -it <dockercontainerid> python manage.py createsuperuser
```

##### Django
```
python manage.py createsuperuser
```

## Adding new projects

In the current version the user isn't able to directly upload new projects through the web interface.

New projects have to be manually added in the /media/projects folder!

The project directories must have the following structure:

```
.
├── ...
├── <Project Name>
|   ├── output
|   ├── input
|       ├── 0001.xml
|       ├── 0001.png
|       ├── 0002.xml
|       ├── 0003.xml
|       └── ... 
└── ...
```
