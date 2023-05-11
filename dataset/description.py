def description(cl):
    try:
        description = {
        "CWE427": {
            "heading": "Uncontrolled search path element",
            "description": "The product uses a fixed or controlled search path to find resources, but one or more locations in that path can be under the control of unintended actors.Although this weakness can occur with any type of resource, it is frequently introduced when a product uses a directory search path to find executables or code libraries, but the path contains a directory that can be modified by an attacker, such as '/tmp' or the current working directory.",
            "link": "https://www.cybersecurity-help.cz/vdb/cwe/427/"
        },
        "CWE114":{
            "heading":"Process control",
            "description":"Executing commands or loading libraries from an untrusted source or in an untrusted environment can cause an application to execute malicious commands (and payloads) on behalf of an attacker.Process control vulnerabilities take two forms: 1. An attacker can change the command that the program executes: the attacker explicitly controls what the command is. 2. An attacker can change the environment in which the command executes: the attacker implicitly controls what the command means. Process control vulnerabilities of the first type occur when either data enters the application from an untrusted source and the data is used as part of a string representing a command that is executed by the application. By executing the command, the application gives an attacker a privilege or capability that the attacker would not otherwise have.",
            "link":"https://cwe.mitre.org/data/definitions/114.html"
        }
        }
        return description[cl]
    except:
        return {"heading":"","description":"Description not found","link":""}