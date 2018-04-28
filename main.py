import urllib.request, urllib.parse
import json
import sys

#http://www.datamuse.com/api/


dmapi = 'http://api.datamuse.com/words'
valid_args = {'means': ['ml',dmapi]}
query = {
    'operation' : '',
    'wordphrase' : '',
    'options' : []
}


def call_api(op,wordphrase):
    api = valid_args[op][1]
    param = '?' + valid_args[op][0] + '='
    url = api + param + wordphrase
    print(url)


    req = urllib.request.Request(url,method='GET')
    with urllib.request.urlopen(req, timeout=5) as res:
        value = res.read().decode('ASCII')
        value = json.loads(str(value))
        return value or False

def validate_args(op):
    if op in valid_args:
        return False
    return True


def display_help():
    print('''
        words:
        a utility for retrieving word information from the datamuse api

        usage:
        words [options...] args [query...]

        examples:
        words --max="10" --sp="*ding" --ml="joining merging tying"
        words --topics="weather clouds" --sl="rimbus"


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


def parse_args():
    args = sys.argv[1:] #words --help; words means a bright light --max-items=5
    query = {}
    query['operation'] = args.pop(0)
    query['wordlist'] = []
    query['options'] = []
    for val in args:
        if val[0:2] == '--':
            op_list = val.split('=')
            query['options'].append(op_list)
        else:
            query['wordlist'].append(val)
    return validate_operation(query['operation']) or query


if __name__ == '__main__':
    if validate_args(operation):
        response = call_api(operation,word_list)
        print(response)
    display_help()
