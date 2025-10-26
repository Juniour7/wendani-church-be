Steps to deploying on pythonanywhere

1. Create a free account
2. Open the bash console
3. git clone your project from github
4. create a virtual environment ()
5. Install dependencies from requirements.txt ( make sure mysqlclient is one for them if youll be using the mysql db)
6. Cd into your project and run migrations
7. collect static files (make sure to set up the urls for media and static files in the web tab first)
8. edit the wsgi file manually, delete everything apart from the django related code, andchange the url to point to your project folder
9. 