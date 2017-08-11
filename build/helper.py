# TODO(marcoskirsch): This file should definitely not live here but I had trouble getting import to work.
# TODO(marcoskirsch): Figure out unit test for this.

from contextlib import contextmanager
import importlib
import re
import pprint
import string
import sys

pp = pprint.PrettyPrinter(indent=4)

# Coding convention transformation functions.

# TODO(marcoskirsch): not being used
def shoutcase_to_camelcase(shout_string):
    '''Converts a C-style SHOUT_CASE string to camelCase'''
    components = shout_string.split('_')
    return components[0].lower() + "".join(component.title() for component in components[1:])

def camelcase_to_snakecase(camelcase_string):
    '''Converts a camelCase string to lower_case_snake_case'''
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camelcase_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def function_to_method_name(f):
    '''Returns an appropriate session method name for a given function'''
    # Method name is camelCase.
    # TODO(marcoskirsch): Some of these should be "_private" if user doesn't need to call directly.
    return f['name'][0].lower() + f['name'][1:]

# Filters

def extract_codegen_functions(functions):
    '''Returns function metadata only for those functions to be included in codegen'''
    funcs = {}
    for x in functions:
        if functions[x]['codegen_method'] != 'no':
            funcs[x] = functions[x]
    return funcs

def extract_input_parameters(parameters, sessionName = 'vi'):
    '''Returns list of parameter dicts only with input parameters'''
    return [x for x in parameters if x['direction'] == 'in' and x['name'] != sessionName]

def extract_output_parameters(parameters):
    '''Returns list of parameters only with output parameters, not including the ivi-dance parameter if it exists'''
    return [x for x in parameters if x['direction'] == 'out' and not x['ivi-dance']]

def extract_enum_parameters(parameters):
    '''Returns a list of parameter dicts that have an associated enum'''
    return [x for x in parameters if x['enum'] is not None]

def extract_ivi_dance_parameter(parameters):
    '''Returns the ivi-dance parameter of a session method if there is one

    There can be only one ivi-dance parameter so return that individual parameter and not a list
    '''
    param = [x for x in parameters if x['ivi-dance']]
    assert len(param) <= 1, '{0} ivi-dance parameters. No more than one is allowed'.format(len(param))
    if len(param) == 0:
        return None
    return param[0]

# Functions to add information to metadata structures that are specific to our codegen needs.

def _add_python_method_name(function, name):
    '''Adds a python_name' key/value pair to the function metadata'''
    if function['codegen_method'] == 'private':
        function['python_name'] = '_' + camelcase_to_snakecase(name)
    else:
        function['python_name'] = camelcase_to_snakecase(name)
    return function

def _add_python_parameter_name(parameter):
    '''Adds a python_name' key/value pair to the parameter metadata'''
    parameter['python_name'] = camelcase_to_snakecase(parameter['name'])
    return parameter

def _add_python_type(parameter):
    '''Adds a python_type key/value pair to the parameter metadata'''
    if parameter['enum'] is None:
        parameter['python_type'] = parameter['type']
    else:
        parameter['python_type'] = 'enums.' + parameter['enum']
    return parameter

def _add_ctypes_variable_name(parameter):
    '''Adds a ctypes_variable_name key/value pair to the parameter metadata for a corresponding ctypes variable'''
    parameter['ctypes_variable_name'] = parameter['python_name'] + '_ctype'
    return parameter

def _add_ctypes_type(parameter):
    '''Adds a ctypes_type key/value pair to the parameter metadata for calling into the library'''
    # TODO(marcoskirsch): handle buffers and strings.
    parameter['ctypes_type'] = parameter['type'] + '_ctype'
    return parameter

def _add_ctypes_return_type(f):
    '''Adds the ctypes_type key/value pair to the function metadata for the return type'''
    f['returns_ctype'] = f['returns'] + '_ctype'
    return f

def _add_python_return_type(f):
    '''Adds the ctypes_type key/value pair to the function metadata for the return type'''
    f['returns_python'] = f['returns']
    return f

