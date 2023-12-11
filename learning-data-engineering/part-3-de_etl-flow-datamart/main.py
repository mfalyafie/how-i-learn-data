"""
    author: m.fauzanalyafie@gmail.com
    project: ETL core from MongoDB AWS to RDS PostgreSQL
"""

from application import (
    ReadData
)

if __name__ == '__main__':
    read_data = ReadData()
    read_data.insert()