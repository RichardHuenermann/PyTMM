""" This file contains code needed for the link to matlab
"""
import argparse
import sys

from PyTMM import Material, RefractiveIndex

parser = argparse.ArgumentParser(
    description="Returns refractive index of material for specified wavelength")
parser.add_argument('catalog')
parser.add_argument('section')
parser.add_argument('book')
parser.add_argument('page')
parser.add_argument('wavelength')

args = parser.parse_args()
catalog = RefractiveIndex(args.catalog)
catalog_path = catalog.get_material_file(args.section, args.book, args.page)
material = Material(catalog_path)
sys.stdout.write(str(material.get_refractive_index(float(args.wavelength))))
