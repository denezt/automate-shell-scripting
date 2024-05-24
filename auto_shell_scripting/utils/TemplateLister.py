#!/usr/bin/env python3.10

from dataclasses import dataclass
import json
import os
import string
import time
from typing import List
from pathlib import Path

@dataclass
class TemplateLister:
    template_source: str = ""

    def getTemplates(self, path) -> str:
        results = []
        for entry in os.listdir(path):
            # Create empty object
            template_obj = {}
            # Get full path
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                results.extend(self.getTemplates(full_path))
            else:
                strOutput = open(full_path, "r")
                obj = json.loads(strOutput.read())
                template_obj["category"] = "\033[33m{}".format(obj['category'])
                template_obj["name"] = "\033[32m{}".format(obj["name"])
                template_obj["purpose"] = "\033[35m{}".format(obj['purpose'])
                results.append({ "name": template_obj["name"], "purpose": template_obj["purpose"], "category": template_obj["category"]})
        return results

    def createMenu(self):
        counter = 0
        try:
            templates = self.getTemplates(self.template_source)
            print("\033[36m==== Available Templates: ====\033[0m")
            for template in templates:
                counter += 1
                print("\033[36m{}: {}::{} - {}".format(counter, template["category"], template["name"], template["purpose"]))
        except FileNotFoundError as fnfe:
            print("Error: Please run the setup script!")
            print(f"{fnfe}")
