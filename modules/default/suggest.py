import configs.module
import requests
from urllib.parse import quote_plus

def init():
    m = configs.module.Module(__name__)
    m.set_help('Get media recommendations from TasteKid (tastekid.com)')
    m.add_command_hook('suggest',
        {
            'help': 'A command to get recommendations from tastekid.com',
            'function': suggest,
            'args': [
                {
                    'name': 'results',
                    'help': 'Number of Results',
                    'optional':True,
                    'keyvalue':'number',
                    },
                {
                    'name': 'things you like',
                    'help': 'Things you like',
                    'optional': False,
                    'end': True,
                    },
                ]
            }
        )
    return m


def suggest(fp, args):
    if fp.ltnserver():
        return "You cannot use this module from a server."
    params = {'q': args.getlinstr('things you like'), 'limit': 5, 'k':"129654-Fourthev-A789FB9C"}
    if 'results' in args.lin:
        params['limit'] = args.getlinstr('results')
    suggestions = requests.get('http://www.tastekid.com/api/similar',
        params=params)
    print (suggestions.url)
    suggestions = suggestions.json()["Similar"]
    if suggestions['Results'] == []:
        fp.replypriv('No results available; Please check your spelling')
        return
    likedmedia = {
        'book': [],
        'game': [],
        'music': [],
        'author': [],
        'movie': [],
        }
    for i in suggestions['Info']:
        likedmedia[i['Type']].append(i['Name'])
    returnstring = "Because you liked the "
    for category in likedmedia:
        if not likedmedia[category] == []:
            if category == 'music':
                returnstring += 'music of ' + likedmedia[
                    'music'][1:-1].replace("'", "") + ','
            else:
                returnstring += category + 's ' + str(likedmedia[
                        category])[1:-1].replace("'", "") + ','
    else:
        returnstring += ' TasteKid suggests '
    for i in suggestions['Results']:
        returnstring += i['Name'] + ','
    fp.replypriv(returnstring)




