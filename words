#!/usr/bin/env python3

import urllib.request, urllib.parse, json, sys

#http://www.datamuse.com/api/


version_id = '0.0.1'
divider = '************************************************************************************'
spacer = '*'


def define_req(data_dict):
    if len(data_dict['wordlist']) > 0:
        word = data_dict['wordlist'][0]
        params = '?' + 'sp=' + word + '&md=d'
        call = call_api(params)
        response = []

        response.extend([divider,spacer])
        response.append('* ' + word + ' is defined as:')
        response.extend([spacer,divider,spacer,spacer])
        if call:
            for index, item in enumerate(call[0]['defs']):
                response.append('* ' + str(index + 1) + '. ' + item[2:])
            response.extend([spacer,spacer,divider])
            return response
        else:
            response.append('* There were no matches for your query')
            response.extend([spacer,spacer,divider,'\n\n'])
            return response
    return ['INPUT ERROR: Define must include a word to look up\n* See: words --help']


def lookup_req(data_dict):
    valid_options = {'means':'ml','max':'max','spelled':'sp','sounds':'sl','topics':'topics'}
    params = '?'
    max_declared = False
    for item in data_dict['options']:
        params += valid_options[item[0]]
        params += '=' + item[1] + '&'
        if item[0] == 'max':
            max = True
    if not max_declared:
        params += 'max=10&'
    call = call_api(params[:-1])

    response = []
    response.extend(['\n\n',divider,spacer])
    response.append('* The following words match yout query:')
    response.extend([spacer,divider,spacer,spacer])
    if call:
        for index, item in enumerate(call):
            response.append('* ' + str(index + 1) + '. ' + item['word'])
        response.extend([spacer,spacer,divider,'\n\n'])
        return response
    response.append('* There were no matches for your query')
    response.extend([spacer,spacer,divider,'\n\n'])
    return response


def call_api(query_string):
    dmapi = 'http://api.datamuse.com/words'
    url = dmapi + query_string
    req = urllib.request.Request(url,method='GET')

    with urllib.request.urlopen(req, timeout=5) as res:
        value = res.read().decode('ASCII')
        value = json.loads(str(value))
        return value or False

def validate_operation(op):
    if op in valid_args:
        return False
    return True


def display_help():
    print('''
        words:
        a utility for retrieving word information from the datamuse api

        usage:
        words define [ word ]
        words lookup [ ... options ... ]

        examples:
        words lookup --max="10" --spelled="*ding" --means="joining merging tying"
        words lookup --topics="weather clouds" --sounds="rimbus"
        words define celebratory
        words define redolent


        operators:

        lookup              initiate a lookup

        define              get a word definition

        help, -h, --help    display this help information

        version, -v,        display the current words version id
        --version



        options:
            these take the form of quoted integers or space delimited strings:


        --max=" ... "       [int]:    number of results to return (default: 10).
                                      can only be used in combination with other
                                      options

        --spelled=" ... "   [string]: require that results be spelled like this string
                                      accepts '*' as a multi-character wildcard & '?'
                                      as single character wildcard -single word

        --means=" ... "     [string]: require that the results have a meaning
                                      related to this string value -space delimited

        --sounds=" ... "    [string]: require that the results are pronounced similarly
                                      to this string of characters -single word

        --topics=" ... "    [string]: results will be skewed toward these topics
                                      space delimited
    ''')

def display_version(id):
    print('Words, Version: ' + id)


def parse_args():
    args = sys.argv[1:]
    query = {}
    if len(args) < 1:
        print('\nInput Error: At least one operator must be provided\nSee: words --help\n')
        return False

    query['operation'] = args.pop(0)
    if query['operation'] in ['help','-h','--help']:
        display_help()
        return False
    elif query['operation'] in ['version','-v','--version']:
        display_version(version_id)
        return False
    elif query['operation'] in ['lookup','define']:
        query['wordlist'] = []
        query['options'] = []
        for val in args:
            if val[0:2] == '--':
                op_list = val.split('=')
                op_list[0] = op_list[0][2:]
                op_list[1] = op_list[1].replace(' ','+')
                query['options'].append(op_list)
            else:
                query['wordlist'].append(val)
        return query
    else:
        print('\nInput error: Invalid operator or syntax.\nSee: words --help\n')
        return False


if __name__ == '__main__':
    instructions = parse_args()
    if instructions:
        if instructions['operation'] == 'define':
            response = define_req(instructions)
        elif instructions['operation'] == 'lookup':
            response = lookup_req(instructions)
        else:
            response = '\nInput error: Unknown operator ' + instructions['operation'] + '\n'
        for item in response:
            print(item)
