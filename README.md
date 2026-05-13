# ControlForge

ControlForge is a local-first IT audit and GRC engineering platform for automating IAM reviews, ITGC testing, compliance evidence generation, and continuous controls monitoring.

## Why This Project Exists

Traditional IT audits often depend on spreadsheets, screenshots, manual evidence collection, and point-in-time testing.

ControlForge explores a better model:

- structured evidence instead of screenshots
- automated control testing instead of manual reconciliation
- repeatable audit logic instead of one-off spreadsheet work
- local-first execution before enterprise or cloud deployment

## Current Capabilities

- HR vs Active Directory reconciliation
- terminated user access testing
- orphaned account detection
- dormant account detection
- privileged dormant account classification
- MFA compliance validation
- structured audit findings generation
- findings export to CSV and JSON
- clean CLI audit summary output

## Sample Evidence Inputs

ControlForge currently uses simulated enterprise data:

```text
data/raw/hr_records.csv
data/raw/ad_accounts.csv
data/raw/role_assignments.csv
data/raw/sod_rules.csv
```

## Run Locally
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py


## Tech Stack

- Python
- pandas
- tabulate
- CSV/JSON evidence processing
- Local-first architecture


## Roadmap

- Segregation of Duties conflict detection
- audit summary reports
- one-click evidence package generation
- AWS IAM and cloud configuration scanning
- policy-as-code control mapping
- compliance framework mapping
- AI-assisted audit finding narratives
- dashboard interface


## Long-Term Vision

ControlForge aims to become an auditor-centric compliance engineering platform that helps IT auditors move from manual evidence collection to automated, repeatable, and defensible control testing.