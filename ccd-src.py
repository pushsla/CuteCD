#!/usr/bin/python3
#-- Advanced version of cd program. Use ccd --help

import configparser
from re import findall as refindall
from os.path import join as osjoin
from os.path import isdir
from os import listdir
from os import environ
from os import chdir
from os import execl
from os import path as ospath
import sys

def helpshow():
    helptext = """    CuteCD Python. Another chdir version written with Python. Will find directory and make chdir to it for you.
    If there will be more than one found dir, you will be able to chose.
    SYNOPSIS:
    \tccd [search name or pattern] [keys]
    KEYS:
        -h --help -? --? This help page

        -d\t\tset start search point. Default -- $HOME value
        -f\t\tmake chdir to the first found directory, will be no choice
        -p\t\tinterpretate [name] as a regular search pattern. Default -- [name] must coincide with dir name.
        -l\t\tcase unsensitive search. Default -- case sensitive
        -a\t\tsearch in hidden directories. Default -- dont search in hidden
        -r < value > \tset search depth limit. Do not set big values. Default -- 100
        -c\t\tuse specified config. Default config stored in $HOME/.config/ccd.pycfg
    """
    print(helptext)
    exit(0)

def configure(args, env, actual_version):
    """
    read config and apply program variables
        :param args: list of keys ans flags. Use sys.argv
        :param env: dict of environment variables as dict. Use os.environ
        :param actual_version: str config version. Hard-coded in main. Needs to
            update config if needed
    """
    start_point = env['HOME']
    search_point = None
    search_by_pattern = False
    search_hidden = False
    end_at_first = False
    recursion_limit = 15
    lowercase = False
    excluded_dirs = "/dev:/run/udev:/proc:/sys"
    exclude_pattern = r"/\.*cache/*|/s*bin/*"


    if args.count('-c') == 0:
        config = "{}/.config/ccd.conf".format(env['HOME'])
        #default_config = True
        found_config = 0
    else:
        try:
            config = args[args.index('-c')+1]
            #default_config = False
            found_config = 1
        except IndexError:
            print('Timid denial to read nameless config')
            exit(1)
    try:
        try:
            config_exist = True
            with open(config, 'r') as c:
                current_version = c.readlines()[-1][:-1]
        except FileNotFoundError:
            config_exist = False

        if not config_exist and found_config == 0 or current_version != actual_version:
            print('Creating new config file')
            # try:
            #     os.mkdir("{}/.config/ccd.conf".format(env['HOME']))
            # except FileExistsError:
            #     pass
            cfgp = configparser.ConfigParser()
            cfgp.add_section("Defaults")
            cfgp.set("Defaults", "start_point", start_point)
            # cfgp.set("Defaults", "search_point", search_point)
            cfgp.set("Defaults", "search_by_pattern", str(search_by_pattern))
            cfgp.set("Defaults", "include_hidden_files", str(search_hidden))
            cfgp.set("Defaults", "search_til_first", str(end_at_first))
            cfgp.set("Defaults", "max_depth", str(recursion_limit))
            cfgp.set("Defaults", "case_sensitive", str(not lowercase))
            cfgp.add_section("Rules")
            cfgp.set("Rules", "excluded_dirs", excluded_dirs)
            cfgp.set("Rules", "exclude_pattern", exclude_pattern)
            with open(config, 'w') as c:
                cfgp.write(c)
                c.write("\n{}\n".format(actual_version))
        else:
            cfgp = configparser.ConfigParser()
            cfgp.read(config)
            try:
                start_point = cfgp.get("Defaults", "start_point")
                # search_point = cfgp.get("Defaults", "search_point")
                search_by_pattern = cfgp.get("Defaults", "search_by_pattern") == 'True'
                search_hidden = cfgp.get("Defaults", "include_hidden_files") == 'True'
                end_at_first = cfgp.get("Defaults", "search_til_first") == 'True'
                recursion_limit = int(cfgp.get("Defaults", "max_depth"))
                lowercase = cfgp.get("Defaults", "case_sensitive") == 'False'
                excluded_dirs = cfgp.get("Rules", "excluded_dirs")
                exclude_pattern = cfgp.get("Rules", "exclude_pattern")
            except configparser.NoSectionError:
                raise FileNotFoundError('Invalid config file {}'.format(config))
                # print("Timid denial to use invalid config file {}".format(config)
                # exit(1)
        # with open(config, 'r') as c:
            # values = c.read()
            # print(values)
            # HERE I MUST EXEC CONFIG VALUES!
    except FileNotFoundError:
        print('{} was not found. use defaults'.format(config))
        found_config = 1

    config = {}
    config['stp'] = start_point
    config['sep'] = search_point
    config['sbp'] = search_by_pattern
    config['seh'] = search_hidden
    config['eaf'] = end_at_first
    config['rel'] = recursion_limit
    config['lwc'] = lowercase
    config['exd'] = excluded_dirs
    config['exp'] = exclude_pattern
    config['fcf'] = found_config

    return config

