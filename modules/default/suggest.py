import configs.module
import requests
import utils


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
    m.add_command_hook('setsuggestkey',
        {
            'help': 'Set the API Key for suggest.',
            'function': setkey,
            'args': [
                {
                    'name': 'key',
                    'help': 'API key',
                    'optional': True,
                    },
                ]
            }
        )
    return m


def setkey(fp, args):
    fp.server.db['suggest.apikey'] = args.getlinstr('key', '')
    return 'The key has been set to "%s"' % fp.server.db['suggest.apikey']


def suggest(fp, args):
    params = {'q': args.getlinstr('things you like'),
        'limit': 5, 'k':
            fp.server.db['suggest.apikey']
            if 'suggest.apikey' in fp.server.db else ''}
    if 'results' in args.lin:
        params['limit'] = args.getlinstr('results')
    if fp.ltnserver() and params['limit'] > 10:
        return "You cannot use this module from a server."
    suggestions = requests.get('http://www.tastekid.com/api/similar',
        params=params)
    suggestions = suggestions.json()["Similar"]
    if suggestions['Results'] == []:
        if params['limit'] <= 10:
            return fp.replypriv(
                'No results available; Please check your spelling')
        fp.replypriv('No results available; Please check your spelling')
        return
    likedmedia = {}
    for i in suggestions['Info']:
        if i['Type'] not in likedmedia:
            likedmedia[i['Type']] = []
        likedmedia[i['Type']].append(i['Name'])
    returnstring = "Recommendations from "
    for category in likedmedia:
        if not likedmedia[category] == []:
            returnstring += category + 's: ' + str(likedmedia[
                    category])[1:-1].replace("'", "") + ', '
        returnstring = returnstring.strip(', ') + '; '
    returnstring = returnstring.strip(',; ')
    returnstring += ' -- '
    returnlist = []
    for i in suggestions['Results']:
        returnlist.append(i['Name'])
    returnstring += utils.ltos(returnlist)
    if params['limit'] <= 10:
        return returnstring
    fp.replypriv(returnstring)




