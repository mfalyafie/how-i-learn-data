"""
    author: m.fauzanalyafie@gmail.com
    project: ETL from pg to datamart
"""

from application import(
    Disburse
)

if __name__ == '__main__':
    read_data = Disburse()
    read_data.datamart()