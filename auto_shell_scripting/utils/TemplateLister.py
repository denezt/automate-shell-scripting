#!/usr/bin/env python3.10

from dataclasses import dataclass
import json
import os
import string
import time


@dataclass
class TemplateLister:

    def getTemplates(self, path) -> str:
        results = []
        purpose = " - "
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                results.extend(self.getTemplates(full_path))
            else:
                strOutput = open(full_path,"r")
                obj = json.loads(strOutput.read())
                try:
                    purpose += "\033[32m{}".format(obj['purpose'])
                except Exception as e:
                    purpose = " - \033[31m{}".format('missing purpose')
                    pass
                results.append(entry.replace('.json', purpose))
        return results

    def createMenu(self):
        counter = 0
        templates = sorted(self.getTemplates("templates"))
        print("\033[36m==== Available Templates: ====\033[0m")
        for template in templates:
            counter += 1
            print("\033[33m{}: \033[35m{}\033[0m".format(counter, template))
