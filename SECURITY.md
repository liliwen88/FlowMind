# Security Policy

## Reporting Security Vulnerabilities

**Do not open public GitHub issues for security vulnerabilities.**

If you discover a security vulnerability in llm-flow-dsl, please report it via email to **liliwen@example.com** (replace with your actual contact).

When reporting, please include:

- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if you have one)

**Response Timeline:**

- We aim to acknowledge your report within 48 hours
- We will work on a fix and provide an update within 7 days
- Critical vulnerabilities will be prioritized

## Security Best Practices

### For Users

1. **Keep llm-flow-dsl updated** to the latest version
2. **Validate input** to flow files before execution
3. **Use secure credentials** management for API keys in `tool` blocks
4. **Run in sandboxed environments** when executing untrusted flows
5. **Review flow files** before running them, especially from untrusted sources

### For Developers

1. **Validate all inputs** - Never trust user-provided flow files
2. **Use prepared queries** for any database operations
3. **Sanitize output** when logging or displaying user data
4. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`
5. **Use type hints** to catch potential errors early

## Known Limitations

- llm-flow-dsl does not provide encryption for flow files - store them securely
- API keys in flow files should be managed via environment variables, not hardcoded
- Always validate LLM responses before making critical decisions
- Tool calls execute with the permissions of the Python process - be careful with untrusted flows

## Security Advisories

We will publish security advisories in GitHub Security Advisories when vulnerabilities are discovered and fixed. See: https://github.com/liliwen88/llm-flow-dsl/security/advisories

## Version Support

| Version | Status | Security Updates |
|---------|--------|-----------------|
| 0.x     | Current | Yes |
| Earlier | EOL | No |

Latest release: https://github.com/liliwen88/llm-flow-dsl/releases
