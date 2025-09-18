import re

# Global storage for relations
relations = {}

def parse_relation(text):
    """Parse a relation definition and store it."""
    # Format: RelationName (attr1, attr2, attr3) = { tuple1 tuple2 ... }
    # Extract relation name and attributes
    header_match = re.match(r'(\w+)\s*\(([^)]+)\)\s*=\s*\{', text)
    if not header_match:
        return

    name = header_match.group(1)
    attrs = [attr.strip() for attr in header_match.group(2).split(',')]

    # Extract everything between { and }
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1:
        return

    tuples_text = text[start+1:end].strip()

    # Parse tuples
    tuples = []
    if tuples_text:
        # Split by lines and parse each tuple
        for tuple_line in tuples_text.split('\n'):
            tuple_line = tuple_line.strip()
            if tuple_line and not tuple_line.startswith('#'):
                # Split by comma and clean up values
                values = [val.strip().strip('"') for val in tuple_line.split(',')]
                # Try to convert numbers
                converted_values = []
                for val in values:
                    try:
                        converted_values.append(int(val))
                    except ValueError:
                        converted_values.append(val)
                tuples.append(converted_values)

    relations[name] = {
        'attributes': attrs,
        'tuples': tuples
    }

def select_operation(relation_name, condition):
    """Perform selection operation."""
    if relation_name not in relations:
        return None

    rel = relations[relation_name]
    result_tuples = []

    for tuple_data in rel['tuples']:
        if evaluate_condition(condition, rel['attributes'], tuple_data):
            result_tuples.append(tuple_data)

    return {
        'attributes': rel['attributes'],
        'tuples': result_tuples
    }

def project_operation(relation_name, attributes):
    """Perform projection operation."""
    if relation_name not in relations:
        return None

    rel = relations[relation_name]

    # Find indices of requested attributes
    indices = []
    for attr in attributes:
        if attr in rel['attributes']:
            indices.append(rel['attributes'].index(attr))

    result_tuples = []
    seen = set()

    for tuple_data in rel['tuples']:
        projected = tuple([tuple_data[i] for i in indices])
        if projected not in seen:
            seen.add(projected)
            result_tuples.append(list(projected))

    return {
        'attributes': attributes,
        'tuples': result_tuples
    }

def evaluate_condition(condition, attributes, tuple_data):
    """Evaluate a condition against a tuple."""
    # Simple condition parsing: attribute operator value
    for op in ['>=', '<=', '>', '<', '=', '!=']:
        if op in condition:
            parts = condition.split(op)
            if len(parts) == 2:
                attr = parts[0].strip()
                value = parts[1].strip()

                if attr in attributes:
                    attr_index = attributes.index(attr)
                    tuple_value = tuple_data[attr_index]

                    # Try to convert value to int if possible
                    try:
                        value = int(value)
                    except ValueError:
                        value = value.strip('"\'')

                    # Evaluate condition
                    if op == '>':
                        return tuple_value > value
                    elif op == '<':
                        return tuple_value < value
                    elif op == '>=':
                        return tuple_value >= value
                    elif op == '<=':
                        return tuple_value <= value
                    elif op == '=' or op == '==':
                        return tuple_value == value
                    elif op == '!=':
                        return tuple_value != value

    return False

def join_operation(relation1_name, relation2_name, condition):
    """Perform natural join operation."""
    if relation1_name not in relations or relation2_name not in relations:
        return None

    rel1 = relations[relation1_name]
    rel2 = relations[relation2_name]

    # Simple equi-join implementation
    result_tuples = []

    # Find common attributes
    common_attrs = set(rel1['attributes']).intersection(set(rel2['attributes']))

    # Create combined attributes (no duplicates)
    result_attrs = rel1['attributes'][:]
    for attr in rel2['attributes']:
        if attr not in result_attrs:
            result_attrs.append(attr)

    # Join tuples
    for tuple1 in rel1['tuples']:
        for tuple2 in rel2['tuples']:
            # Check if join condition is satisfied
            join_valid = True
            for attr in common_attrs:
                idx1 = rel1['attributes'].index(attr)
                idx2 = rel2['attributes'].index(attr)
                if tuple1[idx1] != tuple2[idx2]:
                    join_valid = False
                    break

            if join_valid:
                # Combine tuples
                combined = tuple1[:]
                for i, attr in enumerate(rel2['attributes']):
                    if attr not in rel1['attributes']:
                        combined.append(tuple2[i])
                result_tuples.append(combined)

    return {
        'attributes': result_attrs,
        'tuples': result_tuples
    }

