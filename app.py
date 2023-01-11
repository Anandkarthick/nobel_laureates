import pandas as pd
from dbutils import NobelDB
from nobel import NobelData

nobel_data_struct = NobelData()

def get_laureates(year_from, year_to, limit, offset):
    nobel_data = []
    counter = 0
    while True:
        print(counter)
        api_response = nobel_data_struct.get_data(year_from, year_to, limit, offset)
        nobel_data.extend(api_response.get("nobelPrizes"))
        counter += 1
        # check if next is present
        if "next" in api_response.get("links"):
            print(year_from, year_to, limit, offset)
            offset = limit if offset=='' else offset+limit
            continue
        else:
            break
        
    return nobel_data


def fetch_prepare(api_data):

    api_data_df = pd.json_normalize(api_data, 
                                record_path=['laureates'],
                                meta=['awardYear', 'dateAwarded', 'prizeAmount', 'prizeAmountAdjusted',
                                    ['category', 'en'], ['category', 'se'],
                                    ['categoryFullName', 'en']], errors='ignore',
                                sep='_')

    api_data_df = api_data_df.fillna('')

    for index_value in api_data_df.index[api_data_df['orgName_no'] != ''].tolist():
        api_data_df.loc[index_value, "fullName_en"] = api_data_df.loc[index_value, "orgName_no"]

    for index_value in api_data_df.index[api_data_df['orgName_en'] != ''].tolist():
        api_data_df.loc[index_value, "fullName_en"] = api_data_df.loc[index_value, "orgName_en"]

    final_columns = ['id', 'portion', 'knownName_en', 'fullName_en', 'motivation_en', 'awardYear',
                        'dateAwarded', 'prizeAmount','prizeAmountAdjusted','category_en', 
                        'category_se', 'categoryFullName_en']

    api_data_df = api_data_df[final_columns]

    return api_data_df


# load data

db_access = NobelDB()

def load_api_data(api_data_df):
    # mandatory delete before load
    db_access.run_query('''delete from nobel_laureates''')
    # load records
    for v in api_data_df.values.tolist():
        db_access.insert_table(tuple(v))

def get_table_count():
    return  db_access.run_select_fetch_all('''select count(*) from nobel_laureates''')

def avg_query():
    return '''with avg_prize_data as (select category_en,
                                round(avg(prize_amount_adjusted)) as avg_prize
                                from nobel_laureates 
                                group by category_en)
                            
                                select  
                                    nl.full_name_en as "name",
                                    nl.category_en as "Category",
                                    case 
                                       when nl.prize_amount_adjusted*1.0 < pd.avg_prize then "Lower"
                                       when nl.prize_amount_adjusted*1.0 == pd.avg_prize then "Equal"
                                       when nl.prize_amount_adjusted*1.0 > pd.avg_prize then "Higher"
                                    End as Prize_Classification
                                from nobel_laureates nl
                                left join avg_prize_data pd on 
                                nl.category_en = pd.category_en
                                '''

def run_avg_query():
    return db_access.run_select_fetch_all(avg_query())

def query_to_csv():
    conn = db_access.create_conn()
    avg_data_df = pd.read_sql_query(avg_query(), conn)
    avg_data_df.to_csv("prize_classfication.csv", header=True, index=False)
    conn.close()

if __name__ == "__main__":
    # main starts here
    api_data = get_laureates(1990, 2000, 25, '')

    # prepare data for loading
    load_ready_df = fetch_prepare(api_data)

    # load data into db
    load_api_data(load_ready_df)

    # get table count
    print("Printing table count")
    print(get_table_count())

    # run avg query and save the output to csv
    print("Saving average prize classification data to csv")
    query_to_csv()
   