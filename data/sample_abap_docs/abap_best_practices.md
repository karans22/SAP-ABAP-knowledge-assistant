# ABAP Development Best Practices

## Clean ABAP principles

- Prefer `LOOP AT itab ASSIGNING <fs>` over `LOOP AT itab INTO wa` when
  modifying rows in place, to avoid unnecessary copy overhead.
- Use `VALUE`, `COND`, and `REDUCE` constructor expressions for concise,
  readable functional-style code instead of verbose procedural loops
  where appropriate.
- Avoid `SELECT *`; select only the fields you need to reduce memory
  footprint and improve database performance.
- Favor CDS views and AMDP for data-intensive logic, pushing computation
  to the database layer (HANA) rather than looping in the application
  layer.

## RICEFW documentation standards

Every custom development object should document:

- **Purpose**: Business requirement being addressed
- **Functional Spec reference**: Link to the original FS/TS
- **Inputs/Outputs**: Parameters, selection screens, or interface
  structures
- **Error handling**: What exceptions are raised and how they should be
  handled by calling programs
- **Testing evidence**: Unit test cases, integration test results, and
  UAT sign-off notes

## Performance optimization checklist

1. Avoid nested SELECTs inside loops (classic "SELECT in LOOP"
   anti-pattern) — replace with a single SELECT using `FOR ALL ENTRIES`
   or a JOIN.
2. Use internal table with a sorted or hashed key when frequent lookups
   are required, instead of a standard table with linear search.
3. Buffer master data lookups where the data changes infrequently.
4. Profile with SAT/ST05 before optimizing — don't guess at bottlenecks.

## Agile delivery notes

- Break RICEFW objects into small, independently testable units where
  possible, so they fit within a single sprint.
- Flag scope or design concerns to the team lead as early as possible in
  the sprint rather than at UAT — "minimal red flags at delivery" starts
  with early, honest status updates.