def union_operation(relation1_name, relation2_name):
    """Perform union operation."""
    if relation1_name not in relations or relation2_name not in relations:
        return None

    rel1 = relations[relation1_name]
    rel2 = relations[relation2_name]

    # Check schema compatibility
    if rel1['attributes'] != rel2['attributes']:
        return None

    result_tuples = []
    seen = set()

    # Add tuples from both relations (no duplicates)
    for tuple_data in rel1['tuples'] + rel2['tuples']:
        tuple_key = tuple(tuple_data)
        if tuple_key not in seen:
            seen.add(tuple_key)
            result_tuples.append(tuple_data)

    return {
        'attributes': rel1['attributes'],
        'tuples': result_tuples
    }

def intersection_operation(relation1_name, relation2_name):
    """Perform intersection operation."""
    if relation1_name not in relations or relation2_name not in relations:
        return None

    rel1 = relations[relation1_name]
    rel2 = relations[relation2_name]

    # Check schema compatibility
    if rel1['attributes'] != rel2['attributes']:
        return None

    result_tuples = []
    seen = set()

    # Find tuples that exist in both relations
    rel2_tuples = set(tuple(t) for t in rel2['tuples'])

    for tuple_data in rel1['tuples']:
        tuple_key = tuple(tuple_data)
        if tuple_key in rel2_tuples and tuple_key not in seen:
            seen.add(tuple_key)
            result_tuples.append(tuple_data)

    return {
        'attributes': rel1['attributes'],
        'tuples': result_tuples
    }

def difference_operation(relation1_name, relation2_name):
    """Perform difference operation (rel1 - rel2)."""
    if relation1_name not in relations or relation2_name not in relations:
        return None

    rel1 = relations[relation1_name]
    rel2 = relations[relation2_name]

    # Check schema compatibility
    if rel1['attributes'] != rel2['attributes']:
        return None

    result_tuples = []
    seen = set()

    # Find tuples that exist in rel1 but not in rel2
    rel2_tuples = set(tuple(t) for t in rel2['tuples'])

    for tuple_data in rel1['tuples']:
        tuple_key = tuple(tuple_data)
        if tuple_key not in rel2_tuples and tuple_key not in seen:
            seen.add(tuple_key)
            result_tuples.append(tuple_data)

    return {
        'attributes': rel1['attributes'],
        'tuples': result_tuples
    }

def execute_on_result(operation_result, operation_func, *args):
    """Execute an operation on a result relation."""
    if not operation_result:
        return None

    # Create a temporary relation name
    temp_name = "temp_result"

    # Store the result as a temporary relation
    relations[temp_name] = operation_result

    # Execute the operation
    result = operation_func(temp_name, *args)

    # Clean up temporary relation
    del relations[temp_name]

    return result

