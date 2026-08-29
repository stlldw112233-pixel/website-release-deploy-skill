# Deployment intake template

Use this form when a user asks to update a website but the release boundary is not known. It deliberately excludes passwords, tokens, private keys, and `.env` contents.

```text
Website deployment details

1. Local project
   - Directory:
   - Git branch to publish:

2. Website scope
   - Public domain or URL:
   - App/subdomain to update:

3. Production connection
   - Existing SSH alias (preferred):
   - If no alias: server host, port, and login user:
   - Application directory:
   - Service name / process manager:
   - Expected health URL or port:

4. Data that must be preserved
   - Database path and type:
   - Uploads or user-generated files:
   - Environment/configuration files:
   - Certificates or other persistent files:
```

## Handling incomplete answers

- Ask only for the unanswered fields needed to proceed.
- A domain alone does not identify the correct server directory or service.
- If the user has no SSH alias, use the SSH onboarding flow before deployment.
- Treat credentials as secrets: use an approved secret channel and never add them to this form, a commit, or command output.
