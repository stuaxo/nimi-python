# These dictionaries are applied to the generated functions dictionary at build time
# Any changes to the API should be made here. functions.py is code generated

# By default all functions in functions.py will be generated as a public function
# This will override that with private - add '_' to the beginning of the name, or
# don't generate at all
functions_codegen_method = {
    'InitWithOptions':  { 'codegen_method': 'private',  },
    'Initiate':         { 'codegen_method': 'private',  },
    'close':            { 'codegen_method': 'private',  },
    'Abort':            { 'codegen_method': 'private',  },
    'CheckAttribute.+': { 'codegen_method': 'no',       },  # We do not include any Check Attribute functions
    '.etAttribute.+':   { 'codegen_method': 'private',  },  # All Set/Get Attribute functions are private
    'init':             { 'codegen_method': 'no',       },
    'GetError':         { 'codegen_method': 'private',  },
    'GetErrorMessage':  { 'codegen_method': 'private',  },
    'ClearError':       { 'codegen_method': 'private',  },
    'Control':          { 'codegen_method': 'no',       },
    'LockSession':      { 'codegen_method': 'private',  },
    'UnlockSession':    { 'codegen_method': 'private',  },
    '.+ExtCal':         { 'codegen_method': 'no',       },  # External Calibration is not supported by the Python API
    'CalAdjust.+':      { 'codegen_method': 'no',       },  # External Calibration is not supported by the Python API
    '.+UserDefined.+':  { 'codegen_method': 'no',       },
    'SetCalPassword':   { 'codegen_method': 'no',       },
}

# Attach the given parameter to the given enum from enums.py
functions_enums = {
    'ConfigureTrigger':             { 'parameters': { 1: { 'enum': 'TriggerSource',             }, }, },
    'ConfigureMeasCompleteDest':    { 'parameters': { 1: { 'enum': 'MeasurementCompleteDest',   }, }, },
    'ConfigureMultiPoint':          { 'parameters': { 3: { 'enum': 'SampleTrigger',             }, }, },
    'ConfigureTriggerSlope':        { 'parameters': { 1: { 'enum': 'Slope',                     }, }, },
    'GetApertureTimeInfo':          { 'parameters': { 2: { 'enum': 'ApertureTimeUnits',         }, }, },
    'ConfigureAutoZeroMode':        { 'parameters': { 1: { 'enum': 'AutoZero',                  }, }, },
    'ConfigureMeasurementDigits':   { 'parameters': { 1: { 'enum': 'Function',                  }, }, },
    'ConfigureMeasurementAbsolute': { 'parameters': { 1: { 'enum': 'Function',                  }, }, },
    'ConfigureMeasCompleteSlope':   { 'parameters': { 1: { 'enum': 'Slope',                     }, }, },
    'ConfigureSampleTriggerSlope':  { 'parameters': { 1: { 'enum': 'Slope',                     }, }, },
    'ReadStatus':                   { 'parameters': { 2: { 'enum': 'AcquisitionStatus',         }, }, },
    'ConfigureADCCalibration':      { 'parameters': { 1: { 'enum': 'ADCCalibration',            }, }, },
    'ConfigureOffsetCompOhms':      { 'parameters': { 1: { 'enum': 'OffsetCompensatedOhms',     }, }, },
    'ConfigureCurrentSource':       { 'parameters': { 1: { 'enum': 'CurrentSource',             }, }, },
    'ConfigureCableCompType':       { 'parameters': { 1: { 'enum': 'CableCompensationType',     }, }, },
    'ConfigureWaveformAcquisition': { 'parameters': { 1: { 'enum': 'Function',                  }, }, },
    'ConfigureWaveformCoupling':    { 'parameters': { 1: { 'enum': 'WaveformCouplingMode',      }, }, },
    'ConfigureTransducerType':      { 'parameters': { 1: { 'enum': 'TemperatureTransducerType', }, }, },
    'ConfigureThermistorType':      { 'parameters': { 1: { 'enum': 'TemperatureThermistorType', }, }, },

}

# TODO(texasaggie97) can we get rid of this now that we are code generating the ivi-dance method of buffer retrieval?
functions_params_types = {
    'GetAttributeViString':         { 'parameters': { 4: { 'type': 'ViString',                  }, }, },
    'SetAttributeViString':         { 'parameters': { 3: { 'type': 'ViString',                  }, }, },
}

# This is the additional information needed by the code generator to properly generate the buffer retrieval mechanism
# {'is_buffer': True} is required for all parameters that are arrays. Some were able to be detected as an array when
#   generating functions.py. This sets 'is_buffer' for those parameters where the dectection didn't work
# {'size': <size information>} is required for all output buffers.
# <size information> is a dictionary with two keys: 'mechanism' and 'value'.
#   'mechanism' can be:
#       'fixed':        The size is known ahead of time, usually defined by the API.
#                       'value' should be an int.
#       'passed-in':    When the size comes from another parameter.
#                       'value' should be the name of the parameter through which this is specified.
#       'ivi-dance':    When the size is determined by calling into the function using a size of zero and
#                       interpreting the return value as a size rather than an error.
#                       'value' should be the name of the parameter through which the size (0, then the real
#                       one) is passed in. This parameter won't exist in the corresponding Python Session method.
functions_buffer_info = {
    'GetError':                     { 'parameters': { 3: { 'size': {'mechanism':'ivi-dance', 'value':'bufferSize'}, }, }, },
    'GetErrorMessage':              { 'parameters': { 3: { 'size': {'mechanism':'ivi-dance', 'value':'buffer_size'}, }, }, },
    'self_test':                    { 'parameters': { 2: { 'size': {'mechanism':'fixed', 'value':256}, }, }, }, # From documentation
    'ReadMultiPoint':               { 'parameters': { 3: { 'size': {'mechanism':'passed-in', 'value':'arraySize'}, }, }, },
    'FetchMultiPoint':              { 'parameters': { 3: { 'size': {'mechanism':'passed-in', 'value':'arraySize'}, }, }, },
    'FetchWaveform':                { 'parameters': { 3: { 'size': {'mechanism':'passed-in', 'value':'arraySize'}, }, }, },
    'ReadWaveform':                 { 'parameters': { 3: { 'size': {'mechanism':'passed-in', 'value':'arraySize'}, }, }, },
    'GetAttributeViString':         { 'parameters': { 4: { 'size': {'mechanism':'ivi-dance', 'value':'bufferSize'}, }, }, },
    'GetNextInterchangeWarning':    { 'parameters': { 2: { 'size': {'mechanism':'ivi-dance', 'value':'bufferSize'}, }, }, },
    'GetCalUserDefinedInfo':        { 'parameters': { 2: { 'size': {'mechanism':'fixed', 'value':256}, }, }, }, # From LabVIEW VI, even though niDMM_GetCalUserDefinedInfoMaxSize() exists.
    'init':                         { 'parameters': { 0: { 'is_buffer': True, }, }, },
    'InitWithOptions':              { 'parameters': { 0: { 'is_buffer': True, },
                                                      3: { 'is_buffer': True, }, }, },
    '.etAttribute.+':               { 'parameters': { 1: { 'is_buffer': True, }, }, },
    'CheckAttribute.+':             { 'parameters': { 1: { 'is_buffer': True, }, }, }, # Not actually used since CheckAttribute* not part of API
    'InitExtCal':                   { 'parameters': { 0: { 'is_buffer': True, }, }, }, # Not actually used since External Cal not part of API
    'GetDevTemp':                   { 'parameters': { 1: { 'is_buffer': True, }, }, },
}

