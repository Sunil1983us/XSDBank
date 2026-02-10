#!/usr/bin/env python3
"""
ISO 20022 External Code Sets Loader
Loads and provides access to ISO 20022 external code lists
"""

import json
from pathlib import Path

class ISO20022CodeSets:
    """Load and access ISO 20022 external code sets"""
    
    def __init__(self):
        self.codes = {}
        self._load_codes()
    
    def _load_codes(self):
        """Load external code sets from JSON file"""
        # Try multiple possible locations
        possible_locations = [
            Path(__file__).parent / 'data' / 'external_codes.json',
            Path(__file__).parent.parent / 'data' / 'external_codes.json',
            Path('data') / 'external_codes.json',
        ]
        
        for code_file in possible_locations:
            if code_file.exists():
                try:
                    with open(code_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.codes = data.get('definitions', {})
                    print(f"✅ Loaded {len(self.codes)} ISO 20022 code sets")
                    return
                except Exception as e:
                    print(f"⚠️  Warning: Could not load code sets: {e}")
                    continue
        
        print("⚠️  Warning: External code sets not found. Using generic values.")
    
    def get_code_values(self, code_set_name):
        """
        Get all valid values for a code set
        
        Args:
            code_set_name: Name like 'ExternalServiceLevel1Code'
        
        Returns:
            List of valid code values or empty list
        """
        if code_set_name in self.codes:
            return self.codes[code_set_name].get('enum', [])
        return []
    
    def get_sample_value(self, code_set_name):
        """
        Get a sample value from a code set
        
        Args:
            code_set_name: Name like 'ExternalServiceLevel1Code'
        
        Returns:
            First valid code value or None
        """
        values = self.get_code_values(code_set_name)
        return values[0] if values else None
    
    def has_code_set(self, code_set_name):
        """Check if a code set exists"""
        return code_set_name in self.codes
    
    def get_all_code_set_names(self):
        """Get list of all available code set names"""
        return list(self.codes.keys())


# Singleton instance
_code_sets_instance = None

def get_code_sets():
    """Get singleton instance of code sets"""
    global _code_sets_instance
    if _code_sets_instance is None:
        _code_sets_instance = ISO20022CodeSets()
    return _code_sets_instance


if __name__ == '__main__':
    # Test the loader
    codes = get_code_sets()
    print(f"\n📊 Available code sets: {len(codes.get_all_code_set_names())}")
    
    # Test some common ones
    test_codes = [
        'ExternalServiceLevel1Code',
        'ExternalCategoryPurpose1Code',
        'ExternalClearingSystemIdentification1Code'
    ]
    
    print("\n🧪 Testing sample code sets:")
    for code_name in test_codes:
        values = codes.get_code_values(code_name)
        if values:
            print(f"  {code_name}: {values[:5]}... ({len(values)} total)")
        else:
            print(f"  {code_name}: Not found")
