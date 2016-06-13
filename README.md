
## Notes Application

### Prerequisities:

Installation of *virtualenv* utility.
- Run `virtualenv --version` to check if this utility is installed.
- Install *virtualenv* using *easy_install*: `sudo easy_install virtualenv` (Mac OS X)

### Installation:

1. Run `virtualenv venv' to create the virtual environment.
2. Run `source venv/bin/activate` to activate the virtual environment
3. Run `pip install -r requirements.txt` to install dependencies with pip

### Running the application:

The project uses a launch script called `manage.py`.

- Run the application: `python manage.py runserver`
- Run unit tests: `python manage.py test`
- Run shell commands: 'python manage.py shell'
- Run db migration commands: 'python manage.py db'

### Database Migrations:

- To create a migration script: 'python manage.py db migrate'
- To apply the script to the database: 'python manage.py db upgrade'
