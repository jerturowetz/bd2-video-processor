# Rule: 01-api-incremental-testing.md

---
id: api_incremental_testing
description: "Always test API changes with small datasets before running on full data to prevent mass errors"
---

# API Incremental Testing

When making changes to API interactions, always test incrementally before processing large datasets.

## Core Principle

**Test small, then scale.** Never run modified API code against your entire dataset without validating the changes first.

## Testing Approach

### 1. Single Item Test
```bash
# Test with ONE item first
process_api_data --limit=1

# Verify the result manually
# Check logs, response format, error handling
```

### 2. Small Batch Test
```bash
# Test with a tiny subset (5-10 items)
process_api_data --limit=10

# Validate:
# - No unexpected errors
# - Response format is correct
# - Rate limiting works properly
# - Error handling behaves as expected
```

### 3. Gradual Scale-Up
```bash
# Only after small tests pass
process_api_data --limit=100   # Medium test
process_api_data               # Full dataset
```

## Why This Matters

### ✅ **Prevents Mass Failures:**
- API rate limiting issues discovered early
- Data format changes caught before corrupting large datasets
- Authentication problems identified quickly
- Network timeouts handled before affecting thousands of records

### ✅ **Saves Time:**
- Fix issues on 1 record vs. debugging 10,000 failed records
- Avoid API quota exhaustion from repeated failed requests
- Prevent data corruption requiring full rollback

### ✅ **Reduces Costs:**
- Many APIs charge per request - failed mass operations are expensive
- Prevents hitting rate limits that require waiting periods
- Avoids cleanup work from partial failures

## Implementation Examples

### API Client Changes
```python
# ❌ Don't do this
for item in all_10000_items:
    api_client.process(item)  # Untested changes

# ✅ Do this instead
test_items = all_items[:1]  # Test with 1 item first
for item in test_items:
    result = api_client.process(item)
    print(f"Test result: {result}")  # Verify manually

# After verification, proceed with full dataset
```

### Database Operations
```bash
# ❌ Don't run untested changes on full table
UPDATE users SET new_column = api_fetch(user_id);

# ✅ Test with LIMIT first
UPDATE users SET new_column = api_fetch(user_id) LIMIT 5;
-- Check results manually
-- Then proceed with full update
```

## Red Flags

Stop and test incrementally when you:
- Modified API request format or parameters
- Changed authentication or headers
- Updated error handling logic
- Switched API endpoints or versions
- Added new data processing steps
- Changed rate limiting or retry logic

**Remember: It's always faster to test 1 record properly than to debug 1,000 failed records.**

---

# Rule: 01-be-thorough.md

---
id: be_thorough
description: "Always be thorough and complete in analysis, discovery, and task execution"
---

# Be Thorough

Always be thorough and complete in analysis, discovery, and task execution. Don't skip steps or make assumptions about scope.

## Discovery and analysis

- When asked to analyze a directory, check ALL subdirectories recursively
- Use systematic discovery methods (`find`, `ls -la`, directory traversal) to ensure complete coverage
- Don't assume what's important - examine everything first, then prioritize
- Document what you analyzed vs what you skipped, and why

## Task execution

- Read requirements carefully and completely before starting
- Break down complex tasks into comprehensive checklists
- Verify you've addressed all parts of multi-part requests
- Double-check your work against the original requirements

## When reporting findings

- Clearly state the scope of your analysis ("I analyzed X but did not examine Y")
- Call out any limitations or areas you didn't cover
- If you discover you missed something, acknowledge it explicitly and offer to complete the analysis

## Self-checking

Before declaring a task complete, ask yourself:
- Did I examine all the areas requested?
- Are there obvious places I should have looked but didn't?
- Would someone reviewing my work find glaring omissions?

*This rule exists because thoroughness prevents having to redo work and builds trust through comprehensive analysis.*

---

# Rule: 01-cloud-services-cli-standards.md

---
id: cloud_services_cli_standards
description: "Standards for configuring and using cloud service CLIs and maintaining service integrations"
---

# Cloud Services & CLI Standards

Establish consistent configuration and usage patterns for cloud service CLIs and API integrations.

## ✅ DO

**AWS CLI Configuration**
- Use named profiles for different AWS accounts/environments
- Configure profiles with descriptive names: `personal`, `work-dev`, `work-prod`
- Set default regions appropriate for each profile
- Use AWS SSO when available for better security
- Store profiles in `~/.aws/config` and credentials in `~/.aws/credentials`

**GitHub CLI (gh) Best Practices**
- Authenticate using `gh auth login` with appropriate scopes
- Use SSH keys for repository operations
- Configure default settings for common operations
- Use `gh` for workflow automation instead of web interface when possible
- Set up aliases for frequently used commands

**Docker Configuration**
- Configure Docker daemon settings appropriately for development
- Use BuildKit by default for improved build performance
- Set up multi-platform builds when needed
- Configure resource limits to prevent system impact
- Keep commonly used Docker commands documented and accessible

**Service Integration Principles**
- Use environment-based configuration (development, staging, production)
- Keep service credentials in appropriate secret management (direnv, not hardcoded)
- Document which services require which credentials
- Use service-specific CLI tools when available rather than generic HTTP clients

## ❌ DON'T

**Avoid Configuration Mistakes**
- Don't use default/unnamed profiles for production services
- Don't hardcode credentials in scripts or configuration files
- Don't mix development and production credentials in the same profile
- Don't ignore CLI tool updates that might include security fixes

**Security Anti-patterns**
- Don't store credentials in version control
- Don't use overly broad permissions when specific scopes are available
- Don't skip environment-specific configurations
- Don't share credentials between different environments or projects

## Configuration Examples

**AWS CLI Profile Setup**
```ini
# ~/.aws/config
[profile personal]
region = us-west-2
output = json

[profile work-dev]
region = us-east-1
output = json
sso_start_url = https://company.awsapps.com/start

[profile work-prod]
region = us-east-1
output = json
sso_start_url = https://company.awsapps.com/start
```

**GitHub CLI Configuration**
```bash
# Set up useful aliases
gh alias set prs 'pr list --assignee @me'
gh alias set issues 'issue list --assignee @me'
gh alias set co 'pr checkout'

# Configure default behavior
gh config set git_protocol ssh
gh config set editor vim
```

**Common Docker Commands Reference**
```bash
# Development workflow
docker-compose up -d
docker-compose logs -f
docker system prune  # cleanup

# Multi-platform builds
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64
```

## Service-Specific Guidelines

**AWS Services**
- Use least-privilege IAM policies
- Prefer temporary credentials over long-lived access keys
- Use AWS profiles for different environments
- Document which AWS services each project uses

**GitHub Integration**
- Use GitHub CLI for repository operations
- Set up repository templates with consistent structure
- Use GitHub Actions for CI/CD when appropriate
- Keep issue and PR templates updated

**Docker Workflow**
- Use multi-stage builds for production images
- Keep Docker images minimal and secure
- Use .dockerignore files appropriately
- Document container dependencies and networking requirements

## Backup and Recovery

**Credential Backup**
- Keep secure backups of important credentials (LastPass, 1Password, etc.)
- Document credential recovery procedures
- Test credential recovery process periodically
- Keep emergency access methods documented

**Configuration Backup**
- Include CLI configurations in dotfiles management
- Back up service-specific settings and preferences
- Document service integrations and dependencies
- Keep setup procedures documented for new machines

This approach ensures reliable, secure access to cloud services while maintaining good security practices and operational consistency.

---

# Rule: 01-commit-message-standards.md

---
id: commit_message_standards
description: "Use clear, conventional commit messages with emoji prefixes for consistent project history"
---

# Commit Message Standards

Use clear, conventional, and actionable commit messages to maintain a high-quality project history. Keep commit messages short, clear, and imperative.

## Emoji Prefixes

Start each commit with one emoji:

- 🌪 **New value** · new feature or major addition
- 💨 **Enhancement** · improvements to existing features
- 🧰 **DevX** · developer tooling/workflow changes
- 💡 **KTLO** · routine maintenance/operations
- 🚑 **Hotfix** · urgent critical fix
- 🐛 **Defect** · bug fix for live features

## Format Rules

- Start with an emoji, then a short imperative summary
- Use **imperative mood**: e.g., "Add validation", not "Added validation"
- Focus on **what changed**, not why (rationale goes in PR description)
- Keep the subject line **≤50 characters**, capitalized, no trailing period
- Avoid repetition of filenames or context already evident in the diff
- Don't write rationale; keep messages short and practical

## Examples

**Good commit messages:**
- `🐛 Fix null check in webhook handler`
- `🧰 Speed up local dev with turbo cache`
- `💨 Simplify auth middleware branches`
- `🌪 Add CSV export for workspace reports`

**Bad commit messages:**
- `Updated commit message guidelines for clarity` (too verbose)
- `Fixed bug` (not specific)
- `Added new feature that does X Y and Z because we need it for the client` (too long, includes rationale)
- `fix: correct typo in dashboard label`
- `refactor: streamline auth middleware`
- `docs: add README install instructions`


---

# Rule: 01-digitalocean-infrastructure.md

---
id: digitalocean_infrastructure
description: "DigitalOcean infrastructure management and scalability best practices"
---

# DigitalOcean Infrastructure Management

Manage DigitalOcean infrastructure for uptime, maintainability, and predictable performance.

## ✅ DO

### Monitoring & Alerts
- **Enable DigitalOcean Monitoring** on all Droplets
- **Set CPU, memory, and disk usage alerts** via email or Slack
- **Use floating IPs** for quick failover and blue/green deployments

### Backups & Recovery
- **Enable automatic weekly backups** on all production Droplets
- **Create manual snapshots** before any major change or deployment
- **Maintain documented restore procedures**
- **Test snapshot recovery** on staging environments regularly

### Scalability & Architecture
- **Use load balancers** to distribute traffic for production workloads
- **Prefer managed services** (Managed Databases, DO Kubernetes) over self-managed instances
- **Use DO Projects** or namespaces to isolate experiments from production
- **Auto-tag Droplets and Spaces** by project + environment

### Networking
- **Enforce private networking** between Droplets where applicable
- **Restrict SSH access** to known IPs using firewalls or VPC
- **Use VPCs** for network isolation between environments

## ❌ DON'T

### Anti-patterns
- Don't rely on single Droplets for production workloads without backup plans
- Don't skip backup verification - test restore procedures
- Don't mix production and development resources in same project
- Don't ignore resource monitoring - set up alerts before problems occur

### Scaling Mistakes
- Don't manually scale without load balancers in place
- Don't use unmanaged services when managed alternatives exist
- Don't forget to tag resources for organization and billing tracking

## Implementation Examples

### Basic Monitoring Setup
```bash
# Enable monitoring via doctl CLI
doctl compute droplet enable-monitoring DROPLET_ID

# Set up basic firewall rules
doctl compute firewall create --name "web-firewall" \
  --inbound-rules "protocol:tcp,ports:80,source_addresses:0.0.0.0/0,::0/0" \
  --inbound-rules "protocol:tcp,ports:443,source_addresses:0.0.0.0/0,::0/0" \
  --inbound-rules "protocol:tcp,ports:22,source_addresses:YOUR_IP/32"
```

### Backup Automation
```bash
# Create snapshot before deployment
doctl compute droplet-action snapshot DROPLET_ID --snapshot-name "pre-deploy-$(date +%Y%m%d)"

# List recent snapshots
doctl compute snapshot list --resource droplet
```

This approach ensures reliable, scalable DigitalOcean infrastructure that can handle production workloads.

---

# Rule: 01-github-pages-deployment.md

---
id: github_pages_deployment
description: "GitHub Pages deployment workflow patterns, permissions, and scheduled rebuild strategies"
---

# GitHub Pages Deployment

Standards for deploying static sites to GitHub Pages using GitHub Actions with the official Pages actions.

## Action Chain

Deploy to GitHub Pages using the three official actions, always pinned by SHA:

```yaml
# 1. Configure Pages (once per build job)
- uses: actions/configure-pages@<sha> # v4

# 2. Upload build output as a Pages artifact
- uses: actions/upload-pages-artifact@<sha> # v3
  with:
    path: './dist'

# 3. Deploy the artifact (separate job)
- uses: actions/deploy-pages@<sha> # v4
```

### Job Structure

Split build and deploy into separate jobs. The deploy job captures the Pages URL as an environment output:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - # checkout, setup, build...
      - uses: actions/configure-pages@<sha> # v4
      - uses: actions/upload-pages-artifact@<sha> # v3
        with:
          path: './dist'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@<sha> # v4
```

## Permissions

Pages deployments require elevated permissions beyond the typical `contents: read`:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

- `pages: write` — required to publish to the Pages environment
- `id-token: write` — required for OIDC token exchange with the Pages deployment API
- `contents: read` — checkout access

When the deploy workflow calls a reusable CI workflow via `workflow_call`, scope the CI job to `contents: read` only:

```yaml
jobs:
  ci:
    uses: ./.github/workflows/ci.yml
    permissions:
      contents: read
```

## Concurrency

Use a concurrency group to prevent overlapping deploys. Set `cancel-in-progress: false` to avoid aborting a deploy mid-flight:

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

This ensures only one deploy runs at a time, but a running deploy always finishes before the next one starts.

## Triggers

### Standard Triggers

```yaml
on:
  push:
    branches: [main]       # Deploy on merge to main
  workflow_dispatch:        # Manual deploy button in GitHub UI
```

### Scheduled Rebuilds

For time-sensitive content (seasonal banners, date-driven messaging), add a cron schedule:

```yaml
on:
  schedule:
    - cron: '0 7 * * *'  # 2:00 AM EST (UTC-5) / 3:00 AM EDT (UTC-4)
```

- Cron times are always **UTC** — add a comment with the local time
- Daily rebuilds keep time-sensitive content current without manual deploys
- GitHub may delay scheduled workflows by a few minutes; don't rely on exact timing

### CI Gate Before Deploy

Use `workflow_call` to run full CI as a prerequisite:

```yaml
jobs:
  ci:
    uses: ./.github/workflows/ci.yml
    permissions:
      contents: read

  build:
    needs: ci
    # ... build and upload artifact

  deploy:
    needs: build
    # ... deploy
```

## Build Artifact

- **Never commit `dist/`** — always generate it in CI
- The `upload-pages-artifact` action handles packaging and transfer between jobs
- Point it at the build output directory (e.g., `./dist`, `./build`, `./out`)

## act Compatibility

Pages actions require GitHub infrastructure and won't work with `act`. Guard them:

```yaml
- name: Setup Pages
  if: ${{ !env.ACT }}
  uses: actions/configure-pages@<sha> # v4

- name: Upload artifact
  if: ${{ !env.ACT }}
  uses: actions/upload-pages-artifact@<sha> # v3
  with:
    path: './dist'
```

The deploy job itself won't run locally regardless, but skipping artifact upload prevents errors in local testing.

## Best Practices

### ✅ DO:
- **Split build and deploy into separate jobs** — cleaner failure isolation
- **Use `cancel-in-progress: false`** — never abort a live deploy
- **Gate deploys on CI passing** via `workflow_call` + `needs`
- **Add `workflow_dispatch`** — manual redeploy is useful for emergencies
- **Comment the local timezone** on cron schedules
- **Pin all three Pages actions by SHA**

### ❌ DON'T:
- **Commit build output** — generate it fresh in every CI run
- **Use `cancel-in-progress: true`** for deploy jobs — this can leave Pages in a broken state
- **Skip the `id-token: write` permission** — deploy will fail silently
- **Rely on exact cron timing** — GitHub may delay scheduled runs
- **Put build and deploy in the same job** — artifact upload is the clean handoff point


---

# Rule: 01-local-server-error-monitoring.md

---
id: local_server_error_monitoring
description: "Automatically extract, format, and present local development server errors for easy debugging"
---

# Local Server Error Monitoring

When users run local development servers (http-server, Vite, Astro, Netlify dev, etc.), automatically monitor output for errors and present them in a clear, actionable format.

## When to Monitor

Trigger on server output containing:
- HTTP 404/500 errors
- Build/compilation errors
- Asset loading failures
- CORS errors
- Port conflicts
- Module resolution errors

## Error Presentation Format

### Summary First

```
🔍 Server Issues Detected:
- 3 × 404 errors (missing assets)
- 1 × favicon missing
```

### Detailed Breakdown

List each unique error with type, affected resource, frequency, and suggested fix:

```
📁 Missing Assets (404):
  → /assets/style.css
  → /assets/logos/logo.png

  Likely cause: Build output path mismatch
  Check: Does `dist/assets/` contain these files?
```

## Common Error Patterns

### 404 Errors
- Verify file exists in build output
- Check asset path configuration
- Verify build process completed successfully

### Asset Path Issues
Common causes:
1. Build output path configured incorrectly
2. Assets not copied during build
3. Base URL path mismatch

Quick checks: `ls -la dist/assets/` and review build config (vite.config.js, astro.config.mjs, etc.)

### Port Conflicts
Quick fixes:
- Kill process: `lsof -ti:XXXX | xargs kill`
- Use different port: `--port 3001`
- Check for zombie processes: `ps aux | grep node`

### Build Errors
Present with: affected file, line number (if available), and specific fix based on error type.

## ✅ DO

- **Automatically scan** server output for error patterns
- **Group similar errors** to reduce noise
- **Provide actionable suggestions** for each error type
- **Show file paths** relative to project root
- **Count repeated errors** to highlight frequency

## ❌ DON'T

- Don't show raw log output without processing
- Don't present errors without context or suggestions
- Don't ignore patterns that indicate common misconfigurations
- Don't skip verification steps that could clarify root cause

## Server-Specific Patterns

**http-server**: 404 errors, missing files, CORS issues
**Vite/Astro**: Module resolution errors, hot reload failures, asset transformation issues
**Netlify Dev**: Function errors, redirect/rewrite issues, environment variable problems

## Proactive Debugging

After detecting errors, offer to:
1. Check build output — verify files exist where expected
2. Review configuration — check relevant config files
3. Compare paths — match requested paths to actual file structure
4. Suggest fixes — based on common patterns and project type


---

# Rule: 01-python-code-style.md

---
id: python_code_style
description: "Python code style, formatting, and naming conventions following PEP 8"
---

# Python Code Style and Formatting

Python code style, formatting, and naming conventions following PEP 8 and modern Python development practices.

## Basic Formatting

### Indentation and Line Length
- **Use 4 spaces** for indentation (no tabs)
- **Maximum line length** of 88 characters (Black formatter style)
- **Use parentheses** for line continuation when needed
- **Add trailing comma** after last item in multi-line collections

### String Formatting
- **Use double quotes** for strings consistently
- **Use f-strings** for string interpolation (Python 3.6+)
- **Use triple double quotes** for docstrings

```python
# Good string formatting
name = "John Doe"
message = f"Hello, {name}!"
items = [
    "apple",
    "banana",
    "cherry",  # Trailing comma
]
```

## Naming Conventions

### Variable and Function Names
- **Functions and variables**: `snake_case`
- **Constants**: `UPPER_CASE`
- **Classes**: `PascalCase`
- **Modules**: `lowercase` or `lower_with_underscores`

### Access Modifiers
- **Public**: `public_method()`
- **Internal use**: `_single_leading_underscore`
- **Name mangling**: `__double_leading_underscore`
- **Special methods**: `__dunder_methods__`

```python
# Good naming examples
user_count = 42
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

class UserManager:
    """Manages user operations."""
    
    def get_active_users(self):
        """Public method to get active users."""
        return self._fetch_users()
    
    def _fetch_users(self):
        """Internal method to fetch users from database."""
        return self.__query_database()
    
    def __query_database(self):
        """Private method for database operations."""
        pass
```

## Import Organization

### Import Grouping
**Group imports in this order:**
1. Standard library imports
2. Related third-party library imports  
3. Local application/library imports

**Sort alphabetically within each group and separate groups with blank lines:**

```python
# Standard library
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Third-party
import requests
from django.conf import settings
from sqlalchemy import create_engine

# Local application
from .models import User
from .utils import helper_function
from ..services import external_service
```

### Import Best Practices
- **Use absolute imports** when possible
- **Avoid wildcard imports** (`from module import *`)
- **Use explicit imports** for better readability
- **Import modules, not individual functions** when importing many items

```python
# ✅ Good
import json
from typing import List, Dict, Optional

