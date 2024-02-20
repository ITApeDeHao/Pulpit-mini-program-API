# Pulpit-mini-program-API

## Introduce

This procedure is implemented using mini-condo, django3, mysql, Redis.

## Set up

In your terminal, use the conda command to create a python virtual environment.

~~~bash
conda env create mini-api
~~~

Activate the environment in the current directory

~~~bash
conda activate mini-api
~~~

Once the environment is activated, download third-party libraries using the pip command:

~~~bash
pip install -r requirements.txt
~~~

## Adaptive

In order to use this program, you will now need to change the Redis address and password in CACHES and the mysql address and password in DATABASES in setting.py

![image-20240220174750737](https://www.kedaya.love/pic/202402201747812.png)

![image-20240220174848222](https://www.kedaya.love/pic/202402201748242.png)

Use the command in the terminal to import the database information into your local database

~~~bash
python manage.py makemigrations && python manage.py migrate
~~~

All you need to do is launch the program

~~~bash
python manage.py runserver 0.0.0.0:8080
~~~

## Interface

Interface List [Reference](https://github.com/ITApeDeHao/Pulpit-mini-program-API/blob/main/Interface-List.md)