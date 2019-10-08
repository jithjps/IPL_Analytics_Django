# IPL_Analytics_Django
Analytics of IPL match data using python and django
The project Runs on django and PostgresSQL server.

1. DB Setup
Database shiuld be postgreSQL >9.5
DB details can be changed as per settings.py or update those params based on your DB
Sample DB settings
--------------------
DB name : IPL_DB
username: postgres
passowrd: root


2. Install the required packages using 
   >> pip install -r requirements.txt
   
3. DB schema creation
   Once above steps are done   
   Do django migrations by running below commands inside project directory
     >> python manage.py makemigrations
     >> python manage.py migrate

4. Populate DB
   Run below commnds to populate DB schema
      >> python manage.py upload matches
      >> python manage.py upload_deliveries

   CSV files are located in media/CSVdata folder. Make sure you have enough rights to read the files from the location
   NOTE:
        - Run the commnds in the same order as mentioned
        -  Incase of any issues while running check the result and try again after fixing the problems.
           But before that create a fresh DB to avoid confusions

5. Run server
   >> python manage.py runserver



