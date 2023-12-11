"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from external data csv to RDS PostgreSQL
"""

from application import(
    ReadData
)

if __name__ == '__main__':
    read_data = ReadData()
    read_data.insert()