def _add_buffer_info(parameter):
    '''Adds buffer information to the parameter metadata iff 'size' is defined else assume not a buffer'''
    try:
        parameter['size']
        parameter['is_buffer'] = True
        parameter['ivi-dance'] = False
        if type(parameter['size']) is str and parameter['size'].startswith('ivi-dance,'):
            parameter['ivi-dance'] = True
            parameter['size'] = camelcase_to_snakecase(parameter['size'].split(',')[1])
    except KeyError:
        # Not populated, assume False
        parameter['is_buffer'] = False
        parameter['ivi-dance'] = False
    return parameter

def add_all_metadata(functions):
    '''Adds all codegen-specific metada to the function metadata list'''
    for f in functions:
        _add_python_method_name(functions[f], f)
        _add_ctypes_return_type(functions[f])
        _add_python_return_type(functions[f])
        for p in functions[f]['parameters']:
            _add_python_parameter_name(p)
            _add_python_type(p)
            _add_ctypes_variable_name(p)
            _add_ctypes_type(p)
            _add_buffer_info(p)
    return functions

# Normalize string type between python2 & python3
def normalize_string_type(d):
    if sys.version_info.major < 3:
        if type(d) is dict:
            for k in d:
                d[k] = normalize_string_type(d[k])
        elif type(d) is str:
            d = d.decode('utf-8')

    return d
# Functions that return snippets that can be placed directly in the templates.

def get_method_parameters_snippet(parameters):
    '''Returns a string suitable for the parameter list of a method given a list of parameter objects'''
    snippets = ['self']
    for x in parameters:
        snippets.append(x['python_name'])
    return ', '.join(snippets)

def get_function_parameters_snippet(parameters, sessionName=None):
    '''
    Returns a string suitable for the parameter list of a method given a list of parameter objects

    If sessionName set, skip that parameter
    '''
    snippets = []
    for x in parameters:
        if sessionName is not None and x['python_name'] == sessionName:
            continue
        snippets.append(x['python_name'])
    return ', '.join(snippets)

def get_library_call_parameter_snippet(parameters_list, sessionName = 'vi'):
    '''Returns a string suitable to use as the parameters to the library object, i.e. "self, mode, range, digits_of_resolution"'''
    snippets = []
    for x in parameters_list:
        if x['direction'] == 'in':
            if x['name'] == sessionName:
                snippet = 'self.' + sessionName
            else:
                snippet = x['python_name']
                snippet += '.value' if x['enum'] is not None else ''
                if x['type'] == 'ViString' or x['type'] == 'ViConstString' or x['type'] == 'ViRsrc':
                    snippet += '.encode(\'ascii\')'
        else:
            assert x['direction'] == 'out', pp.pformat(x)
            if x['ivi-dance']:
                snippet = x['ctypes_variable_name']
            elif x['is_buffer']:
                snippet = 'ctypes.cast(' + x['ctypes_variable_name'] + ', ctypes.POINTER(ctypes_types.' + x['ctypes_type'] + '))'
            else:
                snippet = 'ctypes.pointer(' + (x['ctypes_variable_name']) + ')'
        snippets.append(snippet)
    return ', '.join(snippets)

def get_library_call_parameter_types_snippet(parameters_list):
    '''Returns a string suitable to use as the parameters to the library definition object'''
    snippets = []
    for x in parameters_list:
        if x['direction'] == 'out':
            if x['type'] == 'ViString' or x['type'] == 'ViRsrc' or x['type'] == 'ViConstString_ctype':
                # These are defined as c_char_p which is already a pointer!
                snippets.append(x['ctypes_type'])
            else:
                snippets.append("ctypes.POINTER(" + x['ctypes_type'] + ")")
        else:
            assert x['direction'] == 'in', pp.pformat(x)
            snippets.append(x['ctypes_type'])
    return ', '.join(snippets)

