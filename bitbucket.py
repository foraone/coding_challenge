import requests

url = 'https://bitbucket.org/api/2.0/repositories/mailchimp'

def readUrl(url, data=[]):
    print(data)
    r = requests.get(url)
    subdata = r.json()
    
    data = data + subdata['values']
    print(data)
    if 'next' in subdata.keys():
        return readUrl(subdata['next'], data)
    else:
        return data

# data = readUrl(url, [])

# print(len(data))