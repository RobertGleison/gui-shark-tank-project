# Resume

Python application designed to interact with the database file created for a university project. The base code was originally developed by [Eduardo R. B. Marques](https://www.dcc.fc.up.pt/~edrdo/), DCC/FCUP. We modified it for our project, introducing new endpoints and interactions. The project was created in collaboration with Joana Carvalho Dias Pinto and Mariana dos Santos Gomes.

# References

- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Jinja templates](https://jinja.palletsprojects.com/en/3.0.x/)

# Dependencies

## Python 3 and pip 

Ensure you have Python 3 and the package manager pip installed. Then, install the Flask library. If you are using Ubuntu, follow these steps:

```
sudo apt-get install python3 python3-pip
```

## Flask

```
pip3 install --user Flask 
```

# Execution

Starts the application executing `python3 server.py` and
open a browser page with the address [__http://localhost:9001/__](http://localhost:9001/) 

```
$ python3 server.py
2021-11-27 15:07:33 - INFO - Connected to database movie_stream
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2021-11-27 15:07:33 - INFO -  * Running on http://0.0.0.0:9001/ (Press CTRL+C to quit)
...
```


