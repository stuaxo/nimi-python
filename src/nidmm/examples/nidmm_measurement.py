#!/usr/bin/python

import argparse
import nidmm
import sys

parser = argparse.ArgumentParser(description='Performs a single measurement using the NI-DMM API.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-n', '--name', default='PXI1Slot2', help='Resource name of a National Instruments Digital Multimeter.')
parser.add_argument('-f', '--function', default='DC_VOLTS', choices=nidmm.Function.__members__.keys(), type=str.upper, help='Measurement function.')
parser.add_argument('-r', '--range', default=10, type=float, help='Measurement range.')
parser.add_argument('-d', '--digits', default=6.5, type=float, help='Digits of resolution for the measurement.')
args = parser.parse_args()

try:
    with nidmm.Session(args.name) as session:
        session.configure_measurement_digits(nidmm.Function[args.function], args.range, args.digits)
        print(session.read(1000)) # TODO(marcoskirsch): Remove once we have default in the method
except nidmm.Error as e:
    sys.stderr.write(str(e))
    sys.exit(e.code)
