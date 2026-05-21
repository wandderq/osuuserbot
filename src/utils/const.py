from telethon import connection

CONNECTIONS = {
    'randomized': connection.ConnectionTcpMTProxyRandomizedIntermediate,
    'abridged': connection.ConnectionTcpMTProxyAbridged,
    'intermediate': connection.ConnectionTcpIntermediate
}

CONFIG_SCHEMA = {
    'telegram': {
        'required': True,
        'keywords': {
            'api_id': {'required': True, 'type': int},
            'api_hash': {'required': True, 'type': str},
            'bot_token': {'required': True, 'type': str}
        }
    },
    'osu': {
        'required': True,
        'keywords': {
            'client_id': {'required': True, 'type': int},
            'client_secret': {'required': True, 'type': str},
        },
        'subtables': {
            'service': {
                'required': False,
                'keywords': {
                    'max_request_rate': {'required': False, 'type': int, 'default': 20},
                },
                'subtables': {
                    'ttlcache': {
                        'required': False,
                        'keywords': {
                            'max_size': {'required': False, 'type': int, 'default': 1000},
                            'ttl': {'required': False, 'type': int, 'default': 300}
                        }
                    }
                }
            }
        }
    },
    'metadata': {
        'required': True,
        'keywords': {
            'bot_name': {'required': True, 'type': str},
            'bot_username': {'required': True, 'type': str},
            'source_code_url': {'required': True, 'type': str},
            'author': {'required': True, 'type': str}
        }
    },
    'mtproxy': {
        'required': False,
        'default': None,
        'keywords': {
            'server': {'required': True, 'type': str},
            'port': {'required': True, 'type': int},
            'secret': {'required': True, 'type': str},
            'connection': {
                'required': False,
                'type': str,
                'default': 'randomized',
                'choices': ['randomized', 'abridged', 'intermediate']
            }
        }
    }
}