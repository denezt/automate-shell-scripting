#!/usr/bin/env python

import sys
import os
import argparse
from auto_shell_scripting import TemplateBuilder as TemplateBuilder
from auto_shell_scripting.utils import TemplateLister as TemplateLister
from auto_shell_scripting.utils import TemplateManager as TemplateManager

from configparser import ConfigParser

# Get Configuration
'''
 @ToDo: Create a configuration parser in order to set parameters
 and remove static values in code.
'''

# Set Program Parameters
parser = argparse.ArgumentParser(
    prog='py2shell', description='Tool for automating shell scripts creation')
parser.add_argument('--datasource','-ds','--source','-s', type=str, help='Path to JSON data source')
parser.add_argument('--output','-o', type=str, help='Name of target output script name')
parser.add_argument('--debug','-d','--verbose','-v', action="store_true", help="Enable debug mode")
parser.add_argument('--make-executable','-me', action='store_true', default=False, help='Make script executable')
parser.add_argument('--templates','-t', action="store_true", default=False, help="Show available templates")
# Planned feature to append templates
# parser.add_argument('--declare', '--funcs', '--stmts', action="append")
# ./py2shell --declare declarations --funcs functions --stmts statements --output full-script.sh
# Namespace(n=['declarations', 'functions', 'statements'])

args = parser.parse_args()

if args.debug:
    print(args)

# Read the JSON file containing the template data
datasource = args.datasource

output = args.output
view_templates = args.templates
make_executable = args.make_executable

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
                    script_name = "scripts/{}".format(output)
                    # Automatically make scripts executeable
                    if os.path.isfile(script_name):
                        if make_executable:
                            print(f"\033[35mMaking, scripts \033[36m{script_name} \033[35mexecutable.\033[0m")
                            try:
                                os.chmod("{}".format(script_name), 0o777)
                            except FileNotFoundError as fnfe:
                                print(fnfe)
                        else:
                            print(f"\033[35mCreated, non-executable script \033[36m{script_name}\033[0m")
                    print("\033[32mTemplate generated successfully!\033[0m")
            else:
                print("Error: Output script name must end with an '.sh' extension")
        except AttributeError as ae:
            pass
    elif view_templates:
        t = TemplateLister.TemplateLister()
        t.createMenu()
    else:
        print("Missing target output name or datasource template")
