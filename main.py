import urllib.request, urllib.parse
import json
import sys

#http://www.datamuse.com/api/


version_id = '0.0.1'


def define_req(data_dict):
    if len(data_dict['wordlist']) > 0:
        word = data_dict['wordlist'][0]
        params = '?' + 'sp=' + word + '&md=d'
        call = call_api(params)
        response = []
        response.append('\n *----------------------* \n')
        response.append(word + ' is defined as:\n')
        for index, item in enumerate(call[0]['defs']):
            response.append(str(index + 1) + '. ' + item[2:])
        response.append('\n *----------------------* \n')
        return response
    return False

def lookup_req(data_dict):
    valid_options = ['ml','max','sp','sl','topics']
    pass

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
        words [operator] [options...] [query...]

        examples:
        words --max="10" --sp="*ding" --ml="joining merging tying"
        words --topics="weather clouds" --sl="rimbus"


        operators:

        lookup              initiate a lookup

        define              get a word definition

        help, -h, --help    display this help information

        version, -v,        display the current words version id
        --version



        options:
            these take the form of quoted integers or space delimited strings:


        --max=" ... "       [int]:    number of results to return (default: 100).
                                      can only be used in combination with other
                                      options

        --sp=" ... "        [string]: require that results be spelled like this string
                                      accepts '*' as a multi-character wildcard & '?'
                                      as single character wildcard -single word

        --ml=" ... "        [string]: require that the results have a meaning
                                      related to this string value -space delimited

        --sl=" ... "        [string]: require that the results are pronounced similarly
                                      to this string of characters -single word

        --topics=" ... "    [string]: results will be skewed toward these topics
                                      space delimited
    ''')

def display_version(id):
    print('words version: ' + id)


def parse_args():
    args = sys.argv[1:]
    query = {}
    if len(args) < 1:
        print('''
            You must supply at least one operator
            See: words --help
        ''')
        return False

    query['operation'] = args.pop(0)
    if query['operation'] in ['help','-h','--help']:
        display_help()
        return False
    elif query['operation'] in ['version','-v','--version']:
        display_version(version_id)
        return False
    else:
        query['wordlist'] = []
        query['options'] = []
        for val in args:
            if val[0:2] == '--':
                op_list = val.split('=')
                query['options'].append(op_list)
            else:
                query['wordlist'].append(val)
        return query


if __name__ == '__main__':
    instructions = parse_args()
    if instructions:
        if instructions['operation'] == 'define':
            response = define_req(instructions)
        elif instructions['operation'] == 'define':
            response = call_api(lookup_req(instructions))
        else:
            response = 'unknown operator ' + instructions['operation']
        for item in response:
            print(item)
