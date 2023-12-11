"""
    author: m.fauzanalyafie@gmail.com
    project: ETL core from MongoDB AWS to RDS PostgreSQL
"""

from application import (
    SelectData
)

if __name__ == '__main__':
    #read_data = ReadData()
    #read_data.insert()
    select_data = SelectData(
        '''
        select
            *
        from
            revenue r
        inner join
            trx t
                on
            r.advertiser_id = t.advertiser
        '''
    )
    select_data.read()