import configs.module
import requests
import json

def init():
    m = configs.module.Module(__name__)
    m.set_help('Get media recommendations from TasteKid (tastekid.com)')
    m.add_command_hook('suggest',
        {
            'help': 'A command to get recommendations from tastekid.com',
            'function': suggest,
            'args': [
                {
                    'name': 'arg1',
                    'help': 'Things you like',
                    'optional': False,
                    'end': True,
                    },
                {
                    'name': 'results',
                    'help': 'Number of Results',
                    'optional':True,
                    'keyvalue':'number',
                    }
                ]
            }
        )
    return m
def suggest(fp, args):
    if fp.ltnserver():
        break
    params = {'q':,'limit':5,}
    if 'results' in args.lin:
        params['limit'] = args.getlinstr('results')
    suggestions = requests.get('http://www.tastekid.com/api/similar', params)
    suggestions = json.loads(suggestions.read().decode())["Similar"]
    if suggestions['Results'] == []:
        fp.replypriv('No results available; Please check your spelling')
        break
    likedmedia = {
        'book':[],
        'game':[],
        'music':[],
        'author':[],
        'movie':[],
        }
    for i in suggestions['Info']:
        likedmedia[i['Type']].append(i['Name'])
    returnstring = "Because you liked the '
    for category in likedmedia:
        if not likedmedia[category] == []:
            if category == 'music':
                returnstring += 'music of ' + likedmedia['music'][1:-1].replace("'","") + ','
            else:
                returnstring += likedmedia[category] + 's ' +  likedmedia[category][1:-1].replace("'","") + ','
    else:
        returnstring += ' TasteKid suggests '
    for i in suggestions['Results']:
        returnstring += i['Name'] + ','
    fp.replypriv(returnstring)
        
    
                
    
    