def parseargs(args, env, config):
    """
    Parse cmd arguments stored in args
        :param args: list of keys and flags. Use os.argv
        :param env: dict of environment variables as dict. Use os.environ
    """
    if sum(args.count(t) for t in ['-h', ' --help', '-?', ' --?']) > 0:
        return True, None, None, None, None, None, None, None, None, None

    start_point = config['stp']
    search_point = config['sep']
    search_by_pattern = config['sbp']
    search_hidden = config['seh']
    end_at_first = config['eaf']
    recursion_limit = config['rel']
    lowercase = config['lwc']
    excluded_dirs = config['exd']
    exclude_pattern = config['exp']
    found_config = config['fcf']


    found_search = False
    #print(start_point, search_point, search_by_pattern, search_hidden, end_at_first, recursion_limit, lowercase)
    #print(type(start_point), type(search_point), type(search_by_pattern), type(search_hidden), type(end_at_first), type(recursion_limit), type(lowercase))

    i = 0
    while i < len(args):
        arg = args[i]
        try:
            if arg == '-d':
                start_point = args[i + 1]
                i += 2
                continue
            elif arg == '-c':
                if found_config == 0:
                    raise RuntimeError('все пошло нахрен!!!!!')
                elif found_config < 2:
                    found_config += 1
                    i += 2
                    continue
                else:
                    print('Timid remark: config was been already specified by -c flag')
                    exit(1)
            elif arg == '-f':
                end_at_first = True
            elif arg == '-p':
                search_by_pattern = True
            elif arg == '-l':
                lowercase = not lowercase
            elif arg == '-r':
                try:
                    recursion_limit = int(args[i + 1])
                    i += 2
                except ValueError:
                    print('Timid denial to use flag {} with value {}'.format(args[i], args[i+1]))
                    exit(1)
                continue
            elif arg == '-a':
                search_hidden = True
            elif found_search:
                start_point = args[i]
                if start_point[0] == '.':
                    search_hidden = True
            else:
                search_point = args[i]
                found_search = True
                if search_point[0] == '.':
                    search_hidden = True
        except IndexError:
            print('Timid remark: unused flag {}'.format(args[i]))
            exit(1)
        i += 1

    if not found_search:
        print('Timid denial to find a nameless folder')
        exit(1)

    return (False, start_point, search_point, end_at_first,
            search_by_pattern, search_hidden, recursion_limit, lowercase, excluded_dirs, exclude_pattern)


