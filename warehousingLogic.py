from turtle import update
import pymysql
import pandas as pd

def getConnection(user, password, host='localhost', database = 'warehouse'):
    conn = pymysql.connect(host=host,
                        user=user,
                        password=password,
                        database=database
                        )
    
    return conn


def addDeposit(depositDict):
    conn = getConnection(depositDict['user'], depositDict['pwd'])
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

def fetchDeposit(type):
    conn = getConnection('root', 'mysql@123')
    cur = conn.cursor()
    # depositDict = {'depositNumber':2, 'grain': 'wheat', 'bagsQuantity':10, 'pricePerBag': 100, 'partyName':'RajKumar',
    #             'depositDate':'2022-02-02', 'stack': 'A1', 'marketPrice':'12'}
    if(type.lower()=='all'):
        query = 'select * from warehouse.deposits'
    elif(type.lower()=='processed'):
        query = ''' select depositNumber, PartyName, Grain, 
    bagsquantity, priceperbag,depositdate, stack
    from warehouse.deposits where RecieptProcessed=True '''
    elif(type.lower()=='unprocessed'):
        query = ''' select depositNumber, PartyName, Grain, 
    bagsquantity, priceperbag,depositdate, stack
    from warehouse.deposits where RecieptProcessed=False '''
    
    df = pd.read_sql(query, conn)
    html = df.to_html(index=False).replace('<table border="1" class="dataframe">','<table id="tempdt1" class="table table-bordered table-hover table-sm">').replace('<thead>','<thead class="thead-light">').replace('<th>','<th scope="col">').replace('<tr style="text-align: right;">','')
    
    conn.close()
    return html
    
    
def generateReciept(reciepts):
    conn = getConnection(reciepts['user'], reciepts['pwd'])
    cur = conn.cursor()
    # depositDict = {'depositNumber':2, 'grain': 'wheat', 'bagsQuantity':10, 'pricePerBag': 100, 'partyName':'RajKumar',
    #             'depositDate':'2022-02-02', 'stack': 'A1', 'marketPrice':'12'}
    generateRQuery = '''insert into warehouse.reciepts( DepositNumber, PartyNameReciept, RecieptDate, GeneratedBY)
    select
    '{depositNumber}' as DepositNumber,
    '{partyNameReciept}' as PartyNameReciept,
    '{recieptDate}' as RecieptDate,
    session_user() as GeneratedBy
    '''.format(**reciepts)

    cur.execute(generateRQuery)
    conn.commit()
    
    updateDeposit = f'''update warehouse.deposits
                        set RecieptProcessed=True
                        where depositnumber in ({','.join(map(lambda x: x.strip(),reciepts['depositNumber'].split(',')))})'''
                        
    print(updateDeposit)
    cur.execute(updateDeposit)
    conn.commit()
    conn.close()
    
    return 'Reciept Generated Successfully.'
    
    
def getStacksAnalytics():
    conn = getConnection('root', 'mysql@123')
    df = pd.read_sql('select * from warehouse.stacks', conn)
    df['perFilled'] = ((df['UsedCapacity']*100)/df['Capacity']).astype(int)
    rowstart = ' <div class="row"> '
    rowend = ' </div><br> '
    html = ''
    for i, row in df.iterrows():
        i+=1
        col = f'''<div class="col"><div class="circlechart" data-percentage="{row['perFilled']}">{row['StackName']}</div></div>'''
        if(i%5==1):
            html = html+rowstart+'\n'+col
        elif(i%5==0):
            html = html+'\n'+col+'\n'+rowend
        else:
            html = html+'\n'+col
    return html
        
    