def parse_query(query):
    """Parse and execute a query, supporting nested operations."""
    query = query.strip()

    # Handle nested operations by parsing inside out
    # Look for patterns like: operation (nested_operation (relation))

    # Projection with nested operation: project attrs (nested_query)
    nested_project_match = re.match(r'project\s+(.+?)\s*\(\s*(.+)\s*\)', query)
    if nested_project_match:
        attrs_str = nested_project_match.group(1).strip()
        inner_query = nested_project_match.group(2).strip()

        # Check if inner query is just a relation name
        if re.match(r'^\w+$', inner_query):
            # Simple relation name
            attributes = [attr.strip() for attr in attrs_str.split(',')]
            return project_operation(inner_query, attributes)
        else:
            # Nested query - execute inner query first
            inner_result = parse_query(inner_query)
            if inner_result:
                attributes = [attr.strip() for attr in attrs_str.split(',')]
                return execute_on_result(inner_result, project_operation, attributes)

    # Selection with nested operation: select condition (nested_query)
    nested_select_match = re.match(r'select\s+(.+?)\s*\(\s*(.+)\s*\)', query)
    if nested_select_match:
        condition = nested_select_match.group(1).strip()
        inner_query = nested_select_match.group(2).strip()

        # Check if inner query is just a relation name
        if re.match(r'^\w+$', inner_query):
            # Simple relation name
            return select_operation(inner_query, condition)
        else:
            # Nested query - execute inner query first
            inner_result = parse_query(inner_query)
            if inner_result:
                return execute_on_result(inner_result, select_operation, condition)

    # Join query: join relation1 relation2
    join_match = re.match(r'join\s+(\w+)\s+(\w+)', query)
    if join_match:
        rel1 = join_match.group(1)
        rel2 = join_match.group(2)
        return join_operation(rel1, rel2, None)

    # Union query: union relation1 relation2
    union_match = re.match(r'union\s+(\w+)\s+(\w+)', query)
    if union_match:
        rel1 = union_match.group(1)
        rel2 = union_match.group(2)
        return union_operation(rel1, rel2)

    # Intersection query: intersection relation1 relation2
    intersection_match = re.match(r'intersection\s+(\w+)\s+(\w+)', query)
    if intersection_match:
        rel1 = intersection_match.group(1)
        rel2 = intersection_match.group(2)
        return intersection_operation(rel1, rel2)

    # Difference query: difference relation1 relation2
    difference_match = re.match(r'difference\s+(\w+)\s+(\w+)', query)
    if difference_match:
        rel1 = difference_match.group(1)
        rel2 = difference_match.group(2)
        return difference_operation(rel1, rel2)

    return None

def format_result(result, relation_name="Result"):
    """Format result for output."""
    if not result or not result['tuples']:
        return f"{relation_name} = {{}} (empty result)\n"

    output = f"{relation_name} = {{{', '.join(result['attributes'])}\n"
    for tuple_data in result['tuples']:
        tuple_str = ', '.join(f'"{val}"' if isinstance(val, str) else str(val) for val in tuple_data)
        output += f"  {tuple_str}\n"
    output += "}\n"

    return output

def parse_all_relations(content):
    """Parse all relation definitions from content."""
    # Split content into sections by looking for relation patterns
    relation_pattern = r'(\w+)\s*\([^)]+\)\s*=\s*\{'

    # Find all relation starts
    matches = list(re.finditer(relation_pattern, content))

    for i, match in enumerate(matches):
        start = match.start()
        # Find the end of this relation (next relation start or end of content)
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)

        relation_text = content[start:end]
        parse_relation(relation_text)

def main():
    """Main function to process input and generate output."""
    try:
        with open('input.txt', 'r') as f:
            content = f.read()

        # Parse all relations
        parse_all_relations(content)

        # Extract queries
        queries = []
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('Query:'):
                # Extract query after "Query:"
                query = line[6:].strip()
                queries.append(query)
            elif any(line.startswith(op) for op in ['select', 'project', 'join', 'union', 'intersection', 'difference']):
                # Direct query
                queries.append(line)

        # Execute queries and write output
        with open('output.txt', 'w') as f:
            for i, query in enumerate(queries):
                f.write(f"Query {i+1}: {query}\n")
                f.write("=" * 40 + "\n")
                result = parse_query(query)
                if result:
                    f.write(format_result(result))
                else:
                    f.write(f"Error: Could not execute query '{query}'\n")
                f.write('\n')

    except FileNotFoundError:
        print("Error: input.txt not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    print("Query executed. Results written to output.txt")