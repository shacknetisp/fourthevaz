#The file type will read from a file, line-by-line,
##and print the output to stdout
#It is a very basic server template.
#See the 'file' folder for the implementation
#You may run into exceptions when making your own types or using this,
##you will need to add your type to the module.
[
    {
        'type': 'file',
        'settings': 'filetest',
        'apiport': 5719,
        'file': 'userdata/file',
        'modulesets': ['default'],
    }
]