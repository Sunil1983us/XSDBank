#!/usr/bin/env python3
"""
Usage Rules Parser for ISO 20022
Parses rules like "Either 'Structured' or 'Unstructured'"
"""

import re

class UsageRulesParser:
    """Parse and apply ISO 20022 usage rules"""
    
    @staticmethod
    def parse_either_or_rule(rule_text):
        """
        Parse rules like: "Either 'Structured' or 'Unstructured' may be present."
        Returns: list of options or None
        """
        if not rule_text:
            return None
            
        # Pattern: Either 'X' or 'Y'
        pattern = r"Either\s+'([^']+)'\s+or\s+'([^']+)'"
        match = re.search(pattern, rule_text)
        if match:
            return [match.group(1), match.group(2)]
        
        # Pattern: Either X or Y (without quotes)
        pattern2 = r"Either\s+(\w+)\s+or\s+(\w+)"
        match2 = re.search(pattern2, rule_text)
        if match2:
            return [match2.group(1), match2.group(2)]
        
        return None
    
    @staticmethod  
    def should_exclude_field(field_name, selected_option, rule_text):
        """
        Determine if a field should be excluded based on selected option
        
        Example:
          rule_text = "Either 'Structured' or 'Unstructured' may be present."
          selected_option = "Structured"
          field_name = "Unstrd"
          Returns: True (exclude Unstrd because we selected Structured)
        """
        options = UsageRulesParser.parse_either_or_rule(rule_text)
        if not options:
            return False
        
        # If we selected one option, exclude fields matching the other option
        field_lower = field_name.lower()
        
        for i, option in enumerate(options):
            option_lower = option.lower()
            other_option_lower = options[1-i].lower()
            
            # If field matches the option we didn't select, exclude it
            if other_option_lower in field_lower and option_lower == selected_option.lower():
                return True
        
        return False


if __name__ == '__main__':
    # Test
    parser = UsageRulesParser()
    
    rule = "Either 'Structured' or 'Unstructured' may be present."
    options = parser.parse_either_or_rule(rule)
    print(f"Rule: {rule}")
    print(f"Options: {options}")
    
    print(f"\nIf we select 'Structured':")
    print(f"  Include 'Strd' field? {not parser.should_exclude_field('Strd', 'Structured', rule)}")
    print(f"  Include 'Unstrd' field? {not parser.should_exclude_field('Unstrd', 'Structured', rule)}")
