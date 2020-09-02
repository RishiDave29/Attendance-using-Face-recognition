from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

SERVER = 'DESKTOP-953RKA7'
DATABASE = 'AI'
DRIVER = 'SQL Server Native Client 11.0'
USERNAME = 'sa'
PASSWORD = 'Smart@123'
DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

engine = create_engine(DATABASE_CONNECTION)
connection =engine.connect()

stmt = 'select * from Users'
result = connection.execute(stmt)
r = result.fetchall()
print(r)




