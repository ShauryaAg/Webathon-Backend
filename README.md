# Webathon

### About
It is an API to help conduct online hackathons/team events. It consists of user auth, team forming and project submission.

Users have to register individually, and they have the option to either create a new team or join an existing team.
Joining existing team worked similar to that of devfolio. After creating a new team, a token is generated and other team members can join the team using that token (max 4 members per team).
Each team can submit one projects with project_name, git_link, deployment_link, description, etc.

### Inspiration
The project was initially started a year ago when online hackathons was not a thing, hence it was really difficult to get any sponsorship for any online-only event. So, our only option was to create our own backend for any such thing. 
But ever since the pandemic, online events are the only things we are left with.

### Setup locally
- Clone the repo using `git clone https://github.com/ShauryaAg/Webathon-Backend.git`
- Move into the project folder `cd Webathon-Backend/`
- Create a `.env` file in the project folder
```
DEBUG = True
SECRET_KEY = '<DJANGO_SECRET>'
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@example.com'
EMAIL_HOST_PASSWORD = 'password'
DB_NAME = webathon
DB_USER = postgres
DB_PASSWORD = password
DB_HOST = localhost
DB_PORT = 5432
``` 
- Use `pip install -r requirements.txt` to install all the dependency for the project.
- Migrate the database by `python manage.py migrate`
- Create Super User for the project using `python manage.py createsuperuser`

### Production
- Use `python manage.py collectstatic` to collect all the static files.
- Change the `ALLOWED_HOSTS` in `settings.py`
- Set `DEBUG=False` in `.env` file

### Deploy on Heroku
- Sign up on Heroku, (if you haven't already) 
- Click the "Deploy on Heroku" button below

	[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

> Note: the newly created app has created a super-user with credentials
> Email: admin@example.com
> Password: admin
> 
> You can create a new super-user after logging into the admin panel
> or using the Heroku CLI `heroku run bash -a <your-app-name>` to run bash on the newly created application.
> After this you can create the a new super-user using `python manage.py createsuperuser`

- Name your new application
- Specify the mandatory environment variables `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` to send emails.
- Open the newly created application and go to `/admin` to login.
- Set `DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT` environment variables if you have a custom database.
> Note: If `DB_HOST` environment variable is left empty, then it will use the default database provided by heroku.


## Endpoint Usage
#### User
- `/api/auth/reg/student`
	- _Allowed Methods:_ `POST`
	- _Required Fields:_ `{email, college, password}`
	- _Other Fields:_ `{first_name, last_name, phone_no}`
	- Sends a confirmation email to the registered user

> Note: User needs to confirm their email before logging in 

- `/api/auth/login`
	- _Allowed Methods:_ `POST`
	- _Required Fields:_ `{email, password}`
	- Logs in the registered user

- `/api/auth/student`
	- _Allowed Methods:_ `GET`
	- _Authorization:_ `Token <token>`
	- Fetchs information about currently logged in user
	
- `/api/auth/changepassword`
	- _Allowed Methods:_ `PUT`
	- _Required Fields:_ `{old_password, new_password}`
	- _Authorization:_ `Token <token>`
	- Change the current user's password

- `/api/auth/resetpassword`
	- _Allowed Methods:_ `POST`
	- _Required Fields:_ `{email}`
	- Sends an email with a link to reset the user's password (if registered with that email)

- `/api/auth/reg/org`
	- To register an organizer who can log into Admin Panel
	- _Allowed Methods:_ `POST`
	- _Required Fields:_ `{email, college, password}`
	- _Other Fields:_ `{first_name, last_name, phone_no}`
	- Registered organizer can log into the backend directly

#### Team
- `/api/auth/reg/team`
	-	_Allowed Methods:_ `POST`
	- _Required Fields:_ `{team_name, idea}`
	- _Authorization:_ `Token <token>`
	- Creates a new team and adds the current user a member of the team

- `/api/auth/add/student`
	-	_Allowed Methods:_ `POST`
	- _Required Fields:_ `{team_token}`
	- _Authorization:_ `Token <token>`
	- Adds the current user a member of the team

- `/api/auth/student/team`
	- _Allowed Methods:_ `GET`
	- _Authorization:_ `Token <token>`
	- Fetchs currently logged in user's team details

- `/api/team`
	- _Allowed Methods:_ `GET`
	- Fetches all the registered teams

- `/api/team/{id}`
	- _Allowed Methods:_ `GET`
	- Fetches team with the given `id`
 
#### Projects
- `/api/auth/project`
	- _Allowed Methods:_ `GET, POST`
	- _Authorization:_ `Token <token>`
	- _Required Fields:_ `{project_name, git_url}`
	- _Other Fields:_ `{deploy_link, description}`
	- Adds a project to the current user's team

- `/api/auth/project/{id}`
	- _Allowed Methods:_ `GET, PUT, PATCH, DELETE`
	- _Authorization:_ `Token <token>`
	- _Required Fields:_ `{project_name, git_url}`
	- _Other Fields:_ `{deploy_link, description}`
	- Alter's the project with given `id`

#### Documentation
- `/swagger` or `/redoc`
	- Hit these endpoints for more detailed documentation

