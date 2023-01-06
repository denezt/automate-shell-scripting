import os
import argparse
from auto_shell_scripting import TemplateBuilder as TemplateBuilder

# Set Program Parameters
parser = argparse.ArgumentParser(prog='py2shell', description='Tool for automating shell scripts creation')
parser.add_argument('--make-executable', action='store_true', default=False, help='Make script executable')
parser.add_argument('--exec', action='store_true', default=False, help='Make script executable')
parser.add_argument('--datasource', type=str, required=True, help='Path to JSON data source')
parser.add_argument('--output', type=str, required=True, help='Name of target output script name')
args = parser.parse_args()
print(args)
# Read the JSON file containing the template data
datasource = args.datasource
output = args.output

if '__main__' == __name__:
  if output.endswith('.sh') and datasource.endswith('.json'):
    templateBuilder = TemplateBuilder.TemplateBuilder(value="", collector="")
    template_data = templateBuilder.getTemplateData(datasource=datasource)
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
            os.chmod("{}".format(script_name),777)
          except FileNotFoundError as fnfe:
            print(fnfe)
      print("Template generated successfully!")
