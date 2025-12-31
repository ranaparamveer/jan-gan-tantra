# Contributing to Jan-Gan-Tantra

Thank you for your interest in contributing to Jan-Gan-Tantra! This project is built for the public good, and we welcome contributions from developers, designers, translators, and civic activists.

## How to Contribute

### 1. Code Contributions

**Areas We Need Help:**
- Frontend components (React/Next.js)
- Backend APIs (Django REST Framework)
- AI integration (Bhashini, Whisper, Llama)
- Mobile responsiveness
- Performance optimization

**Process:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write tests if applicable
5. Run linters: `npm run lint` (frontend) or `flake8` (backend)
6. Commit with clear messages: `git commit -m "feat: add voice input component"`
7. Push and create a Pull Request

### 2. Data Contributions

**Government Directory Data:**
- Scrape public directories (NIC, state portals)
- Verify officer contact details
- Submit via CSV/JSON in `data/` directory

**Solution Wiki Content:**
- Write "How-To" guides for civic issues
- Create RTI templates
- Share success stories

**Format:**
```json
{
  "title": "How to file RTI for garbage collection",
  "category": "Sanitation",
  "steps": [
    "Step 1: ...",
    "Step 2: ..."
  ],
  "language": "en"
}
```

### 3. Translation

We need translations for:
- UI strings (Hindi, Tamil, Bengali, etc.)
- Solution guides
- Templates

**Process:**
1. Copy `locales/en.json` to `locales/{language_code}.json`
2. Translate all strings
3. Submit PR

### 4. Design & UX

- Mobile-first UI mockups
- Accessibility improvements
- Icon design
- User flow diagrams

Submit designs in `docs/design/` directory.

### 5. Testing

- Manual testing on different devices
- Accessibility testing (screen readers)
- Performance testing
- Security audits

## Development Guidelines

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use type hints
- Max line length: 100 characters
- Run `black` for formatting

**TypeScript (Frontend):**
- Use functional components
- Prefer hooks over class components
- Use TypeScript strict mode
- Run `prettier` for formatting

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

### Testing

**Backend:**
```bash
cd apps/api
python manage.py test
```

**Frontend:**
```bash
cd apps/web
npm test
```

## Community Guidelines

1. **Be Respectful**: This is a civic project serving diverse communities
2. **Be Patient**: Contributors are volunteers
3. **Be Constructive**: Provide actionable feedback
4. **No Politics**: Focus on technical solutions, not political debates

## Legal

By contributing, you agree that your contributions will be licensed under AGPL-3.0.

## Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/jan-gan-tantra/discussions)
- Email: contribute@jan-gan-tantra.org

---

**Thank you for helping build a more accountable government!** 🙏
