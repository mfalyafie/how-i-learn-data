"""
    author: m.fauzanalyafie@gmail.com
    project: ETL core from MongoDB AWS to RDS PostgreSQL
"""

from application import (
    ReadData, ShowData
)

if __name__ == '__main__':
    run_data = ReadData()
    run_data.insert()
    show_data = ShowData(
        '''
        select
            count(*)
        from
            tablefromairbnb
        '''
    )
    show_data.read()