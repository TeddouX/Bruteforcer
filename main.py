import timeit
import itertools
import string
import sys
import re
import py7zr 
import time

numbers = string.digits
uppercase = string.ascii_uppercase
lowercase = string.ascii_lowercase
special = '&#+=$*%!:;?,'

passes = open('top10000.txt').read()
top_10000 = passes.split('\n')

GPU = True
CPU = False

debug_mode = True
charset = ''
max_length = 3
tries = 0

help_page = '''
    -u or --uppercase bruteforce only with uppercase letters
    -l or --lowercase bruteforce only with lowercase letters
    -n or --number bruteforce only with numbers
    -s or --special bruteforce only with special characters

    -a or --all bruteforce with lowercase uppercase numbers and special characters
    # Default is on

    -D or --debug-mode bruteforce with debug
    # Default is on

    --max-lenght=[the max lenght here] set the max lenght of the password to bruteforce (mandatory)

    --GPU bruteforce on your GPU
    --CPU bruteforce on your CPU
    # Default is GPU 
    # If your GPU has a lower frequency than your CPU it is recommendable to switch to using your CPU

    -h or --help show this mesage'''

def check_arg(arg_name: str) -> bool:
    if arg_name == '--max-lenght':
        r = re.compile(r'--max-lenght=[0-9]')
        max_lenghts = list(filter(r.match, sys.argv))

        return any(item in sys.argv for item in max_lenghts)
        
    return True if arg_name in sys.argv else False

def bruteforce():
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(1, max_length + 1)))

def try_pass(pwd: str):
    try: 
        with py7zr.SevenZipFile('locked.7z', mode='r', password=pwd) as z: 
            z.extractall() 
            print(f'''PASSWORD FOUND: {pwd}''')
            sys.exit()
    except py7zr.exceptions.Bad7zFile:
        return ''

if __name__ == '__main__':
    if len(sys.argv) >= 1:
        if check_arg('-h') or check_arg('--help'):
            print(help_page)
        if check_arg('-u') or check_arg('--uppercase'):
            #print('u')
            charset += uppercase
        if check_arg('-l') or check_arg('--lowercase'):
            #print('l')
            charset += lowercase
        if check_arg('-n') or check_arg('--number'):
            #print('n')
            charset += numbers
        if check_arg('-a') or check_arg('--all'):
            #print('a')
            charset += numbers + lowercase + uppercase + special
        
        if check_arg('-D') or check_arg('--debug-mode'):
            #print('d')
            debug_mode = True
        
        if check_arg('--max-lenght'):
            string_argv = ''.join(str(e) for e in sys.argv)
            max_length = int(string_argv[string_argv.index(re.search(r'--max-lenght=\d+', string_argv).group(0))+13:])
            #print(max_lenght)
        else:
            raise RuntimeError('No maximum lenght specified try --help or -h')

        if check_arg('--GPU') and CPU != True:
            #print('gpu')
            GPU = True
        if check_arg('--CPU') and GPU != True:
            #print('cpu')
            CPU = True
        if CPU == True and GPU == True:
            raise RuntimeError('Cannot execute on GPU and CPU simultaneously')
        
        print(charset) if input('Do you want to see your charset ? y/n ') == 'y' else print('')
    else:
        raise RuntimeError('Cannot execute without arguments try --help or -h')
    
    start_time = timeit.default_timer()
    print(f'Starting at {start_time}')

    tries = 0
    print('Trying with commonly used passwords\n')
    time.sleep(2)
    for x in top_10000:
        print(x)
        try_pass(x)
        tries += 1

    print('\n\nTrying with random numbers and letters')
    time.sleep(2)
    for j in bruteforce():
        print(j)
        t = try_pass(j)
        tries += 1