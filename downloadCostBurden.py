import argparse
import pandas as pd
import json
import requests
import os                       

def createPredicatesCostBurden(county, token):
    '''
    create predicates/headers for the CHAS data API
    county - County id for which we want to download the cost burden
    token - API token to access the CHAS API, CHN needs to register for CHAS API and get this token 
    '''
    predicates = {}
    predicates['type'] = 3
    predicates['stateId'] = 26
    predicates['entityId'] = county
    auth_token_string = "Bearer "+ token
    headers = {"Authorization": auth_token_string}
    return(predicates, headers)

# Download Cost Burden data
def download_dataCostBurden(base_uri, token, path, filename):
    filepath = path + filename
    if os.path.isfile(filepath):
        print(filepath)
        print('file already exists, no need to download')
    else:
        for county in range(1, 166):
          predicates, headers = createPredicatesCostBurden(county, token)
          # print(base_uri, predicates, headers)
          result = requests.get(base_uri, params=predicates, headers=headers) 
          if result.status_code == 200:
            if county !=1:
              cost_burden_df = cost_burden_df.append(pd.DataFrame(json.loads(result.content)))
            else:
              cost_burden_df = pd.DataFrame(json.loads(result.content))
              # print(cost_burden_df)
          else:
            print('API returned Error: ', result.status_code, '\n', 'Downloading of data failed.')
        cost_burden_df.to_csv(path + filename)

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
#     parser.add_argument('BASE_URI', help='base uri of dataset API')
    parser.add_argument('ASSET_PATH', help='input path for datasets')
#     parser.add_argument('TOKEN', help='API token for HUDUSER')
    parser.add_argument('OUTPUT_FILE', help='GrossRent by BedRooms file (json)')
    
    args = parser.parse_args()
    
    COST_BURDEN             = 'costBurden.csv'
    datasets_and_uris = {}
    datasets_and_uris[COST_BURDEN] = 'https://www.huduser.gov/hudapi/public/chas' 
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjliODAyYjM0YWY2ZmJlMGUwYjlmZjZkZTMyNWRhM2M0MjNmNTgzZGFjYjcwM2JkZjdjNzAzMGEyZTIyNDRjODUxODlkZDQzNmMxYTY1MmIxIn0.eyJhdWQiOiI2IiwianRpIjoiOWI4MDJiMzRhZjZmYmUwZTBiOWZmNmRlMzI1ZGEzYzQyM2Y1ODNkYWNiNzAzYmRmN2M3MDMwYTJlMjI0NGM4NTE4OWRkNDM2YzFhNjUyYjEiLCJpYXQiOjE2NDMzMDgwNTIsIm5iZiI6MTY0MzMwODA1MiwiZXhwIjoxOTU4ODQwODUyLCJzdWIiOiIyOTM0MCIsInNjb3BlcyI6W119.IR0_v5Z4OrNawpOC3h-m33f1N_PNvKX539pehlrCLrMlCy3eJ5HDL7ddVCViUPiHe3arVJchTmqa7RO-Fc92-A'
        
    download_dataCostBurden(datasets_and_uris[COST_BURDEN], token, args.ASSET_PATH, args.OUTPUT_FILE)
    cost_burden_df = pd.read_csv(args.ASSET_PATH + args.OUTPUT_FILE)
    cost_burden_df = cost_burden_df.iloc[:, 1:]
    cost_burden_df.to_csv(args.OUTPUT_FILE)
