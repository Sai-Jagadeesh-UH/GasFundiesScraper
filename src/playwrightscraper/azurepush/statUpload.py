import pandas as pd
from datetime import datetime


# Create an empty DataFrame with the defined schema
df_empty = pd.DataFrame(columns=['Rundate', 'ScrapeType', 'Pipeline',
                        'Cycle', 'TargetDate',  'StartTime', 'EndTime', 'status', 'Arguments'])


def pullStatFile():
    pass


def UpdateScrapeStart(**configs):

    item = {}
    if (hasattr(configs, "ScrapeType")):
        item['ScrapeType'] = configs.ScrapeType

    if (hasattr(configs, "pipeLine")):
        item['Pipeline'] = configs.pipeLine

    if (hasattr(configs, "cycleSelector")):
        item['Cycle'] = configs.cycleSelector

    if (hasattr(configs, "cycleSelector")):
        item['Cycle'] = configs.cycleSelector

    item['Rundate'] = datetime.today().strftime(r'%m%d%Y')
