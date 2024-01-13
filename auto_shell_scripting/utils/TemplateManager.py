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
    purpose: str = "Default purpose for template"

    def createTemplate(self, path, filename) -> str:
        results = []
        return results
