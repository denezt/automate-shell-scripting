#!/usr/bin/env python3

from dataclasses import dataclass
import json
import os
import string
import time


@dataclass
class TemplateBuilder:
    value: str
    collector: str

    def buildIfStatement(self, if_statement: dict) -> str:
        statement_builder = ""
        print("Building, if statement")
        if_statements = ""
        goal = ""
        for key, value in if_statement:
            if key == "goal":
                goal = value
            if key == "run":
                for k in value:
                    if_statements += "\t{}".format(self.iterateRun(k))
        if if_statements:
            statement_builder += "\n"
            statement_builder += "if [ {} ]; then\n".format(goal)
            statement_builder += if_statements
            statement_builder += "fi\n"
        return statement_builder

    def buildCaseStatement(self, case_statement: dict) -> str:
        print("Building, case statement")
        switch_array = ""
        statement_builder = ""
        goal = ""
        for key, value in case_statement:
            if key == "goal":
                goal = value
            if key == "switch":
                for val in value:
                    for parameter, statement in val.items():
                        switch_array += "\t{}) {};;\n".format(
                            parameter, statement)
        statement_builder += "case ${} in\n".format(goal)
        statement_builder += switch_array
        statement_builder += "esac\n"
        return statement_builder

    def buildNestedCaseStatement(self, case_statement: dict) -> str:
        print("Building, case statement")
        switch_array = ""
        statement_builder = ""
        goal = ""
        for key, value in case_statement:
            if key == "goal":
                goal = value
            if key == "switch":
                for val in value:
                    for parameter, statement in val.items():
                        switch_array += "\t\t{}) {};;\n".format(
                            parameter, statement)
        statement_builder += "\tcase ${} in\n".format(goal)
        statement_builder += switch_array
        statement_builder += "\tesac\n"
        return statement_builder

    def buildForStatement(self, loop_statement: dict) -> str:
        print("Building, loop statement")
        statement_builder = ""
        for_statements = ""
        goal = ""
        for key, value in loop_statement:
            if key == "goal":
                goal = value
            if key == "run":
                for k in value:
                    for_statements += "\t{}".format(self.iterateRun(k))
        if for_statements:
            statement_builder += "for (( {} )) ; do\n".format(goal)
            statement_builder += for_statements
            statement_builder += "done\n"
        return statement_builder

    def buildWhileStatement(self, loop_statement: dict) -> str:
        print("Building, loop statement")
        statement_builder = ""
        while_statements = ""
        goal = ""
        for key, value in loop_statement:
            if key == "goal":
                goal = value
            if key == "run":
                for k in value:
                    if k.keys().__contains__('conditions'):
                        condition = [_v for _k, _v in k.items()][0]
                        while_statements += "{}".format(
                            self.getConditionBuilder(condition))
                    else:
                        while_statements += "\t{}".format(self.iterateRun(k))
        if while_statements:
            statement_builder += "while [ {} ]; do\n".format(goal)
            statement_builder += while_statements
            statement_builder += "done\n"
        return statement_builder

    def getConditionBuilder(self, value) -> str:
        template = ""
        for arr in value:
            # Get Condition Type
            condition_type = [v for k, v in arr.items()][0]
            if condition_type == "if":
                template += self.buildIfStatement(arr.items())
            elif condition_type == "case":
                template += self.buildCaseStatement(arr.items())
            elif condition_type == "case.nested":
                template += self.buildNestedCaseStatement(arr.items())
            elif condition_type == "for":
                template += self.buildForStatement(arr.items())
            elif condition_type == "while":
                template += self.buildWhileStatement(arr.items())
        return template

    def buildFunction(self, function: dict) -> str:
        print("Building, function statement")
        statement_builder = ""
        statements = ""
        name = ""
        for key, value in function:
            if key == "name":
                name = value
            if key == "statements":
                for stmt in value:
                    if stmt.keys().__contains__('conditions'):
                        condition = [v for k, v in stmt.items()][0]
                        statements += self.getConditionBuilder(condition)
                    else:
                        statements += "\t" + self.iterateRun(stmt)
            if key == "control" or key == "onliner":
                statements += "\t" + self.buildOnliner(value)
        if statements:
            statement_builder += "{}(){}".format(name, '{\n')
            statement_builder += statements
            statement_builder += "}\n"
        return statement_builder

    def replaceMetaTag(self, variable: str) -> str:
        variable = variable.replace('__SPACE__', ' ')
        variable = variable.replace('__BEGIN__', '\"')
        variable = variable.replace('__NEWLINE__', '\\n')
        variable = variable.replace('__END__', '\"')
        return variable

    def buildControl(self, value: dict) -> str:
        line = ""
        key = list(value.keys())
        values = list(value.values())
        for v in values[0]:
            line += self.replaceMetaTag(v)
        return "\n{} {}".format(key[0], line)

    def buildOnliner(self, value: dict) -> str:
        line = ""
        key = list(value.keys())
        values = list(value.values())
        for v in values[0]:
            line += self.replaceMetaTag(v)
        return "{} {}\n".format(key[0], line)

    # Normal nested inside of a conditional statement, function and loops
    def iterateRun(self, template_data: dict) -> str:
        line_statement = ""
        run_type = ""
        try:
            for key, value in template_data.items():
                if key == "type":
                    run_type = value
                elif run_type == "parameter" and key != "type":
                    line_statement += "{} \"{}\"\n".format(key, value)
                elif run_type == "declare" and key != "type":
                    line_statement += "{}={}\n".format(key, value)
                elif run_type == "command_call" and key != "type":
                    line_statement += self.buildOnliner(dict({key: value}))
        except AttributeError as ae:
            print(
                "Check datasource syntax and ensure you are using the correct datatype (array, object)")
            print(ae)
            exit(1)
        return line_statement

    def getTemplateData(self, templates, datasource: str) -> dict:
        template_data = {}
        try:
            # Remove extension if present
            datasource = datasource.replace('::', '/')
            datasource = "{}/{}.json".format(templates, datasource)            
            if os.path.exists(datasource):
                with open(datasource, "r") as f:
                    template_data = json.load(f)
            else:
                print("\033[35mWarning: \033[33mMissing or unable to find template (name: {})\033[0m".format(
                    datasource))
        except Exception as e:
            print(
                "Error: Missing or unable to find template (name: {})".format(datasource))
        return template_data

    def generate_template(self, template_data: dict) -> str:
        template = ""
        for key, value in template_data.items():
            if key in ["purpose"]:
                print("\033[36mPURPOSE: \033[33m{}\033[0m".format(value))
            # Writes the initial shell
            if key in ["shell.type"]:
                print("Shell Type is {}".format(value))
                template += "#!/usr/bin/env {}\n\n".format(value)
                # template += "set -x\n\n"
            elif key in ["define.variables"]:
                # Creates a lot of variables
                for k, v in value.items():
                    template += "{}={}\n".format(k, v)
            elif key in ["conditions"]:
                # Iterate
                template += self.getConditionBuilder(value)
            elif key in ["functions"]:
                for arr in value:
                    template += self.buildFunction(arr.items())
            elif key in ["control"] or key in ["command_call"]:
                template += self.buildControl(value)
            elif key in ["onliner"]:
                template += self.buildOnliner(value)
        return template
