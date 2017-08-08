functions = [
    {   'name': 'OpenInstalledDevicesSession',
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
        'returns': 'ViStatus'},
    {   'name': 'GetInstalledDeviceAttributeViString',
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
             'type': 'ViString',
             'is_buffer': True,
             'size': 'ivi-dance,attributeValueBufferSize',
             },
        ],
        'returns': 'ViStatus'},
    {   'name': 'GetInstalledDeviceAttributeViInt32',
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
        'returns': 'ViStatus'},
    {   'name': 'CloseInstalledDevicesSession',
        'codegen_method': 'private',
        'parameters': [
            {'direction': 'in', 'enum': None,
             'name': 'handle', 'type': 'ViSession'},
        ],
        'returns': 'ViStatus'},
    {   'name': 'GetExtendedErrorInfo',
        'codegen_method': 'public',
        'parameters': [
            {'direction': 'in', 'enum': None,
             'name': 'errorInfoBufferSize', 'type': 'ViInt32'},
            {'direction': 'out', 'enum': None,
             'name': 'errorInfo',
             'type': 'ViString',
             'is_buffer': True,
             'size': 'ivi-dance,errorInfoBufferSize'
             },
        ],
        'returns': 'ViStatus'},
]


