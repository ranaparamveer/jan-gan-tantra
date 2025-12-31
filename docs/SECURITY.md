# Supply Chain Security Configuration

## NPM Package Integrity

### 1. Use package-lock.json (ALWAYS commit this)
- Ensures exact versions are installed
- Contains integrity hashes (SHA-512)
- Prevents unexpected updates

### 2. Audit packages before install
```bash
npm audit
npm audit fix  # Only for non-breaking fixes
```

### 3. Use npm ci in CI/CD (we use npm install only when lock file is out of sync)
```bash
npm ci  # Installs from lock file, fails if out of sync
```

### 4. Enable npm audit in CI
Already configured in `.github/workflows/ci.yml`

### 5. Review Dependabot PRs carefully
- Check changelog
- Review diff
- Run tests before merging

## Python Package Integrity

### 1. Pin exact versions in requirements.txt
Already done - all packages have exact versions (==)

### 2. Use pip-audit for vulnerability scanning
```bash
pip install pip-audit
pip-audit
```

### 3. Verify package hashes (optional, for high security)
```bash
pip install --require-hashes -r requirements.txt
```

## Docker Image Security

### 1. Use official images only
- `postgis/postgis:16-3.5` (official)
- `redis:7-alpine` (official)
- `node:20-alpine` (official)
- `python:3.12-slim` (official)

### 2. Pin image versions (already done)
Never use `:latest` tag

### 3. Scan images with Trivy
```bash
trivy image postgis/postgis:16-3.5
```

## GitHub Security Features

### 1. Dependabot (Enabled)
- Automatic security updates
- Weekly dependency updates
- Grouped PRs

### 2. Secret Scanning (Enable in repo settings)
- Detects committed secrets
- Alerts on exposure

### 3. Code Scanning (Optional)
- CodeQL for vulnerability detection
- Requires GitHub Advanced Security

## Pre-commit Hooks (Installed)

### Security checks:
- `detect-secrets` - Prevents committing secrets
- `bandit` - Python security linter
- `safety` - Checks for known vulnerabilities
- `detect-private-key` - Prevents committing SSH keys

### Run manually:
```bash
pre-commit run --all-files
```

## Best Practices

### DO:
✅ Review all Dependabot PRs
✅ Keep dependencies updated weekly
✅ Run `npm audit` before deploying
✅ Use exact versions in production
✅ Commit package-lock.json
✅ Enable 2FA on npm/PyPI accounts
✅ Use scoped packages (@org/package)

### DON'T:
❌ Use `npm install` without reviewing changes
❌ Ignore security warnings
❌ Use deprecated packages
❌ Install packages from unknown sources
❌ Disable integrity checks
❌ Use `--force` or `--legacy-peer-deps` without understanding why

## Incident Response

If supply chain attack detected:

1. **Immediate**: Stop deployments
2. **Investigate**: Check `npm audit` and `pip-audit`
3. **Rollback**: Revert to last known good version
4. **Update**: Pin to secure version
5. **Monitor**: Check logs for suspicious activity

## Monitoring

- **Dependabot**: Weekly PRs
- **npm audit**: Run in CI
- **Pre-commit**: Blocks bad commits
- **GitHub Security**: Alerts tab

---

**Last Updated**: December 31, 2025
