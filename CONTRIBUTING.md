# Contributing Guidelines

## Making Changes

### SQL Queries
1. **Update the relevant SQL file** in `sql/` directory
2. **Test against expected results** - Compare output with validated values
3. **Update documentation** in `docs/` if calculation methods change
4. **Update README.md** if findings or structure change

### Python Scripts
1. **Follow existing patterns** - Use `snowflake_connection.py` for database access
2. **Add error handling** - Include try/except blocks and meaningful error messages
3. **Document functions** - Add docstrings explaining purpose and parameters
4. **Test locally** - Verify scripts work before committing

### Documentation
1. **Keep summaries up-to-date** - Update analysis summaries when findings change
2. **Document calculation methods** - Explain any changes to how metrics are calculated
3. **Include validation notes** - Document how queries were validated

## Commit Messages

Use clear, descriptive commit messages:

```
Short summary (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
- Bullet points for multiple changes
- Reference issue numbers if applicable
```

## Testing

Before committing:
1. Run SQL queries in Snowflake to verify they execute
2. Run Python scripts to ensure they work end-to-end
3. Compare results with expected values
4. Check that output format matches chart requirements

## Code Review Checklist

- [ ] SQL queries follow existing structure
- [ ] Calculation methods match validated approach
- [ ] Documentation updated
- [ ] No hardcoded credentials or sensitive data
- [ ] Error handling included
- [ ] Code is readable and well-commented
