from typing import Dict, Any

class V55RulePerformanceRegistry:
    def __init__(self):
        self.rules: Dict[str, Dict[str, Any]] = {}

    def record(self, rule_id: str, success: bool):
        if rule_id not in self.rules:
            self.rules[rule_id] = {"invocations": 0, "tp": 0, "fp": 0}
        self.rules[rule_id]["invocations"] += 1
        if success:
            self.rules[rule_id]["tp"] += 1
        else:
            self.rules[rule_id]["fp"] += 1

v55_rule_registry = V55RulePerformanceRegistry()
