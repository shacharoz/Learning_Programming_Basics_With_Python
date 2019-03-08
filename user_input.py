import json

import datetime



def load_json_from_server(url):
    print('trying to get the file from url: ' + url)

    test_list = {}
    'test_list = json.dumps(url)'
    return test_list


our_data_file = load_json_from_server('')




d = {
    'vacation': [
        {'date' : '22-02-2019 17:15'}
    ]
}


''' database= 'bring the file '''
''' in the loop '''
''' update the database '''
''' send the database to server '''

while (True):

    user_input = input('come voglio adesso?')



    if d.get(user_input):
        d[user_input].append({'date', str(datetime.datetime.utcnow())})
    else:
        d[user_input] = [{'date', str(datetime.datetime.utcnow())}]



    print (d)














''' simple function with numeric variable '''
drive (10)


''' using input from the user '''
'''
user_speed = input('How fast do you want to drive?')

drive (user_speed)
'''

