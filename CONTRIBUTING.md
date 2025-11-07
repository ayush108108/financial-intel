# Contributing to Financial Intelligence

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the Financial Intelligence Platform.

## 🎯 How Can I Contribute?

### Report Bugs
- Check existing [issues](https://github.com/ayush108108/financial-intel/issues) first
- Describe the bug clearly with steps to reproduce
- Include your environment (OS, Python version, etc.)
- Provide relevant logs and error messages

### Suggest Enhancements
- Open an issue with the label `enhancement`
- Describe the use case and expected behavior
- Include examples or mockups if applicable

### Contribute Code
- Pick an issue labeled `good first issue` or `help wanted`
- Fork the repository
- Create a feature branch: `git checkout -b feature/my-feature`
- Follow the development workflow below
- Submit a pull request with a clear description

### Improve Documentation
- Fix typos, clarify existing docs
- Add examples or tutorials
- Improve API documentation
- Update deployment guides

---

## 🛠️ Development Setup

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR-USERNAME/financial-intel.git
cd financial-intel
git remote add upstream https://github.com/ayush108108/financial-intel.git
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies (Development Mode)
```bash
pip install -r requirements.txt
pip install -r backend/requirements.txt
pip install pytest pytest-cov black flake8 mypy  # Dev tools
```

### 4. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your local Supabase/PostgreSQL credentials
```

### 5. Run Tests
```bash
pytest tests/ -v --cov=backend
```

---

## 📋 Code Style & Standards

We follow PEP 8 with some preferences:

### Formatting
```bash
# Format code with Black
black backend/ scripts/

# Check linting
flake8 backend/ --max-line-length=100

# Type checking
mypy backend/
```

### Python Style
- **Line length**: 100 characters
- **Imports**: Alphabetically sorted, separate stdlib/third-party/local
- **Type hints**: Required for all function signatures
- **Docstrings**: Google-style docstrings for all classes and functions

Example:
```python
def calculate_correlation(
    asset1_prices: pd.Series,
    asset2_prices: pd.Series,
    method: str = "pearson"
) -> float:
    """Calculate correlation between two price series.
    
    Args:
        asset1_prices: OHLCV series for first asset.
        asset2_prices: OHLCV series for second asset.
        method: Correlation method ('pearson' or 'spearman').
    
    Returns:
        Correlation coefficient between -1 and 1.
    
    Raises:
        ValueError: If method is not supported.
    """
    pass
```

### Commit Messages
- Use present tense: "Add feature" not "Added feature"
- Reference issues: "Fix #123" or "Closes #456"
- Keep first line to 50 characters
- Add detailed description after blank line

Example:
```
Add cointegration threshold alerts

Implement WebSocket notifications when cointegration
score crosses user-defined threshold. Refactor
AlertService to support multiple notification channels.

Fixes #456
```

---

## 🔄 Pull Request Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/correlation-heatmap
```

### 2. Make Changes
- Keep commits atomic and focused
- Test your changes locally
- Update documentation if needed

### 3. Run Tests & Linting
```bash
pytest tests/ -v
black backend/ --check
flake8 backend/
mypy backend/
```

### 4. Push & Open PR
```bash
git push origin feature/correlation-heatmap
```

Then open a PR at https://github.com/ayush108108/financial-intel/pulls with:
- Clear title: "Add real-time correlation heatmap"
- Description of changes
- Reference to related issues: "Closes #123"
- Screenshots/GIFs if UI changes

### 5. Address Review Feedback
- Respond to comments politely
- Update code based on feedback
- Force push if needed: `git push -f origin feature/correlation-heatmap`
- Re-request review once addressed

### 6. Merge
Maintainers will merge once approved. Feel free to delete your branch after merge.

---

## 📁 Directory Structure & Responsibilities

```
backend/
  ├─ api/
  │  ├─ services/           # Core business logic
  │  │  ├─ pipeline_service.py       # Data ETL orchestration
  │  │  ├─ correlation_service.py    # Pair analysis
  │  │  ├─ cointegration_service.py  # Statistical testing
  │  │  └─ data_writer_service.py    # Database writes
  │  └─ routers/            # REST endpoints
  └─ clients/
     └─ yfinance_client.py  # Market data fetching

scripts/
  ├─ pipelines/
  │  ├─ daily_eod_pipeline.py        # Tier 1-2 orchestrator
  │  ├─ analytics_computation_pipeline_v2.py  # Tier 3
  │  └─ populate_precomputed.py      # Tier 4 cache
  └─ db/
     └─ schema.sql                    # Schema init

frontend-v2/
  └─ src/
     ├─ components/                   # Reusable Vue components
     ├─ views/                        # Page-level components
     └─ App.vue                       # Root component
```

### Contributing Guidelines by Area

#### **Backend Services** (`backend/api/services/`)
- Add comprehensive docstrings (Google style)
- Use type hints for all parameters and returns
- Include error handling with meaningful messages
- Write unit tests in `tests/test_<service_name>.py`

#### **Data Pipeline** (`scripts/pipelines/`)
- Ensure backward compatibility with existing data
- Add migration scripts if schema changes
- Log important steps for debugging
- Validate data at each tier

#### **Frontend Components** (`frontend-v2/src/`)
- Use TypeScript for type safety
- Follow Vue 3 Composition API patterns
- Add Vitest unit tests for complex logic
- Ensure responsive design (mobile-first)

#### **Database** (`scripts/db/`)
- Document schema changes in migration comments
- Include rollback scripts if applicable
- Update `docs/SCHEMA.md` with changes
- Test on both PostgreSQL 14+ versions

---

## 🧪 Testing Requirements

### Unit Tests
- Minimum 80% code coverage
- Mock external dependencies (yfinance, Supabase)
- Test both success and error paths

```bash
pytest tests/test_correlation_service.py -v --cov=backend/api/services
```

### Integration Tests
- Test with real Supabase schema
- Validate data flow across services
- Run in CI/CD before merge

### Manual Testing
- Test locally with sample data
- Verify UI/API with Swagger/Postman
- Check for performance regressions

---

## 🚀 Release & Versioning

We follow **Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes (e.g., API schema change)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Version is defined in `pyproject.toml` and `package.json`.

---

## 📚 Resources

- **[Architecture](./docs/ARCHITECTURE.md)** — System design details
- **[API Reference](./docs/API.md)** — Endpoint documentation
- **[Database Schema](./docs/SCHEMA.md)** — Table definitions
- **[Deployment](./docs/DEPLOYMENT.md)** — Production setup
- **[Issues](https://github.com/ayush108108/financial-intel/issues)** — Active tasks

---

## ❓ Questions?

- **Discussions**: Ask in [GitHub Discussions](https://github.com/ayush108108/financial-intel/discussions)
- **Email**: ayush@example.com
- **Discord/Slack**: (Coming soon)

---

## 📜 Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors must:
- Be respectful of differing opinions
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

Instances of abusive, harassing, or otherwise unacceptable behavior may result in removal.

---

Thank you for making Financial Intelligence better! 🙏
