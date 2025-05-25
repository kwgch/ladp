import re
import time # Added import

def parse_sexpression(s: str):
    """
    Parses a LADP s-expression string into a Python list structure.
    Handles symbols, numbers (int/float), and double-quoted strings.
    Example: "(msg update-status agent1 controller 1678886400000 (data (status active)))"
    should become:
    ['msg', 'update-status', 'agent1', 'controller', 1678886400000, ['data', ['status', 'active']]]
    """
    s = s.strip()
    if not s.startswith('(') or not s.endswith(')'):
        raise ValueError("S-expression must start with '(' and end with ')'")
    
    s = s[1:-1].strip() 
    
    if not s:
        return []

    tokens = []
    i = 0
    while i < len(s):
        char = s[i]
        
        if char.isspace():
            i += 1
            continue
        
        if char == '(': 
            balance = 1
            j = i + 1
            while j < len(s):
                if s[j] == '(':
                    balance += 1
                elif s[j] == ')':
                    balance -= 1
                if balance == 0:
                    break
                j += 1
            if balance != 0:
                raise ValueError("Unbalanced parentheses in s-expression")
            
            tokens.append(parse_sexpression(s[i:j+1]))
            i = j + 1
            continue
            
        if char == '"': 
            j = i + 1
            str_content = ""
            while j < len(s) and s[j] != '"': # Basic: doesn't handle escaped quotes in string
                str_content += s[j]
                j += 1
            if j == len(s) or s[j] != '"': 
                 raise ValueError("Unterminated string in s-expression")
            tokens.append(str_content)
            i = j + 1 
            continue

        match = re.match(r"^[^\s()\"]+", s[i:])
        if match:
            atom_str = match.group(0)
            try:
                if '.' in atom_str or 'e' in atom_str or 'E' in atom_str: 
                    tokens.append(float(atom_str))
                else:
                    tokens.append(int(atom_str))
            except ValueError:
                tokens.append(atom_str) 
            i += len(atom_str)
        else:
            raise ValueError(f"Unexpected character or structure at index {i}: '{s[i:]}'")
            
    return tokens

# New functions start here
def format_s_expression_component(component):
    """
    Recursively formats a component of a parsed s-expression back into a string.
    """
    if isinstance(component, list):
        return f"({format_s_expression(component)})" 
    elif isinstance(component, str) and (' ' in component or '(' in component or ')' in component or '"' in component):
        # Corrected escaping for f-string
        escaped_component = component.replace('"', '\\"')
        return f'"{escaped_component}"'
    else:
        return str(component)

def format_s_expression(parsed_list: list) -> str:
    """
    Converts a parsed s-expression (list structure) back into a string.
    """
    if not isinstance(parsed_list, list):
        raise TypeError("Input must be a list representing a parsed s-expression.")
    
    if not parsed_list:
        return "" # An empty list inside a sub-expression contributes nothing to join

    return " ".join(format_s_expression_component(item) for item in parsed_list)


def list_to_sexp_string(parsed_list: list) -> str:
    """
    Converts a Python list structure (parsed s-expression) into a LADP s-expression string.
    """
    if not isinstance(parsed_list, list):
        raise TypeError("Input must be a list representing a parsed s-expression.")

    if not parsed_list: 
        return "()"

    components = []
    for item in parsed_list:
        if isinstance(item, list):
            components.append(list_to_sexp_string(item)) 
        elif isinstance(item, str):
            # Corrected escaping for f-string
            if any(c in item for c in [' ', '(', ')', '"']) and not (item.startswith('"') and item.endswith('"')):
                 escaped_item = item.replace('"', '\\"')
                 components.append(f'"{escaped_item}"')
            elif item.startswith('"') and item.endswith('"'):
                components.append(item) # Assume already correctly quoted and escaped
            else:
                components.append(item)
        else: 
            components.append(str(item))
    return f"({' '.join(components)})"


def create_ladp_message(msg_type: str, sender: str, recipient: str, payload: list) -> list:
    """
    Creates a LADP message structure as a Python list.
    """
    epoch_ms = int(time.time() * 1000)
    if not (isinstance(payload, list) and len(payload) > 0 and payload[0] == 'data'):
        wrapped_payload = ['data']
        if isinstance(payload, list):
            wrapped_payload.extend(payload)
        else: 
            wrapped_payload.append(payload)
        final_payload = wrapped_payload
    else:
        final_payload = payload
        
    return ['msg', msg_type, sender, recipient, epoch_ms, final_payload]
# New functions end here

