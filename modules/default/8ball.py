# -*- coding: utf-8 -*-
import configs.module
import random


def init():
    m = configs.module.Module(__name__)
    m.set_help('A Magic 8-ball.')
    m.add_short_command_hook(ball,
        '8ball::Ask the Magic 8-ball a yes/no question.',
        ['question...::Question to ask the Magic 8-ball'],
        )
    m.add_command_alias('8', '8ball')
    return m


def ball(fp, args):
    answers = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful",
        ]
    if not args.getlinstr("question", ""):
        return "You must ask something."
    return random.choice(answers) + '.'