import ast
import os
import sys

violations = []

# Policy 1: No hardcoded API keys
with open("config.py", "r") as file:
    config_tree = ast.parse(file.read())

for node in ast.walk(config_tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "API_KEY":
                if isinstance(node.value, ast.Constant):
                    violations.append("Hardcoded API key detected")

# Policy 2: Debug mode must be disabled
debug_disabled = False

for node in ast.walk(config_tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "DEBUG":
                if isinstance(node.value, ast.Constant):
                    if node.value.value is False:
                        debug_disabled = True

if not debug_disabled:
    violations.append("Debug mode must be disabled")

# Policy 3: Application logging must use a separate file
with open("app.py", "r") as file:
    app_tree = ast.parse(file.read())

logging_enabled = False

for node in ast.walk(app_tree):
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "basicConfig":
                for keyword in node.keywords:
                    if keyword.arg == "filename":
                        if isinstance(keyword.value, ast.Constant):
                            if keyword.value.value == "logs/application.log":
                                logging_enabled = True

if not logging_enabled:
    violations.append(
        "Application logging to a separate file is not enabled"
    )

# Generate compliance report
report = "COMPLIANCE CHECK REPORT\n"
report += "======================\n\n"

if violations:
    report += "STATUS: NON-COMPLIANT\n\n"

    for violation in violations:
        report += "[FAIL] " + violation + "\n"
else:
    report += "STATUS: COMPLIANT\n\n"
    report += "[PASS] No hardcoded API keys\n"
    report += "[PASS] Debug mode disabled\n"
    report += "[PASS] Separate application logging enabled\n"

with open("compliance-report.txt", "w") as file:
    file.write(report)

print(report)

if violations:
    sys.exit(1)
else:
    sys.exit(0)
