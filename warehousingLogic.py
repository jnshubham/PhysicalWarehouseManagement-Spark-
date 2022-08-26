import pymysql
import pandas as pd

def addDeposit(depositDict):
    conn=pymysql.connect(host='localhost',
                        user=depositDict['user'],
                        password=depositDict['pwd'],
                        database='warehouse'
                        )

    cur = conn.cursor()
    # depositDict = {'depositNumber':2, 'grain': 'wheat', 'bagsQuantity':10, 'pricePerBag': 100, 'partyName':'RajKumar',
    #             'depositDate':'2022-02-02', 'stack': 'A1', 'marketPrice':'12'}
    insertDeposit = '''insert into warehouse.deposits(Grain,BagsQuantity, PricePerBag, PartyName, DepositDate, Stack, MarketPrice, RecieptProcessed, CreatedBy)
    select
    '{grain}' as Grain,
    {bagsQuantity} as BagsQuantity,
    {pricePerBag} as PricePerBag,
    '{partyName}' as PartyName,
    '{depositDate}' as DepositDate,
    '{stack}' as Stack,
    {marketPrice} as MarketPrice,
    False as RecieptProcessed,
    session_user() as CreatedBy
    '''.format(**depositDict)

    cur.execute(insertDeposit)
    conn.commit()
    conn.close()
    
    return 'Successfully added new deposit'

def fetchUnprocessedDeposit(type):
    conn=pymysql.connect(host='localhost',
                        user='root',
                        password='mysql@123',
                        database='warehouse'
                        )

    cur = conn.cursor()
    # depositDict = {'depositNumber':2, 'grain': 'wheat', 'bagsQuantity':10, 'pricePerBag': 100, 'partyName':'RajKumar',
    #             'depositDate':'2022-02-02', 'stack': 'A1', 'marketPrice':'12'}
    df = pd.read_sql('select depositNumber, PartyName, Grain, bagsquantity, priceperbag,depositdate, stack from warehouse.deposits where RecieptProcessed=False', conn)
    html = df.to_html(index=False).replace('<table border="1" class="dataframe">','<table id="tempdt1" class="table table-bordered table-hover table-sm">').replace('<thead>','<thead class="thead-light">').replace('<th>','<th scope="col">').replace('<tr style="text-align: right;">','')
    
    conn.close()
    return html
    
    

#fetchDeposit('a')