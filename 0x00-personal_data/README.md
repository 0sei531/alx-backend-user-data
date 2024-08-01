# 0x00. Personal data

## Description

This project involves creating a secure logging system that obfuscates personal data (PII) and implements authentication. It includes tasks such as filtering log messages, creating custom log formatters, securely connecting to a database, reading and filtering data, and encrypting passwords.

## Learning Objectives

By the end of this project, you should be able to:

- Identify examples of Personally Identifiable Information (PII).
- Implement a log filter that obfuscates PII fields.
- Encrypt passwords and validate input passwords.
- Authenticate to a database using environment variables.

## Requirements

- All files are interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7).
- All files should end with a new line.
- The first line of all files should be exactly `#!/usr/bin/env python3`.
- A `README.md` file at the root of the project folder is mandatory.
- Code should follow the pycodestyle style (version 2.5).
- All files must be executable.
- Modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`).
- Classes should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`).
- Functions should have documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`).
- Functions should be type annotated.

## Tasks

### Task 0: Regex-ing

**Objective:** Write a function `filter_datum` to obfuscate log messages.

```python
import re

def filter_datum(fields, redaction, message, separator):
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: m.group(0).split('=')[0] + '=' + redaction, message)
