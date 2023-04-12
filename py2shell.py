#!/usr/bin/env python

import os
import argparse
from auto_shell_scripting import TemplateBuilder as TemplateBuilder
from auto_shell_scripting.utils import TemplateLister as TemplateLister

# Set Program Parameters
parser = argparse.ArgumentParser(
    prog='py2shell', description='Tool for automating shell scripts creation')
parser.add_argument('--make-executable', action='store_true',
                    default=False, help='Make script executable')
parser.add_argument('--exec', action='store_true',
                    default=False, help='Make script executable')
parser.add_argument('--datasource', type=str, help='Path to JSON data source')
parser.add_argument('--output', type=str,
                    help='Name of target output script name')
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
parser.add_argument("--templates", action="store_true",
                    help="Show available templates")

args = parser.parse_args()

# Read the JSON file containing the template data
datasource = args.datasource
output = args.output
view_templates = args.templates

if args.debug:
    print(args)

if '__main__' == __name__:
    if output is not None and datasource is not None:
        try:
            if output.endswith('.sh'):
                templateBuilder = TemplateBuilder.TemplateBuilder(
                    value="", collector="")
                template_data = templateBuilder.getTemplateData(
                    datasource=datasource)
                # Generate the template
                template = templateBuilder.generate_template(template_data)
                print(template)
                # Write the template to a file
                if output.endswith('.sh'):
                    if not os.path.exists("scripts"):
                        os.mkdir("scripts")
                    with open("scripts/{}".format(output), "w") as f:
                        f.write(template)
                    if args.make_executable or args.exec:
                        script_name = "scripts/{}".format(output)
                        if os.path.isfile(script_name):
                            print("Making, script executeable")
                            try:
                                os.chmod("{}".format(script_name), 777)
                            except FileNotFoundError as fnfe:
                                print(fnfe)
                    print("Template generated successfully!")
        except AttributeError as ae:
            pass
    if view_templates:
        t = TemplateLister.TemplateLister()
        t.createMenu()
