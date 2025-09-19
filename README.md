# Relational Algebra Query Processor
## COMP3005 - Bouns Assignment #1

A simple Python implementation of a relational algebra system that can parse text-based relations and execute relational algebra queries.

## Author

**Name:** Bashar Saadi

## Features

- **Selection (σ)** - Filter rows based on conditions
- **Projection (π)** - Select specific columns
- **Join (⋈)** - Natural join between relations
- **Union (∪)** - Combine relations with same schema
- **Intersection (∩)** - Find common tuples between relations
- **Difference (-)** - Find tuples in first relation but not in second
- **Easy to extend** - Simple modular design for adding new operations

## How to Use

1. Define your relations and queries in `input.txt`
2. Run the system: `python3 relational_algebra.py`
3. View results in `output.txt`

## Input Format

### Relations

```
RelationName (attr1, attr2, attr3) = {
  value1, value2, value3
  value4, value5, value6
}
```

### Queries

```
Query: select condition (RelationName)
Query: project attr1, attr2 (RelationName)
Query: join Relation1 Relation2
Query: union Relation1 Relation2
Query: intersect Relation1 Relation2
Query: difference Relation1 Relation2
```

## Quick Demo

**Input (`input.txt`):**

```
Employees (EID, Name, Age) = {
  E1, John, 32
  E2, Alice, 28
  E3, Bob, 29
}

Query: select Age > 30 (Employees)
Query: project Name (Employees)
```

**Output (`output.txt`):**

```
Query 1: select Age > 30 (Employees)
========================================
Result = {EID, Name, Age
  "E1", "John", 32
}

Query 2: project Name (Employees)
========================================
Result = {Name
  "John"
  "Alice"
  "Bob"
}
```

## Supported Operations

| Operation    | Syntax                              | Example                           |
| ------------ | ----------------------------------- | --------------------------------- |
| Selection    | `select condition (relation)`     | `select Age > 25 (Employees)`   |
| Projection   | `project attr1, attr2 (relation)` | `project Name, Age (Employees)` |
| Join         | `join relation1 relation2`        | `join Employees Departments`    |
| Union        | `union relation1 relation2`       | `union Employees Students`      |
| Intersection | `intersect relation1 relation2`   | `intersect Students Employees`  |
| Difference   | `difference relation1 relation2`  | `difference Students Employees` |

## File Structure

- `query_processor.py` - Main system implementation
- `input.txt` - Input relations and queries
- `output.txt` - Generated query results
- `README.md` - This documentation

## Implementation Notes

- All operations implemented from scratch using core Python
- No external libraries (pandas, etc.) used
- Simple modular design for easy extension
- Supports multiple relations and comprehensive query testing
