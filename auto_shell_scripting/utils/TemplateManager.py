#!/usr/bin/env python3.10

from dataclasses import dataclass
import json
import os
import string
import time
from typing import List

@dataclass
class TemplateManager:
    # default purpose if not given
    dynatime: str = str(time.time()).split('.')[0]
    default_purpose: str = "Default purpose for template"
    default_target_path: str = "templates"
    default_filename: str = "template-{}".format(dynatime)

    def createTemplate(self, target_path: str = default_target_path, filename: str = default_filename, purpose: str = default_purpose) -> bool:
        template = "{}/{}.json".format(target_path, filename)
        if not os.path.exists(template):
            print("Creating Template, {}.".format(template))
            fp = open(template, "+w")
            content = "{{\"{}\": \"{}\"}}".format('purpose', self.default_purpose)
            fp.writelines(content)
            fp.close()
        else:
            print("Template {} already exist.".format(template))
        return True