def _get_output_param_return_snippet(output_parameter):
    '''Returns the snippet for returning a single output parameter from a Session method, i.e. "reading_ctype.value"'''
    assert output_parameter['direction'] == 'out', pp.pformat(output_parameter)
    if output_parameter['is_buffer']:
        if output_parameter['type'] == 'ViChar' or output_parameter['type'] == 'ViString':
            snippet = output_parameter['ctypes_variable_name'] + '.value.decode("ascii")'
        else:
            # TODO(marcoskirsch): I don't like calling camelcase_to_snakecase here, it relies on contract that parameter name where the size is stored was created with that function.
            snippet = '[' + output_parameter['ctypes_variable_name'] + '[i].value for i in range(' + camelcase_to_snakecase(output_parameter['size']) + ')]'
    else:
        snippet = output_parameter['ctypes_variable_name'] + '.value'

    return snippet

def get_method_return_snippet(parameters):
    '''Returns a string suitable to use as the return argument of a Session method, i.e. "return reading_ctype.value"'''
    snippets = []
    for x in parameters:
        if x['direction'] == 'out' or x['ivi-dance']:
            snippets.append(_get_output_param_return_snippet(x))
    return ('return ' + ', '.join(snippets)).strip()

def get_enum_type_check_snippet(parameter, indent):
    '''Returns python snippet to check that the type of a parameter is what is expected'''
    assert parameter['enum'] is not None, pp.pformat(parameter)
    assert parameter['direction'] == 'in', pp.pformat(parameter)
    return 'if type(' + parameter['python_name'] + ') is not ' + parameter['python_type'] + ':\n' + (' ' * indent) + 'raise TypeError(\'Parameter mode must be of type \' + str(' + parameter['python_type'] + '))'

def get_ctype_variable_declaration_snippet(parameter):
    '''Returns python snippet to declare and initialize the corresponding ctypes variable'''
    assert parameter['direction'] == 'out', pp.pformat(parameter)
    snippet = parameter['ctypes_variable_name'] + ' = '
    if parameter['is_buffer']:
        if isinstance(parameter['size'], int):
            snippet += '(' + 'ctypes_types.' + parameter['ctypes_type'] + ' * ' + str(parameter['size']) + ')()'
            #snippet += 'ctypes.create_string_buffer(' + str(parameter['size']) + ')'
        elif parameter['size'] == 'ivi-dance':
            snippet += 'ctypes_types.' + parameter['ctypes_type'] + '(0)  # TODO(marcoskirsch): Do the IVI-dance!'
        else:
            # TODO(marcoskirsch): I don't like calling camelcase_to_snakecase here, it relies on contract that parameter name where the size is stored was created with that function.
            snippet += '(' + 'ctypes_types.' + parameter['ctypes_type'] + ' * ' + camelcase_to_snakecase(parameter['size']) + ')()'
    else:
        snippet += 'ctypes_types.' + parameter['ctypes_type'] + '(0)'
    return snippet

def get_dictionary_snippet(d, indent=4):
    '''Returns a formatted dictionary'''
    d_str = pprint.pformat(d)
    d_lines = d_str.splitlines()
    return ('\n' + (' ' * indent)).join(d_lines)

def sorted_attrs(a):
    return sorted(a, key=lambda k: a[k]['name'])

def get_indented_docstring_snippet(d, indent=4):
    '''
    Returns a docstring with the correct amount of indentation.

    First line is not indented.

    Can't use similar construct as get_dictionary_snippet
    ('\n' + (' ' * indent)).join(d_lines) because empty lines would get
    the spaces, which violates pep8 and causes the flake8 step to fail

    Args:
        docstring (str): multiline string to format
        indent (int): How much to indent lines 2+

    Returns:
        str: formatted string
    '''
    d_lines = d.strip().splitlines()
    ret_val = ''
    for l in d_lines:
        if len(ret_val) > 0:
            ret_val += '\n'
            if len(l.rstrip()) > 0:
                ret_val += (' ' * indent)
        ret_val += normalize_string_type(l.rstrip())
    return ret_val

