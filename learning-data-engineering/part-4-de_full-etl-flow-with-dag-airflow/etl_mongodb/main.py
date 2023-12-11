"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from MongoDB AWS to RDS PostgreSQL
"""

from application import(
    ReadMongo
)

if __name__ == '__main__':
    insert_data = ReadMongo()
    insert_data.insert()