
## Notes Application

### Prerequisities:

Installation of *virtualenv* utility.
- Run `virtualenv --version` to check if this utility is installed
- Install *virtualenv* using *easy_install*: `sudo easy_install virtualenv` (Mac OS X)

### Installation:

1. Run `virtualenv venv` to create the virtual environment
2. Run `source venv/bin/activate` to activate the virtual environment
3. Run `pip install -r requirements.txt` to install dependencies with pip
4. Run `python manage.py db migrate` to create a migration script for your database
5. Run `python manage.py db upgrade` to apply the script to your database

### Running the application:

The project uses a launch script called `manage.py`, when returning to the project you will need to restart your virtual environment.

- Run `source venv/bin/activate` to reactivate the virtual environment
- Run the application: `python manage.py runserver`
- Run unit tests: `python manage.py test`

To deactivate the *virtualenv*, run `deactivate`.