def get_rst_header_snippet(t, header_level='='):
    '''Get rst formatted heading
    '''
    ret_val = t + '\n'
    ret_val += header_level * len(t)
    return ret_val

# We need this in the global namespace so we can reference it from the sub() callback
config = None
def replace_func_python_name_no_link(f_match):
    '''callback function for regex sub command when link not needed

    Args:
        m (match object): Match object from the function substitution command

    Returns:
        str: python name of the function
    '''
    fname = "Unknown"
    if f_match and f_match.group(1) in config['functions']:
        fname = config['functions'][f_match.group(1)]['python_name']
    return '{0} '.format(fname)

def replace_func_python_name_with_link(f_match):
    '''callback function for regex sub command when link needed

    Args:
        m (match object): Match object from the function substitution command

    Returns:
        str: rst link to function using python name
    '''
    fname = "Unknown"
    if f_match and f_match.group(1) in config['functions']:
        fname = config['functions'][f_match.group(1)]['python_name']
    return ':py:func:`{0}.{1}` '.format(config['module_name'], fname)

def find_attribute_by_name(attributes, name):
    '''Returns the attribute with the given name if there is one

    There should only be one so return that individual parameter and not a list
    '''
    attr = [attributes[x] for x in attributes if attributes[x]['name'] == name]
    assert len(attr) <= 1, '{0} attributes with name {1}. No more than one is allowed'.format(len(attr), name)
    if len(attr) == 0:
        return None
    return attr[0]

def replace_attribute_python_name_no_link(a_match):
    '''callback function for regex sub command when link not needed

    Args:
        m (match object): Match object from the attribute substitution command

    Returns:
        str: python name of the attribute
    '''
    aname = "Unknown"
    if a_match:
        attr = find_attribute_by_name(config['attributes'], a_match.group(1))
        aname = a_match.group(1)
        if attr:
            aname = attr['name'].lower()
    return '{0}'.format(aname)

def replace_attribute_python_name_with_link(a_match):
    '''callback function for regex sub command when link needed

    Args:
        m (match object): Match object from the attribute substitution command

    Returns:
        str: rst link to attribute using python name
    '''
    aname = "Unknown"
    if a_match:
        attr = find_attribute_by_name(config['attributes'], a_match.group(1).replace('\_', '_'))
        aname = a_match.group(1)
        if attr:
            aname = attr['name'].lower()
    return ':py:data:`{0}.{1}`'.format(config['module_name'], aname)

def fix_references(doc, cfg, make_link=False):
    '''Replace ATTR and function mentions in documentation

    Args:
        doc (str): documentation string to be updated
        config (dict): config dictionary from metadata
        make_link (bool): Default False
            True - references are replaced with a rst style link
            False - references are replaced with just the python name

    Returns:
        str: documentation with references replaces based on make_link
    '''

    global config
    config = cfg

    attr_re = re.compile('{0}\\\\_ATTR\\\\_([A-Z0-9\\\\_]+)'.format(config['module_name'].upper()))
    func_re = re.compile('{0}(.+?) '.format(config['c_function_prefix'].replace('_', '\_')))
    enum_re = re.compile('enums.(.+)')

    if make_link:
        m = attr_re.search(doc)
        if m:
            doc = attr_re.sub(replace_attribute_python_name_with_link, doc)
            m = attr_re.search(doc)

        m = func_re.search(doc)
        if m:
            doc = func_re.sub(replace_func_python_name_with_link, doc)
            m = func_re.search(doc)
    else:
        m = attr_re.search(doc)
        if m:
            doc = attr_re.sub(replace_attribute_python_name_no_link, doc)
            m = attr_re.search(doc)

        m = func_re.search(doc)
        if m:
            doc = func_re.sub(replace_func_python_name_no_link, doc)
            m = func_re.search(doc)

        doc = doc.replace('\_', '_')
    return doc

