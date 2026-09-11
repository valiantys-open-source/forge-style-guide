# Contributing

Thank you for helping improve the Forge Style Guide.

## Propose a change

1. Open an issue or pull request that explains the problem the guidance should solve.
2. Keep recommendations focused, practical, and supported by current Atlassian documentation.
3. Include a complete example when changing technical guidance.
4. Run the Markdown converter and its tests before submitting:

   ```bash
   python3 -m unittest discover -s .github/scripts -p 'test_*.py'
   python3 .github/scripts/md_to_html.py README.md
   node --check .github/scripts/publish-to-hubspot.js
   ```

Pull requests publish only after review and merge to `main`.

## Content standards

- Prefer clear language and typed TypeScript examples.
- Label recommendations as **Do** or **Avoid** without relying on color alone.
- Link time-sensitive claims to primary Atlassian documentation.
- Do not include credentials, customer information, or other sensitive data.

## Reporting security issues

Do not open a public issue for a vulnerability. Follow [SECURITY.md](./SECURITY.md).
