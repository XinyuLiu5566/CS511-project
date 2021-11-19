# CS511-Project
## Project setup instruction
To run the application:
1. first clone the Github Repository using\
```git clone https://github.com/XinyuLiu5566/CS511-project.git ```
2. Install the project dependencies:
```pip install -r requirements.txt```
3. Set up the local Neo4j and MySQL server.
4. Then run the server using ```python manage.py runserver``` (sometimes ```python manage.py migrate``` and ```python manage.py makemigrations``` needed to propagate changes you make to your models)