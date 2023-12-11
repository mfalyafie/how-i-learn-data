"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from s3 to RDS PostgreSQL
"""

from application import(
    MoveData
)

if __name__ == '__main__':
    move_data = MoveData()
    move_data.tosql()