def get_function_rst(fname, config, indent=0):
    '''Gets rst formatted documentation for given function

    Args:
        fname (str): Function name - key in function dictionary
        function (dict): function entry correcsponding to fname in function dictionary

    Returns:
        str: rst formatted documentation
    '''
    function = config['functions'][fname]
    rst = '.. function:: ' + function['python_name'] + '('
    rst += get_function_parameters_snippet(function['parameters'], sessionName='vi') + ')'
    indent += 4
    if 'purpose' in function:
        rst += '\n\n' + (' ' * indent) + get_indented_docstring_snippet(fix_references(function['purpose'], config, make_link=True), indent)
    if 'long_description' in function:
        rst += '\n\n' + (' ' * indent) + get_indented_docstring_snippet(fix_references(function['long_description'], config, make_link=True), indent)

    input_params = extract_input_parameters(function['parameters'])
    if len(input_params) > 0:
        rst += '\n'
    for p in input_params:
        rst +=  '\n' + (' ' * indent) + ':param {0}: '.format(p['python_name']) + '\n'
        if 'long_description' in p:
            rst += (' ' * (indent + 4)) + get_indented_docstring_snippet(fix_references(p['long_description'], config, make_link=True), indent + 4) + '\n'
        p_type = p['python_type']
        if p_type.startswith('enums.'):
            p_type = p_type.replace('enums.', '')
            p_type = ':py:data:`{0}.{1}`'.format(config['module_name'], p_type)
        rst += '\n' + (' ' * indent) + ':type {0}: '.format(p['python_name']) + p_type


    output_params = extract_output_parameters(function['parameters'])
    if len(output_params) > 1:
        rst += '\n\n' + (' ' * indent) + ':rtype: tuple ('+ ', '.join([p['python_name'] for p in output_params]) + ')\n\n'
        rst += (' ' * (indent + 4)) + 'WHERE\n'
        for p in output_params:
            rst += '\n' + (' ' * (indent + 4)) + '{0} ({1}): '.format(p['python_name'], p['python_type']) + '\n'
            if 'long_description' in p:
                rst += (' ' * (indent + 8)) + get_indented_docstring_snippet(fix_references(p['long_description'], config, make_link=True), indent + 8) + '\n'
    elif len(output_params) == 1:
        p = output_params[0]
        rst += '\n\n' + (' ' * indent) + ':rtype: '+ p['python_type']

    return rst

def get_function_docstring(fname, config, indent=0):
    '''Gets formatted documentation for given function that can be used as a docstring

    Args:
        fname (str): Function name - key in function dictionary
        function (dict): function entry correcsponding to fname in function dictionary

    Returns:
        str: docstring formatted documentation
    '''
    docstring = ''
    function = config['functions'][fname]
    if 'purpose' in function:
        docstring += get_indented_docstring_snippet(fix_references(function['purpose'], config, make_link=False), indent)
    elif 'long_description' in function:
        docstring += get_indented_docstring_snippet(fix_references(function['long_description'], config, make_link=False), indent)

    input_params = extract_input_parameters(function['parameters'])
    if len(input_params) > 0:
        docstring += '\n\n' + (' ' * indent) + 'Args:'
    for p in input_params:
        docstring +=  '\n' + (' ' * (indent + 4)) + '{0} ({1}): '.format(p['python_name'], p['python_type'])
        if 'long_description' in p:
            docstring += get_indented_docstring_snippet(fix_references(p['long_description'], config, make_link=False), indent + 8)


    output_params = extract_output_parameters(function['parameters'])
    if len(output_params) > 0:
        docstring += '\n\n' + (' ' * indent) + 'Returns:'
        for p in output_params:
            docstring += '\n' + (' ' * (indent + 4)) + '{0} ({1}): '.format(p['python_name'], p['python_type'])
            if 'long_description' in p:
                docstring += get_indented_docstring_snippet(fix_references(p['long_description'], config, make_link=False), indent + 8)

    return docstring


