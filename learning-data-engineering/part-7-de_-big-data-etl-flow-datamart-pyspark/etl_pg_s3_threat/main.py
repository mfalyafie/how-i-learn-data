"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from s3 to RDS PostgreSQL
"""

from application import(
    SQL
)

if __name__ == '__main__':
    sql_data = SQL()
    sql_data.query()