# ❌ Avoid
from json import *
from some_module import func1, func2, func3, func4, func5
```

## Code Organization

### Function Organization
- **Keep functions small** and focused on single responsibility
- **Use descriptive names** that clearly indicate purpose
- **Order functions logically** - public methods first, then private

### Class Organization
```python
class ExampleClass:
    """Class-level docstring."""
    
    # Class variables
    CLASS_CONSTANT = "value"
    
    def __init__(self, param):
        """Initialize instance."""
        self.instance_var = param
        self._private_var = None
    
    # Public methods
    def public_method(self):
        """Public interface method."""
        return self._helper_method()
    
    # Private methods
    def _helper_method(self):
        """Internal helper method."""
        pass
    
    # Special methods
    def __str__(self):
        """String representation."""
        return f"ExampleClass({self.instance_var})"
```

## Formatting Tools Integration

### Black Formatter
```bash
# Install Black
pip install black

# Format code
black src/

# Check what would be formatted
black --check src/

# Configuration in pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  migrations/
  | \.git
  | \.venv
)/
'''
```

### Other Formatting Tools
```bash
# isort for import organization
pip install isort
isort src/

# autopep8 for PEP 8 compliance
pip install autopep8
autopep8 --in-place --recursive src/
```

## Configuration Files

### pyproject.toml Example
```toml
[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["myproject"]

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
```

## Best Practices

### ✅ DO:
- **Follow PEP 8** for style consistency
- **Use automated formatters** like Black to maintain consistency
- **Be consistent** within a project - establish team standards
- **Use meaningful names** that describe purpose, not implementation
- **Keep line length reasonable** for readability on different screen sizes
- **Use blank lines** to separate logical sections

### ❌ DON'T:
- **Mix tabs and spaces** - use only spaces
- **Use single-letter variable names** except for short loops
- **Write overly long lines** that require horizontal scrolling
- **Use inconsistent naming** within the same codebase
- **Skip the formatter** - automate style consistency

**Remember: Consistent code style makes code easier to read, maintain, and collaborate on. Use automated tools to enforce consistency across your team.**

---

# Rule: 01-task-brief-formats.md

---
id: task_brief_formats
description: "Two formats for task briefs: structured multi-disciplinary and casual short-form"
---

# Task Brief Formats

Choose between two formats based on task complexity and audience.

## Type 1: Structured task briefs

For multi-disciplinary teams requiring detailed context and planning.

### Format requirements

Start with a short intro paragraph **without a heading** — this should feel like a GitHub readme: plainspoken, context-rich, and immediately informative. Avoid any fluff.

Use clearly labeled section headings to organize content:

1. **Intro paragraph (no heading):**
   - Summarize where the task originated and current scope
   - Mention specific user or business trigger if relevant
   - State the goal or change at a high level

2. **# Why?**
   - Explain why the task matters
   - Provide motivation: recurring pain points, missed opportunities, or business upside
   - Include relevant trends, stakeholder asks, or time-sensitive needs

3. **# Use cases / real examples**
   - Bullet real or hypothetical examples of usage
   - Include links to related tasks, docs, designs, or recorded context
   - Ground the abstract goal in tangible situations

4. **# Requirements**
   - List specific needs for the solution, organized clearly
   - Include design/dev specs, config options, performance needs
   - Call out constraints or dependencies

5. **# Next step**
   - Clarify the immediate action expected
   - For dev tasks: "make an RFC"
   - For design/product/QA: specific evaluation or mockup tasks

### Style requirements

- Clear, intelligent, respectful of reader's time, occasionally funny
- No verbosity, no justification, don't embellish
- Assume assignee is capable and familiar with internal tools
- Avoid corporate speak or over-formality
- Always write for people outside your immediate discipline

### Additional requirements

- Prefer specific examples and real internal links over hypotheticals
- Include at least one screenshot, Figma link, or Loom if UX/UI related
- Keep section headers simple and functional — don't get poetic

## Type 2: Casual task descriptions

For straightforward tasks requiring quick, informal communication.

### Format requirements

Write 1–2 casual, human-sounding paragraphs. Avoid structured headers like "Goals" or "Next Steps" — just lay out the context and what needs doing naturally, like you'd say it in Slack.

### Style requirements

- Direct, thoughtful, and informal without being sloppy
- Assume assignee is smart and doesn't need hand-holding
- Prioritize clarity and tone over formality
- Should be easy to absorb at a glance

### Example

> The product overview page feels pretty clunky when scanned quickly — too much visual weight on secondary stuff, and the key message isn't landing above the fold. Can you take a pass at tightening it up? Not expecting a full redesign, just enough to make the hierarchy feel more intentional.

---

# Rule: 02-api-response-caching.md

---
id: api_response_caching
description: "Cache API responses to avoid redundant requests during development and testing, reducing costs and improving performance"
---

# API Response Caching

Implement intelligent caching to reduce API costs and improve performance during development and testing.

## Core Principle

**Cache API responses during development** to avoid hitting rate limits, reduce costs, and improve development speed.

## When to Use Caching

### Development and Testing
- **During development** - Avoid repeated API calls while iterating on code
- **When testing** - Use cached responses to test data processing without API overhead
- **For expensive APIs** - Cache responses from costly external services
- **During debugging** - Avoid re-fetching data while debugging processing logic

### Production Considerations
- **Frequent requests** - Cache responses for data that doesn't change often
- **Rate-limited APIs** - Prevent hitting rate limits with intelligent caching
- **Expensive operations** - Cache results of computationally expensive API calls

## Caching Strategies

### File-Based Caching (Simple)
Use for development and small-scale applications:

```python
import json
import os
from pathlib import Path
from datetime import datetime, timedelta

class APICache:
    def __init__(self, cache_dir=".cache/api"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, max_age_hours: int = 24):
        """Get cached response if not expired."""
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        with open(cache_file) as f:
            data = json.load(f)

        # Check if cache is expired
        cached_time = datetime.fromisoformat(data['timestamp'])
        if datetime.now() - cached_time > timedelta(hours=max_age_hours):
            cache_file.unlink()  # Remove expired cache
            return None

        return data['response']

    def set(self, key: str, response: dict):
        """Cache API response."""
        cache_file = self.cache_dir / f"{key}.json"

        data = {
            'timestamp': datetime.now().isoformat(),
            'response': response
        }

        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
```

### JavaScript/Node.js Implementation

```javascript
const fs = require('fs');
const path = require('path');

class APICache {
  constructor(cacheDir = '.cache/api') {
    this.cacheDir = cacheDir;
    // Ensure cache directory exists
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }
  }

  get(key, maxAgeHours = 24) {
    const cacheFile = path.join(this.cacheDir, `${key}.json`);

    if (!fs.existsSync(cacheFile)) {
      return null;
    }

    const data = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
    const cachedTime = new Date(data.timestamp);
    const now = new Date();

    if (now - cachedTime > maxAgeHours * 60 * 60 * 1000) {
      fs.unlinkSync(cacheFile);
      return null;
    }

    return data.response;
  }

  set(key, response) {
    const cacheFile = path.join(this.cacheDir, `${key}.json`);

    const data = {
      timestamp: new Date().toISOString(),
      response: response,
    };

    fs.writeFileSync(cacheFile, JSON.stringify(data, null, 2));
  }
}
```

## Cache Key Strategies

### URL-Based Keys
```python
def get_cache_key(url: str, params: dict = None) -> str:
    """Generate cache key from URL and parameters."""
    key = url.replace('/', '_').replace('?', '_').replace('&', '_')
    if params:
        param_str = '_'.join(f"{k}_{v}" for k, v in sorted(params.items()))
        key += f"_{param_str}"
    return key
```

### Content-Based Keys  
```python
import hashlib

def get_content_cache_key(content: str) -> str:
    """Generate cache key from content hash."""
    return hashlib.md5(content.encode()).hexdigest()
```

## Cache Usage Pattern

```python
# Initialize cache
cache = APICache()

def fetch_user_data(user_id: int, use_cache: bool = True):
    cache_key = f"user_{user_id}"
    
    # Try cache first
    if use_cache:
        cached_data = cache.get(cache_key, max_age_hours=6)
        if cached_data:
            print(f"Using cached data for user {user_id}")
            return cached_data
    
    # Fetch from API
    print(f"Fetching fresh data for user {user_id}")
    response = api_client.get_user(user_id)
    
    # Cache the response
    if use_cache:
        cache.set(cache_key, response)
    
    return response
```

## Cache Invalidation

### Time-Based Expiration
- Set appropriate expiration times based on data freshness requirements
- Use shorter cache times for frequently changing data
- Use longer cache times for stable reference data

### Manual Invalidation
```python
def invalidate_cache(pattern: str = "*"):
    """Invalidate cache files matching pattern."""
    cache_dir = Path(".cache/api")
    for cache_file in cache_dir.glob(f"{pattern}.json"):
        cache_file.unlink()
        print(f"Invalidated cache: {cache_file.name}")
```

### Environment-Based Invalidation
```bash
# Clear all cache when switching environments
rm -rf .cache/api/

# Clear specific API cache
rm -f .cache/api/notion_*.json
```

## Best Practices

### ✅ DO:
- **Use descriptive cache keys** that include relevant parameters
- **Set appropriate expiration times** based on data freshness needs
- **Add cache debugging** to log cache hits/misses during development
- **Include cache status in logs** to track cache effectiveness
- **Use different cache directories** for different environments
- **Version your cache keys** when API response format changes

### ❌ DON'T:
- Cache sensitive data like authentication tokens or personal information
- Use overly short cache expiration times (defeats the purpose)
- Cache error responses (let them fail fresh each time)
- Ignore cache directory size (implement cleanup for large caches)
- Cache during production without considering data freshness requirements

## Cache Directory Structure

```
.cache/
├── api/
│   ├── notion_pages_123.json
│   ├── notion_blocks_456.json
│   ├── hubspot_contacts.json
│   └── user_data_789.json
├── images/
└── temp/
```

## Environment Integration

### Development Environment
```python
# Enable caching in development
USE_CACHE = os.getenv('NODE_ENV') == 'development'

data = fetch_api_data(params, use_cache=USE_CACHE)
```

### .gitignore Entry
```
# Cache directories
.cache/
*.cache
```

**Remember: API caching is primarily a development tool. Always consider data freshness requirements and cache invalidation strategies for production use.**

---

# Rule: 02-communication-style-direct.md

---
id: communication_style_direct
description: "Clear, efficient communication that prioritizes clarity and accuracy over style or persuasion"
---

# Direct Communication Style

Use a no-fluff tone — direct, technically credible, and minimal on adjectives or enthusiasm.

## Key principles

Avoid hype, "marketing-speak," embellishments, or unnecessary polish. Favor clear, utilitarian language that gets to the point without sounding cold.

Communication should read like something a smart, confident, and grounded person would write — sometimes fun even, but not performative or overly eager.

## Specific guidelines

- Be succinct. Avoid excessive adjectives
- Favor a skeptical, curious stance over absolutes
- Ask questions when unsure; don't assume without data
- Eliminate filler language or exaggerated claims
- Avoid persuasive or salesy tone unless requested
- Use a professional tone that respects the user's time and intelligence
- Default to a professional, neutral tone that works across roles
- Prioritize clarity and accuracy over style or persuasion
- Provide concise answers and practical suggestions
- Use structured output where relevant (bullets, headings, tables)
- Avoid hype or sales language
- Be direct, but not abrupt
- Ask clarifying questions when context is missing
- Avoid unnecessary preamble and keep messages streamlined and to-the-point

## For different contexts

**Email**: Make it sound like a human who types quickly but thoughtfully. Keep efficient, friendly, and lightly conversational. No fluffy sign-offs or over-thanking.

**Slack/Async**: Keep direct, structured, and efficient. Use plainspoken language with technical clarity. Format for scan-ability with headers and bullet points. Tag people with purpose, not ceremony.

---

# Rule: 02-cursor-standards.md

---
id: cursor_standards
description: "Standards for Cursor IDE configuration and rules organization"
---

# Cursor IDE Standards

Configuration standards and best practices for working with Cursor IDE.

## Rules Directory Structure

- Place Cursor rules files in the `.cursor/rules/` directory
- **Do not** use `cursorrules` or other non-standard directory names
- Organize rules by domain or functionality when you have multiple rule files
- Use descriptive filenames that clearly indicate the rule's purpose

## Examples

✅ **Correct directory structure:**

    .cursor/
      rules/
        general.md
        typescript.md
        testing.md

❌ **Avoid these patterns:**

    cursorrules/          # Wrong directory name
    .cursorrules/         # Wrong directory name
    .cursor/cursorrules   # Wrong nested structure

## File Organization

- Keep rules focused and specific to avoid conflicts
- Use clear, descriptive rule names
- Group related rules together in the same file
- Separate language-specific rules from general coding standards

## Best Practices

- Regularly review and update Cursor rules to match project evolution
- Test rules with actual code to ensure they work as expected
- Document any custom rules that team members should be aware of
- Keep rules version controlled with the rest of your project configuration

---

# Rule: 02-daily-development-workflows.md

---
id: daily_development_workflows
description: "Standardized daily workflows for development setup, maintenance, and common operations"
---

# Daily Development Workflows

Establish consistent, efficient workflows for common development tasks and system maintenance.

## ✅ DO

**Morning Setup Routine**
- Check system status: disk space, running services, updates needed
- Update key repositories and configurations (`chezmoi update`, `git pull` on active projects)
- Verify development environment health (language versions, key services running)
- Review any overnight build failures or alerts

**Project Switching Workflow**
- Use `direnv` to automatically load project-specific environment variables
- Verify correct language versions are active (check `.python-version`, `.nvmrc`)
- Pull latest changes and check for dependency updates
- Run health checks (tests, linting) after switching contexts

**Common Development Operations**
- Use consistent shortcuts and aliases for frequent operations
- Maintain a personal command reference for complex operations
- Use `gh` CLI for GitHub operations instead of web interface when possible
- Keep commonly used Docker commands and configurations readily available

**End-of-Day Cleanup**
- Commit and push work in progress with clear WIP markers
- Close unnecessary applications and free up system resources
- Back up any important configuration changes
- Review and clean up temporary files and downloads

## ❌ DON'T

**Avoid Inefficient Patterns**
- Don't manually recreate the same environment setups repeatedly
- Don't skip environment verification when switching projects
- Don't leave uncommitted changes without clear tracking
- Don't accumulate system clutter without regular cleanup

**Bad Habits to Avoid**
- Don't rely on memory for complex command sequences - document them
- Don't skip backing up configurations before making changes
- Don't ignore system health indicators (disk space, memory usage)
- Don't let temporary solutions become permanent without proper implementation

## Quick Reference Commands

**System Status**
```bash
# Disk space and system health
df -h
top -l 1 | head -10
brew doctor  # if using Homebrew
```

**Git Operations**
```bash
# Quick status across projects
find ~/Projects -name .git -type d -exec dirname {} \; | xargs -I {} sh -c 'echo "\n=== {} ==="; git -C {} status --porcelain'

# Common GitHub CLI operations
gh repo list
gh pr status
gh issue list --assignee @me
```

**Development Environment**
```bash
# Verify language versions
python --version && which python
node --version && which node
docker --version && docker ps

# direnv status
direnv status
env | grep -E "(API_KEY|TOKEN)"
```

**Project Templates**
- Maintain templates for new project initialization
- Include standard files: README.md, .gitignore, .envrc template, basic CI/CD
- Keep language-specific templates (Python with poetry, Node with package.json)
- Document project setup steps that can't be automated

## Integration with AI Tools

**AI Rule Management**
- Keep AI rules updated as development practices evolve
- Use rulebook-ai project sync to apply rules to new projects
- Document any project-specific AI rule requirements
- Regular review of AI-generated code against established standards

**Automation Opportunities**
- Script repetitive setup tasks
- Use make files or task runners for common project operations
- Automate environment verification and health checks
- Create shortcuts for complex multi-step operations

This approach creates predictable, efficient workflows that scale across different projects and development contexts.

---

# Rule: 02-digitalocean-observability.md

---
id: digitalocean_observability
description: "DigitalOcean logging, monitoring, and observability best practices"
---

# DigitalOcean Observability

Implement comprehensive observability for DigitalOcean infrastructure to ensure reliability and enable proactive problem resolution.

## ✅ DO

### Logging
- **Centralize logs** using DO Spaces, Papertrail, ELK stack, or similar
- **Tag logs with environment and version metadata** for easy filtering
- **Structure logs in JSON format** when possible for better parsing
- **Set up log rotation** to prevent disk space issues
- **Archive logs regularly** for compliance and historical analysis

### Health Checks & Monitoring
- **Expose `/health` endpoints** for all services
- **Implement readiness and liveness checks** for containerized applications
- **Set up external monitoring** (UptimeRobot, Pingdom) for critical services
- **Monitor key metrics**: CPU, memory, disk usage, network I/O
- **Create custom dashboards** for application-specific metrics

### Alerting
- **Configure alerting thresholds** based on historical data and SLAs
- **Set up escalation policies** for different severity levels
- **Use multiple notification channels** (email, Slack, PagerDuty)
- **Implement alert fatigue prevention** with proper grouping and suppression

### Performance Monitoring
- **Track response times** and error rates for all endpoints
- **Monitor database performance** including slow queries and connections
- **Set up APM tools** (New Relic, DataDog) for application insights
- **Monitor resource utilization trends** to predict scaling needs

## ❌ DON'T

### Logging Mistakes
- Don't store logs only locally without backup or centralization
- Don't log sensitive information (passwords, tokens, PII)
- Don't ignore log rotation - prevent disk space exhaustion
- Don't use inconsistent log formats across services

### Monitoring Anti-patterns
- Don't rely solely on internal monitoring without external checks
- Don't set up alerts without clear ownership and response procedures
- Don't monitor everything - focus on business-critical metrics
- Don't ignore baseline establishment for meaningful alerting

### Performance Monitoring Issues
- Don't monitor only infrastructure metrics - include application metrics
- Don't set alert thresholds without understanding normal behavior patterns
- Don't forget to monitor batch jobs and background processes
- Don't overlook user experience metrics (page load times, error rates)

## Implementation Examples

### Centralized Logging Setup
```bash path=null start=null
# Configure rsyslog to send to external service
echo "*.* @@logs.papertrailapp.com:XXXXX" >> /etc/rsyslog.conf
systemctl restart rsyslog

# Docker logging driver for centralized logs
docker run -d --log-driver=syslog --log-opt syslog-address=udp://logs.papertrailapp.com:XXXXX app
```

### Health Check Implementation
```python path=null start=null
# Flask health check endpoint
@app.route('/health')
def health_check():
    checks = {
        'database': check_database_connection(),
        'redis': check_redis_connection(),
        'external_api': check_external_services()
    }
    
    if all(checks.values()):
        return jsonify({'status': 'healthy', 'checks': checks}), 200
    else:
        return jsonify({'status': 'unhealthy', 'checks': checks}), 503
```

### Monitoring Script
```bash path=null start=null
#!/bin/bash
# Basic monitoring script for cron
SERVICE_URL="https://your-app.com/health"
LOG_FILE="/var/log/health-check.log"

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

if [ $RESPONSE -ne 200 ]; then
    echo "$TIMESTAMP - Health check failed: HTTP $RESPONSE" >> $LOG_FILE
    # Send alert notification
    curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"Service health check failed"}' \
        $SLACK_WEBHOOK_URL
fi
```

### Custom Metrics Collection
```bash path=null start=null
# Send custom metrics to DigitalOcean Monitoring
curl -X POST "https://api.digitalocean.com/v2/monitoring/metrics" \
  -H "Authorization: Bearer $DO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{
      "name": "custom.app.active_users",
      "value": 150,
      "timestamp": 1609459200,
      "tags": {
        "environment": "production",
        "service": "web-app"
      }
    }]
  }'
```

## Monitoring Stack Example

### Basic Stack Components
- **DigitalOcean Monitoring**: Built-in infrastructure metrics
- **Papertrail**: Centralized log management
- **UptimeRobot**: External uptime monitoring
- **Grafana + Prometheus**: Custom dashboards and metrics

### Advanced Stack Components  
- **DataDog or New Relic**: APM and detailed application monitoring
- **PagerDuty**: Alert management and escalation
- **Sentry**: Error tracking and performance monitoring
- **DO Spaces**: Long-term log and metric storage

## Observability Checklist

### Initial Setup
- [ ] Log centralization configured
- [ ] Health checks implemented for all services
- [ ] Basic monitoring alerts set up
- [ ] External uptime monitoring configured
- [ ] Dashboard created for key metrics

### Ongoing Operations
- [ ] Log retention policies implemented
- [ ] Alert thresholds reviewed and tuned monthly
- [ ] Dashboards updated with new services
- [ ] Monitoring coverage assessed quarterly
- [ ] Incident response procedures documented

This comprehensive observability approach ensures you can detect, diagnose, and resolve issues quickly while maintaining system reliability.

---

# Rule: 02-python-documentation.md

---
id: python_documentation
description: "Python documentation standards using docstrings and type hints for better code maintainability"
---

# Python Documentation and Type Hints

Python documentation standards using docstrings and type hints for better code maintainability.

## Docstring Standards

### Google-Style Docstrings
Use Google-style docstrings for all public functions, classes, and modules:

```python
def process_user_data(user_id: int, include_metadata: bool = False) -> dict:
    """Process user data and return formatted result.

    This function retrieves user data from the database, processes it
    according to business rules, and returns a standardized format.

    Args:
        user_id: The unique identifier for the user
        include_metadata: Whether to include additional metadata in the result

    Returns:
        Dictionary containing processed user data with the following structure:
        {
            'id': int,
            'name': str,
            'email': str,
            'metadata': dict (optional)
        }

    Raises:
        ValidationError: If user_id is invalid or not found
        APIError: If external API call fails
        DatabaseError: If database query fails

    Example:
        >>> data = process_user_data(123, include_metadata=True)
        >>> print(data['name'])
        'John Doe'
        >>> print('metadata' in data)
        True
    """
    pass
```

### Class Documentation
```python
class UserManager:
    """Manages user operations including CRUD and authentication.
    
    This class provides a high-level interface for user management
    operations, handling database interactions, validation, and
    business logic.
    
    Attributes:
        database: Database connection instance
        cache_enabled: Whether caching is enabled for operations
        default_permissions: Default permissions for new users
    
    Example:
        >>> manager = UserManager(database=db, cache_enabled=True)
        >>> user = manager.create_user('john@example.com', 'password')
        >>> manager.activate_user(user.id)
    """
    
    def __init__(self, database, cache_enabled: bool = True):
        """Initialize UserManager with database connection.
        
        Args:
            database: Database connection instance
            cache_enabled: Whether to enable caching for operations
        """
        self.database = database
        self.cache_enabled = cache_enabled
        self.default_permissions = ['read']
    
    def create_user(self, email: str, password: str) -> User:
        """Create a new user account.
        
        Args:
            email: User's email address (must be valid format)
            password: User's password (must meet security requirements)
            
        Returns:
            User instance for the newly created user
            
        Raises:
            ValidationError: If email format is invalid or password is weak
            DatabaseError: If user creation fails
        """
        pass
```

### Module Documentation
```python
"""User management utilities and classes.

This module provides comprehensive user management functionality including
user creation, authentication, permissions, and profile management.

Classes:
    UserManager: Main interface for user operations
    User: User data model with validation
    UserPermissions: Permission management for users

Functions:
    validate_email: Email format validation
    hash_password: Secure password hashing
    generate_token: Authentication token generation

Example:
    >>> from user_management import UserManager
    >>> manager = UserManager(database=db)
    >>> user = manager.create_user('john@example.com', 'secure_password')
"""
```

## Type Hints Best Practices

### Basic Type Annotations
```python
from typing import List, Dict, Optional, Union, Any, Tuple
from pathlib import Path

# Basic types
def calculate_total(prices: List[float]) -> float:
    """Calculate total of all prices."""
    return sum(prices)

def get_user_data(user_id: int) -> Dict[str, Any]:
    """Get user data as dictionary."""
    pass

def find_user(email: str) -> Optional[User]:
    """Find user by email, return None if not found."""
    pass

# Union types for multiple possibilities
def process_data(value: Union[str, int, float]) -> str:
    """Process data that can be string, int, or float."""
    return str(value)

# Modern Python 3.10+ union syntax
def process_data_modern(value: str | int | float) -> str:
    """Process data using modern union syntax."""
    return str(value)
```

### Complex Type Annotations
```python
from typing import Dict, List, Optional, Callable, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum

# Type variables for generic functions
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

def get_first_item(items: List[T]) -> Optional[T]:
    """Get first item from list or None if empty."""
    return items[0] if items else None

# Callable type hints
def apply_filter(
    items: List[T], 
    filter_func: Callable[[T], bool]
) -> List[T]:
    """Apply filter function to list of items."""
    return [item for item in items if filter_func(item)]

# Complex nested structures
UserData = Dict[str, Union[str, int, List[str]]]
ApiResponse = Dict[str, Union[str, int, List[UserData]]]

def process_api_response(response: ApiResponse) -> List[UserData]:
    """Process API response and extract user data."""
    pass
```

### Using dataclasses with Type Hints
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class User:
    """User data model with validation.
    
    Attributes:
        id: Unique user identifier
        email: User's email address
        name: User's full name
        created_at: Account creation timestamp
        permissions: List of user permissions
        metadata: Additional user metadata
    """
    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    permissions: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate user data after initialization."""
        if not self.email or '@' not in self.email:
            raise ValidationError("Invalid email format")
        
        if not self.name.strip():
            raise ValidationError("Name cannot be empty")

@dataclass
class UserPreferences:
    """User preference settings."""
    theme: str = "light"
    language: str = "en"
    notifications_enabled: bool = True
    email_frequency: str = "daily"
```

### Protocol and Abstract Base Classes
```python
from typing import Protocol
from abc import ABC, abstractmethod

class Serializable(Protocol):
    """Protocol for objects that can be serialized."""
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize object to dictionary."""
        ...
    
    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'Serializable':
        """Create object from dictionary data."""
        ...

class DataProcessor(ABC):
    """Abstract base class for data processors."""
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data and return result."""
        pass
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data format."""
        return isinstance(data, dict) and len(data) > 0
```

## Documentation Best Practices

### Function Documentation Guidelines
```python
def analyze_user_behavior(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    include_sessions: bool = True,
    metrics: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Analyze user behavior patterns within a date range.
    
    Processes user activity data to identify patterns, trends, and insights
    about user engagement and behavior. Optionally includes session data
    and specific metrics.
    
    Args:
        user_id: Unique identifier for the user to analyze
        start_date: Beginning of the analysis period (inclusive)
        end_date: End of the analysis period (inclusive)
        include_sessions: Whether to include detailed session data in analysis
        metrics: Specific metrics to calculate. If None, calculates all
                available metrics. Available options: ['engagement', 'retention',
                'conversion', 'activity_score']
    
    Returns:
        Analysis results containing:
        - 'summary': Dict with high-level statistics
        - 'trends': List of identified behavioral trends
        - 'sessions': List of session data (if include_sessions=True)
        - 'metrics': Dict of calculated metrics
        - 'period': Analysis period information
    
    Raises:
        ValidationError: If user_id is invalid or dates are malformed
        DataNotFoundError: If no data exists for the specified period
        CalculationError: If metric calculations fail
    
    Example:
        >>> from datetime import datetime
        >>> start = datetime(2024, 1, 1)
        >>> end = datetime(2024, 1, 31)
        >>> result = analyze_user_behavior(
        ...     user_id=123,
        ...     start_date=start,
        ...     end_date=end,
        ...     metrics=['engagement', 'retention']
        ... )
        >>> print(result['summary']['total_sessions'])
        45
    """
    pass
```

### Error Documentation
```python
class ValidationError(Exception):
    """Raised when data validation fails.
    
    This exception is raised when input data doesn't meet the required
    format, constraints, or business rules.
    
    Attributes:
        message: Human-readable error description
        field: The field that failed validation (optional)
        value: The invalid value that caused the error (optional)
        error_code: Machine-readable error code for API responses
    
    Example:
        >>> raise ValidationError(
        ...     "Email must contain @ symbol",
        ...     field="email",
        ...     value="invalid-email",
        ...     error_code="INVALID_EMAIL_FORMAT"
        ... )
    """
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Any = None,
        error_code: Optional[str] = None
    ):
        self.field = field
        self.value = value
        self.error_code = error_code
        super().__init__(message)
```

## Tools and Configuration

### mypy Configuration
```ini
# mypy.ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True

# Per-module options
[mypy-requests.*]
ignore_missing_imports = True

[mypy-pandas.*]
ignore_missing_imports = True
```

### Type Checking Commands
```bash
# Run type checking
mypy src/

# Type check specific files
mypy src/user_management.py src/api_client.py

# Generate type coverage report
mypy --html-report mypy-report src/
```

## Best Practices

### ✅ DO:
- **Document all public APIs** with comprehensive docstrings
- **Use type hints consistently** across your codebase
- **Include usage examples** in docstrings for complex functions
- **Document exceptions** that functions can raise
- **Keep docstrings up to date** when changing function behavior
- **Use meaningful parameter names** that are self-documenting
- **Document complex algorithms** and business logic

### ❌ DON'T:
- **Document obvious code** - let well-named functions speak for themselves
- **Copy docstrings** between similar functions without customization
- **Use vague type hints** like `Any` when more specific types are available
- **Ignore type checking warnings** - they often reveal real issues
- **Over-document simple functions** - focus on complex or public APIs
- **Use outdated docstring formats** - stick to Google or NumPy style consistently

**Remember: Good documentation and type hints make your code self-explaining and help prevent bugs before they happen.**

---

# Rule: 02-server-log-analysis-on-demand.md

---
id: server_log_analysis_on_demand
description: "When users share server output, automatically analyze and present errors in actionable format"
---

# Server Log Analysis on Demand

When users share local server output (via command history, pasted logs, or terminal output), automatically extract and analyze errors without being asked.

## Trigger Patterns

Automatically analyze when you see:
- Command output containing server logs
- Server startup messages followed by request logs
- HTTP status codes in terminal output
- Error patterns in development server output

## Analysis Workflow

### 1. Extract Error Information
Scan for: HTTP error codes, error messages, failed requests, missing resources, repeated patterns.

### 2. Group and Categorize
Organize by:
- **Type**: 404s, 500s, build errors, etc.
- **Frequency**: one-time vs. repeated
- **Severity**: critical vs. informational
- **Resource**: files, routes, APIs, etc.

### 3. Present Findings

```
🔍 Server Log Analysis

Issues Detected:
- 2 × Missing assets (404)
- 1 × Missing favicon

Missing Assets:
  → /assets/style.css
  → /assets/logos/logo.png

Root Cause Analysis:
[educated guess based on patterns]

Verification Steps:
1. [specific command to verify hypothesis]
2. [specific file/config to review]
```

## ✅ DO

- **Automatically analyze** shared server logs without being asked
- **Identify patterns** proactively
- **Offer specific next steps** based on findings
- **Ask permission** before running diagnostic commands

## ❌ DON'T

- Don't wait for user to ask for analysis
- Don't present raw logs without interpretation
- Don't offer generic advice without analyzing the specific errors
- Don't run commands without user permission

## Common Scenarios

### Build Output Mismatch
Server requests `/assets/style.css`, build output has `dist/css/style.css` → path mismatch between build output and HTML references.

### Assets Not Copied
Server requests `/assets/logos/logo.png`, assets folder missing from dist → configure build tool to copy static assets.

### Base Path Issues
Paths are correct and files exist but still 404 → rebuild and hard refresh, or check base URL config.

## Post-Analysis Flow

1. Confirm issues found in the logs
2. Propose investigation steps
3. Execute verification commands (with permission)
4. Suggest fixes based on findings

**Always provide analysis proactively when server logs are shared. Users want immediate understanding of issues, not just confirmation that errors exist.**


---

# Rule: 03-avoid-over-scripting.md

---
id: avoid_over_scripting
description: "Don't write scripts for simple tasks that can be done manually - especially for small datasets"
---

# Avoid Over-Scripting

You don't need to automate everything. Sometimes manual inspection and decision-making is faster and more appropriate than writing a script.

## Core Principle

**Script when it saves time, not when it feels sophisticated.** Manual work is often faster for small, one-time tasks.

## When NOT to Write Scripts

### Small File Counts
```bash
# ❌ Don't write a Python script for this
ls project_files/
# Only 5 files? Just look at them manually
cat file1.txt  # Quick manual review
cat file2.txt
```

### One-Time Operations
```bash
# ❌ Don't script this
# "Write a script to check these 3 config files for syntax errors"

# ✅ Just do this
yamllint config1.yaml
yamllint config2.yaml  
yamllint config3.yaml
```

### Simple Decision Trees
```bash
# ❌ Don't script complex logic for
ls uploads/ | wc -l  # 7 files

# ✅ Just manually check each file
file uploads/doc1.pdf  # "PDF document, version 1.4"
file uploads/img2.jpg  # "JPEG image data"
# Make decisions based on what you see
```

## When TO Write Scripts

### High Volume
```bash
# ✅ Script makes sense here
find /logs -name "*.log" | wc -l  # 15,000 files
# Yes, write a script to process these
```

### Repeated Operations
```bash
# ✅ You'll do this weekly
# Write a script for recurring tasks
```

### Complex Logic
```bash
# ✅ Multi-step validation across many files
# Write a script when manual steps would be error-prone
```

## Decision Framework

Ask yourself:

1. **How many items?** 
   - < 10 items → Probably manual
   - > 50 items → Probably script
   - 10-50 items → Depends on complexity

2. **How often will this run?**
   - Once → Probably manual
   - Weekly → Probably script
   - Occasionally → Depends on complexity

3. **How complex is the logic?**
   - Simple check → Manual
   - Multi-step validation → Script
   - Complex conditionals → Script

## Examples

### ✅ **Good Manual Approach:**
```bash
# Task: "Check if these 5 API endpoints are responding"
curl -I https://api1.example.com/health
curl -I https://api2.example.com/health  
curl -I https://api3.example.com/health
curl -I https://api4.example.com/health
curl -I https://api5.example.com/health
```

### ❌ **Over-Scripted:**
```python
#!/usr/bin/env python3
import requests
import concurrent.futures
from typing import List

def check_endpoints(urls: List[str]) -> dict:
    """Check health of multiple endpoints with threading and error handling..."""
    # 30 lines of code for something that takes 30 seconds manually
```

### ✅ **Good Scripted Approach:**
```bash
# Task: "Check if these 100 log files contain errors"
# This many files? Script makes sense.
find /logs -name "*.log" -exec grep -l "ERROR" {} \;
```

## Red Flags for Over-Scripting

Stop and consider manual approach when:
- Writing more than 10 lines for a one-time task
- Spending more time writing the script than doing the task manually
- Adding error handling for edge cases that won't occur in your specific use case
- Creating reusable functions for something you'll never reuse

## Time Investment Guide

**5-minute rule**: If the manual task takes less than 5 minutes and you won't repeat it soon, don't script it.

**Script time vs. execution time**: If writing the script takes longer than doing the task manually × number of times you'll do it, don't script it.

## Remember

- **Efficiency over elegance** - Choose the approach that gets you to the result fastest
- **Manual doesn't mean sloppy** - You can still be systematic and thorough
- **Scripts aren't always better** - They introduce complexity, debugging, and maintenance overhead

**Sometimes `ls` and your eyes are the best tools for the job.**

---

# Rule: 03-digitalocean-security.md

---
id: digitalocean_security
description: "DigitalOcean security, access control, and hardening best practices"
---

# DigitalOcean Security

Implement security best practices for DigitalOcean infrastructure to protect against unauthorized access and ensure compliance.

## ✅ DO

### Access Control
- **Enforce SSH key authentication only** - disable password authentication
- **Use separate API tokens** per environment (dev/staging/prod)
- **Create sudo-capable user accounts** instead of using root directly
- **Disable root login** via SSH configuration

### System Hardening
- **Automate OS updates** via cron or unattended-upgrades
- **Configure automatic security updates** for critical patches
- **Use fail2ban** or similar intrusion prevention systems
- **Enable UFW or iptables** for host-based firewalls

### Network Security
- **Restrict SSH to known IPs** using DigitalOcean Firewalls
- **Use private networking** for internal service communication
- **Implement VPC isolation** between environments
- **Close unused ports** and services

### Secrets Management
- **Never store secrets** in code or environment variables directly
- **Use DO Secrets Manager** or HashiCorp Vault for sensitive data
- **Rotate API keys and tokens** regularly
- **Use service-specific credentials** with minimal required permissions

## ❌ DON'T

### Access Control Anti-patterns
- Don't use password authentication for SSH access
- Don't share API tokens between environments or team members
- Don't use root account for routine operations
- Don't hardcode credentials in deployment scripts

### Network Security Mistakes
- Don't expose services to 0.0.0.0/0 unless absolutely necessary
- Don't use default firewall rules without reviewing them
- Don't skip SSL/TLS termination for web services
- Don't trust internal network traffic without authentication

### Secrets Management Mistakes
- Don't commit secrets to version control in any form
- Don't use the same credentials across multiple environments
- Don't store database passwords in plain text configuration files
- Don't ignore credential rotation schedules

## Implementation Examples

### SSH Hardening
```bash path=null start=null
# /etc/ssh/sshd_config
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
```

### Firewall Setup
```bash path=null start=null
# Enable UFW and set defaults
ufw default deny incoming
ufw default allow outgoing

# Allow essential services
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw enable
```

### API Token Management
```bash path=null start=null
# Create environment-specific tokens
doctl auth init --context production
doctl auth init --context staging
doctl auth init --context development

# Switch between contexts
doctl auth switch --context production
```

### Automated Updates
```bash path=null start=null
# Enable unattended upgrades (Ubuntu/Debian)
echo 'Unattended-Upgrade::Automatic-Reboot "false";' >> /etc/apt/apt.conf.d/50unattended-upgrades
systemctl enable unattended-upgrades
```

## Security Checklist

### Initial Setup
- [ ] SSH keys configured, password auth disabled
- [ ] Root login disabled, sudo user created
- [ ] Firewall rules configured and enabled
- [ ] Automatic updates enabled
- [ ] Monitoring and alerting set up

### Ongoing Maintenance
- [ ] API tokens rotated quarterly
- [ ] Security updates applied monthly
- [ ] Access logs reviewed regularly
- [ ] Firewall rules audited quarterly
- [ ] Backup encryption verified

This approach provides defense in depth for DigitalOcean infrastructure while maintaining operational efficiency.

---

# Rule: 03-git-pager-handling.md

---
id: git_pager_handling
description: "Ensure git and GitHub CLI commands produce full output by disabling pagers"
---

# Git Command Pager Handling

When running git commands or GitHub CLI commands that might produce paginated output, always use pager-disabling options or pipe to cat to ensure full output is captured. Many git commands (like git log, git diff, gh repo view) use pagers by default, which can cause empty or incomplete output in AI interactions.

## Implementation

✅ **DO:**
- Use the `--no-pager` global flag for git commands: `git --no-pager log`
- Pipe output to cat for other commands: `gh repo view repo-name | cat`
- Set `uses_pager: true` in tool calls when commands might invoke a pager
- Be proactive about pager handling for any VCS or CLI tool that might paginate

❌ **DON'T:**
- Run git commands without pager considerations: `git log` (may truncate)
- Assume tools won't paginate output in AI environments
- Ignore pagination settings when using CLI tools through AI interfaces

## Common Commands Requiring Pager Handling

**Git Commands:**
```bash
git --no-pager log
git --no-pager diff
git --no-pager show
git --no-pager blame
```

**GitHub CLI:**
```bash
gh repo view repo-name | cat
gh pr list | cat
gh issue list | cat
```

**Other Tools:**
```bash
less file.txt | cat
man command | cat
```

## Rationale

Pagers are designed for interactive terminal use but can interfere with programmatic access to command output. In AI interactions, incomplete output leads to poor analysis and decision-making.

---

# Rule: 03-local-environment-macos.md

---
id: local_environment_macos
description: "Local development assumes macOS with Homebrew; use platform-appropriate approaches for cloud/CI environments"
---

# Local Environment: macOS

The local development machine runs macOS. Assume macOS conventions, paths, and tooling for any local scripting or development work.

## Local (macOS)

- Homebrew is the package manager — `brew install` is the default for local tooling
- Use macOS-native paths (`/usr/local/`, `/opt/homebrew/`, `~/Library/`, etc.)
- Assume `zsh` as the default shell
- Use `launchd` for local services, not `systemd`
- Prefer macOS-compatible flags for CLI tools (e.g. BSD `sed`, `date`, etc.) or use GNU versions installed via Homebrew when needed

## Remote / Cloud / CI

When working in non-local environments, use platform-appropriate tooling:

- **Docker**: Assume Debian/Alpine base images unless specified; use `apt-get` or `apk`
- **GitHub Actions**: Use Ubuntu runners by default; use `apt-get` for dependencies
- **DigitalOcean / Linux VMs**: Assume Ubuntu/Debian; use `apt-get` or `snap`
- **General**: Don't assume Homebrew or macOS tools are available outside the local machine

## ✅ DO

- Use `brew install` for local tool installation
- Detect the environment when writing cross-platform scripts
- Use `/bin/bash` or `/bin/sh` for portable scripts targeting CI/cloud
- Note BSD vs GNU differences when they matter (e.g. `sed -i ''` on macOS vs `sed -i` on Linux)

## ❌ DON'T

- Don't suggest `apt-get` for local macOS installs
- Don't suggest `brew` in Dockerfiles, CI pipelines, or remote servers
- Don't assume `systemd` locally or `launchd` remotely


---

# Rule: 03-python-error-handling.md

---
id: python_error_handling
description: "Python error handling, exception management, and robust error recovery patterns"
---

# Python Error Handling

Python error handling, exception management, and robust error recovery patterns.

## Exception Handling Best Practices

### Use Specific Exception Types
- **Use specific exception types**, not bare `except:`
- **Catch the most specific exception first**
- **Include meaningful error messages**
- **Log errors appropriately** with context

```python
# ✅ Good exception handling
try:
    result = api_call()
except requests.exceptions.RequestException as e:
    logger.error(f"API call failed: {e}")
    return None
except ValueError as e:
    logger.warning(f"Invalid data received: {e}")
    return default_value
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise

# ❌ Poor exception handling
try:
    result = api_call()
except:
    pass
```

### Exception Hierarchy
```python
# Handle exceptions from most specific to most general
try:
    process_data()
except FileNotFoundError:
    # Handle missing file specifically
    logger.error("Configuration file not found")
    create_default_config()
except PermissionError:
    # Handle permission issues
    logger.error("Permission denied accessing file")
    raise
except IOError:
    # Handle other I/O errors
    logger.error("I/O error occurred")
    raise
except Exception:
    # Handle any other unexpected errors
    logger.exception("Unexpected error during processing")
    raise
```

## Custom Exceptions

### Create Domain-Specific Exceptions
```python
class APIError(Exception):
    """Base exception for API-related errors."""
    pass

class AuthenticationError(APIError):
    """Raised when authentication fails."""
    pass

class ValidationError(Exception):
    """Raised when data validation fails."""
    
    def __init__(self, message, field=None, value=None):
        self.field = field
        self.value = value
        super().__init__(message)

class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    
    def __init__(self, message, config_key=None):
        self.config_key = config_key
        super().__init__(message)
```

### Using Custom Exceptions
```python
def validate_user_input(data):
    """Validate user input data."""
    if not data.get('email'):
        raise ValidationError("Email is required", field='email')
    
    if not data.get('age') or data['age'] < 0:
        raise ValidationError(
            "Age must be a positive number", 
            field='age', 
            value=data.get('age')
        )

def authenticate_user(token):
    """Authenticate user with token."""
    if not token:
        raise AuthenticationError("Token is required")
    
    if not is_valid_token(token):
        raise AuthenticationError("Invalid token provided")
```

## API Error Handling Patterns

### Retry Logic with Exponential Backoff
```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """Decorator for retrying functions with exponential backoff."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError, 
                       requests.exceptions.Timeout) as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    # Calculate delay with jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0.1, 0.3) * delay
                    time.sleep(delay + jitter)
                    
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.1f}s")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def make_api_call(url, data):
    """Make API call with automatic retry."""
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
    return response.json()
```

### Notion API Error Handling (Specific Example)
```python
import time
from notion_client import APIResponseError

def safe_notion_query(notion_client, **query_params):
    """Make Notion API call with proper error handling."""
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            return notion_client.databases.query(**query_params)
            
        except APIResponseError as e:
            if e.status == 429:  # Rate limited
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Rate limited, waiting {delay}s before retry")
                time.sleep(delay)
                continue
                
            elif e.status == 401:
                raise AuthenticationError("Invalid Notion API token")
                
            elif e.status == 404:
                raise APIError(f"Notion resource not found: {e}")
                
            else:
                logger.error(f"Notion API error: {e.status} - {e}")
                raise APIError(f"Notion API error: {e}")
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise APIError(f"Network error calling Notion API: {e}")
            
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
    
    raise APIError(f"Failed after {max_retries} attempts")
```

## Error Logging Best Practices

### Structured Logging
```python
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_user_data(user_id):
    """Process user data with proper error logging."""
    try:
        user = fetch_user(user_id)
        result = complex_processing(user)
        return result
        
    except ValidationError as e:
        logger.warning(
            f"Validation failed for user {user_id}: {e}",
            extra={'user_id': user_id, 'field': e.field}
        )
        raise
        
    except APIError as e:
        logger.error(
            f"API error processing user {user_id}: {e}",
            extra={'user_id': user_id}
        )
        raise
        
    except Exception as e:
        logger.exception(
            f"Unexpected error processing user {user_id}: {e}",
            extra={'user_id': user_id}
        )
        raise
```

### Context Managers for Resource Management
```python
import contextlib
from pathlib import Path

@contextlib.contextmanager
def safe_file_operation(file_path, mode='r'):
    """Context manager for safe file operations."""
    file_obj = None
    try:
        file_obj = open(file_path, mode)
        yield file_obj
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        raise
    except IOError as e:
        logger.error(f"I/O error with file {file_path}: {e}")
        raise
    finally:
        if file_obj:
            file_obj.close()

# Usage
try:
    with safe_file_operation('config.json') as f:
        data = json.load(f)
except (FileNotFoundError, PermissionError, IOError):
    # Handle errors appropriately
    data = create_default_config()
```

## Error Recovery Patterns

### Graceful Degradation
```python
def get_user_preferences(user_id, use_cache=True):
    """Get user preferences with graceful degradation."""
    try:
        # Try primary data source
        return fetch_from_database(user_id)
        
    except DatabaseError as e:
        logger.warning(f"Database error, trying cache: {e}")
        
        if use_cache:
            try:
                return fetch_from_cache(user_id)
            except CacheError:
                logger.warning("Cache also failed, using defaults")
        
        # Fall back to defaults
        return get_default_preferences()

def send_notification(user_id, message):
    """Send notification with multiple fallback methods."""
    methods = [
        ('email', send_email),
        ('sms', send_sms),
        ('push', send_push_notification)
    ]
    
    for method_name, method_func in methods:
        try:
            result = method_func(user_id, message)
            logger.info(f"Notification sent via {method_name}")
            return result
            
        except NotificationError as e:
            logger.warning(f"{method_name} notification failed: {e}")
            continue
    
    # All methods failed
    logger.error(f"All notification methods failed for user {user_id}")
    raise NotificationError("All notification methods failed")
```

## Best Practices

### ✅ DO:
- **Use specific exception types** that clearly indicate the error
- **Include contextual information** in error messages
- **Log errors with appropriate levels** (warning, error, critical)
- **Implement retry logic** for transient failures
- **Use context managers** for resource management
- **Create custom exceptions** for domain-specific errors
- **Handle errors at the appropriate level** in your application

### ❌ DON'T:
- **Use bare except clauses** - they catch everything, including system exits
- **Ignore exceptions silently** - always log or handle appropriately
- **Raise generic exceptions** when specific ones would be more helpful
- **Retry indefinitely** - always set retry limits
- **Log sensitive information** in error messages
- **Re-raise exceptions without context** - add meaningful information

**Remember: Good error handling makes your application more robust and easier to debug. Always think about what could go wrong and handle it gracefully.**

---

# Rule: 03-systematic-problem-solving.md

---
id: systematic_problem_solving
description: "Always use systematic, skeptical approach to problem-solving and debugging"
---

# Systematic Problem-Solving Approach

Never jump to conclusions. Always use a systematic, methodical approach to understanding and solving problems.

## Core principles

- Never jump to conclusions
- Always ask clarifying questions before diagnosing problems
- Break problems down into components before recommending solutions
- Validate assumptions before proposing any fix
- Do not start by problem-solving — start by debugging
- Never invent context or guess intent; ask first

## Debugging protocol

Always debug first — do not attempt a solution before the root cause is clear.

1. **Identify the problem**: Get full logs, error messages, stack traces
   - Clarify vague reports before analyzing the issue
   - Get concrete details: specific error messages, reproduction steps, environment info
   
2. **List and verify likely failure points**: Auth, DB, config, network, etc.
   - Test each point independently starting from the simplest
   - Count and verify - use concrete numbers to confirm scope of issue
   
3. **Investigate systematically**:
   - Start with verification: Check what should be there vs. what actually exists
   - Use command-line tools to validate assumptions (e.g., `unzip -l`, `find`, `wc -l`)
   - Test each component separately before integrating solutions
   - Follow the data: Let evidence guide investigation, not assumptions
   
4. **Evaluate each hypothesis separately**: Isolate the issue before proposing a fix
   - Reproduce the issue in isolation to confirm the root cause
   - If multiple suspects exist, test them separately
   - Use systematic elimination to narrow down the problem
   
5. **Test understanding**: Don't rely on the first Stack Overflow hit — understand the actual failure mode
6. **Eliminate systematically**: If multiple potential causes, eliminate them one by one

7. **Recommend solutions carefully**:
   - Propose solutions only after identifying the root cause
   - Address only the identified issue - avoid scope creep
   - Test the fix before considering the issue resolved
   - Verify the solution resolves the original problem completely

## Implementation Guidelines

### ✅ DO:
- Stay systematic - follow logical progression
- Use concrete evidence - numbers, logs, reproducible steps over assumptions
- Test incrementally - verify each step before moving to the next
- Document findings - track what you've tested and learned
- Build minimal reproducible examples

### ❌ DON'T:
- Jump between solutions without systematic investigation
- Make assumptions without verification
- Skip steps in the debugging process
- Run persistent commands (`npm run dev`, `npm start`) in terminal - use one-shot commands (`npm run build`)
- Fix multiple issues simultaneously

## Confidence and verification

- If unsure, state confidence level explicitly
- Suggest verification steps when uncertain
- Cite relevant standards or documentation when recommending tools or techniques
- Be transparent — explicitly note when something is inferred or uncertain


---

# Rule: 04-avoid-regex-parsing.md

---
id: avoid_regex_parsing
description: "Never use regular expressions for parsing structured text formats"
---

# Avoid Regex for Structured Data Parsing

Never use regular expressions for parsing or transforming structured text formats (like Markdown, HTML, JSON, YAML, or code).

Always use well-maintained, officially supported libraries that are purpose-built for the format you're working with.

## Examples

✅ **DO USE:**
- `remark` to modify Markdown documents
- `turndown` (mixmark-io) to convert HTML to Markdown
- YAML parser to handle frontmatter
- JSON.parse() for JSON data
- DOM parser for HTML manipulation

❌ **AVOID:**
- `text.replace(/#+ (.+)/g, ...)` to parse headings
- `htmlString.match(/<h[1-6]>(.*?)<\/h[1-6]>/g)` for DOM parsing
- Regex patterns for extracting YAML frontmatter
- Complex regex for code parsing

## Why This Matters

- **Reliability**: Regex is brittle and error-prone when applied to structured formats
- **Readability**: Parser libraries make your intent clearer to collaborators
- **Maintainability**: Purpose-built libraries handle edge cases and evolution of formats
- **Bug Prevention**: Reduces risk of subtle parsing errors and security vulnerabilities

## When Regex Is Appropriate

Regex should be used for:
- Simple string validation (email format, phone numbers)
- Find-and-replace operations on plain text
- Pattern matching in unstructured text
- Log parsing for specific known patterns

---

# Rule: 04-github-actions-workflow-standards.md

---
id: github_actions_workflow_standards
description: "Security, maintainability, and correctness standards for GitHub Actions workflows"
---

# GitHub Actions Workflow Standards

Write secure, maintainable, and correct GitHub Actions workflows by following these standards.

## Security

### Pin actions by SHA
- Always pin third-party actions to a full commit SHA, not a mutable tag
- Add a version comment for readability: `uses: actions/checkout@<sha> # v4`
- Floating tags (`@v4`, `@main`) can be silently replaced with malicious code

### Restrict permissions
- Always include an explicit `permissions` block at the workflow level
- Use the minimum permissions required (e.g., `contents: read` for CI)
- Never rely on the repository's default token permissions

### Pin Docker images
- Use specific version tags for Docker images, not `:latest`
- `:latest` is non-reproducible and can break without warning

## Maintainability

### Eliminate duplication with composite actions
- When the same setup steps repeat across multiple jobs, extract them into a local composite action (e.g., `.github/actions/setup-project/action.yml`)
- Composite actions accept inputs, making them flexible enough for slight variations (e.g., extra extensions, dev vs. prod installs)
- This reduces workflow files to business logic only

### Cache keys must reference committed files
- Cache keys like `hashFiles('**/lockfile')` only work if the lockfile is committed
- If a lockfile is gitignored, use the manifest file instead (e.g., `composer.json`, `package.json`)
- A cache key that always resolves to the same hash is effectively no cache at all

### Composer scripts must use vendor/bin/
- Always reference tools via `vendor/bin/<tool>` in `composer.json` scripts
- Bare command names (e.g., `phpunit`) depend on PATH, which varies between local, CI, and container environments
- This applies equally to `phpcs`, `phpstan`, `phpunit`, and any other Composer-installed binary

## act compatibility

- Use `if: ${{ !env.ACT }}` to skip steps that require GitHub infrastructure (artifact uploads, Pages deployment, PR comments, Docker-in-Docker)
- See the `local-ci-act` directive for full `act` setup and usage standards

## ✅ DO

- Pin all action versions by SHA with version comments
- Add explicit `permissions` block to every workflow
- Pin Docker image tags to specific versions
- Extract repeated steps into composite actions
- Verify cache keys reference committed files

## ❌ DON'T

- Don't use floating tags (`@v4`, `@latest`) for actions or Docker images
- Don't rely on default repository permissions
- Don't duplicate setup steps across multiple jobs
- Don't use bare command names in CI scripts when a full path is available
- Don't assume lockfiles exist in the repo without checking `.gitignore`


---

# Rule: 04-prefer-ssh-remotes.md

---
id: prefer_ssh_remotes
description: "Always use SSH instead of HTTPS for Git remotes and CLI tool authentication"
---

# Prefer SSH Remotes

Always configure Git remotes and CLI tools to use SSH instead of HTTPS for authentication.

## Core Principle

**SSH keys over password prompts.** SSH provides better security and eliminates repeated authentication prompts.

## Git Remotes

### ✅ **Preferred SSH Format:**
```bash
# When adding remotes
git remote add origin git@github.com:username/repository.git

# When cloning
git clone git@github.com:username/repository.git

# GitHub CLI setup
gh auth login  # Choose SSH when prompted
```

### ❌ **Avoid HTTPS Format:**
```bash
# Avoid these formats
git remote add origin https://github.com/username/repository.git
git clone https://github.com/username/repository.git
```

## Converting Existing HTTPS Remotes

### Check Current Remote
```bash
git remote -v
# origin  https://github.com/username/repo.git (fetch)
# origin  https://github.com/username/repo.git (push)
```

### Convert to SSH
```bash
git remote set-url origin git@github.com:username/repo.git

# Verify the change
git remote -v
# origin  git@github.com:username/repo.git (fetch)
# origin  git@github.com:username/repo.git (push)
```

## SSH Key Setup

### Generate SSH Key (if needed)
```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519
```

### Add to GitHub/GitLab/Bitbucket
```bash
# Copy public key to clipboard (macOS)
pbcopy < ~/.ssh/id_ed25519.pub

# Then add to your Git provider's SSH keys settings
```

### Test SSH Connection
```bash
# Test GitHub connection
ssh -T git@github.com

# Expected response:
# Hi username! You've successfully authenticated...
```

## CLI Tools Configuration

### GitHub CLI
```bash
# Login with SSH preference
gh auth login
# Choose: "GitHub.com"
# Choose: "SSH"
# Choose: "Upload your SSH public key"
```

### Other Git Providers
```bash
# GitLab
git clone git@gitlab.com:username/project.git

# Bitbucket  
git clone git@bitbucket.org:username/project.git

# Custom Git servers
git clone git@your-server.com:username/project.git
```

## Why SSH is Better

### ✅ **Security Benefits:**
- **No password transmission** - Keys are never sent over the network
- **Strong cryptographic authentication** - Much harder to compromise than passwords
- **Key-based access control** - Easy to revoke specific keys without affecting others

### ✅ **Convenience Benefits:**
- **No repeated login prompts** - Authentication happens automatically
- **Works with 2FA** - No need to generate tokens for command line access
- **Better for automation** - Scripts can run without interactive authentication

### ✅ **Performance Benefits:**
- **Faster connection setup** - No OAuth/token exchange overhead
- **Persistent connections** - SSH can reuse connections for multiple operations

## Common Issues and Solutions

### SSH Agent Not Running
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Make persistent (add to ~/.zshrc or ~/.bashrc)
echo 'eval "$(ssh-agent -s)"' >> ~/.zshrc
echo 'ssh-add ~/.ssh/id_ed25519' >> ~/.zshrc
```

### Permission Denied
```bash
# Check if key is added to agent
ssh-add -l

# If not listed, add it
ssh-add ~/.ssh/id_ed25519

# Verify key is uploaded to Git provider
```

### Wrong Key Used
```bash
# Specify key explicitly
ssh -i ~/.ssh/specific_key git@github.com

# Or configure in ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

## Team Guidelines

### For New Projects
- Always clone with SSH
- Add SSH setup to project README
- Include SSH key generation in onboarding docs

### For Existing Projects
- Convert HTTPS remotes to SSH during next setup
- Document the conversion process for team members
- Update deployment scripts to use SSH

**Remember: SSH setup takes 5 minutes once, but saves authentication headaches forever.**

---

# Rule: 04-python-standards.md

---
id: python_standards
description: "Core Python development standards and best practices overview"
---

# Python Standards Overview

Core Python development standards and best practices for consistent, maintainable code.

## Core Principles

### Code Quality Standards
- **Follow PEP 8** for style consistency
- **Use Black formatter** for automatic code formatting (88 character line length)
- **Write descriptive names** that clearly indicate purpose
- **Keep functions small** and focused on single responsibility
- **Use type hints** consistently across your codebase

### Development Environment
- **Always use virtual environments** (`venv`, `conda`, or `poetry`)
- **Never install packages globally** for project work
- **Use `python-dotenv`** for environment variable management
- **Include dependency files** (`requirements.txt` or `pyproject.toml`)

### Error Handling
- **Use specific exception types**, not bare `except:`
- **Create custom exceptions** for domain-specific errors
- **Include contextual information** in error messages
- **Implement retry logic** for transient failures

### Documentation
- **Use Google-style docstrings** for all public functions and classes
- **Include usage examples** in docstrings for complex functions
- **Document exceptions** that functions can raise
- **Use type hints** for function parameters and return values

### Testing
- **Use pytest** as the testing framework
- **Write descriptive test names** that explain the scenario
- **Use the AAA pattern** (Arrange, Act, Assert)
- **Mock external dependencies** to isolate units under test
- **Aim for high test coverage** (80%+) with focus on quality

## Quick Reference

### Basic Code Style
```python
# Good naming and structure
user_count = 42
MAX_RETRIES = 3

class UserManager:
    """Manages user operations."""
    
    def get_active_users(self) -> List[User]:
        """Return list of active users."""
        return self._fetch_users(active=True)
    
    def _fetch_users(self, active: bool = True) -> List[User]:
        """Internal method to fetch users."""
        pass
```

### Import Organization
```python
# Standard library
import os
from pathlib import Path
from typing import List, Optional

# Third-party
import requests
from django.conf import settings

# Local application
from .models import User
from .utils import helper_function
```

### Error Handling Pattern
```python
try:
    result = api_call()
except requests.exceptions.RequestException as e:
    logger.error(f"API call failed: {e}")
    return None
except ValueError as e:
    logger.warning(f"Invalid data: {e}")
    return default_value
```

## Essential Tools

### Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/  # or ruff check src/

# Type check
mypy src/

# Run tests with coverage
pytest --cov=src
```

### Project Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## Configuration Example

### pyproject.toml
```toml
[tool.black]
line-length = 88
target-version = ['py39']

[tool.mypy]
python_version = "3.9"
warn_return_any = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=html"
```

## Related Rules

For detailed guidance on specific areas:
- **Code Style**: See `python-code-style.md` for formatting and naming conventions
- **Error Handling**: See `python-error-handling.md` for exception patterns
- **Documentation**: See `python-documentation.md` for docstring and type hint standards
- **Testing**: See `python-testing.md` for comprehensive testing practices

**Remember: Consistency is key. Establish team standards and stick to them across your entire project.**


---

# Rule: 04-tone-neutral.md

---
id: tone_neutral
description: "Maintain a neutral, matter-of-fact tone without excessive positivity or enthusiasm"
---

# Neutral Tone

Use a neutral, matter-of-fact tone. Be friendly but concise. Avoid excessive positivity, filler, or enthusiasm. Prioritize clarity and precision.

## Core principle

Respond with professional neutrality. Don't inject artificial enthusiasm or overly positive language.

## Avoid

❌ "Great question!"  
❌ "I'd be happy to help!"  
❌ "Excellent work on..."  
❌ "Absolutely!"  
❌ "Perfect!"  
❌ "Amazing!"  
❌ "Sounds good!"

## Instead

✅ State facts directly  
✅ Answer the question  
✅ Acknowledge without embellishment  
✅ Use "yes" or "correct" instead of "absolutely" or "perfect"

## Examples

**Instead of**: "Great question! I'd be happy to help you with that. This is actually a really interesting problem!"

**Use**: "Here's how to solve that:"

---

**Instead of**: "Absolutely! That's a perfect approach. Great thinking!"

**Use**: "That approach works."

---

**Instead of**: "Thanks so much for the clarification! That's super helpful!"

**Use**: "Understood. Here's the updated solution:"


---

# Rule: 05-code-formatting-guidelines.md

---
id: code_formatting_guidelines
description: "Specific formatting preferences for code blocks, headings, and document structure"
---

# Code Formatting Guidelines

Use consistent formatting for code blocks, headings, and document structure.

## Code block formatting

- Use 4-space indentation for code blocks instead of triple backticks
- Single backticks are fine for inline code
- Maintain consistent indentation throughout code examples

## Code organization

- Define constant logic at the top of functions/modules, avoiding split logic between different control structures
- Keep related logic together rather than scattered across multiple conditional blocks
- Initialize variables and constants before using them in control flow

## Document structure

- Don't use '...' or '---' to divide sections unnecessarily
- Rely on proper heading structure for organization
- Don't bold headings (e.g., avoid `## **Heading**`)
- Use clean heading hierarchy without additional formatting

## Examples

✅ **Good code formatting:**

    function example() {
        const data = fetchData();
        return processData(data);
    }

✅ **Good logic organization:**

    function processUserData(users, filters) {
        // Define constants at the top
        const MAX_RESULTS = 100;
        const DEFAULT_SORT = 'name';
        const VALID_STATUSES = ['active', 'pending', 'inactive'];
        
        // Apply logic consistently
        const filteredUsers = users
            .filter(user => VALID_STATUSES.includes(user.status))
            .sort((a, b) => a[DEFAULT_SORT].localeCompare(b[DEFAULT_SORT]))
            .slice(0, MAX_RESULTS);
        
        return filteredUsers;
    }

❌ **Avoid scattered logic:**

    function processUserData(users, filters) {
        let results = [];
        for (let user of users) {
            const MAX_RESULTS = 100; // Don't define constants in loops
            if (user.status === 'active' || user.status === 'pending') {
                results.push(user);
            } else if (user.status === 'inactive') { // Split logic
                results.push(user);
            }
            if (results.length >= MAX_RESULTS) break;
        }
        return results;
    }

❌ **Avoid triple backticks for multi-line code**

✅ **Good heading structure:**

    # Main Heading
    ## Sub Heading
    ### Details

❌ **Avoid bolded headings:**

    ## **Sub Heading**


---

# Rule: 05-list-formatting.md

---
id: list_formatting
description: "Use consistent, scannable list formatting with proper structure and minimal nesting"
---

# List Formatting Standards

Use consistent, scannable formatting for lists to improve readability and structure.

## Basic list guidelines

- Use **single-level lists only** — no sub-bullets or excessive nesting
- Avoid starting a section directly with a list — include a brief intro paragraph first
- Use lists only when helpful — prefer paragraphs over stacked lists when appropriate

## Titled list items

When list items have titles:

- The title should be on the same line as the bullet
- Follow the title with a colon
- Format as: `- **Title:** Description or details`

## Examples

✅ **Good formatting:**
- **Define data contract:** Use the Data Attributes API to enumerate available fields

❌ **Bad formatting:**
- **Define data contract**  
Use the Data Attributes API to enumerate available fields

## Task list formatting

For action items:
- Format as: `**Action or Focus:** Clarifying detail`
- Keep items as human-readable task lines
- Avoid nested action items

## Structural guidelines

- Use proper heading hierarchy (`#`, `##`, `###`) for organization
- Follow every heading with a full sentence or paragraph before any list
- Prefer `#` for main section headings to improve scannability in flat editors
- Use **sentence case** for all section headings and subheadings

---

# Rule: 05-python-testing.md

---
id: python_testing
description: "Python testing standards using pytest with comprehensive test organization and coverage guidelines"
---

# Python Testing Standards

Python testing standards using pytest with comprehensive test organization and coverage guidelines.

## Testing Framework

### pytest as Standard
Use **pytest** as the primary testing framework for all Python projects:

```bash
# Install pytest with common plugins
pip install pytest pytest-cov pytest-mock pytest-xdist

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run tests in parallel
pytest -n auto
```

## Test Organization

### Directory Structure
```
project/
├── src/
│   ├── myproject/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── services.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api_integration.py
│   └── fixtures/
│       ├── sample_data.json
│       └── test_database.db
└── pytest.ini
```

### Test File Naming
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- Test classes: `Test*`

## Test Writing Best Practices

### Test Function Structure (AAA Pattern)
```python
import pytest
from myproject.services import UserService
from myproject.models import User

class TestUserService:
    """Test cases for UserService class."""
    
    def test_create_user_returns_user_when_valid_data_provided(self):
        """Test that create_user returns a User object with valid input."""
        # Arrange
        service = UserService()
        email = "test@example.com"
        name = "Test User"
        
        # Act
        result = service.create_user(email=email, name=name)
        
        # Assert
        assert isinstance(result, User)
        assert result.email == email
        assert result.name == name
        assert result.id is not None
    
    def test_create_user_raises_validation_error_when_invalid_email(self):
        """Test that create_user raises ValidationError with invalid email."""
        # Arrange
        service = UserService()
        invalid_email = "not-an-email"
        name = "Test User"
        
        # Act & Assert
        with pytest.raises(ValidationError, match="Invalid email format"):
            service.create_user(email=invalid_email, name=name)
```

### Descriptive Test Names
Use descriptive names that explain the scenario:

```python
# ✅ Good test names
def test_should_return_user_when_valid_id_provided(self):
def test_should_raise_not_found_error_when_user_does_not_exist(self):
def test_should_calculate_correct_total_when_multiple_items_provided(self):
def test_should_handle_empty_list_gracefully(self):

# ❌ Poor test names
def test_get_user(self):
def test_calculate(self):
def test_error(self):
```

## Fixtures and Test Data

### Using pytest Fixtures
```python
# conftest.py
import pytest
from myproject.database import Database
from myproject.models import User

@pytest.fixture
def database():
    """Provide a test database instance."""
    db = Database(":memory:")  # In-memory SQLite for tests
    db.create_tables()
    yield db
    db.close()

@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return User(
        id=1,
        email="test@example.com",
        name="Test User",
        is_active=True
    )

@pytest.fixture
def user_service(database):
    """Provide a UserService instance with test database."""
    from myproject.services import UserService
    return UserService(database=database)

@pytest.fixture
def sample_users():
    """Provide multiple sample users."""
    return [
        User(id=1, email="user1@test.com", name="User One"),
        User(id=2, email="user2@test.com", name="User Two"),
        User(id=3, email="user3@test.com", name="User Three"),
    ]
```

### Using Fixtures in Tests
```python
def test_get_user_returns_correct_user(user_service, sample_user):
    """Test retrieving a specific user."""
    # Arrange
    user_service.save_user(sample_user)
    
    # Act
    result = user_service.get_user(sample_user.id)
    
    # Assert
    assert result.email == sample_user.email
    assert result.name == sample_user.name

def test_get_all_users_returns_all_saved_users(user_service, sample_users):
    """Test retrieving all users."""
    # Arrange
    for user in sample_users:
        user_service.save_user(user)
    
    # Act
    result = user_service.get_all_users()
    
    # Assert
    assert len(result) == len(sample_users)
    assert all(isinstance(user, User) for user in result)
```

## Mocking and Patching

### Using pytest-mock
```python
def test_send_welcome_email_calls_email_service(mocker, user_service):
    """Test that welcome email is sent when user is created."""
    # Arrange
    mock_email_service = mocker.patch('myproject.services.EmailService')
    user_data = {"email": "test@example.com", "name": "Test User"}
    
    # Act
    user = user_service.create_user(**user_data)
    
    # Assert
    mock_email_service.send_welcome_email.assert_called_once_with(user.email)

def test_api_retry_logic_with_temporary_failure(mocker, api_client):
    """Test API retry logic with temporary failure."""
    # Arrange
    mock_request = mocker.patch('requests.post')
    mock_request.side_effect = [
        requests.exceptions.ConnectionError("Temporary failure"),
        mocker.Mock(status_code=200, json=lambda: {"success": True})
    ]
    
    # Act
    result = api_client.make_request("/test", {"data": "test"})
    
    # Assert
    assert result["success"] is True
    assert mock_request.call_count == 2
```

### Mocking External Services
```python
@pytest.fixture
def mock_notion_client(mocker):
    """Mock Notion client for testing."""
    client = mocker.Mock()
    client.databases.query.return_value = {
        "results": [
            {
                "id": "123",
                "properties": {
                    "Name": {"title": [{"plain_text": "Test Page"}]}
                }
            }
        ]
    }
    return client

def test_notion_service_processes_response_correctly(mock_notion_client):
    """Test that NotionService correctly processes API response."""
    # Arrange
    service = NotionService(client=mock_notion_client)
    database_id = "test-db-id"
    
    # Act
    result = service.get_pages(database_id)
    
    # Assert
    assert len(result) == 1
    assert result[0]["name"] == "Test Page"
    mock_notion_client.databases.query.assert_called_once_with(
        database_id=database_id
    )
```

## Parameterized Tests

### Testing Multiple Scenarios
```python
@pytest.mark.parametrize("email,expected_valid", [
    ("test@example.com", True),
    ("user@domain.org", True),
    ("invalid-email", False),
    ("@domain.com", False),
    ("user@", False),
    ("", False),
])
def test_email_validation(email, expected_valid):
    """Test email validation with various inputs."""
    from myproject.utils import is_valid_email
    
    result = is_valid_email(email)
    assert result == expected_valid

@pytest.mark.parametrize("age,expected_category", [
    (5, "child"),
    (12, "child"),
    (16, "teen"),
    (18, "adult"),
    (65, "senior"),
    (80, "senior"),
])
def test_age_categorization(age, expected_category):
    """Test age categorization logic."""
    from myproject.utils import categorize_age
    
    result = categorize_age(age)
    assert result == expected_category
```

### Complex Parameter Combinations
```python
@pytest.mark.parametrize("user_type,permissions,expected_access", [
    ("admin", ["read", "write", "delete"], True),
    ("user", ["read", "write"], False),
    ("guest", ["read"], False),
    ("admin", [], False),  # Admin with no permissions
])
def test_access_control(user_type, permissions, expected_access):
    """Test access control logic."""
    from myproject.auth import check_delete_access
    
    user = User(type=user_type, permissions=permissions)
    result = check_delete_access(user)
    assert result == expected_access
```

## Test Coverage

### Coverage Configuration
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Coverage Commands
```bash
# Run tests with coverage
pytest --cov=src

# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Show missing lines in terminal
pytest --cov=src --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=85
```

## Test Categories and Markers

### Using pytest Markers
```python
import pytest

@pytest.mark.unit
def test_user_model_validation():
    """Unit test for user model validation."""
    pass

@pytest.mark.integration
def test_database_connection():
    """Integration test for database operations."""
    pass

@pytest.mark.slow
def test_bulk_data_processing():
    """Slow test that processes large datasets."""
    pass

@pytest.mark.api
def test_external_api_integration():
    """Test external API integration."""
    pass
```

### Running Specific Test Categories
```bash
# Run only unit tests
pytest -m unit

# Run integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run API tests only
pytest -m api
```

## Error and Exception Testing

### Testing Expected Exceptions
```python
def test_divide_by_zero_raises_zero_division_error():
    """Test that division by zero raises appropriate error."""
    from myproject.calculator import divide
    
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_invalid_user_id_raises_validation_error_with_message():
    """Test specific error message for invalid user ID."""
    service = UserService()
    
    with pytest.raises(ValidationError, match="User ID must be positive"):
        service.get_user(-1)

def test_api_timeout_raises_timeout_error():
    """Test API timeout handling."""
    api_client = APIClient(timeout=0.1)
    
    with pytest.raises(TimeoutError) as exc_info:
        api_client.slow_operation()
    
    assert "Request timed out" in str(exc_info.value)
```

## Performance Testing

### Basic Performance Tests
```python
import time
import pytest

def test_user_creation_performance():
    """Test that user creation completes within reasonable time."""
    service = UserService()
    
    start_time = time.time()
    user = service.create_user("test@example.com", "Test User")
    execution_time = time.time() - start_time
    
    assert user is not None
    assert execution_time < 1.0  # Should complete within 1 second

@pytest.mark.slow
def test_bulk_operation_performance(sample_users):
    """Test bulk operations performance."""
    service = UserService()
    
    start_time = time.time()
    results = service.bulk_create_users(sample_users)
    execution_time = time.time() - start_time
    
    assert len(results) == len(sample_users)
    assert execution_time < 5.0  # Should complete within 5 seconds
```

## Best Practices

### ✅ DO:
- **Write descriptive test names** that explain the scenario
- **Use the AAA pattern** (Arrange, Act, Assert) for test structure
- **Test both happy path and error cases**
- **Use fixtures** for common test data and setup
- **Mock external dependencies** to isolate units under test
- **Aim for high test coverage** (80%+) but focus on quality over quantity
- **Use parametrized tests** for testing multiple similar scenarios
- **Keep tests independent** - they should be able to run in any order

### ❌ DON'T:
- **Write tests that depend on external services** in unit tests
- **Test implementation details** - test behavior, not internal structure
- **Write overly complex tests** - if a test is hard to understand, simplify it
- **Skip edge cases** - test boundary conditions and error scenarios
- **Use real databases or files** in unit tests - use mocks or in-memory alternatives
- **Ignore failing tests** - fix them immediately or remove them
- **Test everything** - focus on critical business logic and public APIs

**Remember: Good tests serve as documentation, catch regressions, and give confidence when refactoring code.**

---

# Rule: 05-validate-sources.md

---
id: validate_sources
description: "Always validate tool features, config formats, or APIs against authoritative and current sources before use"
---

# Validate Sources

When referencing features, configuration files, or APIs from tools (e.g. Cursor, Warp, Copilot, ChatGPT), always **validate against at least one authoritative source** to confirm they are current and supported.

## Preferred verification sources

In order of reliability:

1. **Official documentation or product website** (e.g. `docs.cursor.com`, `docs.warp.dev`, `docs.github.com/copilot`)
2. **Release notes or changelogs** on official channels (e.g. GitHub Releases, product blog posts)
3. **Official community forums or Slack/Discord announcements** maintained by the vendor
4. **Actively maintained GitHub repositories** from the tool maintainers

## When uncertain

If you cannot verify against authoritative sources:

- Explicitly mark the information as **uncertain or possibly deprecated**
- Suggest checking the above sources directly instead of asserting as fact
- Prefer pointing to the most likely replacement feature (if identifiable) with a note that it requires confirmation

## Rationale

Many AI toolchains evolve quickly and deprecate features (e.g. `.cursorrules`). This prevents reliance on outdated or unsupported practices.

---

# Rule: 06-database-evolution-principle.md

---
id: database_evolution_principle
description: "Prefer extending existing databases with new columns over creating separate databases for each feature"
---

# Database Evolution Principle

When working with CSV-type databases, prefer extending existing databases with new columns rather than creating separate databases for everything.

## Core Principle

**Evolve, don't multiply.** Enhance existing data structures non-destructively rather than fragmenting data across multiple databases.

## Preferred Approach: Column Extension

### ✅ **Extend Existing Database:**
```csv
# Original users.csv
user_id,name,email,created_at
1,John Doe,john@example.com,2024-01-01
2,Jane Smith,jane@example.com,2024-01-02

# After adding subscription feature
user_id,name,email,created_at,subscription_tier,subscription_start
1,John Doe,john@example.com,2024-01-01,premium,2024-01-15
2,Jane Smith,jane@example.com,2024-01-02,basic,2024-01-10
```

### ❌ **Avoid Database Fragmentation:**
```csv
# users.csv
user_id,name,email,created_at
1,John Doe,john@example.com,2024-01-01

# subscriptions.csv (separate database)
user_id,subscription_tier,subscription_start  
1,premium,2024-01-15

# user_preferences.csv (another separate database)
user_id,theme,notifications
1,dark,enabled

# user_analytics.csv (yet another database)
user_id,last_login,page_views
1,2024-01-20,45
```

## When Column Extension Makes Sense

### ✅ **Good Candidates for Column Addition:**
- **Related user attributes** (preferences, settings, status)
- **Simple feature flags** (is_verified, is_premium)
- **Timestamp tracking** (last_updated, last_login)
- **Calculated fields** (total_orders, lifetime_value)
- **Status fields** (subscription_status, account_status)

### ✅ **Benefits:**
- **Single source of truth** - All user data in one place
- **Simpler queries** - No complex joins across multiple files
- **Easier maintenance** - One schema to manage
- **Better performance** - No cross-database lookups for basic operations
- **Clearer relationships** - Data naturally belongs together

## When to Create Separate Databases

### ✅ **Valid Reasons for Separation:**

#### High Volume/Performance Issues
```csv
# If user events table becomes massive (millions of rows)
users.csv          # User profiles (hundreds/thousands of rows)
user_events.csv    # Event tracking (millions of rows)
```

#### Fundamentally Different Entities
```csv
users.csv          # User entities
products.csv       # Product catalog
orders.csv         # Transaction records
```

#### Security/Access Separation
```csv
users.csv          # Public user data
user_secrets.csv   # API keys, encrypted data (restricted access)
```

#### Complex Relationships (Many-to-Many)
```csv
users.csv          # One user
user_skills.csv    # Many skills per user
skills.csv         # Skill definitions
```

## Implementation Guidelines

### Non-Destructive Column Addition
```python
# ✅ Safe column addition
def add_subscription_columns(csv_file):
    # Add columns with sensible defaults
    df['subscription_tier'] = df.get('subscription_tier', 'free')
    df['subscription_start'] = df.get('subscription_start', None)
    return df
```

### Gradual Migration
```python
# ✅ Migrate data gradually
def migrate_subscription_data():
    users_df = pd.read_csv('users.csv')
    subscriptions_df = pd.read_csv('subscriptions.csv')  # Old separate file
    
    # Merge subscription data into users
    merged = users_df.merge(subscriptions_df, on='user_id', how='left')
    merged.to_csv('users.csv', index=False)
    
    # Archive old file instead of deleting
    subscriptions_df.to_csv('archived/subscriptions_backup.csv', index=False)
```

### Handle Missing Data Gracefully
```python
# ✅ Robust handling of new columns
def get_user_subscription(user_id):
    user = users_df[users_df['user_id'] == user_id].iloc[0]
    
    # Handle cases where new columns might not exist for all rows
    tier = user.get('subscription_tier', 'free')
    start_date = user.get('subscription_start', None)
    
    return tier, start_date
```

## Decision Framework

Ask yourself before creating a new database:

1. **Is this data fundamentally about the same entity?**
   - User preferences → Add to users.csv
   - Product reviews → Separate reviews.csv

2. **Will queries commonly need both datasets?**
   - User profile + subscription status → Same database
   - User profile + detailed analytics → Consider separation

3. **Is performance becoming an issue?**
   - < 100K rows → Probably keep together
   - > 1M rows → Consider separation

4. **Do these fields have different update patterns?**
   - Profile updated occasionally, login timestamps updated frequently → Consider separation

## Common Patterns

### ✅ **User Profile Evolution:**
```csv
# Start simple
user_id,name,email

# Add authentication
user_id,name,email,password_hash,created_at

# Add preferences  
user_id,name,email,password_hash,created_at,theme,language,notifications

# Add subscription
user_id,name,email,password_hash,created_at,theme,language,notifications,subscription_tier,billing_cycle
```

### ✅ **Product Catalog Evolution:**
```csv
# Start with basics
product_id,name,price,description

# Add inventory tracking
product_id,name,price,description,stock_count,last_restocked

# Add categorization
product_id,name,price,description,stock_count,last_restocked,category,tags,featured
```

## Remember

- **Start simple** - Begin with broader schemas and refactor when necessary
- **Monitor performance** - Separate when file size/query performance becomes problematic  
- **Preserve relationships** - Keep related data together when it makes logical sense
- **Non-destructive changes** - Always add columns, rarely remove them

**A well-evolved single database is usually better than a constellation of tiny, fragmented databases.**

---

# Rule: 06-no-code-in-briefs.md

---
id: no_code_in_briefs
description: "Prevents inclusion of code examples in planning or brief-type documents"
---

# No Code in Briefs

When generating **briefs, task drafts, project overviews, or planning docs**, do not include code examples or implementation details.

## What to avoid

- Code examples, snippets, or implementation details
- Specific syntax or technical implementations
- Opinionated solutions before exploration begins

## What to include instead

- Keep content conceptual, requirements-level, or descriptive only
- Express technical details in plain language, not code
- Focus on the problem and requirements rather than solutions

## Rationale

The purpose is to avoid opinionated solutions before proper exploration and analysis begins. Planning documents should focus on understanding the problem space and requirements, not prescribing specific technical implementations.

---

# Rule: 07-development-cleanup-guidelines.md

---
id: development_cleanup_guidelines
description: "Remove temporary files and development artifacts that shouldn't persist in codebases before committing"
---

# Development File Cleanup Guidelines

Remove temporary files and development artifacts that shouldn't persist in the codebase, especially before committing to version control.

## Files to Clean Up

### Temporary Files
- `*.tmp`, `*.temp`, `temp-*`
- `*.bak`, `*.backup`, `*.orig`
- `.cache`, `node_modules/.cache`
- OS-specific temporary files (`.DS_Store`, `Thumbs.db`)

### Development Artifacts
- `console.log()`, `console.debug()` statements
- `debugger;` statements  
- Large blocks of commented-out code
- Test files created during development
- Debugging print statements (`print()`, `echo`, etc.)

### Build and Cache Artifacts
- `dist/` directory before new builds (unless ignored)
- `build/` output directories
- `.cache/` directories
- Compiled files that should be regenerated

### Project-Specific Artifacts
- Unused images in asset directories (`src/assets/images/uploads/`)
- Deprecated config files (e.g., `.cursorrules`)
- Temporary data files
- Screenshot files from debugging
- Generated files that should not be committed

## When to Clean Up

### Before Committing
- **Always remove debug code** and temporary files
- Review diff for unintended inclusions
- Clean up console/debug statements
- Remove temporary test code

### After Development Sessions  
- Clean temporary artifacts created during development
- Remove downloaded test files or samples
- Clear debugging output files

### Before Deployment
- Ensure no development files are included in build
- Remove test-specific configurations
- Clean up any hardcoded debugging values

### During Code Review
- Check for overlooked debug statements
- Identify temporary files that slipped through
- Remove experimental code that didn't make it to final solution

### Proactive Cleanup Offers
**After completing tasks or reaching milestones**, proactively offer to clean up temporary files:
- Ask "Should I clean up the temporary files from this work?"
- Be specific about what would be removed
- **Never automatically delete files** - always ask permission
- Provide clear file/folder names and locations
- Explain why files are no longer needed

**Example cleanup offers:**
- "I can remove the `/temp/analysis-data/` folder and the 3 `test-output.json` files"
- "The download cache in `/temp/` is no longer needed. Clean it up?"
- "We have 15 test files from the processing. Keep them or remove?"
- "This analysis created several temp folders in Downloads. Should I clean them up?"

## Cleanup Commands

### Quick Cleanup
```bash
# Remove common temp files
find . -name "*.tmp" -delete
find . -name "*.temp" -delete
find . -name "temp-*" -delete

# Remove backup files
find . -name "*.bak" -delete
find . -name "*.orig" -delete

# Remove OS-specific files
find . -name ".DS_Store" -delete
find . -name "Thumbs.db" -delete
```

### Git-Based Cleanup
```bash
# See untracked files before cleaning
git status --ignored

# Clean untracked files (be careful!)
git clean -n  # dry run first
git clean -fd # remove untracked files and directories

# Remove files from git but keep locally
git rm --cached filename
```

### Code Pattern Cleanup
```bash
# Find console.log statements
grep -r "console\.log" src/ --include="*.js" --include="*.ts"

# Find debugger statements  
grep -r "debugger" src/ --include="*.js" --include="*.ts"

# Find print statements in Python
grep -r "print(" . --include="*.py"
```

### Project-Specific Cleanup
```bash
# Remove dist/build before rebuild
rm -rf dist/ build/

# Clean npm/node artifacts
npm run clean  # if available
rm -rf node_modules/.cache/
```

## Best Practices

### ✅ DO:
- **Review diffs carefully** before committing to catch overlooked artifacts
- **Use .gitignore** to prevent temporary files from being tracked
- **Set up pre-commit hooks** to automatically clean common artifacts  
- **Document cleanup commands** in project README if project-specific
- **Use build scripts** that clean before building
- **Remove debug code** as you finish each development session

### ❌ DON'T:
- Commit console.log or debug statements to production code
- Leave large commented-out code blocks - remove or document why they're kept
- Include temporary test files in commits
- Skip reviewing the diff - easy to miss temporary files
- Use `git clean -fd` without understanding what it will remove
- Leave hardcoded debugging values in configuration files

## Integration with Workflow

### Pre-commit Checklist
1. **Search for debug statements**: `grep -r "console\.log\|debugger\|print(" src/`
2. **Check for temp files**: `find . -name "*.tmp" -o -name "*.temp"`
3. **Review git status**: `git status` - look for unintended additions
4. **Clean if needed**: Remove identified artifacts
5. **Final review**: Check diff one more time before commit

### Automated Cleanup
Consider setting up:
- Pre-commit hooks that run cleanup commands
- Build scripts that clean before building
- Linting rules that catch debug statements
- `.gitignore` patterns for common temporary files

**Remember: A clean codebase is easier to maintain, debug, and deploy. Make cleanup part of your regular development workflow.**

---

# Rule: 07-pr-summary-standards.md

---
id: pr_summary_standards
description: "Structured pull request summaries with emoji titles and issue-first sourcing approach"
---

# Pull Request Summary Standards

Write short, goal-based PR summaries with emoji titles that help reviewers understand context and changes. Never repeat the diff content.

## Title Format

PR titles must start with an emoji prefix:

- 🌪 **New value** · new feature or major addition
- 💨 **Enhancement** · improvements to existing features
- 🧰 **DevX** · developer tooling/workflow changes
- 💡 **KTLO** · routine maintenance/operations
- 🚑 **Hotfix** · urgent critical fix
- 🐛 **Defect** · bug fix for live features

**Example title:**
`💨 Speed up CI by caching pnpm store`

## Content Guidelines

### No Screenshots, Links, or Feature Flags
- Keep summaries text-only for clarity
- Avoid external dependencies in PR descriptions
- Focus on the essential information

### Sourcing Rule for AI
- **If an issue exists**: Read the issue first, then scan code changes, then write the summary
- **If no issue**: Infer intent from the code changes

## Required Structure

### Top Line (Issue Reference)
- If closing an issue: `closes #123`
- If related only: `relates to #123`

### Three-Section Format

**Goal:** Why this PR exists (1–2 sentences)
**Scope:** High-level description of what changed (not the diff details)  
**How to test:** Steps reviewers can follow, with expected result

## Example Summary

```
closes #123

**Goal:** Reduce CI time to under 8 minutes by caching dependencies.
**Scope:** Add `actions/cache` keyed to lockfile; no app logic changes.
**How to test:** Push branch, confirm cache restore in install step, total job < 8 minutes.
```

## What NOT to Include

- **Don't repeat the diff** - reviewers can see file changes
- **Don't include rationale** - that goes in the issue or commit messages
- **Don't list every file changed** - focus on the high-level impact
- **Don't include implementation details** - stick to the "what" and "why"

## AI Assistant Guidelines

When helping write PR summaries:

1. **Always check for linked issues first** - read the full issue context
2. **Scan the code diff** - understand the technical changes
3. **Focus on business impact** - why does this matter to the team/product?
4. **Keep it scannable** - busy reviewers need quick context
5. **Make testing actionable** - provide specific steps, not vague suggestions

---

# Rule: 08-directory-organization-philosophy.md

---
id: directory_organization_philosophy
description: "Philosophy for organizing directories, configs, and avoiding tool pollution in home directory"
---

# Directory Organization Philosophy

Maintain clean separation between different types of files and avoid tools that pollute the home directory with unnecessary initialization files.

## ✅ DO

**Directory Structure Principles**
- Separate configuration files, data files, and applications
- Use dedicated directories for different purposes: `~/Projects/`, `~/Unito/`, etc.
- Keep the home directory clean of application-specific files when possible
- Use `~/.config/` for configuration files that support XDG Base Directory specification

**Project Organization**
- Use logical directory hierarchies: `~/Projects/personal/`, `~/Unito/work-projects/`
- Group related projects together by context (work, personal, experiments)
- Keep project templates and standards consistent across similar projects
- Document project structure and conventions in README files

**Configuration Management**
- Store configurations in version-controlled dotfiles
- Use tools that support clean directory structures (chezmoi, not random dotfile dumps)
- Separate machine-specific configs from universal configs
- Keep backup configurations for critical tools

## ❌ DON'T

**Avoid Directory Pollution**
- Don't use tools that create unnecessary files in home directory (like `warp init` in home)
- Don't let package managers scatter config files everywhere without organization
- Don't mix personal and work projects in the same directory structure
- Don't create deep nested hierarchies that make navigation difficult

**Anti-patterns to Avoid**
- Don't use tools that force their directory structure on you
- Don't accept default locations if they create clutter
- Don't ignore where tools put their files - be intentional about organization
- Don't let tools create initialization files in places you don't want them

## Integration Points

**With Dotfiles Management**
- Use chezmoi for version-controlled config files
- Keep dotfiles repository clean and well-organized
- Document which configs are managed where

**With Development Tools**
- Configure tools to use appropriate directories (`~/.config/` when supported)
- Use project-local configurations when possible
- Avoid global installations that affect all projects unnecessarily

**With Package Managers**
- Use virtual environments and project-local dependencies
- Keep global installations minimal and purposeful
- Document global dependencies and their purposes

This approach maintains a clean, navigable system while supporting efficient development workflows.

---

# Rule: 08-project-templates-standards.md

---
id: project_templates_standards
description: "Standards for creating project templates and maintaining consistent development practices across projects"
---

# Project Templates & Standards

Establish consistent project initialization and development standards to ensure quality and maintainability across all projects.

## ✅ DO

**Project Template Components**
- Create template repositories for common project types (Python, Node.js, Astro, WordPress)
- Include essential files in templates: README.md, .gitignore, .envrc template, LICENSE
- Add basic CI/CD configuration appropriate for the project type
- Include development environment setup instructions
- Provide code quality tools configuration (linting, formatting, testing)

**README.md Standards**
- Include clear project description and purpose
- Document installation and setup requirements
- Provide usage examples and common commands
- Include contribution guidelines and development setup
- Document environment variables and configuration requirements

**Code Quality Standards**
- Set up automatic code formatting (black, prettier, etc.)
- Configure linting rules appropriate for the language/framework
- Include basic test structure and examples
- Set up pre-commit hooks where beneficial
- Document coding conventions and style guidelines

**Project Structure Conventions**
- Use consistent directory structures within project types
- Separate source code, tests, documentation, and configuration
- Include scripts directory for common development tasks
- Use standard locations for configuration files
- Document any deviations from standard structure

## ❌ DON'T

**Template Maintenance Mistakes**
- Don't let templates become outdated with old dependencies or practices
- Don't include sensitive information or credentials in templates
- Don't create overly complex templates that obscure simple projects
- Don't skip documentation of template choices and conventions

**Project Setup Anti-patterns**
- Don't skip project setup automation when it would save repeated work
- Don't ignore established conventions without good reason
- Don't mix different architectural patterns within the same project type
- Don't leave placeholder content in production-ready projects

## Template Categories

**Backend Projects (Python/Node.js/etc.)**
- Virtual environment setup instructions
- Database configuration examples
- API documentation structure
- Environment variable templates
- Docker configuration for development and production

**Frontend Projects (React/Astro/etc.)**
- Build tool configuration
- Asset management setup
- Component organization structure
- Testing framework integration
- Deployment pipeline configuration

**WordPress Projects**
- Theme/plugin development structure
- Local development environment (Docker/Local)
- Build tools for assets (Webpack/Vite)
- WordPress coding standards configuration
- Deployment and staging procedures

**Full-Stack Projects**
- Monorepo or multi-repo organization
- Shared configuration management
- Development environment orchestration
- Cross-service communication patterns
- Integrated testing strategies

## Integration with AI Rules

**Rulebook-AI Integration**
- Include .rulebook-ai configuration in project templates
- Document which AI rule packs are recommended for each project type
- Provide project-specific AI rules when needed
- Keep AI rules consistent with project conventions

**Code Generation Standards**
- Establish patterns for AI-generated code review
- Document when AI assistance is appropriate vs. manual coding
- Include AI-generated code attribution in comments when helpful
- Maintain consistency between AI-generated and manually written code

## Quality Assurance

**Template Testing**
- Regularly test project templates on clean environments
- Verify all dependencies install correctly
- Test that basic project functions work out of the box
- Update templates when dependencies or practices change

**Documentation Maintenance**
- Keep setup instructions current with actual requirements
- Test documentation steps on different operating systems when relevant
- Update examples and screenshots when interfaces change
- Gather feedback from developers using the templates

**Version Management**
- Tag template versions to allow rollback if needed
- Document major changes and migration paths
- Keep changelog of template updates
- Coordinate template updates with team practices

## Automation Opportunities

**Project Initialization**
- Create scripts to generate projects from templates
- Automate initial git setup and remote configuration
- Set up development environment with single command when possible
- Generate project-specific documentation from templates

**Maintenance Scripts**
- Create scripts to update existing projects with template changes
- Automate dependency updates across similar projects
- Generate reports on project compliance with standards
- Batch update common configuration changes

This approach ensures consistent, high-quality project initialization while reducing repetitive setup work and maintaining standards across all development efforts.

---

# Rule: 09-documentation-first-research.md

---
id: documentation_first_research
description: Always prioritize comprehensive official documentation research before attempting custom implementations
---

# Documentation-First Research Protocol

## Core Principle

**ALWAYS research official documentation thoroughly before attempting any custom implementation, workaround, or third-party solution.**

## Research Protocol

### 1. Official Documentation Deep Dive
✅ **DO:**
- Search the complete official documentation, not just getting started guides
- Look specifically for:
  - Built-in features that solve your exact use case
  - Template systems, themes, or layout options
  - Configuration options and frontmatter
  - Advanced features and reference sections
- Check examples, tutorials, and advanced guides
- Look for "reference" sections which often contain comprehensive feature lists

❌ **DON'T:**
- Skip to Stack Overflow or tutorials without exhausting official docs
- Assume a feature doesn't exist because it's not in the getting started guide
- Start with custom implementations before confirming no built-in solution exists

### 2. Documentation Search Strategy
✅ **Search for these patterns:**
- Templates, themes, layouts
- Configuration, frontmatter, options
- Built-in components or features
- Override, customize, extend
- Advanced features, reference guides

### 3. Framework-Specific Research
✅ **For any framework/tool:**
- Check the complete API reference
- Look for plugin/extension ecosystems
- Search for "recipes" or "guides" sections
- Check GitHub discussions, issues, and examples
- Review changelog for recent feature additions

## Implementation Rule

**Only after exhaustive documentation research should you consider:**
1. Custom implementations
2. Third-party libraries
3. Workarounds or hacks
4. Overriding core functionality

## Real-World Example

❌ **What happened:** Weeks spent creating custom landing page overrides for Astro Starlight
✅ **What should have happened:** Found the built-in `splash` template in the frontmatter reference documentation in 10 minutes

## Verification Questions

Before any custom implementation, ask:
1. Have I read the complete official documentation?
2. Have I checked the API reference section?
3. Have I searched for built-in templates, themes, or layouts?
4. Have I looked at the configuration/frontmatter options?
5. Does this framework have a feature that already solves this exact problem?

## Time Investment Rule

Spend at least 30 minutes in official documentation before considering custom solutions. Complex frameworks may require 1-2 hours of documentation research.

---

# Rule: 09-repository-creation-standards.md

---
id: repository_creation_standards
description: "Standardize repository creation using GitHub CLI with secure defaults"
---

# Repository Creation Standards

When creating or managing repositories, use consistent tooling and secure defaults to ensure proper repository management practices.

## Implementation

### Repository Creation
✅ **DO:**
- Use GitHub CLI (`gh` command) for repository operations instead of web interfaces
- Default to private repositories unless explicitly told otherwise
- Use `gh repo create repo-name --private` as the standard creation command
- Only use `--public` when specifically requested by the user

❌ **DON'T:**
- Create repositories through web interfaces when CLI is available
- Default to public repositories without explicit user request
- Use inconsistent tooling across repository operations

### Command Standards

**Repository Creation:**
```bash
# Default (secure)
gh repo create project-name --private

# Only when explicitly requested
gh repo create project-name --public

# With additional options
gh repo create project-name --private --description "Project description" --clone
```

**Repository Management:**
```bash
# Consistent use of gh CLI for other operations
gh repo view
gh repo clone owner/repo-name
gh repo fork owner/repo-name
```

## Rationale

- **Security First**: Private by default reduces risk of accidental data exposure
- **Tool Consistency**: Using GitHub CLI provides consistent, scriptable repository management
- **Audit Trail**: CLI operations are easier to track and reproduce than web interface actions
- **Automation Ready**: CLI-based operations integrate better with scripts and workflows

---

# Rule: 10-dotfiles-management-chezmoi.md

---
id: dotfiles_management_chezmoi
description: "Effective dotfiles management using chezmoi with automated workflows and proper file organization"
---

# Dotfiles Management with chezmoi

Use chezmoi for version-controlled, automated dotfiles management with clear separation between managed configs and dynamic content.

## ✅ DO

**File Management Strategy**
- Use `chezmoi managed` to verify what's tracked before making changes
- Use `chezmoi re-add` (no arguments) to update all modified managed files at once
- Use `chezmoi re-add <file>` for specific files when you know exactly what changed
- Use `chezmoi status` to see what's been modified before re-adding
- Keep `.gitignore` comprehensive to prevent unwanted file tracking

**Content Organization**
- Separate configuration files (managed by chezmoi) from dynamic/generated content
- Use templates only when files need variable substitution across machines
- Store machine-specific configs in separate files (e.g., `.gitconfig-work`)
- Document the purpose of each managed file in README.md

**Repository Hygiene**
- Include comprehensive `.gitignore` for macOS (`.DS_Store`, `._*`, etc.)
- Use `encrypted_*DS_Store*` patterns to catch encrypted unwanted files
- Set up autocommit and autopush for seamless updates
- Use descriptive commit messages that explain what changed

**Backup and Recovery**
- Keep backup copies of critical configs before major changes
- Use `chezmoi archive` for full backups before system changes
- Document recovery procedures in README.md
- Test dotfiles installation on clean systems periodically

## ❌ DON'T

**Avoid These Mistakes**
- Don't track dynamic content like logs, caches, or generated files
- Don't use chezmoi for secrets management - use direnv instead
- Don't commit `.DS_Store` or other OS-generated files
- Don't edit files directly in `~/.local/share/chezmoi/` - use `chezmoi edit`

**Management Anti-patterns**
- Don't add entire directories without understanding what's in them
- Don't use encryption for non-sensitive files that need frequent access
- Don't ignore the `.gitignore` - add patterns proactively
- Don't skip `--dry-run` testing for complex changes

## Common Workflows

**Daily Updates**
```bash
# Check what's changed
chezmoi status

# Update all modified files
chezmoi re-add

# Or update specific files
chezmoi re-add ~/.zshrc ~/.gitconfig
```

**Adding New Files**
```bash
# Add a new config file
chezmoi add ~/.newconfig

# Add with encryption (only if needed)
chezmoi add ~/.sensitive-config --encrypt
```

**Preventing Unwanted Files**
```bash
# Check what would be added before doing it
find ~/config-dir -name ".*" | head -10

# Use .gitignore patterns like:
# .DS_Store
# *.log
# *.cache
# encrypted_*DS_Store*
```

**Cross-Machine Sync**
```bash
# On new machine
chezmoi init --apply username/dotfiles

# Regular updates
chezmoi update
```

## Integration with Other Tools

**With direnv (for secrets)**
- Don't manage `.envrc` files with chezmoi (they're project-specific)
- Don't manage `~/.config/secrets/` with chezmoi (contains sensitive data)
- Do document the relationship in README.md

**With package managers**
- Track package manager config files (`.npmrc`, etc.)
- Don't track package installation lists unless they're minimal
- Use separate setup scripts for package installation

**Repository Structure**
```
dotfiles-repo/
├── .gitignore                    # Comprehensive exclusions
├── README.md                     # Usage and recovery docs
├── dot_zshrc                     # Shell configuration
├── dot_gitconfig                 # Git configuration
├── private_dot_ssh/              # SSH configs and keys
└── .chezmoiignore               # chezmoi-specific exclusions
```

This approach maintains clean, version-controlled dotfiles while avoiding common pitfalls and keeping sensitive data properly separated.

---

# Rule: 10-system-maintenance-cleanup.md

---
id: system_maintenance_cleanup
description: "Systematic approach to identifying, evaluating, and cleaning up deprecated system configurations and folders"
---

# System Maintenance and Cleanup

Regularly audit and clean up deprecated configurations, unused folders, and outdated system setups to maintain a clean development environment.

## ✅ DO

**Regular Audit Process**
- Review hidden folders in home directory periodically (`ls -la ~ | grep "^\."`)
- Check for duplicate functionality (e.g., multiple secrets management approaches)
- Investigate unfamiliar folders before deletion - they may serve active purposes
- Compare file modification dates to identify potentially deprecated content
- Look for references in configs before removing directories

**Safe Cleanup Methodology**
- Always create backups before removing configurations: `cp -r ~/.old-config ~/.old-config.backup`
- Use `find` and `grep` to search for references before deletion
- Test functionality after removal to ensure nothing breaks
- Document cleanup decisions for future reference
- Remove empty directories after migrating contents: `rmdir ~/.empty-folder`

**Configuration Migration**
- Consolidate similar functionality into single, well-organized locations
- Update all references when moving configurations
- Use consistent patterns (e.g., all secrets in `~/.config/secrets/`)
- Maintain clear documentation of new organization
- Test all dependent systems after migration

**Version Control Integration**
- Update dotfiles repository to reflect cleanup changes
- Remove old entries from tracking (e.g., `chezmoi forget ~/.deprecated-config`)
- Update README files to document new organization
- Commit cleanup changes with clear messages

## ❌ DON'T

**Avoid These Cleanup Mistakes**
- Don't remove folders without understanding their purpose
- Don't assume folders are deprecated based on age alone - check if they're actively used
- Don't skip searching for references in scripts, configs, and documentation
- Don't delete unique configurations that don't have clear replacements

**Migration Anti-patterns**
- Don't leave broken references after moving configurations
- Don't create multiple competing systems for the same function
- Don't ignore error messages after cleanup - they indicate missed references
- Don't rush cleanup - systematic investigation prevents mistakes

## Investigation Workflow

**Identify Potential Cleanup Candidates**
```bash
# Find hidden folders/files modified more than 90 days ago
find ~ -maxdepth 1 -name ".*" -type d -mtime +90

# Look for duplicate functionality
ls -la ~/.config/ | grep -i secret
ls -la ~ | grep -i secret
```

**Evaluate Before Removal**
```bash
# Check for references in common config locations
grep -r "deprecated-folder" ~/.zshrc ~/.bashrc ~/.config/ ~/.*rc

# Look for recent file access
find ~/.deprecated-folder -type f -atime -30  # accessed in last 30 days
```

**Safe Removal Process**
```bash
# 1. Create backup
cp -r ~/.deprecated-config ~/.deprecated-config.$(date +%Y%m%d)

# 2. Remove from version control if tracked
chezmoi forget ~/.deprecated-config

# 3. Remove actual folder
rm -rf ~/.deprecated-config

# 4. Test dependent systems
```

## Common Cleanup Scenarios

**Secrets Management Consolidation**
- Migrate from multiple secrets locations to single `~/.config/secrets/` structure
- Update all environment variable references to new paths
- Remove old secrets directories only after confirming migration success
- Update documentation to reflect new organization

**Dotfiles Organization**
- Remove files from dotfiles tracking that are now managed elsewhere
- Consolidate similar configuration files
- Clean up `.gitignore` patterns after removing tracked files
- Update repository documentation

**Tool Migration**
- Remove old tool configurations after migrating to new tools
- Update shell aliases and PATH modifications
- Clean up old scripts and shortcuts
- Document tool migration decisions

This systematic approach prevents accidental deletion of important configurations while maintaining a clean, organized development environment.

---

# Rule: 11-env-var-management.md

---
id: env_var_management
description: "Standard patterns for loading environment variables with direnv and .env fallback"
---

# Environment Variable Management

Support two automatic methods for loading environment variables in every project: direnv (recommended) and `.env` file fallback. No manual `source` or `export` commands needed.

## File Responsibilities

```
.env.example          — Template. Committed to git. Lists all required vars.
.env                  — Local values. Gitignored. Never committed.
.envrc                — direnv config. Committed. Loads .env then secrets.
Makefile              — Loads .env as fallback if direnv isn't active.
```

## Precedence (highest wins)

1. Shell environment (already exported vars)
2. direnv / secret manager overrides
3. `.env` file values

## ✅ DO

**direnv Setup (Primary)**
- Use `dotenv_if_exists` in `.envrc` to load `.env` when present
- Override with secrets from a secrets manager (e.g. `export-secret`) when available
- Require only `direnv allow` for first-time setup

**`.env` Fallback (Secondary)**
- Provide `.env.example` with all required vars and comments
- Conditionally load `.env` in Makefile only when env vars aren't already set
- Ensure all workflows function with just a `.env` file for contributors without direnv

**Adding a New Variable**
- Add to `.env.example` with an empty value and a comment
- Add the `export` line to `.envrc`
- Add a `ifndef` warning block in Makefile if it depends on it
- Document it in the project README

**Naming Conventions**
- Terraform variables: `TF_VAR_<variable_name>` — prefix uppercase, variable name lowercase (e.g. `TF_VAR_cloudflare_api_token`)
- Provider/tool credentials: Use the name the tool expects natively (e.g. `CLOUDFLARE_API_TOKEN`, `AWS_ACCESS_KEY_ID`)
- Project-specific: `SCREAMING_SNAKE_CASE` (e.g. `R2_ENDPOINT`)

## ❌ DON'T

- Don't commit `.env` — it's gitignored
- Don't pass secrets as CLI arguments — use env vars that tools read natively (`TF_VAR_*`, `AWS_*`), not `-var` or `-backend-config` flags
- Don't let `.env.example` drift from `.envrc` — every variable should appear in both
- Don't require direnv — all workflows must work with just `.env`


---

# Rule: 12-implementation-standards.md

---
id: implementation_standards
description: "Use libraries and methods with active support, prioritizing maintainability and ecosystem standards"
---

# Implementation Standards

Solutions should prioritize maintainability, readability, and alignment with ecosystem standards.

## Documentation Research Priority

**BEFORE ANY IMPLEMENTATION: Research official documentation thoroughly.**

- Always check complete official documentation before attempting custom solutions
- Look specifically for built-in features, templates, configuration options
- Search API reference sections and advanced guides, not just getting started docs
- Verify that no built-in functionality already solves the problem
- Only consider custom implementations after exhaustive documentation research

## Library and tool selection

- Use libraries and methods with active support and documentation
- Don't copy solutions that rely on obscure hacks or unmaintained packages
- Prefer standard libraries over regex-based hacks
- Recommend only actively maintained and safe libraries (check commit activity and issues)
- Avoid abandoned or deprecated packages

## Language-specific guidelines

**JavaScript/TypeScript**: Prefer `URL`, `path`, or platform-native utilities for routing and string parsing over brittle regular expressions.

## Best practice enforcement

- Validate that recommended tools or methods follow current best practices
- Ensure compatibility with the project's existing environment and configurations
- If a standard or config file exists (e.g., `.phpcs.xml.dist`, `phpstan.neon`, `settings.json`), defer to those
- Avoid re-defining behavior that is already handled by CLI tools or linters
- Prefer configurations that are command-line-friendly and visible in version control

## Shell command reliability

**Keep shell commands simple and testable**: Avoid complex chained commands that are difficult to debug and prone to failure.

✅ **Reliable approaches:**
- Use separate commands instead of complex chains with multiple `&&` operators
- Test commands individually before chaining them
- Place complex variable substitutions in separate variables first
- Use basic ASCII characters for formatting rather than Unicode/emojis in critical operations

❌ **Avoid:**
- Chaining more than 2-3 commands with `&&` when complexity increases
- Mixing complex variable substitution with heavy formatting in single commands
- Relying on Unicode characters in automated scripts

## New project initialization

- Start from first principles — don't inherit assumptions from other stacks
- Research and validate all tool or architecture recommendations
- Build one component at a time; verify functionality before moving on
- Ensure each module is independently testable and documented
- Include a minimal, accurate README with setup, usage, and testing instructions


---

# Rule: 13-inline-comments-guidelines.md

---
id: inline_comments_guidelines
description: "Guidelines for writing clear, concise inline comments that enhance code readability by explaining reasoning and context"
---

# Inline Comments Guidelines

Write clear, concise inline comments that enhance code readability by explaining the "why" and "reasoning" behind decisions, not restating what the code obviously does.

## Core Principle

**Comments should enhance code readability** by explaining reasoning behind business logic, architectural decisions, and providing context for future maintainers.

## When to Comment

### ✅ DO Comment:
- **Explain reasoning** behind business logic or architectural decisions
- **Document complex algorithms** or non-obvious implementations
- **Clarify edge cases** or workarounds for external limitations
- **Provide context** for future maintainers about historical decisions
- **Document assumptions** that might not be obvious
- **Explain "magic numbers"** or configuration values
- **Describe performance optimizations** and their trade-offs

### ❌ DON'T Comment:
- **Obvious code** that clearly describes what it does
- **Simple variable assignments** or basic operations
- **Self-documenting code** where the intent is clear from naming
- **Every single line** - over-commenting reduces readability

## Formatting Requirements

### General Comments
- Use **sentence case** (capitalize first word)
- Include **proper punctuation** (periods, commas, etc.)
- Keep comments **brief and focused**
- Place comments **above** the relevant code line(s)
- Use consistent comment style for the language

### Language-Specific Formats
```php
// PHP: Use double slashes for single-line comments.
/* PHP: Use block comments for multi-line explanations. */
```

```javascript
// JavaScript: Use double slashes for single-line comments.
/* JavaScript: Use block comments for multi-line explanations. */
```

```python
# Python: Use hash for single-line comments.
"""Python: Use triple quotes for docstrings and multi-line comments."""
```

## Comment Examples

### ✅ Good Comments

```php
// Validate user permissions before processing sensitive data.
if (!current_user_can('manage_options')) {
    return new WP_Error('insufficient_permissions');
}

// Cache expensive API response for 5 minutes to reduce load.
$cached_data = get_transient('api_response_' . $user_id);

// Workaround for legacy browser compatibility with CSS Grid.
if (!$this->supports_modern_css()) {
    $this->use_fallback_layout();
}

// Rate limit API calls to avoid hitting external service limits.
if ($this->get_request_count() > self::MAX_REQUESTS_PER_MINUTE) {
    sleep(60);
}
```

```javascript
// Debounce search input to avoid excessive API calls during typing.
const debouncedSearch = debounce(handleSearch, 300);

// Handle legacy browser compatibility for CSS Grid.
if (!CSS.supports('display', 'grid')) {
  fallbackToFlexbox();
}

// Batch DOM updates to prevent layout thrashing.
requestAnimationFrame(() => {
  elements.forEach(el => el.classList.add('active'));
});
```

```python
# Cache API responses to avoid redundant network calls during development.
cached_response = cache.get(api_key, max_age_hours=6)

# Convert timestamps to UTC to ensure consistent timezone handling.
utc_timestamp = local_time.astimezone(timezone.utc)

# Use binary search for O(log n) lookup performance on large datasets.
index = bisect.bisect_left(sorted_data, target_value)
```

### ❌ Poor Comments

```php
// Set the variable to true
$is_enabled = true;

// Loop through the array
foreach ($items as $item) {
    // Do something with the item
    process_item($item);
}

// Get the user ID
$user_id = get_current_user_id();
```

```javascript
// Get the element
const element = document.getElementById('myElement');

// Add click event listener
element.addEventListener('click', handleClick);

// Return the result
return result;
```

```python
# Increment counter
counter += 1

# Print the value
print(value)

# Create empty list
items = []
```

## TODO Comments

### Format
All TODO comments must follow this exact format:

```
// TODO: [clear, actionable description]
```

### Examples

```php
// TODO: Implement proper error handling for failed API calls.
// TODO: Add unit tests for this authentication function.
// TODO: Remove debug logging before production deployment.
// TODO: Optimize database queries for better performance.
```

```javascript
// TODO: Add loading states for better user experience.
// TODO: Extract this logic into a reusable custom hook.
// TODO: Implement proper error boundaries for component failures.
// TODO: Add accessibility attributes for screen readers.
```

```python
# TODO: Implement retry logic for failed API requests.
# TODO: Add type hints for better code documentation.
# TODO: Optimize algorithm for better time complexity.
# TODO: Add validation for edge cases.
```

### TODO Guidelines
- Write **clear, actionable descriptions**
- Use **sentence case** with proper punctuation
- Focus on **what needs to be done**, not how
- Place TODO comments **immediately before** the relevant code
- **Remove TODOs** when the work is completed
- **Track TODOs** in issue trackers for larger tasks

## Complex Logic Documentation

### Algorithm Explanations
```python
# Implement Floyd's cycle detection algorithm to find duplicates.
# Uses two pointers moving at different speeds to detect cycles in O(n) time.
slow = nums[0]
fast = nums[0]

# Phase 1: Detect if cycle exists
do:
    slow = nums[slow]
    fast = nums[nums[fast]]
while slow != fast:
```

### Business Logic Context
```javascript
// Apply promotional discount only for first-time customers
// during the holiday season (Nov 1 - Jan 15) to increase conversion.
const isEligibleForDiscount = (
  customer.isFirstTime &&
  isHolidaySeason(currentDate) &&
  !customer.hasUsedPromotion
);
```

### Performance Optimizations
```php
// Pre-load user permissions to avoid N+1 query problem.
// Single query fetches all permissions instead of individual lookups.
$user_permissions = $this->get_bulk_user_permissions($user_ids);
```

## Best Practices

### ✅ DO:
- **Focus on the "why"** rather than the "what"
- **Explain business rules** and their context
- **Document assumptions** that might not be obvious
- **Use proper grammar** and punctuation
- **Keep comments current** - update them when code changes
- **Write for future maintainers** including yourself in 6 months

### ❌ DON'T:
- **State the obvious** - good code is self-documenting
- **Write novels** - keep comments concise and focused
- **Leave outdated comments** - they mislead more than they help
- **Comment bad code** - refactor it instead
- **Use comments to disable code** - use version control instead

## Comment Maintenance

### During Code Reviews
- **Check comment accuracy** - do they still match the code?
- **Identify missing context** - where would comments help future maintainers?
- **Remove obvious comments** - they add noise without value
- **Ensure TODO format** - consistent formatting helps tracking

### During Refactoring
- **Update relevant comments** when changing code behavior
- **Remove outdated comments** that no longer apply
- **Add comments for new complexity** introduced during refactoring

**Remember: Good comments explain WHY the code exists and WHY decisions were made, not WHAT the code is doing.**

---

# Rule: 14-local-ci-act.md

---
id: local_ci_act
description: "Standards for running GitHub Actions locally with act to catch CI failures before pushing"
---

# Local CI Testing with act

Use [`act`](https://github.com/nektos/act) to run GitHub Actions workflows locally in Docker containers. Catch CI failures before pushing and avoid burning Actions minutes.

## Prerequisites

- Docker Desktop (or compatible runtime like Colima) running
- `act` installed: `brew install act`

## Project Setup

### `.actrc` (commit this)

Create `.actrc` in the project root with default flags:

```
-P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-24.04
--container-architecture linux/amd64
```

- Use `catthehacker/ubuntu:act-*` images — purpose-built for act, much smaller than official runner images
- `--container-architecture linux/amd64` is required on Apple Silicon Macs
- Available tags: `act-22.04`, `act-24.04`. Use `full-*` variants only if `act-*` is missing tools your workflow needs

### Makefile Target (recommended)

Wrap `act` invocations so the team has a single command:

```makefile
test-ci:
	@command -v act >/dev/null 2>&1 || { echo "act not installed. Run: brew install act"; exit 1; }
	act pull_request -W .github/workflows/ci.yml \
		--secret TOKEN_A="$$TOKEN_A" \
		--secret TOKEN_B="$$TOKEN_B"
```

The `$$` escaping passes shell variables through Make's parser. Secrets come from direnv-loaded env vars — never from committed files.

## ✅ DO

**Secrets Handling**
- Pass secrets from env vars via `--secret` flags — never store in committed files
- Use `--secret` for `${{ secrets.X }}` references; use `--env` for `${{ env.X }}` references
- Add `.env`, `.secrets` to `.gitignore`
- For `GITHUB_TOKEN`, pass manually: `--secret GITHUB_TOKEN="$(gh auth token)"`

**Workflow Compatibility**
- Pin actions by SHA, not tag: `uses: actions/checkout@<sha> # v4.3.1`
- Use `if: ${{ !env.ACT }}` to skip steps that won't work locally (artifact uploads, PR comments, caching)
- Keep secrets generic — map repo-specific secret names to generic env vars in the workflow's `env:` block

**Running Workflows**
- Use `act <event> -n` for dry runs before real runs
- Use `act <event> -W .github/workflows/<file>.yml` to target specific workflows
- Use `act <event> -j <job>` to run a single job
- Use `act workflow_dispatch --input action=plan` to pass dispatch inputs

## ❌ DON'T

- Don't use `ubuntu-latest=ubuntu:24.04` images — missing runner tooling
- Don't use deprecated `nektos/act-environments-ubuntu:18.04` images
- Don't expect `actions/cache`, service containers, or `workflow_run` events to work
- Don't store secrets in `.actrc` or any committed file

## Troubleshooting

- **Image not found / slow first run**: First pull is ~1.2GB, one-time cost. Ensure Docker is running.
- **exec format error (Apple Silicon)**: Add `--container-architecture linux/amd64` to `.actrc`
- **Fails in act but works on GitHub**: Check for GitHub API dependencies, unsupported features, or missing tools in `act-*` images
- **Permission denied on scripts**: Add `chmod +x` before running or use `bash script.sh`
- **Secrets not available**: Confirm `--secret` (not `--env`) for `${{ secrets.X }}` references
- **Auth errors**: Run `direnv allow` to reload env vars

## Debugging

```bash
act pull_request -v          # verbose output
act pull_request -v -v       # very verbose (Docker commands)
act pull_request --reuse     # keep containers after failure for inspection
docker exec -it <id> bash    # shell into container
```


---

# Rule: 15-package-management-standards.md

---
id: package_management_standards
description: "Standards for managing packages across different language ecosystems and keeping environments clean"
---

# Package Management Standards

Maintain clean, reproducible environments across different programming languages and package managers while avoiding dependency conflicts.

## ✅ DO

**Language Managers**
- Use version managers for each language: `pyenv` (Python), `nvm` (Node.js), `rbenv` (Ruby)
- Install language versions as needed per project, not globally
- Document required language versions in project files (`.python-version`, `.nvmrc`)
- Keep system package managers (Homebrew) separate from language package managers

**Virtual Environments**
- Use virtual environments for all Python projects (`venv`, `virtualenv`, or `poetry`)
- Use project-local `node_modules` for Node.js projects
- Isolate dependencies per project to avoid conflicts
- Document environment setup steps in project README files

**Dependency Management**
- Pin dependency versions in lock files (`requirements.txt`, `package-lock.json`, `composer.lock`)
- Separate development dependencies from production dependencies
- Keep dependency lists minimal - only include what's actually needed
- Regularly audit and update dependencies for security

**Homebrew Essentials**
- Use Homebrew for system tools and utilities, not programming language runtimes
- Keep a `Brewfile` for essential system packages
- Document purpose of each Homebrew package
- Regular cleanup with `brew cleanup` and `brew autoremove`

## ❌ DON'T

**Avoid Global Pollution**
- Don't install language packages globally unless absolutely necessary
- Don't mix system packages with language-specific packages
- Don't let package managers install to system directories without explicit permission
- Don't ignore lock files or commit history of dependency changes

**Common Mistakes**
- Don't use `sudo` for language package installations
- Don't install different versions of the same package globally
- Don't skip virtual environments "for quick scripts"
- Don't commit `node_modules/` or other dependency directories to version control

**Version Management**
- Don't rely on system-installed language versions for development
- Don't skip documenting version requirements
- Don't assume other developers have the same versions installed
- Don't mix global and local package installations carelessly

## Package Manager Best Practices

**Python (pip/pipenv/poetry)**
```bash
# Use virtual environments
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Or use poetry
poetry install
poetry shell
```

**Node.js (npm/yarn)**
```bash
# Use exact versions
nvm use  # reads from .nvmrc
npm install --exact
npm ci   # for production/CI builds
```

**Homebrew (system tools)**
```bash
# Essential tools only
brew install git gh direnv age
brew bundle  # from Brewfile
brew cleanup
```

## Environment Reproducibility

**Documentation Requirements**
- Document all required versions in project files
- Include setup instructions in README.md
- List any global dependencies that must be installed
- Provide troubleshooting steps for common environment issues

**CI/CD Integration**
- Use same package manager commands in CI as locally
- Pin versions in CI environments
- Cache dependencies appropriately
- Test with clean environments regularly

This approach ensures consistent, reproducible development environments while keeping system and project dependencies properly isolated.

---

# Rule: 16-secrets-management-direnv.md

---
id: secrets_management_direnv
description: "Modern secrets management using direnv with organized ~/.config/secrets/ structure"
---

# Secrets Management with direnv

Use direnv for project-specific, context-aware secrets management with organized file structure in `~/.config/secrets/`.

## File Organization

```
~/.config/secrets/
├── personal.env           # Personal API keys (Dropbox, Trakt.tv, etc.)
├── unito.env              # Work-related API keys (OpenAI, Airtable, etc.)
└── credentials/           # JSON/binary credential files (service accounts)
    └── *.json
```

## ✅ DO

**Environment File Format**
- Use `KEY=value` format without `export` statements
- No quotes needed unless value contains spaces or special chars
- Group related secrets with comments
- One environment variable per line

**Project Setup**
- Create `.envrc` files in project directories to load secrets using `~/.config/scripts/export-secret`
- Secrets are NOT sourced directly - use the `export-secret` helper to selectively export variables
- Use `~/.config/secrets/personal.env` for personal projects
- Use `~/.config/secrets/unito.env` for work projects

**Security Practices**
- Never commit `.envrc` files to version control (add to `.gitignore`)
- Use full paths for credential files: `GOOGLE_APPLICATION_CREDENTIALS="/Users/username/.config/secrets/credentials/service-account.json"`
- Keep backup copies of secrets files with `.backup` extension
- Store JSON credentials in `credentials/` subfolder

**direnv Workflow**
- Run `direnv allow` after creating/editing `.envrc` files
- Use `direnv reload` after modifying secrets files
- Check `direnv status` to verify what's loaded
- Use `env | grep -E "(API_KEY|TOKEN|CREDENTIALS)"` to verify secrets are loaded

## ❌ DON'T

**Anti-patterns**
- Don't use global shell exports in `.zshrc` or `.bashrc` for project secrets
- Don't mix personal and work secrets in the same file
- Don't use tilde (`~`) paths in environment variables - use full paths
- Don't commit secrets to version control in any form
- Don't use `source` or `source_env` to load entire secrets files - use `export-secret` for selective loading

**Avoid These Legacy Approaches**
- Don't use `.env` files in project roots (security risk)
- Don't use encrypted dotfile managers for frequently-changing secrets
- Don't source secrets globally in shell startup files
- Don't hardcode secrets in scripts or configuration files
- Don't source entire secrets files - only export what's needed for the project

## Integration Examples

**Using export-secret Helper**

The `~/.config/scripts/export-secret` utility selectively exports variables from secrets files:

```bash
# Usage: export-secret VARIABLE_NAME [secrets_file]
# If secrets_file is omitted, defaults to ~/.config/secrets/unito.env
```

**Personal Project `.envrc`**
```bash
# Load specific secrets from personal.env
eval "$(~/.config/scripts/export-secret TRAKT_CLIENT_ID ~/.config/secrets/personal.env)"
eval "$(~/.config/scripts/export-secret TRAKT_CLIENT_SECRET ~/.config/secrets/personal.env)"
eval "$(~/.config/scripts/export-secret TRAKT_ACCESS_TOKEN ~/.config/secrets/personal.env)"
eval "$(~/.config/scripts/export-secret TRAKT_REFRESH_TOKEN ~/.config/secrets/personal.env)"

# Project-specific settings
export PROJECT_NAME=my-project
```

**Work Project `.envrc`**
```bash
# Load work secrets (defaults to unito.env)
eval "$(~/.config/scripts/export-secret OPENAI_API_KEY)"
eval "$(~/.config/scripts/export-secret AIRTABLE_API_KEY)"

# Or specify file explicitly
eval "$(~/.config/scripts/export-secret DATABASE_URL ~/.config/secrets/unito.env)"
```

**Mixed/Sandbox Project `.envrc`**
```bash
# Load secrets from both personal and work files
eval "$(~/.config/scripts/export-secret DROPBOX_TOKEN ~/.config/secrets/personal.env)"
eval "$(~/.config/scripts/export-secret OPENAI_API_KEY ~/.config/secrets/unito.env)"

# Project settings
export ENVIRONMENT=development
```

## Troubleshooting

**Secrets not loading**
1. Check if you're in a directory with `.envrc` file
2. Run `direnv allow` to approve the `.envrc` file
3. Verify file paths are absolute (no tilde expansion issues)
4. Use `direnv status` to check loading status

**Path resolution issues**
- Use absolute paths for all file references
- Avoid shell expansion (use `/Users/username/` not `~/`)
- Check file permissions are readable

This approach provides project-isolation while maintaining organized, secure secrets management.

---

# Rule: 17-secrets-storage-standards.md

---
id: secrets_storage_standards
description: "Standard hierarchy and naming conventions for organizing secrets across projects and environments"
---

# Secrets Storage Standards

Define a consistent structure for storing and organizing credentials, API keys, tokens, and other secrets. These conventions are backend-agnostic — they apply whether using `pass`, AWS Secrets Manager, 1Password, Vault, or any other system.

## Path Hierarchy

Organize secrets using a shallow, predictable structure:

```
<context>/<service>/<credential-type>
```

- **Context**: Top-level grouping by business domain or environment
- **Service**: The external service or internal system
- **Credential type**: The specific secret

Keep depth to 2–3 levels. Deeper nesting creates friction without adding clarity.

## Standard Credential Type Names

Use these consistently across all services:

- `api-key` — general-purpose API key
- `access-token` — OAuth or bearer token
- `refresh-token` — OAuth refresh token
- `client-id` — OAuth client identifier
- `client-secret` — OAuth client secret
- `access-key-id` — AWS-style access key identifier
- `secret-access-key` — AWS-style secret key
- `personal-token` — personal access token (e.g. GitHub PAT)
- `password` — account password
- `webhook-secret` — webhook signing secret
- `signing-key` — cryptographic signing key
- `connection-string` — database or service connection string
- `service-account` — service account credential (often a JSON file path)

If a service has only one credential, the type alone is sufficient (e.g. `work/openai/api-key`).

## Context Groupings

- `work/` — credentials for work projects and internal services
- `personal/` — personal accounts and side projects
- `infrastructure/` — cloud providers, CI/CD, hosting, DNS
- `shared/` — team-shared credentials (use sparingly)

## ✅ DO

**Naming**
- Use **lowercase** throughout
- Use **hyphens** to separate words (not underscores or camelCase)
- Use **explicit credential types** from the standard list above
- Make names self-documenting — someone unfamiliar with the project should understand the purpose

**Organization**
- One secret per entry — don't combine multiple values in a single entry
- Use the standard credential type names before inventing new ones
- Preserve the `context/service/credential-type` structure regardless of backend

**Usage in Scripts**
- Export secrets via env vars: `export OPENAI_API_KEY=$(pass show work/openai/api-key)`
- Use `pass show <context>/<service>/` to list all secrets for a service

## ❌ DON'T

- Don't store secrets in version control — not in code, `.env` files, or config files
- Don't nest deeper than 3 levels
- Don't duplicate secrets across contexts — pick one location and reference it
- Don't call everything `key` — use the specific credential type name
- Don't skip documentation for non-obvious secrets

## Migration

When migrating between backends:
- Preserve the `context/service/credential-type` path structure
- Map paths directly to the new system
- Update retrieval commands in scripts and `.envrc` files
- Verify all references resolve after migration


---

# Rule: 18-simple-solutions-principle.md

---
id: simple_solutions_principle
description: "Prefer simple, direct solutions over complex workarounds"
---

# Simple Solutions Principle

Prefer simple, direct solutions over complex workarounds. When you find yourself adding layers of abstraction, parameters, or conditional logic to solve a problem, step back and ask: "Is there a simpler way?"

## Anti-Patterns to Avoid

### ❌ Redundant Parameters
Don't add parameters to track what the system already knows:
```yaml
# BAD: Adding unnecessary parameters
inputs:
  isAutomated: true  # System already knows this
  triggerSource: "workflow"  # Context provides this
```

### ❌ Complex Conditionals
Don't create complex logic when simpler approaches exist:
```yaml
# BAD: Complex conditionals
if: always() && github.event_name == 'workflow_dispatch' && inputs.isAutomated != true
```

### ❌ Workarounds Instead of Proper Solutions
Don't use CLI calls when proper APIs exist:
```yaml
# BAD: Using CLI workarounds
run: gh workflow run other-workflow.yml -f param1=value1
```

### ❌ Multiple Ways to Do the Same Thing
Don't support multiple approaches for identical functionality:
```yaml
# BAD: Duplicate trigger types
on:
  workflow_dispatch: # Complex inputs
  workflow_call:     # Nearly identical inputs
```

## Better Approaches

### ✅ Use Built-in Context
```yaml
# GOOD: Use what the system provides
if: always() && github.event_name == 'workflow_dispatch'
```

### ✅ Use Proper Architecture
```yaml
# GOOD: Use workflow_call for automated calls
jobs:
  backup:
    uses: ./.github/workflows/wpengine-api-backup.yml
    with:
      installName: ${{ inputs.installName }}
    secrets: inherit
```

### ✅ Single Responsibility
```yaml
# GOOD: One workflow, one purpose
on:
  workflow_dispatch:
    inputs:
      installName:
        type: string
        required: true
```

## Decision Framework

Before adding complexity, ask:

1. **Does the system already provide this information?**
   - Check system context variables
   - Review platform documentation
   - Look for built-in capabilities

2. **Is there a simpler architectural approach?**
   - Can we use proper APIs instead of CLI?
   - Can we restructure to avoid the complexity?
   - Is there a more direct solution?

3. **Will this make maintenance harder?**
   - More parameters = more places for bugs
   - Complex conditionals = harder to debug
   - Multiple code paths = more testing needed

4. **What's the real requirement?**
   - Step back from the immediate problem
   - What are we actually trying to achieve?
   - Is there a different way to meet the requirement?

## Remember

- **The system is smarter than you think** - leverage built-in capabilities
- **Simple is maintainable** - fewer moving parts = fewer bugs
- **Architecture matters** - use the right tool for the job
- **When in doubt, ask** - "Is there a simpler way to do this?"

The best code is the code you don't have to write.

---

# Rule: 19-systematic-code-crafting.md

---
id: systematic_code_crafting
description: "Build solutions incrementally with verification at every step, ensuring each component works before moving to the next"
---

# Systematic Code Crafting

Build solutions incrementally with verification at every step, ensuring each component works before moving to the next.

## Core Methodology

### Build Incrementally
- **One component at a time**: Implement and test each piece before moving to the next
- **Verify functionality**: Test each increment independently before integration
- **Start simple**: Begin with the most basic working version, then enhance
- **Fail fast**: Identify issues early through constant verification

### Verification at Every Step
- **Test after each change**: Run the code/script after every significant modification
- **Validate assumptions**: Use concrete tests to confirm each component works as expected
- **Check integration points**: Verify that new components work with existing ones
- **Measure progress**: Use concrete metrics to confirm functionality

## Development Workflow

### 1. Plan the Approach
- Break down the solution into discrete, testable components
- Identify the smallest working unit to build first
- Map out dependencies and integration points
- Define success criteria for each component

### 2. Implement the Foundation
- Build and test the basic structure
- Ensure the foundation works independently
- Document any assumptions or constraints discovered
- Verify core functionality before adding features

### 3. Add Features Incrementally
- **One feature at a time** with testing
- Verify each feature works before proceeding
- Test integration with existing components
- Maintain working state throughout development

### 4. Integrate Carefully
- Connect components one by one
- Test each integration point thoroughly
- Validate that new features work with existing code
- Resolve conflicts as they arise

### 5. Validate Completeness
- Ensure all requirements are met
- Test end-to-end functionality
- Verify performance and edge cases
- Document the complete solution

## Implementation Guidelines

### When Building New Features
- **Start with a minimal working prototype**
- Add complexity one layer at a time
- Test each layer before adding the next
- Use concrete examples to validate functionality

### When Refactoring Existing Code
- **Make one change at a time**
- Test after each modification
- Ensure the change doesn't break existing functionality
- Verify the refactored code works as expected

### When Integrating Systems
- **Test each system independently first**
- Create a simple integration test
- Add complexity gradually
- Validate the complete integration works

## Key Behaviors

### ✅ DO:
- Stay systematic - follow logical progression
- Build incrementally - one working piece at a time
- Verify constantly - test after every significant change
- Use concrete evidence - test results and metrics over assumptions
- Document progress - keep track of what's been implemented and tested
- Fail fast - identify issues early through constant verification

### ❌ DON'T:
- Jump between solutions without completing current work
- Add multiple features simultaneously without testing
- Skip verification steps to "save time"
- Build large components without incremental testing
- Assume integration will work without testing
- Continue building on broken foundations

## Success Indicators

- Each increment works independently
- Integration points are tested and verified
- The complete solution meets all requirements
- Performance and edge cases are validated
- Code is maintainable and well-documented
- Development process is reproducible and systematic

## Example Workflow

1. **Implement core data structure** → test independently
2. **Add basic functionality** → verify it works with core structure  
3. **Add error handling** → test error scenarios
4. **Integrate with external systems** → test integration points
5. **Add advanced features** → verify they work with existing code
6. **Optimize and finalize** → test complete solution

**Remember: Each step should result in a working system, even if incomplete. Never build on broken foundations.**

---

# Rule: 20-systematic-file-operations.md

---
id: systematic_file_operations
description: "Always follow systematic validation approach for bulk file operations, especially potentially destructive ones"
---

# Systematic File Operations with Validation

When performing bulk file operations (especially potentially destructive ones like deleting files), always follow a systematic validation approach to minimize data loss risk.

## Core principles

### Test small first
- **Always** start with a single file or small subset before bulk operations
- Validate the process works correctly on the test case
- Only proceed to bulk operations after successful validation

### Non-interactive operations
- Use appropriate flags to avoid interactive prompts in automated scripts
- Handle edge cases programmatically rather than requiring user input
- Examples: `-o` (overwrite), `-j` (junk paths), `-q` (quiet) for unzip operations

### Verification before deletion
- Never delete source files until extraction/operation is completely verified
- Check file counts, checksums, or other validation metrics
- Provide clear success/failure indicators

### Graceful error handling
- Check for common issues: disk space, permissions, file corruption
- Provide meaningful error messages
- Fail safely - prefer keeping original files over risky deletions

## Implementation pattern

    #!/bin/bash
    # Template for systematic file operations
    
    # 1. Pre-flight checks
    check_disk_space
    check_permissions
    validate_input_files
    
    # 2. Test with single file
    process_single_file_test()
    
    # 3. If test succeeds, process all files
    for file in files; do
        if process_file "$file"; then
            verify_operation "$file"
            if verification_passed; then
                cleanup_source_file "$file"
            else
                log_warning "Verification failed for $file"
            fi
        else
            log_error "Processing failed for $file"
        fi
    done
    
    # 4. Final verification and summary
    generate_operation_report

## Error recovery

- Keep detailed logs of all operations
- Provide rollback mechanisms where possible
- Never assume operations succeeded without verification

## Common use cases

- Bulk file extraction/compression
- File format conversions
- Data migrations
- Batch file processing

## Why this matters

This systematic approach ensures reliable, predictable file operations while minimizing the risk of data loss through premature deletion or incomplete processing.

---

# Rule: 21-tooling-parity.md

---
id: tooling_parity
description: "Ensure consistent behavior between command-line environment, CI/CD, and IDE"
---

# Tooling Parity Between IDE and CLI

Ensure consistent behavior between the **command-line environment**, **CI/CD**, and the **IDE** by aligning all tooling on a single source of configuration and minimal duplication.

## Core Requirements

### 🔁 Use Shared Config

- Use one **shared config file** for any tool:
  - e.g. `phpstan.neon`, `.eslintrc.json`, `.prettierrc`, `.stylelint.config.js`
- Both the CLI and IDE **must read from this file** — no overrides, no forks

### 🧩 Recommend Extensions That Respect Config

- Recommend IDE extensions (e.g., via `.vscode/extensions.json`) that:
  - Automatically use the project's config file
  - Require minimal or no additional setup
- Example: `swordev.phpstan` extension respects `phpstan.neon` directly

### ⚙️ Minimal IDE Settings

- If needed, IDE settings (e.g., in `.vscode/settings.json`) must only enable the extension:

  ```json
  {
    "phpstan.enabled": true
  }
  ```

- Avoid duplicating rules, paths, or settings in the IDE config

## What NOT to Do

- Do **not** define separate config for the same tool in `.vscode` or global settings
- Do **not** rely on manual extension-specific settings to replicate CLI behavior
- Do **not** use tools that behave inconsistently between CLI and editor

## Goal

All contributors should see the **same output and errors**, whether they:

- Run a command like `npm run lint` or `composer analyse`
- Save a file in the IDE
- Push code through CI

No drift. No duplication. One source of truth.

## Example: WordPress + PHPStan

- CLI: `phpstan analyse` reads from `phpstan.neon`
- IDE: `swordev.phpstan` reads the same file
- IDE config:

  ```json
  {
    "phpstan.enabled": true
  }
  ```

→ Both environments behave identically. No extra maintenance required.

## Troubleshooting

If results differ between CLI and IDE, check:
- Is the IDE using the same config file?
- Are there conflicting settings in `.vscode/settings.json`?
- Is the extension outdated or not respecting the shared config?

→ If the tool or extension can't respect the shared config, consider a different one.