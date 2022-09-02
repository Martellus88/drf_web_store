# DRF web_store

Web store written in DRF with the option to pay with bitcoin.

## Application launch order

    --- Initialization ---
    
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd web_store
    python manage.py migrate
    
    --- Starting celery and redis --- 

    docker run -d -p 6379:6379 redis
    celery -A web_store worker -l info
    
    --- Run server ---
    
    python manage.py runserver

## Some settings:

* Set your environment variables in the **.env** file
* To send mail to the console, set in the **settings**: EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
* By default, the **Testnet** is used for bitcoin payments. To replace, change the **TYPE_WALLET** settings to **Key**

## Running with docker (django, gunicorn, nginx, celery, redis):

    --- Environment variables ---    

    Change the DOCKER variable in the .env file to True
    Set your database settings in the .env.db
    
    --- Create and run container --    

    docker-compose build
    docker-compose up -d
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py collectstatic
    
    --- Create superuser ---

    docker-compose exec -it web python manage.py createsuperuser

    --------------------------------------------------------------
    The application is running on port 80


