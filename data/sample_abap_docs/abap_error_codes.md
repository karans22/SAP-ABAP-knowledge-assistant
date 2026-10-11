# Common ABAP Runtime Errors and SY-SUBRC Codes

## SY-SUBRC reference

`SY-SUBRC` is the system field that reports the return status of the last
executed ABAP statement. `0` typically means success; nonzero values are
statement-specific.

| Statement | SY-SUBRC | Meaning |
|---|---|---|
| SELECT SINGLE | 4 | No matching record found |
| READ TABLE | 4 | Line not found in internal table |
| CALL FUNCTION | 1–99 | Exception raised by the function module (check the EXCEPTIONS list) |
| OPEN CURSOR | 8 | Cursor could not be opened |
| INSERT (database) | 4 | Record already exists (duplicate key) |

## Frequently encountered dumps

- **DBIF_RSQL_INVALID_RSQL**: Usually caused by a malformed Open SQL
  statement, such as referencing a non-existent field alias or an
  unsupported function in the WHERE clause.
- **CONVT_NO_NUMBER**: Occurs when attempting to convert a non-numeric
  string into a numeric type. Common in file uploads with unexpected
  characters in numeric columns — validate input before conversion.
- **TABLE_INVALID_INDEX**: Raised when accessing an internal table by
  index outside its current bounds (e.g. `itab[ 5 ]` when the table has
  only 3 rows). Prefer `READ TABLE ... TRANSPORTING NO FIELDS` with a
  SY-SUBRC check over direct index access when the row count is uncertain.
- **MESSAGE_TYPE_X**: A generic short dump raised by an explicit
  `MESSAGE ... TYPE 'X'` in custom code, usually indicating an
  unrecoverable business-logic error the developer intentionally raised.

## Debugging approach

1. Reproduce the issue with `/h` in the command field to enter debug mode.
2. Check SY-SUBRC immediately after the suspect statement.
3. For dumps, review transaction `ST22` for the full call stack and
   variable state at the time of the dump.
4. For performance-related issues, use `SAT` (runtime analysis) or `ST05`
   (SQL trace) to identify expensive statements.
