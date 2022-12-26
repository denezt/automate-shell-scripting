#!/usr/bin/env python3

import argparse
from TemplateBuilder import TemplateBuilder

# Set Program Parameters
parser = argparse.ArgumentParser()
parser.add_argument('--datasource', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

# Read the JSON file containing the template data
datasource = args.datasource
output = args.output

if '__main__' == __name__:
  if output.endswith('.sh') and datasource.endswith('.json'):
    templateBuilder = TemplateBuilder(value="", collector="")
    template_data = templateBuilder.getTemplateData(datasource=datasource)
    # Generate the template
    template = templateBuilder.generate_template(template_data)
    print(template)
    # Write the template to a file
    if output.endswith('.sh'):
      with open(output, "w") as f:
        f.write(template)
      print("Template generated successfully!")