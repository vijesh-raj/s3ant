# coding: utf-8

import os
import json
import types
import core.utils as utils
import core.hash as hash
from collections import OrderedDict

class Configure(object):
    ''' Handle configure '''
    
    config_filepath = utils.abspath('config.json')
    
    # User input config
    __user_config = OrderedDict([
        ('aws_access_key_id', None),
        ('aws_secret_access_key', None),
        ('region', None),
        
        ('bucket', None),
        ('bucket_basepath', None),
        ('backup_paths', ['/bach/home', '/test/test/test']),
        
        ('keep_days', '7'),
        ('timezone', 'Asia/Tokyo'),
    ])
    
    # System config
    __sys_config = OrderedDict([
        ('hostname', None),
    ])
    
    # Full config
    __config = OrderedDict()


    @classmethod
    def set(cls, config):
        ''' Update config in memory '''
        config = dict((k, v) for k, v in config.items() \
            if k in cls.__config and (v or v==0))
        cls.__config.update(config)
        
        # Standardize config value
        if isinstance(cls.__config['backup_paths'], types.StringTypes):
            cls.__config['backup_paths'] = cls.__config['backup_paths'].split(' ')
        if isinstance(cls.__config['keep_days'], types.StringTypes):
            cls.__config['keep_days'] = int(cls.__config['keep_days'])
        if isinstance(cls.__config['bucket_basepath'], types.StringTypes):
            cls.__config['bucket_basepath'] = cls.__config['bucket_basepath'].strip('/')


    @classmethod
    def get(cls, path=None):
        ''' Return config from provided path '''
        if path is None:
            return cls.__config
        else:
            return hash.get(cls.__config, path)
    
    
    @classmethod
    def initialize(cls):
        ''' Initialize config file '''
        cls.user_input()
        cls.sys_input()
        cls.write_to_file()
    

    @classmethod
    def user_input(cls):
        ''' Prompt user input for config '''
        cls.read_from_file()
        config = {}
        for key in cls.__user_config:
            if key == 'backup_paths':
                default_val = ' '.join(cls.__config[key])
            else:
                default_val = cls.__config[key]
            config[key] = utils.input(' %s [%s]:\n -> ' % (key, default_val))
            if not config[key]:
                config[key] = default_val
        cls.set(config)


    @classmethod
    def sys_input(cls):
        ''' Set system config '''
        config = {
            'hostname': utils.hostname(),
        }
        cls.set(config)
        

    @classmethod
    def write_to_file(cls):
        ''' Write config to file '''
        with open(cls.config_filepath, 'w') as f:
            json.dump(cls.__config, f, indent=4)


    @classmethod
    def read_from_file(cls):
        ''' Read config from file '''
        cls.__config.update(cls.__user_config)
        cls.__config.update(cls.__sys_config)
        config = {}
        if (os.path.isfile(cls.config_filepath)):
            with open(cls.config_filepath, 'r') as f:
                config = json.load(f)
        cls.set(config)


# Initialize
Configure.read_from_file()