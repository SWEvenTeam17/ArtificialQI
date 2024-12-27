### Server
You want the server to run in a python virtual environment.  
To create one, run this command in your folder of choice:
```
python -m venv <directory>
```
Then, to activate it:
```
\\ Windows cmd:
<directory>\Scripts\activate.bat

\\ Windows PowerShell:
<directory>\Scripts\Activate.ps1

\\ Linux/MacOS
source <directory>/bin/activate
```
While inside the venv, navigate to the `server/ArtificialQI` folder and migrate
Django models to the database (both if it's your first time running it and whenever models are changed).
```
python manage.py migrate
```
Finally, you can run the server (in the same folder):
```
python manage.py runserver
```

### Client
To run the client locally, you're required to have [node.js](https://nodejs.org/en) and npm installed. After that, navigate to the `client/frontend` folder and run the following commands to install next.js:
```
npm install
npm update
```
Finally, run the server:
```
npm run dev
```