# From http://code.activestate.com/recipes/579054-generate-sphinx-table/
def as_rest_table(data, full=False):
    """
    >>> from report_table import as_rest_table
    >>> data = [('what', 'how', 'who'),
    ...         ('lorem', 'that is a long value', 3.1415),
    ...         ('ipsum', 89798, 0.2)]
    >>> print as_rest_table(data, full=True)
    +-------+----------------------+--------+
    | what  | how                  | who    |
    +=======+======================+========+
    | lorem | that is a long value | 3.1415 |
    +-------+----------------------+--------+
    | ipsum |                89798 |    0.2 |
    +-------+----------------------+--------+

    >>> print as_rest_table(data)
    =====  ====================  ======
    what   how                   who
    =====  ====================  ======
    lorem  that is a long value  3.1415
    ipsum                 89798     0.2
    =====  ====================  ======

    """
    data = data if data else [['No Data']]
    table = []
    # max size of each column
    sizes = map(max, zip(*[[len(str(elt)) for elt in member]
                           for member in data]))
    if sys.version_info.major >= 3:
        sizes = list(sizes)
    num_elts = len(sizes)

    if full:
        start_of_line = '| '
        vertical_separator = ' | '
        end_of_line = ' |'
        line_marker = '-'
    else:
        start_of_line = ''
        vertical_separator = '  '
        end_of_line = ''
        line_marker = '='

    meta_template = vertical_separator.join(['{{{{{0}:{{{0}}}}}}}'.format(i)
                                             for i in range(num_elts)])
    template = '{0}{1}{2}'.format(start_of_line,
                                  meta_template.format(*sizes),
                                  end_of_line)
    # determine top/bottom borders
    if full:
        to_separator = {ord('|'): '+', ord(' '): '-'}
        if sys.version_info.major < 3:
            to_separator = string.maketrans('| ', '+-')
    else:
        to_separator = {ord('|'): '+'}
        if sys.version_info.major < 3:
            to_separator = string.maketrans('|', '+')
    start_of_line = start_of_line.translate(to_separator)
    vertical_separator = vertical_separator.translate(to_separator)
    end_of_line = end_of_line.translate(to_separator)
    separator = '{0}{1}{2}'.format(start_of_line,
                                   vertical_separator.join([x*line_marker for x in sizes]),
                                   end_of_line)
    # determine header separator
    th_separator_tr = {ord('-'): '='}
    if sys.version_info.major < 3:
        th_separator_tr = string.maketrans('-', '=')
    start_of_line = start_of_line.translate(th_separator_tr)
    line_marker = line_marker.translate(th_separator_tr)
    vertical_separator = vertical_separator.translate(th_separator_tr)
    end_of_line = end_of_line.translate(th_separator_tr)
    th_separator = '{0}{1}{2}'.format(start_of_line,
                                      vertical_separator.join([x*line_marker for x in sizes]),
                                      end_of_line)
    # prepare result
    table.append(separator)
    # set table header
    titles = data[0]
    table.append(template.format(*titles))
    table.append(th_separator)

    for d in data[1:-1]:
        table.append(template.format(*d))
        if full:
            table.append(separator)
    table.append(template.format(*data[-1]))
    table.append(separator)
    return '\n'.join(table)

# We need this to allow us to dynamically add and remove a folder to the search
# path becaise importlib.import_module() won't work with a module hierarchy in python2
@contextmanager
def add_to_path(p):
    import sys
    old_path = sys.path
    sys.path = sys.path[:]
    sys.path.insert(0, p)
    try:
        yield
    finally:
        sys.path = old_path

def get_python_type_from_visa_type(visa_type):
    if sys.version_info.major < 3:
        with add_to_path('build/templates'):
            p_types = importlib.import_module('python_types')
    else:
        p_types = importlib.import_module('build.templates.python_types')
    v_type = getattr(p_types, visa_type)
    p_type = v_type().python_type()

    return p_type


