# -*- coding: utf-8 -*-
import configs.module


#This function returns the module data.
#You can also use init(server),
#this will pass the server when the module registers.
def init():
    #Create the class, the argument is the name of the module.
    m = configs.module.Module(__name__)
    #This function sets the module help, returned by modhelp
    m.set_help('An example module.')

    ###

    #Modules interact with the rest of the bot by means of hooks
    #There are several kinds of hooks

    ##

    #Base hooks are called on server events
    #This hook is called upon any IRC message
    m.add_base_hook('recv', recv)
    #This hook is called upon the end of the MOTD
    m.add_base_hook('joined', joined)

    ##

    #Timed hooks are called on a timer
    #The timer is not exact
    m.add_timer_hook(10 * 1000, tensecondtimer)

    ##

    #Command hooks are processed by the commands module
    #They define regular commands such as echo or google
    #This is the short definition:
    m.add_short_command_hook(
        #Function
        example,
        #Command Name::Help text
        'exampleshort::An example command, echoes text.',
        #Arguments (see below for more information)
        ['-kv1=string',
            'arg1',
            '[arg2...]'],
        #Level, optional
        0)
    #This is the long definition:
    m.add_command_hook('examplelong',
        {
            #Help text to be displayed with help
            'help': 'An example command, echoes text.',
            #Required access level, if ommitted defaults to 0
            'level': 0,
            #Function to call
            'function': example,
            #Argument definitions
            'args': [
                {
                    #Name of the argument
                    'name': 'kv1',
                    #Help text
                    'help': 'Display this.',
                    #Optional?
                    'optional': False,
                    #Keyvalue (-kv1=<keyvalue>),
                    #if it is '' then it's just a flag, otherwise it's a value
                    'keyvalue': 'string',
                    },
                {
                    #Name of the argument
                    'name': 'arg1',
                    #Help text
                    'help': 'Echo this.',
                    #Optional?
                    'optional': False,
                    },
                {
                    #Name of the argument
                    'name': 'arg2',
                    #Help text
                    'help': 'Echo this if it exists.',
                    #Optional?
                    'optional': True,
                    #If end is True, then anything after the last non-end
                    #will be put into this
                    'end': True,
                    }
                ]
            }
        )
    return m


def recv(fp):
    #The recv base hook is passed a fullparse object
    #A fullparse object contains a splitparse object and a server reference
    print(('Received: ' + fp.sp.message))


def joined(server):
    #The joined base hook is passed a server object
    print('Ready!')


def tensecondtimer():
    print('Ten seconds have passed.')


def example(fp, args):
    #Return a message with arg1 (no default) and arg2 (default '')
    #Prefix of kv1 (default '')
    kv1 = args.getlinstr('kv1', '')
    return kv1 + ': ' + args.getlinstr(
        'arg1') + ' -- ' + args.getlinstr('arg2', '')