if __name__ == '__main__':
    # Test cases for parse_sexpression (existing)
    test_expressions = [
        ("(foo bar (baz qux) 123)", ['foo', 'bar', ['baz', 'qux'], 123]),
        ("(msg update-status agent1 controller 1678886400000 (data (status active)))", ['msg', 'update-status', 'agent1', 'controller', 1678886400000, ['data', ['status', 'active']]]),
        ("(data \"this is a string\" (value 10.5))", ['data', "this is a string", ['value', 10.5]]),
        ("(empty_payload (data))", ['empty_payload', ['data']]),
        ("(single_item)", ['single_item']), 
        ("(a (b (c)))", ['a', ['b', ['c']]]),
        ("(   lots   of   spaces  )", ['lots', 'of', 'spaces']),
        ("(with-hyphens and_underscores)", ["with-hyphens", "and_underscores"]),
        ("(\"string with spaces\")", ["string with spaces"]),
        ("()", []) 
    ]

    print("Running s-expression parser tests:")
    all_passed = True 
    parsing_passed = True
    for exp_str, expected_list in test_expressions:
        try:
            parsed = parse_sexpression(exp_str)
            if parsed == expected_list:
                print(f"PASS: '{exp_str}' -> {parsed}")
            else:
                print(f"FAIL: '{exp_str}' -> {parsed}, Expected: {expected_list}")
                parsing_passed = False
                all_passed = False
        except ValueError as e:
            print(f"ERROR parsing '{exp_str}': {e}")
            parsing_passed = False
            all_passed = False
            if expected_list == "ERROR": 
                 print(f"NOTE: Test was expected to error, and it did: '{exp_str}'")

    if parsing_passed:
        print("\nAll parsing tests passed!")
    else:
        print("\nSome parsing tests FAILED.")

    # New test cases start here
    print("\nTesting s-expression formatting (list_to_sexp_string):")
    format_test_cases = [
        (['foo', 'bar', ['baz', 'qux'], 123], "(foo bar (baz qux) 123)"),
        (['msg', 'update-status', 'agent1', 'controller', 1678886400000, ['data', ['status', 'active']]], 
         "(msg update-status agent1 controller 1678886400000 (data (status active)))"),
        (['data', "this is a string", ['value', 10.5]], '(data "this is a string" (value 10.5))'),
        ([], "()"), 
        (['a', ['b', []], 'c'], '(a (b ()) c)'), 
        (['item1', '"quoted string"'], '(item1 "quoted string")') 
    ]

    formatting_passed = True
    for py_list, expected_str in format_test_cases:
        try:
            s_exp_str = list_to_sexp_string(py_list)
            if s_exp_str == expected_str:
                print(f"PASS: {py_list} -> '{s_exp_str}'")
            else:
                print(f"FAIL: {py_list} -> '{s_exp_str}', Expected: '{expected_str}'")
                formatting_passed = False
                all_passed = False
        except Exception as e:
            print(f"ERROR formatting {py_list}: {e}")
            formatting_passed = False
            all_passed = False
    
    if formatting_passed:
        print("All formatting tests passed!")
    else:
        print("Some formatting tests FAILED.")


    print("\nTesting LADP message creation (create_ladp_message):")
    creation_test_cases = [
        (("status", "agentA", "controller", [['level', 10]]), 
         ['msg', 'status', 'agentA', 'controller', int(time.time()*1000), ['data', ['level', 10]]], 
         "(msg status agentA controller {NOW} (data (level 10)))"),
        
        (("query", "user", "agentB", ['data', ['text', "hello world"]]), 
         ['msg', 'query', 'user', 'agentB', int(time.time()*1000), ['data', ['text', "hello world"]]],
         '(msg query user agentB {NOW} (data (text "hello world")))')
    ]

    creation_passed = True
    for (args, expected_list_structure, expected_str_structure) in creation_test_cases:
        try:
            created_list = create_ladp_message(*args)
            current_time = created_list[4]
            expected_list_structure[4] = current_time 
            
            list_match = (created_list[:-1] == expected_list_structure[:-1] and 
                          created_list[-1] == expected_list_structure[-1] and 
                          isinstance(current_time, int))

            if list_match:
                print(f"PASS (list): create_ladp_message{args} -> {created_list}")
            else:
                print(f"FAIL (list): create_ladp_message{args} -> {created_list}, Expected structure: {expected_list_structure}")
                creation_passed = False
                all_passed = False

            created_str = list_to_sexp_string(created_list)
            expected_str_filled = expected_str_structure.replace("{NOW}", str(current_time))
            if created_str == expected_str_filled:
                 print(f"PASS (str): create_ladp_message{args} -> '{created_str}'")
            else:
                print(f"FAIL (str): create_ladp_message{args} -> '{created_str}', Expected: '{expected_str_filled}'")
                creation_passed = False
                all_passed = False

        except Exception as e:
            print(f"ERROR creating/formatting message for {args}: {e}")
            creation_passed = False
            all_passed = False

    if creation_passed:
        print("All message creation tests passed!")
    else:
        print("Some message creation tests FAILED.")

    if all_passed:
        print("\nAll PARSING, FORMATTING, and CREATION tests passed!")
    else:
        print("\nSome tests FAILED across parsing, formatting, or creation.")