def searchdepth(search_dir, search_point, end_at_first,
                search_by_pattern, search_hidden, lowercase, excluded_dirs, exclude_pattern, already_found, recursion):
    """
    recursive function to depth search
        :param search_dir: str destination directory name or pattern
        :param search_point: str directory where to search at this iteration
        :param end_at_first: bool will stop search at first found directory
        :param search_by_pattern: bool interprete search_dir ad pattern
        :param search_hidden: bool include also hidden files to search
        :param lowercase: bool same as case-sensitive
        :param already_found: internal variable. If some dirs were already found
        :param recursion: internal variable. Need to set search depth limit
    """
    if (end_at_first and already_found) or (recursion <= 0):
        return []

    e_d = excluded_dirs.split(':')
    try:
        dir_list = []
        for f in listdir(path = search_dir):
            path = osjoin(search_dir, f)

            if isdir(path) and (path not in e_d) and (len(refindall(exclude_pattern, path)) == 0):
                dir_list.append(f)
        # dir_list = [f for f in listdir(path = search_dir) if isdir(osjoin(search_dir, f)) and osjoin(search_dir, f) not in e_d]
    except PermissionError:
        return []

    if not search_hidden:
        dir_list = [f for f in dir_list if f[0] != '.']

    if search_by_pattern and lowercase:
        found_list = [f for f in dir_list if len(refindall(search_point.lower(), f.lower())) > 0]
    elif search_by_pattern:
        found_list = [f for f in dir_list if len(refindall(search_point, f)) > 0]
    elif lowercase:
        found_list = [f for f in dir_list if f.lower() == search_point.lower()]
    else:
        found_list = [f for f in dir_list if f == search_point]

    # if not search_hidden:
    #     found_list = [f for f in found_list if f[0] != '.']

    if len(found_list) > 0 and end_at_first:
        already_found = True
        return [osjoin(search_dir, sorted(found_list)[0])]
    elif len(found_list) > 0:
        already_found = True

    for d in dir_list:
        found_list += searchdepth(osjoin(search_dir, d), search_point, end_at_first,
                                  search_by_pattern, search_hidden, lowercase, excluded_dirs, exclude_pattern, already_found, recursion-1)

    return [osjoin(search_dir, f) for f in found_list]


def request_chdir(dir_list, end_at_first, key):
    """
    make chdir to directories
        :param dir_list: list of found dirs to ask user in which to cd
        :param end_at_first: bool auto make cd in first dir without asking
        :param key: function sorting type
    """
    if len(dir_list) == 0:
        print('...nothing')
        exit(1)

    if end_at_first or len(dir_list) == 1:
        chdir(dir_list[0])
        execl(environ['SHELL'], environ['SHELL'].split('/')[-1])
        exit(0)

    dir_list = sorted(dir_list, key = key)
    keys = list(range(len(dir_list)))
    # requests = dict(zip(keys, dir_list))
    for k in keys:
        print("({}) {}".format(k, dir_list[k]))

    while True:
        seq = input('Which do you need? (0): ')
        if seq == '':
            seq = 0
        else:
            try:
                seq = int(seq)
            except ValueError:
                if seq in ['q', 'Q']:
                    exit(0)
                else:
                    continue
        try:
            chdir(dir_list[seq])
            execl(environ['SHELL'], environ['SHELL'].split('/')[-1])
            exit(0)
        # except KeyError:  # if use dictionary
        #     continue
        except IndexError:  # if use list
            continue


def key_default(x):
    try:
        hid_dep = len(x) - x.index('.')
    except ValueError:
        hid_dep = 0
    return x.count('/') + x.count('/.')*hid_dep

def key_default_reversed(x):
    global key_default
    return (-1)*key_default(x)


config = configure(sys.argv[1:], environ, 'ConfigVersion = v1.0')


(helppage, start_point,
 search_point, end_at_first,
 search_by_pattern, search_hidden,
 recursion_limit, lowercase, excluded_dirs, exclude_pattern) = parseargs(sys.argv[1:], environ, config)
if helppage:
    helpshow()

found_dirs = searchdepth(start_point, search_point, end_at_first,
                         search_by_pattern, search_hidden, lowercase, excluded_dirs, exclude_pattern, False, recursion_limit)

request_chdir(found_dirs, end_at_first, key_default_reversed)
