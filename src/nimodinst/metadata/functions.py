functions = {
    'OpenInstalledDevicesSession': {
        'codegen_method': 'private',
        'parameters': [
            {'direction': 'in', 'enum': None,
             'name': 'driver',
             'type': 'ViConstString'},
            {'direction': 'out', 'enum': None,
             'name': 'handle',
             'type': 'ViSession'},
            {'direction': 'out', 'enum': None,
             'name': 'item_count',
             'type': 'ViInt32'},
        ],
        'returns': 'ViStatus',
    },
    'GetInstalledDeviceAttributeViString': {
        'codegen_method': 'private',
        'parameters': [
            {'direction': 'in', 'enum': None,
             'name': 'handle',
             'type': 'ViSession'},
            {'direction': 'in', 'enum': None,
             'name': 'index',
             'type': 'ViInt32'},
            {'direction': 'in', 'enum': None,
             'name': 'attributeID',
             'type': 'ViInt32'},
            {'direction': 'in', 'enum': None,
             'name': 'attributeValueBufferSize',
             'type': 'ViInt32'},
            {'direction': 'out', 'enum': None,
             'name': 'attributeValue',
<<<<<<< HEAD
             'type': 'ViChar',
             'is_buffer': True,
             'size': 'ivi-dance',
=======
             'type': 'ViString',
             'is_buffer': True,
             'size': 'ivi-dance,attributeValueBufferSize',
>>>>>>> master
             },
        ],
        'returns': 'ViStatus',
    },
    'GetInstalledDeviceAttributeViInt32': {
        'codegen_method': 'private',
        'parameters': [
            {'direction': 'in', 'enum': None,
             'name': 'handle',
             'type': 'ViSession'},
            {'direction': 'in', 'enum': None,
             'name': 'index',
             'type': 'ViInt32'},
            {'direction': 'in', 'enum': None,
             'name': 'attributeID',
             'type': 'ViInt32'},
            {'direction': 'out', 'enum': None,
             'name': 'attributeValue',
             'type': 'ViInt32'},
        ],
        'returns': 'ViStatus',
    },
    'CloseInstalledDevicesSession': {
        'codegen_method': 'private',
        'parameters': [
            {'direction': 'in', 'enum': None,
             'name': 'handle', 'type': 'ViSession'},
        ],
        'returns': 'ViStatus',
    },
    'GetExtendedErrorInfo': {
        'codegen_method': 'public',
        'parameters': [
            {'direction': 'in', 'enum': None,
             'name': 'errorInfoBufferSize', 'type': 'ViInt32'},
            {'direction': 'out', 'enum': None,
             'name': 'errorInfo',
<<<<<<< HEAD
             'type': 'ViChar',
             'is_buffer': True,
             'size': 'ivi-dance'
=======
             'type': 'ViString',
             'is_buffer': True,
             'size': 'ivi-dance,errorInfoBufferSize'
>>>>>>> master
             },
        ],
        'returns': 'ViStatus',
    },
}


