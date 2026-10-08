"""
Mock banking onboarding corpus.

Each doc has the same shape so connectors can normalize easily:
  id, source, title, url, author, updated_at (ISO), tags, body

The body supports a small markdown-lite dialect that the doc renderer
understands: '## heading', '- bullet', '1. numbered', '```code fences```',
'**bold**', and pipe-tables. Anything not matching those falls through as
plain paragraph text.

Timestamps are spread over ~2 years so the recency-boost ranking has
something to show off. Some docs deliberately conflict (old vs new policy).
"""

CONFLUENCE_DOCS = [
    # -------- Onboarding / HR --------
    {
        "id": "CONF-101",
        "title": "New Joiner - Day 1 Checklist",
        "url": "https://confluence.bank.internal/display/HR/day-1-checklist",
        "author": "Priya Menon (People Ops)",
        "updated_at": "2026-08-14T09:30:00Z",
        "tags": ["onboarding", "hr", "day-1"],
        "body": (
            "## Day 1 checklist for new joiners\n"
            "Welcome to PNC Bank. Complete every step below on your first day.\n\n"
            "1. Collect your access badge from reception on floor 3.\n"
            "2. Complete the mandatory Code of Conduct e-learning on the Learning Portal.\n"
            "3. Sign the confidentiality and insider-trading acknowledgement in Workday.\n"
            "4. Meet your buddy who will walk you through the org chart.\n\n"
            "## Where to get help\n"
            "- Laptop and MFA: IT Service Desk, ext. 4111\n"
            "- HR queries: people-ops@bank.internal\n"
            "- Access blockers: your line manager, then IAM team"
        ),
    },
    {
        "id": "CONF-505",
        "title": "Engineering Onboarding - First 2 Weeks",
        "url": "https://confluence.bank.internal/display/ENG/eng-onboarding",
        "author": "Anna Kowalski (Platform Eng)",
        "updated_at": "2026-07-05T13:00:00Z",
        "tags": ["engineering", "onboarding", "developer"],
        "body": (
            "## Week 1 - environment setup\n"
            "- Install JDK 21, Node 20, Python 3.11, Docker Desktop\n"
            "- Get GitHub Enterprise account provisioned (raise CRQ in ServiceNow)\n"
            "- Clone developer-handbook repo\n"
            "- Attend architecture overview session (Tuesdays 2pm)\n\n"
            "## Week 2 - first PR\n"
            "- Pick up a 'good-first-issue' from your team backlog\n"
            "- Open your first PR by end of week 2\n"
            "- Do NOT wait silently if blocked - escalate to your manager"
        ),
    },
    {
        "id": "CONF-610",
        "title": "Cafeteria, Gym, and Wellness",
        "url": "https://confluence.bank.internal/display/HR/wellness",
        "author": "Facilities",
        "updated_at": "2025-01-15T08:00:00Z",
        "tags": ["hr", "perks", "facilities"],
        "body": (
            "Cafeteria is on floor 2, open 8am-4pm. Gym is on floor 24, badge access required. "
            "Wellness sessions every Wednesday 5pm. Subsidised meal plan available via Workday."
        ),
    },

    # -------- Entitlements / Access --------
    {
        "id": "CONF-ENT-001",
        "title": "Entitlement Provisioning - Active Directory Groups",
        "url": "https://confluence.bank.internal/display/IAM/entitlement-ad-groups",
        "author": "IAM Platform Team",
        "updated_at": "2026-08-02T09:00:00Z",
        "tags": ["iam", "entitlements", "ad", "access"],
        "body": (
            "## Overview\n"
            "All application entitlements at PNC are backed by Active Directory groups. "
            "Membership is granted via SailPoint IdentityIQ and reviewed quarterly.\n\n"
            "## Group naming convention\n"
            "```\n"
            "PNC-<APP>-<ENV>-<ROLE>\n"
            "e.g. PNC-FINBI-PROD-READER\n"
            "     PNC-FINBI-PROD-ADMIN\n"
            "     PNC-PAYMENTS-UAT-DEVELOPER\n"
            "```\n\n"
            "## Request flow\n"
            "1. User raises request in SailPoint (Access Request > Application)\n"
            "2. Line-manager approval (auto-routed)\n"
            "3. App-owner approval (for RESTRICTED apps only)\n"
            "4. Provisioning agent syncs the AD group within 30 minutes\n"
            "5. User must re-login for the token to pick up new claims\n\n"
            "## Related pages\n"
            "- Database Access Request Procedure\n"
            "- Quarterly Access Recertification\n"
            "- Snowflake Warehouse Access Setup"
        ),
    },
    {
        "id": "CONF-ENT-002",
        "title": "Database Access Request Procedure",
        "url": "https://confluence.bank.internal/display/DBA/db-access-request",
        "author": "DBA Team",
        "updated_at": "2026-06-18T09:00:00Z",
        "tags": ["dba", "entitlements", "database", "access"],
        "body": (
            "## Scope\n"
            "Covers Oracle, SQL Server, Postgres and Snowflake. Direct prod-DB access is "
            "restricted to break-fix scenarios only. All access is time-boxed.\n\n"
            "## Approval matrix\n"
            "| Environment | Approver | Max duration |\n"
            "|---|---|---|\n"
            "| DEV / SIT | App team lead | Standing |\n"
            "| UAT | App team lead + DBA | 30 days |\n"
            "| PROD (read) | App owner + Data Steward | 7 days |\n"
            "| PROD (write) | App owner + Data Steward + Head of Ops | 4 hours (break-fix) |\n\n"
            "## Request steps\n"
            "1. Raise ServiceNow ticket, category 'Database > Access Request'\n"
            "2. Attach a business justification and query samples\n"
            "3. DBA provisions a named account, NEVER a shared/service account\n"
            "4. All prod queries are logged to the audit lake\n\n"
            "## Rejection reasons\n"
            "- Missing business justification\n"
            "- Request for 'select *' on PII tables (must be column-scoped)\n"
            "- Shared account requested"
        ),
    },
    {
        "id": "CONF-ENT-003",
        "title": "Quarterly Access Recertification",
        "url": "https://confluence.bank.internal/display/IAM/access-recert-quarterly",
        "author": "IAM Governance",
        "updated_at": "2026-07-30T09:00:00Z",
        "tags": ["iam", "audit", "recertification", "compliance"],
        "body": (
            "## What\n"
            "Every quarter, managers must review and recertify every entitlement held by their team. "
            "Any entitlement not reviewed within 14 days is auto-revoked.\n\n"
            "## Timeline\n"
            "- Q1: Feb 1 - Feb 14\n"
            "- Q2: May 1 - May 14\n"
            "- Q3: Aug 1 - Aug 14\n"
            "- Q4: Nov 1 - Nov 14\n\n"
            "## How\n"
            "Managers receive an email from SailPoint with a personalised recert URL. "
            "For each entitlement they must choose: **Keep**, **Revoke**, or **Delegate**.\n\n"
            "## Escalation\n"
            "Missed recert = auto-revoke + audit finding. Repeated misses trigger a CAO escalation."
        ),
    },
    {
        "id": "CONF-ENT-004",
        "title": "Entitlement List - Onboarding Access Request Template",
        "url": "https://confluence.bank.internal/display/IAM/entitlement-details-template",
        "author": "IAM Platform Team",
        "updated_at": "2026-09-18T09:00:00Z",
        "tags": [
            "iam", "entitlements", "entitlement-list", "access", "onboarding",
            "template", "list", "roster", "register",
            "excel", "xlsx", "spreadsheet", "download", "form", "checklist",
        ],
        "body": (
            "The Entitlement List is the canonical access-request template every new joiner "
            "at the bank must fill in on Day 1 to enumerate the applications, environments, "
            "and roles they need. "
            "Download the attached Excel workbook, complete one row per entitlement, get your "
            "line-manager to sign off in the Approver column, and attach the completed list to "
            "your SailPoint access request. "
            "The template covers every paved-path application (ABC, SSM, EPM, Snowflake, GitHub, "
            "Confluence, SharePoint) and enforces the naming convention "
            "`PNC-<APP>-<ENV>-<ROLE>` for every entitlement row. "
            "Managers can reuse the same workbook for quarterly recertification and for bulk "
            "onboarding a whole squad in one go.\n\n"
            "### What the workbook contains\n"
            "| Column | Purpose | Example |\n"
            "|---|---|---|\n"
            "| Application | Target app / system | Snowflake |\n"
            "| Environment | DEV / SIT / UAT / PROD | PROD |\n"
            "| Role | Requested AD role | READER |\n"
            "| Justification | 1-line business reason | Q4 finance reporting |\n"
            "| Approver | Line-manager (name + date) | Anil Sharma, 2026-09-18 |\n"
            "| Ticket | SailPoint request ID (filled after submit) | SP-482910 |\n\n"
            "### Who uses this\n"
            "- New joiners on Day 1 to request all initial entitlements in one shot.\n"
            "- Managers running the quarterly recertification cycle (audit-ready list).\n"
            "- Team leads onboarding a whole squad in a single bulk request.\n\n"
            "### How to use\n"
            "1. Download the Excel template: "
            "[Entitlement_Details_Template.xlsx](/static/attachments/Entitlement_Details_Template.xlsx)\n"
            "2. Fill in one row per entitlement (application, environment, role, justification).\n"
            "3. Get line-manager sign-off in the Approver column.\n"
            "4. Attach the completed workbook to your SailPoint access request.\n"
            "5. Provisioning is auto-routed and typically completes within 30 minutes.\n\n"
            "### Confluence location\n"
            "The canonical copy of this entitlement list lives at "
            "confluence.bank.internal/display/IAM/entitlement-details-template - always download "
            "from Confluence, never from a colleague's copy, so you have the latest columns.\n\n"
            "### Attachment\n"
            "[Entitlement_Details_Template.xlsx](/static/attachments/Entitlement_Details_Template.xlsx)\n\n"
            "### Related\n"
            "- Entitlement Provisioning - Active Directory Groups\n"
            "- Database Access Request Procedure\n"
            "- Quarterly Access Recertification"
        ),
    },

    # -------- Compliance / KYC --------
    {
        "id": "CONF-102",
        "title": "KYC Review Process - Corporate Clients (v4)",
        "url": "https://confluence.bank.internal/display/COMP/kyc-corporate-v4",
        "author": "Rahul Verma (Compliance)",
        "updated_at": "2026-07-22T14:10:00Z",
        "tags": ["compliance", "kyc", "corporate", "aml"],
        "body": (
            "## Stages\n"
            "The corporate KYC review is a 4-stage process.\n\n"
            "1. **Client Identification** - collect certificate of incorporation, "
            "beneficial ownership registry (UBO >=25%), and board resolution.\n"
            "2. **Risk Rating** - run the client through the AML risk model in RiskHub.\n"
            "3. **Enhanced Due Diligence (EDD)** for high-risk clients - PEP screening, "
            "adverse media check, source-of-wealth documentation.\n"
            "4. **Approval** - L1 for low risk, MLRO for high risk.\n\n"
            "## SLAs\n"
            "- Standard: 5 business days\n"
            "- EDD: 10 business days\n\n"
            "Use the KYC-Corporate template in RiskHub. Do NOT reuse legacy v2 checklist."
        ),
    },
    {
        "id": "CONF-055",
        "title": "KYC Review Process - Corporate Clients (v2) [DEPRECATED]",
        "url": "https://confluence.bank.internal/display/COMP/kyc-corporate-v2",
        "author": "Sarah Klein (Compliance, former)",
        "updated_at": "2024-11-03T10:00:00Z",
        "tags": ["compliance", "kyc", "corporate", "deprecated"],
        "body": (
            "**DEPRECATED - see v4.**\n\n"
            "Legacy 3-stage KYC process from 2024: identification, risk rating, approval. "
            "This version does NOT include the mandatory EDD stage or UBO >=25% threshold "
            "introduced in 2025. Do not follow."
        ),
    },
    {
        "id": "CONF-820",
        "title": "Data Classification & Handling",
        "url": "https://confluence.bank.internal/display/RISK/data-classification",
        "author": "Chief Data Office",
        "updated_at": "2026-03-02T09:15:00Z",
        "tags": ["data", "classification", "risk", "pii"],
        "body": (
            "## The 4 tiers\n"
            "| Tier | Example | Storage rules |\n"
            "|---|---|---|\n"
            "| Public | Marketing collateral | No restriction |\n"
            "| Internal | Org chart, run books | Bank systems only |\n"
            "| Confidential | Financial reports pre-publish | Access-controlled, audit-logged |\n"
            "| Restricted | PII, PAN, national ID | KMS-encrypted, TLS 1.3, DLP tags |\n\n"
            "## Rules for Restricted data\n"
            "- Never copy to personal drives, personal email, or unmanaged AI tools\n"
            "- Use the enterprise AI copilot for AI-assisted work\n"
            "- Access requires a Data Steward approval, tracked in SailPoint"
        ),
    },

    # -------- Deployment / Migration (this is the type in the screenshot) --------
    {
        "id": "CONF-DEP-105",
        "title": "Deployment Procedure (v10.5) - Detailed Version",
        "url": "https://confluence.bank.internal/display/CM/deployment-procedure-v10-5",
        "author": "Hans Burger (Change Management)",
        "updated_at": "2026-08-12T10:00:00Z",
        "tags": ["deployment", "change-mgmt", "release", "procedure", "informatica"],
        "body": (
            "## R. Deployment Procedure (v10.5) - Detailed Version\n\n"
            "This page describes the end-to-end deployment procedure for Informatica "
            "PowerCenter v10.5 releases from DEV -> SIT -> UAT -> PROD.\n\n"
            "### iii. Creating a component list will identify the objects for migration\n\n"
            "To create a component list, create a dummy query in test environment and execute "
            "the query created a list of all the objects that were labeled for migration.\n\n"
            "1. Open PowerCenter Repository Manager.\n"
            "2. Logon to the source repository where the new query will be created, then navigate "
            "to the Tool menu option and select 'Queries'.\n"
            "3. After selecting 'Queries', the Query Browser window will appear.\n"
            "4. Select 'New' to create a new query.\n"
            "5. In the query, set the parameter type to 'Label' and select the migration label.\n"
            "6. Save the query with a name like `<APP>_<REL>_MIGRATION_LIST`.\n"
            "7. Execute and export the result as a CSV.\n\n"
            "### iv. Deployment Groups\n"
            "- Create a dynamic Deployment Group with the query above\n"
            "- Compare source vs target repository - resolve conflicts before proceeding\n"
            "- Copy Deployment Group into target with rollback plan attached\n\n"
            "### v. Rollback\n"
            "Every deployment must have a signed-off rollback query. Roll back by re-importing "
            "the pre-deployment backup .xml, then running the labelled revert deployment group.\n\n"
            "## Related pages\n"
            "- Component List Creation for Migration\n"
            "- PowerCenter Repository Manager Setup\n"
            "- Informatica ETL Migration Runbook"
        ),
    },
    {
        "id": "CONF-DEP-106",
        "title": "Component List Creation for Migration",
        "url": "https://confluence.bank.internal/display/CM/component-list-migration",
        "author": "ETL Migration Team",
        "updated_at": "2026-08-05T11:00:00Z",
        "tags": ["migration", "informatica", "etl", "component-list"],
        "body": (
            "## Purpose\n"
            "A component list is a manifest of all Informatica objects (mappings, workflows, "
            "sessions, connections, parameter files) participating in a release.\n\n"
            "## Required columns\n"
            "| Column | Example |\n"
            "|---|---|\n"
            "| Object Type | Mapping |\n"
            "| Object Name | m_LOAD_CUSTOMER_DIM |\n"
            "| Folder | FIN_BI_DELIVERY |\n"
            "| Repository | REP1_TEST |\n"
            "| Label | REL_2026_09 |\n"
            "| Version | 42 |\n\n"
            "## How to generate\n"
            "1. Label the objects in the source repo using the RM label tool\n"
            "2. Follow the Deployment Procedure (v10.5) query steps\n"
            "3. Export the CSV and attach to the CRQ ticket\n"
            "4. Peer review by another Informatica developer"
        ),
    },
    {
        "id": "CONF-DEP-107",
        "title": "PowerCenter Repository Manager Setup",
        "url": "https://confluence.bank.internal/display/CM/rm-setup",
        "author": "ETL Migration Team",
        "updated_at": "2026-05-20T09:00:00Z",
        "tags": ["informatica", "repository-manager", "setup"],
        "body": (
            "## Client install\n"
            "Download the PowerCenter 10.5 client from Software Center. Install as Administrator. "
            "During install, register the following domains:\n"
            "- REP1_DEV\n"
            "- REP1_SIT\n"
            "- REP1_UAT\n"
            "- REP1_PROD (read-only for most users)\n\n"
            "## First login\n"
            "Use your PNC AD credentials. Access must be requested through SailPoint under "
            "the AD group `PNC-INFA-<ENV>-DEVELOPER` or `PNC-INFA-<ENV>-DEPLOYER`.\n\n"
            "## Common issues\n"
            "- **Cannot connect to repository**: check corp VPN and firewall rules to port 6005\n"
            "- **Locked out**: 5 failed attempts = 30-minute lockout, resets automatically"
        ),
    },
    {
        "id": "CONF-DEP-108",
        "title": "Informatica ETL Migration Runbook",
        "url": "https://confluence.bank.internal/display/CM/etl-migration-runbook",
        "author": "ETL Migration Team",
        "updated_at": "2026-08-30T10:00:00Z",
        "tags": ["migration", "informatica", "etl", "runbook"],
        "body": (
            "## Pre-migration checklist\n"
            "- [ ] CRQ raised and approved (T-3 days)\n"
            "- [ ] Component list peer-reviewed\n"
            "- [ ] Rollback deployment group prepared\n"
            "- [ ] Downstream teams notified (Finance BI, Reg Reporting)\n"
            "- [ ] Autosys job holds requested for the migration window\n\n"
            "## Migration window\n"
            "```\n"
            "T-30m   Freeze source repo\n"
            "T-15m   Take repo backup\n"
            "T0      Execute deployment group\n"
            "T+30m   Smoke tests\n"
            "T+45m   Release Autosys holds\n"
            "T+60m   Post-deployment validation with downstream teams\n"
            "```\n\n"
            "## Smoke tests\n"
            "Run the `smoke_test_workflow` in the target repo. All 12 mappings must complete "
            "with row-count deltas <= 1% vs the last DEV run."
        ),
    },

    # -------- Change Management --------
    {
        "id": "CONF-CRQ-001",
        "title": "Change Request Workflow - CRQ Process",
        "url": "https://confluence.bank.internal/display/CM/crq-workflow",
        "author": "Change Advisory Board",
        "updated_at": "2026-08-01T09:00:00Z",
        "tags": ["change-mgmt", "crq", "cab", "workflow"],
        "body": (
            "## CRQ lifecycle\n"
            "```\n"
            " Draft --> Peer Review --> Manager Approval --> CAB --> Scheduled --> Implemented --> Closed\n"
            "                              |                                       |\n"
            "                              v                                       v\n"
            "                          Rejected                                 Rolled Back\n"
            "```\n\n"
            "## Change types\n"
            "| Type | CAB required | Lead time |\n"
            "|---|---|---|\n"
            "| Standard (pre-approved) | No | 1 day |\n"
            "| Normal | Yes | 5 business days |\n"
            "| Emergency | Post-implementation CAB | 4 hours |\n\n"
            "## When to raise a CRQ\n"
            "- Any prod deployment\n"
            "- Any config change on a Tier-1 application\n"
            "- Firewall rule changes\n"
            "- Autosys schedule changes\n"
            "- Certificate rotations\n\n"
            "## Templates\n"
            "See attachments: `CRQ_TEMPLATE_STANDARD.docx`, `CRQ_TEMPLATE_EMERGENCY.docx`."
        ),
    },
    {
        "id": "CONF-CRQ-002",
        "title": "IT Change Advisory Board (CAB) - Meeting Minutes Template",
        "url": "https://confluence.bank.internal/display/CM/cab-minutes-template",
        "author": "Change Advisory Board",
        "updated_at": "2026-07-11T09:00:00Z",
        "tags": ["cab", "change-mgmt", "template"],
        "body": (
            "## CAB meeting cadence\n"
            "Every Wednesday 3pm SGT. Standing attendees: Head of Ops, App Owners, InfoSec, "
            "DBA, Network, Compliance rep.\n\n"
            "## Agenda template\n"
            "1. Review of previous week's changes (success/rollback/incident linkage)\n"
            "2. This week's normal changes (walk-through, approvals)\n"
            "3. Next week's forward schedule\n"
            "4. Emergency changes retrospective\n"
            "5. AOB\n\n"
            "## Attendance quorum\n"
            "CAB is quorate with at least: 1 Ops, 1 InfoSec, 1 App Owner for each change reviewed."
        ),
    },
    {
        "id": "CONF-CRQ-003",
        "title": "Production Deployment Change Freeze Calendar 2026",
        "url": "https://confluence.bank.internal/display/CM/freeze-calendar-2026",
        "author": "Change Advisory Board",
        "updated_at": "2026-06-15T09:00:00Z",
        "tags": ["change-mgmt", "freeze", "calendar"],
        "body": (
            "## Blackout windows\n"
            "No non-emergency prod changes may be deployed during:\n"
            "- Quarter-end +/- 3 business days (Mar, Jun, Sep, Dec)\n"
            "- Year-end freeze: Dec 15 - Jan 5\n"
            "- Regulatory reporting week (last week of month for MAS/RBI submissions)\n"
            "- Payroll run windows (26th - month-end)\n\n"
            "## Exceptions\n"
            "Emergency fixes for SEV1/SEV2 incidents are always allowed but must be "
            "retrospectively approved at the next CAB."
        ),
    },

    # -------- Incident Management --------
    {
        "id": "CONF-201",
        "title": "Incident Response Runbook - Production Outage",
        "url": "https://confluence.bank.internal/display/SRE/prod-incident-runbook",
        "author": "Dan Osei (SRE Lead)",
        "updated_at": "2026-08-28T16:45:00Z",
        "tags": ["sre", "incident", "runbook", "on-call"],
        "body": (
            "## When to declare\n"
            "Declare an incident if a customer-facing service is degraded or down.\n\n"
            "## The first 15 minutes\n"
            "1. Declare in PagerDuty with severity SEV1 or SEV2\n"
            "2. Join `#incident-bridge` on Slack, start a Zoom bridge\n"
            "3. On-call SRE is Incident Commander (IC) by default until relieved\n"
            "4. Post status update to statuspage every 15 minutes\n"
            "5. Notify Compliance within 30 minutes for MAS/RBI reportable incidents\n\n"
            "## Roles\n"
            "| Role | Responsibility |\n"
            "|---|---|\n"
            "| IC | Overall coordination, decisions |\n"
            "| Scribe | Timeline, actions, decisions |\n"
            "| Comms | Internal + external status updates |\n"
            "| SME | Technical investigation |\n\n"
            "## Post-mortem\n"
            "Publish to Confluence within 5 business days. Blameless format. See RCA templates."
        ),
    },
    {
        "id": "CONF-INC-002",
        "title": "RCA - Payment Gateway Outage 03-Sep-2026",
        "url": "https://confluence.bank.internal/display/SRE/rca-payment-gateway-2026-09-03",
        "author": "Dan Osei (SRE Lead)",
        "updated_at": "2026-09-06T09:00:00Z",
        "tags": ["rca", "incident", "payments", "post-mortem"],
        "body": (
            "## Summary\n"
            "On 2026-09-03 between 10:12 - 11:47 SGT, the payments-service was unavailable for "
            "SEPA and FPS flows. Retail app users saw 'Payment pending' errors. RTGS unaffected.\n\n"
            "## Impact\n"
            "- ~14,200 payments delayed (later processed successfully)\n"
            "- 1 hour 35 minutes total downtime\n"
            "- No financial loss; regulatory notification made to MAS at 10:38\n\n"
            "## Root cause\n"
            "A Kafka consumer group rebalance was triggered by a rolling restart of the "
            "sanctions-screening service. The payments-service had a bug where a stuck "
            "coordinator would not re-join for 90 minutes.\n\n"
            "## Timeline\n"
            "```\n"
            "10:12  First alert: payments p99 > 5s (Argus)\n"
            "10:15  On-call paged, joins #incident-bridge\n"
            "10:22  Sanctions restart correlated as trigger\n"
            "10:38  MAS notification sent (T+26m)\n"
            "10:55  Rollback sanctions restart - no effect\n"
            "11:31  Payments consumer group force-reset\n"
            "11:47  Full recovery\n"
            "```\n\n"
            "## Action items\n"
            "| # | Action | Owner | Due |\n"
            "|---|---|---|---|\n"
            "| 1 | Upgrade payments-service to Kafka client 3.7 | pod-alpha | 2026-09-20 |\n"
            "| 2 | Add coordinator-stuck alert | SRE | 2026-09-15 |\n"
            "| 3 | Add sanctions-restart canary check | pod-gamma | 2026-09-30 |"
        ),
    },
    {
        "id": "CONF-INC-003",
        "title": "RCA - Reconciliation Job Failure 22-Aug-2026",
        "url": "https://confluence.bank.internal/display/SRE/rca-recon-2026-08-22",
        "author": "pod-delta",
        "updated_at": "2026-08-26T09:00:00Z",
        "tags": ["rca", "reconciliation", "batch", "post-mortem"],
        "body": (
            "## Summary\n"
            "Nightly recon job `RECON_EOD_MAIN` failed at 22:14 SGT on 2026-08-22 due to a "
            "schema change in the upstream Nostro feed that was not communicated.\n\n"
            "## Root cause\n"
            "Upstream vendor added a new column `settlement_currency_iso3` between "
            "`settlement_ccy` and `amount`. The Informatica mapping used positional parsing "
            "instead of named columns.\n\n"
            "## Fix\n"
            "- Immediate: hand-patched the source parser, reran RECON_EOD_MAIN at 03:40\n"
            "- Long-term: switched all Nostro parsers to named-column mode (see PR #4218)\n\n"
            "## Action items\n"
            "- Contract with vendor to require 30-day advance notice on schema changes\n"
            "- Add schema-diff canary job that runs at T-1hr before RECON_EOD_MAIN"
        ),
    },
    {
        "id": "CONF-INC-004",
        "title": "Production Support Escalation Matrix",
        "url": "https://confluence.bank.internal/display/SRE/escalation-matrix",
        "author": "Operations Command Center",
        "updated_at": "2026-07-25T09:00:00Z",
        "tags": ["incident", "escalation", "on-call"],
        "body": (
            "## Escalation levels\n"
            "| Level | Who | When to engage |\n"
            "|---|---|---|\n"
            "| L1 | Operations Command Center | 24x7 monitoring |\n"
            "| L2 | App on-call (pod) | Within 5 min for SEV1/2 |\n"
            "| L3 | App SME + Lead | 15 min if unresolved |\n"
            "| L4 | Head of App Eng | 30 min |\n"
            "| L5 | CIO on-call | 60 min or MAS-reportable |\n\n"
            "## Pager numbers\n"
            "OCC: ext. 9999 / bridge 852-9999-1000\n"
            "InfoSec on-call: infosec-oncall@bank.internal (also pageable)\n"
            "Compliance duty officer: compliance-duty@bank.internal"
        ),
    },

    # -------- Architecture / ETL / Data --------
    {
        "id": "CONF-ARCH-001",
        "title": "Finance BI - End to End Architecture",
        "url": "https://confluence.bank.internal/display/FINBI/architecture-e2e",
        "author": "Finance BI Architecture",
        "updated_at": "2026-08-19T09:00:00Z",
        "tags": ["architecture", "finance-bi", "etl", "data"],
        "body": (
            "## High-level flow\n"
            "```\n"
            "  +-----------+    +-----------+    +----------+    +---------+    +---------+\n"
            "  | Source    |--->| Landing   |--->| Staging  |--->| Curated |--->| Tableau |\n"
            "  | Systems   |    | (S3/HDFS) |    | (Snow)   |    | (Snow)  |    |         |\n"
            "  +-----------+    +-----------+    +----------+    +---------+    +---------+\n"
            "        |               |                |                |             |\n"
            "        |               v                v                v             v\n"
            "        |          Informatica       DBT tests        Data-Vault    Row-level\n"
            "        |          PowerCenter       + Great          modeling      security\n"
            "        |          ingest jobs       Expectations     (raw/biz/mart)\n"
            "        v\n"
            "  Autosys jobs schedule all steps; Airflow orchestrates ML feature builds.\n"
            "```\n\n"
            "## Tech stack\n"
            "- Ingest: Informatica PowerCenter 10.5, Kafka Connect for CDC\n"
            "- Storage: S3 landing, Snowflake staging + curated + mart\n"
            "- Transform: DBT, Spark on EMR for heavy jobs\n"
            "- Orchestration: Autosys (batch), Airflow (feature builds)\n"
            "- Consumption: Tableau Server, Snowflake connector, entitlement via row-access policies\n\n"
            "## Related pages\n"
            "- Data Lineage - Finance BI\n"
            "- Snowflake Warehouse Access Setup\n"
            "- Batch Job Scheduling with Autosys"
        ),
    },
    {
        "id": "CONF-ARCH-002",
        "title": "Data Lineage - Finance BI",
        "url": "https://confluence.bank.internal/display/FINBI/data-lineage",
        "author": "Finance BI Architecture",
        "updated_at": "2026-07-10T09:00:00Z",
        "tags": ["lineage", "finance-bi", "data"],
        "body": (
            "## Core lineage - GL to Tableau\n"
            "```\n"
            "  Oracle GL --(CDC)--> Kafka gl.txn --> S3 landing/gl/YYYY-MM-DD/\n"
            "     --(Informatica m_LOAD_GL_STG)--> SNOW.STG_GL_TXN\n"
            "     --(dbt model curated.fct_gl_txn)--> SNOW.CURATED.FCT_GL_TXN\n"
            "     --(dbt model mart.finance.gl_daily_pnl)--> SNOW.MART_FIN.GL_DAILY_PNL\n"
            "     --(Tableau extract)--> workbook: Finance PnL Daily\n"
            "```\n\n"
            "## Sensitive columns\n"
            "| Column | Source | Classification |\n"
            "|---|---|---|\n"
            "| customer_name | CIF | Restricted |\n"
            "| account_no | GL | Restricted |\n"
            "| trader_id | GL | Confidential |\n"
            "| amount_local | GL | Confidential |\n\n"
            "## Ownership\n"
            "Data Steward: Finance CDO. Change to model requires steward sign-off in the CRQ."
        ),
    },
    {
        "id": "CONF-ARCH-003",
        "title": "Batch Job Scheduling with Autosys",
        "url": "https://confluence.bank.internal/display/CM/autosys-scheduling",
        "author": "Autosys Admins",
        "updated_at": "2026-06-30T09:00:00Z",
        "tags": ["autosys", "batch", "scheduling"],
        "body": (
            "## Job types we use\n"
            "- **CMD** - executes a shell command on the agent host\n"
            "- **BOX** - container for a sequence of jobs, boxes can nest\n"
            "- **FW** - file-watcher, triggers when a sentinel file lands\n\n"
            "## JIL template - CMD\n"
            "```\n"
            "insert_job: PNC_FINBI_LOAD_GL_DAILY\n"
            "job_type: CMD\n"
            "command: /apps/finbi/bin/run_load_gl.sh\n"
            "machine: finbi-agent-p01\n"
            "owner: svc_finbi_prod\n"
            "date_conditions: 1\n"
            "days_of_week: mo,tu,we,th,fr\n"
            "start_times: '22:00'\n"
            "condition: s(PNC_FINBI_CDC_GL_LATEST) and s(PNC_FINBI_LOAD_CIF_DAILY)\n"
            "alarm_if_fail: 1\n"
            "n_retrys: 2\n"
            "```\n\n"
            "## Deployment\n"
            "JIL changes deployed via `jil -f <file>` from the deployment agent. All changes "
            "require a CRQ and go through the same CAB as code changes."
        ),
    },
    {
        "id": "CONF-ARCH-004",
        "title": "ETL Job Rerun Procedure",
        "url": "https://confluence.bank.internal/display/CM/etl-rerun-procedure",
        "author": "ETL Support",
        "updated_at": "2026-07-16T09:00:00Z",
        "tags": ["etl", "rerun", "informatica", "runbook"],
        "body": (
            "## Standard rerun\n"
            "1. Confirm root cause (source file, schema mismatch, etc.) and fix upstream\n"
            "2. In Autosys: `sendevent -E FORCE_STARTJOB -J <job_name>`\n"
            "3. Monitor the workflow in PowerCenter Monitor\n"
            "4. On completion, notify downstream (Tableau team, Reg Reporting team)\n\n"
            "## Partial rerun (from a specific session)\n"
            "1. In Workflow Monitor, right-click the failed session\n"
            "2. Choose 'Restart Workflow from Task'\n"
            "3. Confirm the parameter file is refreshed for the correct business date\n\n"
            "## When NOT to rerun\n"
            "- Financial-reporting jobs after regulatory cut-off (need Finance CDO sign-off)\n"
            "- Any job that produced a downstream file already consumed by trading systems"
        ),
    },
    {
        "id": "CONF-ARCH-005",
        "title": "Cross-Region Data Replication Architecture",
        "url": "https://confluence.bank.internal/display/ARCH/cross-region-replication",
        "author": "Cloud Platform / Data",
        "updated_at": "2026-05-22T09:00:00Z",
        "tags": ["dr", "replication", "architecture", "resilience"],
        "body": (
            "## Regions\n"
            "- Primary: ap-southeast-1 (Singapore)\n"
            "- DR: ap-northeast-1 (Tokyo)\n\n"
            "## Replication strategy\n"
            "```\n"
            "  Snowflake (SG)  ==(account replication)==>  Snowflake (JP)\n"
            "  S3 (SG)         ==(CRR, 15-min RPO)========>  S3 (JP)\n"
            "  Aurora Postgres ==(cross-region read replica)==>  Aurora JP\n"
            "  Kafka MSK       ==(MirrorMaker 2, active-passive)==>  Kafka JP\n"
            "```\n\n"
            "## RPO / RTO\n"
            "| Data | RPO | RTO |\n"
            "|---|---|---|\n"
            "| Payments (transactional) | 0 (sync) | 15 min |\n"
            "| Finance BI (batch) | 4 hours | 4 hours |\n"
            "| ML feature store | 1 hour | 2 hours |\n\n"
            "## Failover drills\n"
            "Executed twice a year. See BCP page for tabletop schedule."
        ),
    },
    {
        "id": "CONF-ARCH-006",
        "title": "Snowflake Warehouse Access Setup",
        "url": "https://confluence.bank.internal/display/DATA/snowflake-access",
        "author": "Snowflake Platform Team",
        "updated_at": "2026-08-04T09:00:00Z",
        "tags": ["snowflake", "access", "data"],
        "body": (
            "## Warehouse layout\n"
            "| Warehouse | Size | Purpose |\n"
            "|---|---|---|\n"
            "| WH_ETL_S | Small | Nightly loads |\n"
            "| WH_ETL_L | Large | Heavy transforms |\n"
            "| WH_BI_XS | XSmall | Interactive Tableau |\n"
            "| WH_ADHOC_S | Small | Ad-hoc SQL |\n\n"
            "## Roles\n"
            "- `ROLE_FINBI_READER` -> read-only on MART_FIN\n"
            "- `ROLE_FINBI_ANALYST` -> read/write on STG_ANALYTICS\n"
            "- `ROLE_FINBI_ENGINEER` -> full access except PROD\n\n"
            "## Request access\n"
            "Via SailPoint (see Entitlement Provisioning). Row-access policies enforce "
            "PII masking based on Data Steward tagging."
        ),
    },
    {
        "id": "CONF-ARCH-007",
        "title": "Tableau Publishing Workflow",
        "url": "https://confluence.bank.internal/display/BI/tableau-publishing",
        "author": "BI Platform Team",
        "updated_at": "2026-04-28T09:00:00Z",
        "tags": ["tableau", "bi", "publishing"],
        "body": (
            "## From dev to prod\n"
            "```\n"
            "  Author (Desktop) -> Publish to DEV site -> Peer review\n"
            "     -> Publish to UAT -> UAT sign-off by business\n"
            "     -> Package .tdsx -> CRQ -> Publish to PROD via API\n"
            "```\n\n"
            "## Naming convention\n"
            "`<Team>_<Domain>_<Subject>_<Cadence>` e.g. `FINBI_PnL_Daily`\n\n"
            "## Rules\n"
            "- No live connections to prod databases from Desktop - use extracts\n"
            "- Extracts refresh via server schedules only (no client-side scheduling)\n"
            "- Workbooks with Restricted data require row-level security applied at datasource"
        ),
    },
    {
        "id": "CONF-ARCH-008",
        "title": "Airflow DAG Deployment Guide",
        "url": "https://confluence.bank.internal/display/DATA/airflow-dag-deploy",
        "author": "Data Platform Team",
        "updated_at": "2026-07-02T09:00:00Z",
        "tags": ["airflow", "orchestration", "deployment"],
        "body": (
            "## Repo layout\n"
            "All DAGs live in `github.bank.internal/data-platform/airflow-dags`. Structure:\n"
            "```\n"
            "airflow-dags/\n"
            "  dags/\n"
            "    finbi/\n"
            "      load_gl_daily.py\n"
            "      feature_build_fraud.py\n"
            "    payments/\n"
            "  plugins/\n"
            "  tests/\n"
            "```\n\n"
            "## CI/CD\n"
            "- On PR: lint, unit-test, DAG-parse test\n"
            "- On merge to main: sync to Airflow DEV within 5 min\n"
            "- Promote to PROD via CRQ + tag push `prod-YYYYMMDD-N`\n\n"
            "## Standards\n"
            "- Every DAG must have owner, sla, retries, on_failure_callback\n"
            "- No credentials in code - use Airflow Connections backed by Vault"
        ),
    },
    {
        "id": "CONF-ARCH-009",
        "title": "LDAP Group Membership Management",
        "url": "https://confluence.bank.internal/display/IAM/ldap-group-mgmt",
        "author": "IAM Platform Team",
        "updated_at": "2026-06-05T09:00:00Z",
        "tags": ["ldap", "iam", "groups"],
        "body": (
            "## Overview\n"
            "LDAP groups are the transport for entitlements between AD and downstream apps "
            "that don't support SAML/OIDC directly. LDAP tree structure:\n"
            "```\n"
            "  ou=groups,dc=bank,dc=internal\n"
            "    +-- cn=PNC-FINBI-PROD-READER\n"
            "    +-- cn=PNC-FINBI-PROD-ADMIN\n"
            "    +-- cn=PNC-INFA-PROD-DEPLOYER\n"
            "    +-- ... (~14000 groups)\n"
            "```\n\n"
            "## Sync\n"
            "AD -> LDAP replication every 5 minutes via `ldap-sync-service` (see GitHub repo).\n\n"
            "## Reading groups from an app\n"
            "Bind DN: `cn=svc_<appname>,ou=services,dc=bank,dc=internal`\n"
            "Search base: `ou=groups,dc=bank,dc=internal`\n"
            "Filter: `(&(objectClass=groupOfNames)(cn=PNC-<APP>-*))`"
        ),
    },

    # -------- Ownership / Services --------
    {
        "id": "CONF-411",
        "title": "Payments Team - Service Ownership Map",
        "url": "https://confluence.bank.internal/display/PAY/service-ownership",
        "author": "Mei Tanaka (Payments Eng Mgr)",
        "updated_at": "2026-06-30T11:20:00Z",
        "tags": ["payments", "ownership", "services"],
        "body": (
            "## Pods and services\n"
            "| Pod | Service | Language | On-call |\n"
            "|---|---|---|---|\n"
            "| Alpha | payments-service | Java 21 / Spring | payments-p1 |\n"
            "| Beta | fx-service | Go 1.22 | fx-p1 |\n"
            "| Gamma | sanctions-screening | Rust | sanctions-p1 |\n"
            "| Delta | reconciliation-service | Kotlin / Spring Batch | recon-p1 |\n\n"
            "See the GitHub repos under `github.bank.internal/payments-platform`."
        ),
    },
    {
        "id": "CONF-310",
        "title": "Trading Floor VPN Access",
        "url": "https://confluence.bank.internal/display/IT/trading-floor-vpn",
        "author": "IT Security",
        "updated_at": "2026-05-11T08:00:00Z",
        "tags": ["vpn", "trading", "access", "security"],
        "body": (
            "## Trading floor VPN\n"
            "The tf-vpn.bank.internal profile is separate from the corp VPN.\n\n"
            "## Steps to request access\n"
            "1. Manager files access request in ServiceNow - category 'Trading Floor Access'\n"
            "2. Compliance sign-off (required for anyone touching order-management systems)\n"
            "3. IT Security provisions the profile in Cisco AnyConnect, typically same-day\n\n"
            "## Rules\n"
            "- Must use a bank-issued laptop\n"
            "- Must be physically in a whitelisted office\n"
            "- Personal devices are never permitted on tf-vpn"
        ),
    },
    {
        "id": "CONF-712",
        "title": "Code Review Guidelines",
        "url": "https://confluence.bank.internal/display/ENG/code-review-guidelines",
        "author": "Anna Kowalski (Platform Eng)",
        "updated_at": "2026-04-18T10:30:00Z",
        "tags": ["engineering", "code-review", "quality"],
        "body": (
            "## Rules\n"
            "- Every PR requires at least one approving review from a CODEOWNER\n"
            "- PRs touching production-critical paths (payments, sanctions, ledger) require "
            "two approvers and a Compliance sign-off label\n"
            "- Use conventional-commits format\n"
            "- Keep PRs under 400 lines of diff where possible\n\n"
            "## Change freeze\n"
            "Never merge on Friday after 3pm local - the change freeze policy is enforced by CI."
        ),
    },
]

GITHUB_DOCS = [
    # -------- Payments platform --------
    {
        "id": "GH-payments-service-README",
        "title": "payments-service - README",
        "url": "https://github.bank.internal/payments-platform/payments-service",
        "author": "pod-alpha",
        "updated_at": "2026-08-30T18:00:00Z",
        "tags": ["repo", "payments", "readme", "service"],
        "body": (
            "# payments-service\n\n"
            "SEPA / FPS / RTGS orchestration service written in Java 21 / Spring Boot.\n\n"
            "## Run locally\n"
            "```\n"
            "./gradlew bootRun\n"
            "# requires Docker to bring up postgres + kafka:\n"
            "docker compose up -d\n"
            "```\n\n"
            "## Environment variables\n"
            "| Var | Purpose |\n"
            "|---|---|\n"
            "| PAYMENTS_DB_URL | Aurora Postgres endpoint |\n"
            "| KAFKA_BOOTSTRAP | MSK bootstrap URL |\n"
            "| SANCTIONS_URL | sanctions-screening gRPC endpoint |\n\n"
            "## API\n"
            "OpenAPI spec at `/v3/api-docs`. Health: `/actuator/health`.\n\n"
            "## Ownership\n"
            "Pod Alpha. On-call PagerDuty schedule `payments-p1`."
        ),
    },
    {
        "id": "GH-fx-service-README",
        "title": "fx-service - README",
        "url": "https://github.bank.internal/payments-platform/fx-service",
        "author": "pod-beta",
        "updated_at": "2026-07-19T12:00:00Z",
        "tags": ["repo", "fx", "readme", "service"],
        "body": (
            "# fx-service\n\n"
            "Real-time FX rate lookup and conversion. Go 1.22.\n\n"
            "Rates ingested from Refinitiv and Bloomberg feeds. Fallback rate served from "
            "cache if both feeds are stale >30s.\n\n"
            "## Commands\n"
            "```\n"
            "make run       # local server on :8080\n"
            "make test      # unit tests\n"
            "make bench     # rate-lookup benchmark\n"
            "```\n\n"
            "**Do not use for regulatory reporting** - use reconciliation-service instead."
        ),
    },
    {
        "id": "GH-sanctions-screening-README",
        "title": "sanctions-screening - README",
        "url": "https://github.bank.internal/payments-platform/sanctions-screening",
        "author": "pod-gamma",
        "updated_at": "2026-06-12T15:30:00Z",
        "tags": ["repo", "sanctions", "compliance", "service"],
        "body": (
            "# sanctions-screening\n\n"
            "Real-time counterparty screening against OFAC, UN, EU, and internal watchlists.\n\n"
            "- Language: Rust\n"
            "- p99 SLO: < 80ms\n"
            "- Compliance sign-off required (label: `compliance-approved`) for any change to "
            "the matching algorithm; MLRO review required. See CODEOWNERS."
        ),
    },
    {
        "id": "GH-reconciliation-service-README",
        "title": "reconciliation-service - README",
        "url": "https://github.bank.internal/payments-platform/reconciliation-service",
        "author": "pod-delta",
        "updated_at": "2026-05-25T11:00:00Z",
        "tags": ["repo", "reconciliation", "service"],
        "body": (
            "# reconciliation-service\n\n"
            "End-of-day reconciliation vs Nostro accounts. Kotlin / Spring Batch. "
            "Runs nightly at 22:00 UTC. Outputs land in the `recon-reports` S3 bucket and "
            "are pushed to the Finance data lake.\n\n"
            "Recon breaks > $10k auto-alert to `#payments-oncall`."
        ),
    },

    # -------- Platform / Infra --------
    {
        "id": "GH-developer-handbook",
        "title": "developer-handbook - Getting Started",
        "url": "https://github.bank.internal/platform-eng/developer-handbook",
        "author": "platform-eng",
        "updated_at": "2026-08-20T09:00:00Z",
        "tags": ["handbook", "onboarding", "dev"],
        "body": (
            "# Developer Handbook\n\n"
            "Source of truth for engineering practices.\n\n"
            "## Sections\n"
            "- local-dev-setup\n"
            "- ci-cd\n"
            "- security-baseline\n"
            "- on-call\n"
            "- code-review\n"
            "- releases\n\n"
            "## Laptop bootstrap\n"
            "```\n"
            "./scripts/bootstrap.sh\n"
            "```\n"
            "Installs toolchain, configures git, sets up Artifactory + npm-internal, enrolls SSH key."
        ),
    },
    {
        "id": "GH-infra-terraform",
        "title": "infra-terraform - Cloud Landing Zone",
        "url": "https://github.bank.internal/platform-eng/infra-terraform",
        "author": "cloud-platform",
        "updated_at": "2026-02-14T10:00:00Z",
        "tags": ["infra", "terraform", "cloud"],
        "body": (
            "# infra-terraform\n\n"
            "Terraform modules for AWS + Azure landing zone. New services must provision "
            "cloud footprint via the `cloud-service` module - raw resource blocks are "
            "rejected by the policy gate."
        ),
    },
    {
        "id": "GH-terraform-network-modules",
        "title": "terraform-network-modules - VPCs, TGW, VPN",
        "url": "https://github.bank.internal/cloud-platform/terraform-network-modules",
        "author": "cloud-platform",
        "updated_at": "2026-06-20T09:00:00Z",
        "tags": ["terraform", "network", "vpc", "infra"],
        "body": (
            "# terraform-network-modules\n\n"
            "Reusable network primitives:\n"
            "- `module.vpc` - 3-AZ VPC with public/private/isolated tiers\n"
            "- `module.tgw` - Transit Gateway attachment\n"
            "- `module.vpn` - site-to-site VPN for legacy DC\n"
            "- `module.egress-controls` - restricted egress via NAT proxy\n\n"
            "All CIDR blocks are managed centrally in `cidr-registry.yaml`. Do NOT hand-allocate."
        ),
    },
    {
        "id": "GH-security-baseline",
        "title": "security-baseline - Required Controls",
        "url": "https://github.bank.internal/security/security-baseline",
        "author": "security",
        "updated_at": "2026-07-01T09:00:00Z",
        "tags": ["security", "baseline", "controls"],
        "body": (
            "# Security baseline\n\n"
            "Every service must:\n"
            "- Publish an SBOM on every build\n"
            "- Pass image scanning\n"
            "- Store secrets in Vault (not env files)\n"
            "- Use TLS 1.3 for all ingress/egress\n"
            "- Place WAF in front of any public endpoint\n"
            "- Have a quarterly access review\n"
            "- Have a signed-off threat model in `docs/threat-model.md`"
        ),
    },
    {
        "id": "GH-vault-secret-rotator",
        "title": "vault-secret-rotator - Automated rotation",
        "url": "https://github.bank.internal/security/vault-secret-rotator",
        "author": "security",
        "updated_at": "2026-05-10T09:00:00Z",
        "tags": ["vault", "secrets", "rotation"],
        "body": (
            "# vault-secret-rotator\n\n"
            "Rotates database passwords, cloud IAM keys, and service-account tokens on a "
            "schedule (default 45 days). Rotation is transactional: new secret is written, "
            "downstream apps roll, then old secret is destroyed.\n\n"
            "Supported backends: Aurora Postgres, Snowflake, AWS IAM, Azure SP, LDAP bind users."
        ),
    },

    # -------- IAM / Entitlements --------
    {
        "id": "GH-entitlement-service",
        "title": "entitlement-service - README",
        "url": "https://github.bank.internal/iam-platform/entitlement-service",
        "author": "iam-platform",
        "updated_at": "2026-08-08T09:00:00Z",
        "tags": ["repo", "iam", "entitlements", "service"],
        "body": (
            "# entitlement-service\n\n"
            "REST API in front of SailPoint IdentityIQ. Provides:\n"
            "- `GET /users/{id}/entitlements` - all AD groups + application roles\n"
            "- `POST /requests` - submit an access request\n"
            "- `POST /revocations` - immediate revoke (SecOps break-glass only)\n"
            "- `GET /recert/{campaignId}` - recert campaign data for a manager\n\n"
            "## Language / stack\n"
            "Java 21 / Spring Boot, Postgres, Kafka event bus.\n\n"
            "## Consumers\n"
            "SelfServe portal, mobile employee app, entitlement-audit-lake ETL."
        ),
    },
    {
        "id": "GH-ldap-sync-service",
        "title": "ldap-sync-service - AD to LDAP replicator",
        "url": "https://github.bank.internal/iam-platform/ldap-sync-service",
        "author": "iam-platform",
        "updated_at": "2026-06-01T09:00:00Z",
        "tags": ["repo", "ldap", "sync", "iam"],
        "body": (
            "# ldap-sync-service\n\n"
            "Replicates group membership from AD to LDAP every 5 min.\n\n"
            "## Config\n"
            "- `LDAP_URL` / `LDAP_BIND_DN` / `LDAP_BIND_PW`\n"
            "- `AD_ENDPOINT` (Graph API)\n"
            "- `SYNC_INTERVAL_SEC=300`\n\n"
            "Runs as a Kubernetes CronJob in cluster `iam-prod-1`."
        ),
    },

    # -------- Change Requests / Migration --------
    {
        "id": "GH-change-request-orchestrator",
        "title": "change-request-orchestrator - CRQ automation",
        "url": "https://github.bank.internal/change-mgmt/change-request-orchestrator",
        "author": "change-mgmt",
        "updated_at": "2026-08-27T09:00:00Z",
        "tags": ["repo", "crq", "change-mgmt"],
        "body": (
            "# change-request-orchestrator\n\n"
            "Automates the CRQ lifecycle in ServiceNow: creation, peer-review routing, CAB "
            "packet generation, calendar conflict checks, and rollback tracking.\n\n"
            "## Integrations\n"
            "- ServiceNow (source of truth)\n"
            "- Autosys (schedule freeze verification)\n"
            "- Jenkins (build tag capture)\n"
            "- Slack (`#change-approvals`)\n"
            "- Confluence (auto-attach RFC page)"
        ),
    },
    {
        "id": "GH-informatica-migration-scripts",
        "title": "informatica-migration-scripts - PowerCenter helpers",
        "url": "https://github.bank.internal/etl-team/informatica-migration-scripts",
        "author": "etl-team",
        "updated_at": "2026-08-15T09:00:00Z",
        "tags": ["repo", "informatica", "migration", "scripts"],
        "body": (
            "# informatica-migration-scripts\n\n"
            "Utilities for Informatica PowerCenter 10.5 migrations:\n"
            "- `label_objects.sh` - bulk-label mappings for a release\n"
            "- `export_deployment_group.py` - export a dep group to XML with checksums\n"
            "- `diff_repos.py` - compare source vs target repo, output HTML diff\n"
            "- `component_list.py` - generate the migration component CSV\n\n"
            "See CONF-DEP-105 (Deployment Procedure v10.5 Detailed Version) for the process."
        ),
    },
    {
        "id": "GH-autosys-jil-templates",
        "title": "autosys-jil-templates - Standard JIL patterns",
        "url": "https://github.bank.internal/etl-team/autosys-jil-templates",
        "author": "etl-team",
        "updated_at": "2026-06-30T09:00:00Z",
        "tags": ["repo", "autosys", "jil", "templates"],
        "body": (
            "# autosys-jil-templates\n\n"
            "Standard JIL fragments for CMD, BOX, FW jobs. Every new job MUST use these "
            "as a starting point - inline overrides only where justified.\n\n"
            "Includes calendar templates for month-end, quarter-end, and blackout windows."
        ),
    },

    # -------- Data platform --------
    {
        "id": "GH-data-warehouse-etl",
        "title": "data-warehouse-etl - DBT project",
        "url": "https://github.bank.internal/data-platform/data-warehouse-etl",
        "author": "data-platform",
        "updated_at": "2026-08-22T09:00:00Z",
        "tags": ["repo", "dbt", "snowflake", "etl"],
        "body": (
            "# data-warehouse-etl\n\n"
            "DBT project for Snowflake curated + mart layers.\n\n"
            "## Layout\n"
            "```\n"
            "models/\n"
            "  staging/     # 1:1 with source tables\n"
            "  curated/     # data-vault style raw/biz\n"
            "  mart/        # domain marts (fin, risk, ops, customer)\n"
            "tests/\n"
            "macros/\n"
            "```\n\n"
            "## CI\n"
            "- PR: `dbt compile`, `dbt test` in DEV\n"
            "- Merge: promote to UAT, run downstream Tableau extract refresh\n"
            "- Release: manual via CRQ, promote to PROD"
        ),
    },
    {
        "id": "GH-finance-bi-pipeline",
        "title": "finance-bi-pipeline - Airflow + DBT + Tableau glue",
        "url": "https://github.bank.internal/finance-bi/finance-bi-pipeline",
        "author": "finance-bi",
        "updated_at": "2026-08-01T09:00:00Z",
        "tags": ["repo", "finance-bi", "airflow", "dbt"],
        "body": (
            "# finance-bi-pipeline\n\n"
            "Orchestration for the daily Finance BI refresh:\n"
            "```\n"
            "  Informatica CDC (Autosys) --> Snowflake staging\n"
            "     --> DBT curated (Airflow DAG: finbi_curated)\n"
            "     --> DBT mart (Airflow DAG: finbi_mart)\n"
            "     --> Tableau extract refresh (Airflow: tableau_refresh)\n"
            "     --> Slack notification to #finbi-daily\n"
            "```\n\n"
            "Owner: Finance BI Delivery team (SharePoint site: Finance BI Delivery / SSM)."
        ),
    },
    {
        "id": "GH-kafka-connectors",
        "title": "kafka-connectors - CDC and sink connectors",
        "url": "https://github.bank.internal/data-platform/kafka-connectors",
        "author": "data-platform",
        "updated_at": "2026-07-08T09:00:00Z",
        "tags": ["repo", "kafka", "cdc", "connectors"],
        "body": (
            "# kafka-connectors\n\n"
            "Custom Kafka Connect connectors:\n"
            "- `oracle-golden-gate-source` - CDC from Oracle GL/CIF\n"
            "- `snowflake-sink` - streaming sink with idempotency\n"
            "- `s3-parquet-sink` - partitioned parquet sink for the data lake\n"
            "- `dlq-router` - routes bad events to per-topic DLQs"
        ),
    },
    {
        "id": "GH-audit-log-aggregator",
        "title": "audit-log-aggregator - Central audit lake",
        "url": "https://github.bank.internal/security/audit-log-aggregator",
        "author": "security",
        "updated_at": "2026-04-18T09:00:00Z",
        "tags": ["repo", "audit", "logging", "security"],
        "body": (
            "# audit-log-aggregator\n\n"
            "Collects audit trails from all Tier-1 apps into the audit lake for compliance "
            "and regulator queries. 7-year retention. WORM storage.\n\n"
            "Sources include: SailPoint, AD, Vault, prod-DB, Snowflake QUERY_HISTORY, "
            "Autosys job history, Jenkins deploy history, ServiceNow CRQ history."
        ),
    },
    {
        "id": "GH-reg-reporting-service",
        "title": "reg-reporting-service - MAS/RBI/APRA generator",
        "url": "https://github.bank.internal/regulatory/reg-reporting-service",
        "author": "regulatory",
        "updated_at": "2026-08-10T09:00:00Z",
        "tags": ["repo", "regulatory", "reporting", "mas", "rbi"],
        "body": (
            "# reg-reporting-service\n\n"
            "Generates regulatory reports from the curated warehouse:\n"
            "- MAS 610 (Singapore) - monthly\n"
            "- RBI DSB (India) - quarterly\n"
            "- APRA ARF (Australia) - quarterly\n\n"
            "All reports go through a 4-eyes approval flow before submission. "
            "Reports are archived to WORM storage with a submission receipt from the regulator."
        ),
    },

    # -------- CI/CD / Tooling --------
    {
        "id": "GH-cicd-jenkins-shared-library",
        "title": "cicd-jenkins-shared-library - Reusable pipeline",
        "url": "https://github.bank.internal/platform-eng/cicd-jenkins-shared-library",
        "author": "platform-eng",
        "updated_at": "2026-06-25T09:00:00Z",
        "tags": ["repo", "jenkins", "ci-cd"],
        "body": (
            "# cicd-jenkins-shared-library\n\n"
            "Shared Jenkins pipeline steps: `buildJava`, `buildGo`, `buildRust`, `deploy`, "
            "`securityScan`, `attachCRQ`. Enforces the security baseline (SBOM, image scan) "
            "and blocks deploys during change-freeze windows.\n\n"
            "## Usage\n"
            "```\n"
            "@Library('cicd-jenkins-shared-library@stable') _\n"
            "pipeline {\n"
            "  agent any\n"
            "  stages { buildJava(); securityScan(); deploy(env: 'DEV') }\n"
            "}\n"
            "```"
        ),
    },
    {
        "id": "GH-incident-bot",
        "title": "incident-bot - Slack incident helper",
        "url": "https://github.bank.internal/sre/incident-bot",
        "author": "sre",
        "updated_at": "2026-05-30T09:00:00Z",
        "tags": ["repo", "slack-bot", "incident", "sre"],
        "body": (
            "# incident-bot\n\n"
            "Slack bot that:\n"
            "- Creates the `#incident-YYYYMMDD-<slug>` channel\n"
            "- Pages the correct on-call from PagerDuty\n"
            "- Auto-drafts the RCA Confluence page\n"
            "- Posts a timeline of key events (SME joined, mitigation deployed, service restored)\n"
            "- Notifies Compliance for MAS/RBI-reportable severity events"
        ),
    },
    {
        "id": "GH-api-gateway-config",
        "title": "api-gateway-config - Kong config-as-code",
        "url": "https://github.bank.internal/platform-eng/api-gateway-config",
        "author": "platform-eng",
        "updated_at": "2026-07-18T09:00:00Z",
        "tags": ["repo", "kong", "api-gateway"],
        "body": (
            "# api-gateway-config\n\n"
            "Kong routes, plugins, and consumers as YAML. CI runs `decK diff` on PR, "
            "`decK sync` on merge to the target environment.\n\n"
            "Enforces org-wide plugins: rate-limit, JWT auth (via IAM), correlation-id, "
            "response-transformer (strips PII from error bodies)."
        ),
    },
    {
        "id": "GH-good-first-issues",
        "title": "Curated 'Good First Issue' List",
        "url": "https://github.bank.internal/platform-eng/good-first-issues",
        "author": "platform-eng",
        "updated_at": "2026-08-10T14:00:00Z",
        "tags": ["onboarding", "issues", "starter"],
        "body": (
            "Curated starter issues across bank repos, tagged by skill (java, go, rust, "
            "kotlin, python, frontend) and difficulty. Pick one, comment to claim it, "
            "and open a PR. Your buddy or manager will review."
        ),
    },
    {
        "id": "GH-ml-fraud-detection",
        "title": "ml-fraud-detection - Model & Pipelines",
        "url": "https://github.bank.internal/data-science/ml-fraud-detection",
        "author": "data-science",
        "updated_at": "2026-04-08T16:00:00Z",
        "tags": ["ml", "fraud", "python"],
        "body": (
            "# ml-fraud-detection\n\n"
            "XGBoost model + rules layer. Training on Airflow, artifacts in MLflow. "
            "Retrains that shift precision/recall by >2% require MRM (Model Risk Management) "
            "review before deployment."
        ),
    },
    {
        "id": "GH-mobile-app",
        "title": "mobile-app - iOS & Android",
        "url": "https://github.bank.internal/consumer/mobile-app",
        "author": "consumer-mobile",
        "updated_at": "2026-08-05T10:00:00Z",
        "tags": ["mobile", "consumer", "ios", "android"],
        "body": (
            "# mobile-app\n\n"
            "Consumer mobile app (React Native + native iOS/Android modules for biometrics). "
            "Feature flags via LaunchDarkly. Fortnightly release cadence."
        ),
    },
]

SHAREPOINT_DOCS = [
    # =========================================================================
    # THREE APPLICATIONS: ABC, SSM, EPM
    # Each application has six folders:
    #   ADHOC Requests, Analysis, Releases, Business Data Requirements,
    #   Onboarding New Member, Planning
    # Each folder has a landing page + several documents.
    # Every doc carries: app (ABC|SSM|EPM) + folder metadata via tags.
    # =========================================================================

    # -----------------------------------------------------------------
    # ABC (Analytics & Business Compliance) - Landing
    # -----------------------------------------------------------------
    {
        "id": "SP-ABC-HOME",
        "title": "ABC - Analytics & Business Compliance (Home)",
        "url": "https://sharepoint.bank.internal/sites/ABC/Home.aspx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-09-10T09:00:00Z",
        "tags": ["abc", "home", "landing"],
        "body": (
            "## Welcome to ABC\n"
            "ABC (Analytics & Business Compliance) is the delivery workstream that owns "
            "the regulatory analytics book of work - MAS 610, RBI DSB, APRA ARF, and the "
            "internal ABC compliance dashboards.\n\n"
            "## Folders on this site\n"
            "- [ADHOC Requests](/doc/SP-ABC-ADHOC-INDEX)\n"
            "- [Analysis](/doc/SP-ABC-ANALYSIS-INDEX)\n"
            "- [Releases](/doc/SP-ABC-RELEASES-INDEX)\n"
            "- [Business Data Requirements](/doc/SP-ABC-BDR-INDEX)\n"
            "- [Onboarding New Member](/doc/SP-ABC-ONBOARDING-INDEX)\n"
            "- [Planning](/doc/SP-ABC-PLANNING-INDEX)\n\n"
            "## Team\n"
            "- Application Lead: Safaya, Sunita\n"
            "- Analytics Lead: Sharma, Anil\n"
            "- Compliance Steward: Verma, Rahul\n"
            "- On-call rota: `#abc-support`"
        ),
    },

    # ---- ABC / ADHOC ----
    {
        "id": "SP-ABC-ADHOC-INDEX",
        "title": "ABC - ADHOC Requests",
        "url": "https://sharepoint.bank.internal/sites/ABC/ADHOC/Forms/AllItems.aspx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-09-08T09:00:00Z",
        "tags": ["abc", "adhoc", "index"],
        "body": (
            "## ADHOC Requests - ABC\n"
            "Off-cycle report and data requests from Compliance and Finance.\n\n"
            "## Documents in this folder\n"
            "- [ABC-ADHOC-Intake-Form-2026.docx](/doc/SP-ABC-ADHOC-INTAKE)\n"
            "- [ABC-ADHOC-Register.xlsx](/doc/SP-ABC-ADHOC-REGISTER)\n"
            "- [ABC-ADHOC-Q3-Summary.docx](/doc/SP-ABC-ADHOC-Q3-SUMMARY)\n\n"
            "## Turnaround SLAs\n"
            "| Category | SLA |\n"
            "|---|---|\n"
            "| Report tweak | 2 business days |\n"
            "| New extract | 5 business days |\n"
            "| One-off data pull | 3 business days |"
        ),
    },
    {
        "id": "SP-ABC-ADHOC-INTAKE",
        "title": "ABC-ADHOC-Intake-Form-2026.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/ADHOC/Intake-Form-2026.docx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["abc", "adhoc", "template", "intake"],
        "body": (
            "## ABC ADHOC Intake Form\n"
            "Use this template to raise an off-cycle request against the ABC team.\n\n"
            "### Section 1 - Requester\n"
            "- Requester Name:\n"
            "- Team / Cost centre:\n"
            "- Business sponsor:\n\n"
            "### Section 2 - Request\n"
            "- Category (report tweak / new extract / one-off pull):\n"
            "- Business justification:\n"
            "- Required by (date):\n"
            "- Data sensitivity (Public / Internal / Confidential / Restricted):\n\n"
            "### Section 3 - Data\n"
            "- Source systems (e.g. GL, CIF, RiskHub):\n"
            "- Columns / measures required:\n"
            "- Filters / grouping:\n\n"
            "### Section 4 - Sign-off\n"
            "- Line-manager approval:\n"
            "- Data Steward approval (if Restricted):"
        ),
    },
    {
        "id": "SP-ABC-ADHOC-REGISTER",
        "title": "ABC-ADHOC-Register.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/ADHOC/Register.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-05T09:00:00Z",
        "tags": ["abc", "adhoc", "register"],
        "body": (
            "## ABC ADHOC Register\n"
            "Every ADHOC delivered by the ABC team, tracked here.\n\n"
            "| ID | Title | Requester | Delivered | Effort (days) |\n"
            "|---|---|---|---|---|\n"
            "| ABC-ADH-1042 | MAS 610 line 34 breakdown | Compliance | 2026-08-11 | 1.5 |\n"
            "| ABC-ADH-1043 | UBO refresh for top-200 corporates | KYC Ops | 2026-08-14 | 3 |\n"
            "| ABC-ADH-1044 | Trader-limits daily extract | Market Risk | 2026-08-19 | 2 |\n"
            "| ABC-ADH-1045 | Retail complaints heatmap | CX Analytics | 2026-08-24 | 4 |\n"
            "| ABC-ADH-1046 | High-value payment corridor Tableau | Payments | 2026-09-02 | 2 |"
        ),
    },
    {
        "id": "SP-ABC-ADHOC-Q3-SUMMARY",
        "title": "ABC-ADHOC-Q3-Summary.docx",
        "author": "Lohar, Kavita",
        "url": "https://sharepoint.bank.internal/sites/ABC/ADHOC/Q3-Summary.docx",
        "updated_at": "2026-09-08T09:00:00Z",
        "tags": ["abc", "adhoc", "summary", "q3"],
        "body": (
            "## Q3 2026 ADHOC Summary - ABC\n"
            "17 ADHOC requests delivered against 19 raised (2 rolled to Q4).\n\n"
            "### Highlights\n"
            "- Median turnaround dropped from 4.2 days to 3.0 days\n"
            "- 100% of Compliance requests met their statutory deadline\n"
            "- No data-quality incidents attributed to ADHOC deliveries\n\n"
            "### Watch items for Q4\n"
            "- MAS 610 quarterly refresh - 4 known ADHOC follow-ups anticipated\n"
            "- Snowflake credit consumption up 22% - see Planning folder for budget"
        ),
    },

    # ---- ABC / ANALYSIS ----
    {
        "id": "SP-ABC-ANALYSIS-INDEX",
        "title": "ABC - Analysis",
        "url": "https://sharepoint.bank.internal/sites/ABC/Analysis/Forms/AllItems.aspx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-02T09:00:00Z",
        "tags": ["abc", "analysis", "index"],
        "body": (
            "## Analysis - ABC\n"
            "Ad-hoc and standing analyses produced by the ABC team.\n\n"
            "## Documents in this folder\n"
            "- [ABC-Data-Quality-Report-Aug-2026.pdf](/doc/SP-ABC-DQ-REPORT)\n"
            "- [ABC-Regulatory-Trend-Analysis-2026H1.docx](/doc/SP-ABC-REG-TREND)\n"
            "- [ABC-Snowflake-Cost-Analysis.xlsx](/doc/SP-ABC-SNOW-COST)"
        ),
    },
    {
        "id": "SP-ABC-DQ-REPORT",
        "title": "ABC-Data-Quality-Report-Aug-2026.pdf",
        "url": "https://sharepoint.bank.internal/sites/ABC/Analysis/DQ-Aug-2026.pdf",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["abc", "analysis", "data-quality"],
        "body": (
            "## Data Quality Report - August 2026\n"
            "Monthly data-quality report on the ABC curated marts.\n\n"
            "### Overall grade: A- (was B+ in July)\n\n"
            "### Findings by domain\n"
            "| Domain | Rows / day | Null-rate | Freshness (median lag) | Grade |\n"
            "|---|---|---|---|---|\n"
            "| GL | 2.1M | 0.02% | 47 min | A |\n"
            "| CIF | 480k | 0.08% | 61 min | A- |\n"
            "| Payments | 5.6M | 0.11% | 22 min | A |\n"
            "| Sanctions hits | 1.2k | 0.00% | 15 min | A+ |\n\n"
            "### Action items\n"
            "- CIF nulls on `country_of_incorporation` - 32 records - raised with KYC Ops\n"
            "- Freshness lag on GL exceeded 90 min on 3 days - root-caused to Autosys retry"
        ),
    },
    {
        "id": "SP-ABC-REG-TREND",
        "title": "ABC-Regulatory-Trend-Analysis-2026H1.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Analysis/RegTrend-2026H1.docx",
        "author": "Verma, Rahul",
        "updated_at": "2026-08-14T09:00:00Z",
        "tags": ["abc", "analysis", "regulatory", "trend"],
        "body": (
            "## Regulatory Trend Analysis - 2026 H1\n"
            "Themes emerging from MAS, RBI, and APRA in the first half of 2026.\n\n"
            "### Cross-cutting themes\n"
            "- Beneficial-ownership transparency (UBO >=10% under consultation)\n"
            "- AI governance - draft guidance from MAS on LLM use in banking\n"
            "- Operational resilience - impact-tolerance testing under 3rd-party outages\n\n"
            "### Implications for ABC\n"
            "- Prepare data model for UBO >=10% (currently >=25%)\n"
            "- Extend model-risk register to cover generative-AI copilots\n"
            "- Add 3rd-party outage scenarios to BCP tabletop schedule"
        ),
    },
    {
        "id": "SP-ABC-SNOW-COST",
        "title": "ABC-Snowflake-Cost-Analysis.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Analysis/Snowflake-Cost.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-27T09:00:00Z",
        "tags": ["abc", "analysis", "snowflake", "cost"],
        "body": (
            "## Snowflake Cost Analysis - Q3 2026\n"
            "Warehouse-level compute + storage cost for ABC workloads.\n\n"
            "| Warehouse | Q2 spend | Q3 spend | Delta |\n"
            "|---|---|---|---|\n"
            "| WH_ETL_L | $18,400 | $22,100 | +20% |\n"
            "| WH_ETL_S | $6,200 | $6,050 | -2% |\n"
            "| WH_BI_XS | $2,100 | $2,400 | +14% |\n"
            "| WH_ADHOC_S | $3,900 | $4,700 | +21% |\n\n"
            "### Drivers\n"
            "- WH_ETL_L uplift attributable to reg-reporting build-out\n"
            "- WH_ADHOC_S growth aligns with ADHOC register volumes"
        ),
    },

    # ---- ABC / RELEASES ----
    {
        "id": "SP-ABC-RELEASES-INDEX",
        "title": "ABC - Releases",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Forms/AllItems.aspx",
        "author": "Burger, Hans",
        "updated_at": "2026-09-06T09:00:00Z",
        "tags": ["abc", "releases", "index"],
        "body": (
            "## Releases - ABC\n"
            "Bi-weekly production release cadence: every second Thursday, 22:00 - 02:00 SGT.\n\n"
            "## Documents in this folder\n"
            "- [ABC-Release-Calendar-2026.xlsx](/doc/SP-ABC-REL-CAL)\n"
            "- [ABC-Release-Checklist-Template.docx](/doc/SP-ABC-REL-CHECKLIST)\n"
            "- [ABC-Release-Notes-2026.09.xlsx](/doc/SP-ABC-REL-NOTES-SEP)\n"
            "- [ABC-Rollback-Playbook.docx](/doc/SP-ABC-REL-ROLLBACK)"
        ),
    },
    {
        "id": "SP-ABC-REL-CAL",
        "title": "ABC-Release-Calendar-2026.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Calendar-2026.xlsx",
        "author": "Burger, Hans",
        "updated_at": "2026-01-14T09:00:00Z",
        "tags": ["abc", "releases", "calendar"],
        "body": (
            "## ABC Release Calendar 2026\n"
            "| Release | Cutover date | CRQ | Freeze notes |\n"
            "|---|---|---|---|\n"
            "| 2026.01 | 2026-01-22 | CRQ-71204 | - |\n"
            "| 2026.05 | 2026-05-14 | CRQ-73310 | Post month-end |\n"
            "| 2026.07 | 2026-07-09 | CRQ-75188 | - |\n"
            "| 2026.09 | 2026-09-11 | CRQ-88230 | Post MAS 610 cutoff |\n"
            "| 2026.11 | 2026-11-12 | CRQ-89901 | Pre year-end freeze |\n\n"
            "Year-end freeze: Dec 15 - Jan 5. No non-emergency releases."
        ),
    },
    {
        "id": "SP-ABC-REL-CHECKLIST",
        "title": "ABC-Release-Checklist-Template.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Checklist-Template.docx",
        "author": "Burger, Hans",
        "updated_at": "2026-04-18T09:00:00Z",
        "tags": ["abc", "releases", "checklist", "template"],
        "body": (
            "## ABC Release Checklist\n"
            "Complete before every production release.\n\n"
            "### T-3 days\n"
            "- [ ] CRQ raised in ServiceNow\n"
            "- [ ] Component list peer-reviewed\n"
            "- [ ] Downstream teams notified\n\n"
            "### T-1 day\n"
            "- [ ] Autosys job holds scheduled\n"
            "- [ ] Rollback deployment group prepared\n\n"
            "### T0 (release window)\n"
            "- [ ] Repo backup taken\n"
            "- [ ] Deployment group executed\n"
            "- [ ] Smoke tests green\n"
            "- [ ] Downstream validation with Compliance + Finance BI"
        ),
    },
    {
        "id": "SP-ABC-REL-NOTES-SEP",
        "title": "ABC-Release-Notes-2026.09.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Notes-2026-09.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-11T09:00:00Z",
        "tags": ["abc", "releases", "notes"],
        "body": (
            "## Release Notes - ABC 2026.09\n"
            "Cutover: 2026-09-11 22:00 SGT. Duration: 3h 12m. Status: SUCCESS.\n\n"
            "### Included changes\n"
            "| Ticket | Description |\n"
            "|---|---|\n"
            "| JIRA-4218 | Nostro parser switched to named-column mode |\n"
            "| JIRA-4231 | MAS 610 line 34 refactor |\n"
            "| JIRA-4237 | dbt mart.finance.gl_daily_pnl - add trader_desk grain |\n"
            "| JIRA-4241 | Autosys job PNC_ABC_LOAD_UBO retry from 2 to 4 |\n\n"
            "### Post-implementation validation\n"
            "- Recon breaks: 0\n"
            "- Row-count drift vs T-1: < 0.4% across all mapped tables"
        ),
    },
    {
        "id": "SP-ABC-REL-ROLLBACK",
        "title": "ABC-Rollback-Playbook.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Rollback-Playbook.docx",
        "author": "Burger, Hans",
        "updated_at": "2026-06-30T09:00:00Z",
        "tags": ["abc", "releases", "rollback", "playbook"],
        "body": (
            "## Rollback Playbook - ABC\n"
            "Roll back if any of the following occur within T+60 minutes of cutover.\n\n"
            "### Rollback triggers\n"
            "- Smoke test failure\n"
            "- Row-count drift > 2%\n"
            "- Downstream Tableau extract failure\n"
            "- MAS/RBI reg-report generation failure\n\n"
            "### Steps\n"
            "1. Declare rollback in `#abc-release-bridge` and page release manager\n"
            "2. Restore repo from the pre-cutover backup XML\n"
            "3. Run the labelled REVERT deployment group\n"
            "4. Rerun smoke tests\n"
            "5. Notify Compliance if any regulatory submission is affected"
        ),
    },

    # ---- ABC / BDR ----
    {
        "id": "SP-ABC-BDR-INDEX",
        "title": "ABC - Business Data Requirements",
        "url": "https://sharepoint.bank.internal/sites/ABC/BDR/Forms/AllItems.aspx",
        "author": "Verma, Rahul",
        "updated_at": "2026-08-19T09:00:00Z",
        "tags": ["abc", "bdr", "index"],
        "body": (
            "## Business Data Requirements - ABC\n"
            "Formal captures of business data needs.\n\n"
            "## Documents in this folder\n"
            "- [BDR-ABC-2026-01-UBO-Threshold.docx](/doc/SP-ABC-BDR-UBO)\n"
            "- [BDR-ABC-2026-02-MAS610-Line34.docx](/doc/SP-ABC-BDR-MAS)\n"
            "- [BDR-Template-2026.docx](/doc/SP-ABC-BDR-TEMPLATE)"
        ),
    },
    {
        "id": "SP-ABC-BDR-UBO",
        "title": "BDR-ABC-2026-01-UBO-Threshold.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/BDR/UBO-Threshold.docx",
        "author": "Verma, Rahul",
        "updated_at": "2026-08-04T09:00:00Z",
        "tags": ["abc", "bdr", "ubo", "kyc"],
        "body": (
            "## BDR: UBO threshold change from >=25% to >=10%\n"
            "\n"
            "### Business context\n"
            "MAS consultation paper 03/2026 proposes lowering the beneficial-ownership disclosure "
            "threshold from 25% to 10%. Implementation window: Q1 2027.\n\n"
            "### Data impact\n"
            "- CIF.corporate_beneficial_ownership - add flag `disclosed_at_10pct`\n"
            "- KYC.review - add new EDD sub-step\n"
            "- Reg reporting - MAS 610 line 34, line 40 restated\n\n"
            "### Sign-offs\n"
            "- Compliance: Verma, Rahul\n"
            "- Finance CDO: pending\n"
            "- InfoSec: pending"
        ),
    },
    {
        "id": "SP-ABC-BDR-MAS",
        "title": "BDR-ABC-2026-02-MAS610-Line34.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/BDR/MAS610-Line34.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-07-22T09:00:00Z",
        "tags": ["abc", "bdr", "mas610", "regulatory"],
        "body": (
            "## BDR: MAS 610 line 34 - trading-book split\n"
            "\n"
            "### Business context\n"
            "MAS 610 line 34 (trading-book exposures) requires further breakdown by product "
            "family effective 2026-10-01.\n\n"
            "### Data impact\n"
            "- New product-family dimension - sourced from Murex reference data\n"
            "- Snowflake curated: extend `fct_trading_exposure` with `product_family`\n"
            "- Tableau workbook: MAS 610 refresh datasource"
        ),
    },
    {
        "id": "SP-ABC-BDR-TEMPLATE",
        "title": "BDR-Template-2026.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/BDR/Template-2026.docx",
        "author": "Verma, Rahul",
        "updated_at": "2026-01-20T09:00:00Z",
        "tags": ["abc", "bdr", "template"],
        "body": (
            "## Business Data Requirement Template\n\n"
            "### 1. Business context\n"
            "- Regulator / stakeholder ask:\n"
            "- Effective date:\n\n"
            "### 2. Data impact\n"
            "- Source systems affected:\n"
            "- Target curated / mart tables:\n"
            "- New attributes / new grain:\n\n"
            "### 3. Sign-offs\n"
            "- Compliance:\n"
            "- Finance CDO:\n"
            "- InfoSec:"
        ),
    },

    # ---- ABC / ONBOARDING ----
    {
        "id": "SP-ABC-ONBOARDING-INDEX",
        "title": "ABC - Onboarding New Member",
        "url": "https://sharepoint.bank.internal/sites/ABC/Onboarding/Forms/AllItems.aspx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-09-04T09:00:00Z",
        "tags": ["abc", "onboarding", "index"],
        "body": (
            "## Onboarding New Member - ABC\n"
            "First-week onboarding kit for new members joining the ABC team.\n\n"
            "## Documents in this folder\n"
            "- [ABC-Onboarding-Checklist.docx](/doc/SP-ABC-ONB-CHECKLIST)\n"
            "- [ABC-Access-Request-Guide.docx](/doc/SP-ABC-ONB-ACCESS)\n"
            "- [ABC-Team-Org-Chart.pdf](/doc/SP-ABC-ONB-ORG)\n"
            "- [ABC-First-2-Weeks-Plan.docx](/doc/SP-ABC-ONB-2WEEKS)"
        ),
    },
    {
        "id": "SP-ABC-ONB-CHECKLIST",
        "title": "ABC-Onboarding-Checklist.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Onboarding/Checklist.docx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-08-28T09:00:00Z",
        "tags": ["abc", "onboarding", "checklist"],
        "body": (
            "## ABC Onboarding Checklist\n"
            "- [ ] SailPoint request for `PNC-ABC-PROD-READER`\n"
            "- [ ] PowerCenter client installed\n"
            "- [ ] Snowflake role `ROLE_ABC_READER` granted\n"
            "- [ ] Tableau access to `ABC` project\n"
            "- [ ] `#abc-daily` and `#abc-support` channels joined\n"
            "- [ ] Buddy pairing scheduled\n"
            "- [ ] Read Finance BI E2E Architecture (Confluence)\n"
            "- [ ] Read ABC ADHOC Register (Analysis folder)"
        ),
    },
    {
        "id": "SP-ABC-ONB-ACCESS",
        "title": "ABC-Access-Request-Guide.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Onboarding/Access-Guide.docx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-08-30T09:00:00Z",
        "tags": ["abc", "onboarding", "access"],
        "body": (
            "## Access Request Guide - ABC\n"
            "Where to request each entitlement.\n\n"
            "| Access | Group | Approver | Portal |\n"
            "|---|---|---|---|\n"
            "| Snowflake reader | ROLE_ABC_READER | Data Steward | SailPoint |\n"
            "| PowerCenter dev | PNC-INFA-DEV-DEVELOPER | ABC Lead | SailPoint |\n"
            "| Tableau ABC | Tableau/ABC | ABC Lead | ServiceNow |\n"
            "| AWS console (RO) | AWS-ABC-READ | Cloud Platform | SailPoint |"
        ),
    },
    {
        "id": "SP-ABC-ONB-ORG",
        "title": "ABC-Team-Org-Chart.pdf",
        "url": "https://sharepoint.bank.internal/sites/ABC/Onboarding/Org-Chart.pdf",
        "author": "Lohar, Kavita",
        "updated_at": "2026-07-15T09:00:00Z",
        "tags": ["abc", "onboarding", "org"],
        "body": (
            "## ABC Team - Org Chart\n"
            "```\n"
            "  Delivery Lead - Lohar, Kavita\n"
            "     |\n"
            "     +-- Analytics - Sharma, Anil\n"
            "     |     +-- Sr Analyst (x2), Analyst (x3)\n"
            "     +-- Compliance Steward - Verma, Rahul\n"
            "     |     +-- Compliance Analyst (x1)\n"
            "     +-- ETL - Burger, Hans\n"
            "           +-- ETL Dev (x2), ETL Support (x1)\n"
            "```"
        ),
    },
    {
        "id": "SP-ABC-ONB-2WEEKS",
        "title": "ABC-First-2-Weeks-Plan.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Onboarding/First-2-Weeks.docx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-08-12T09:00:00Z",
        "tags": ["abc", "onboarding", "plan"],
        "body": (
            "## First 2 Weeks - ABC\n"
            "### Week 1\n"
            "- Complete Day 1 checklist (Confluence: Day 1 Checklist)\n"
            "- Shadow on-call rota\n"
            "- Read Data Classification & Handling\n\n"
            "### Week 2\n"
            "- Take one ADHOC request end-to-end (with buddy pairing)\n"
            "- Attend the CAB standing meeting as a listener\n"
            "- Present a 5-min intro at the Friday team stand-up"
        ),
    },

    # ---- ABC / PLANNING ----
    {
        "id": "SP-ABC-PLANNING-INDEX",
        "title": "ABC - Planning",
        "url": "https://sharepoint.bank.internal/sites/ABC/Planning/Forms/AllItems.aspx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["abc", "planning", "index"],
        "body": (
            "## Planning - ABC\n"
            "Roadmap, OKRs, capacity and budget.\n\n"
            "## Documents in this folder\n"
            "- [ABC-Roadmap-2026-2027.xlsx](/doc/SP-ABC-PLAN-ROADMAP)\n"
            "- [ABC-2026-OKRs.docx](/doc/SP-ABC-PLAN-OKRS)\n"
            "- [ABC-Capacity-Plan.xlsx](/doc/SP-ABC-PLAN-CAPACITY)"
        ),
    },
    {
        "id": "SP-ABC-PLAN-ROADMAP",
        "title": "ABC-Roadmap-2026-2027.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Planning/Roadmap-2026-2027.xlsx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-08-25T09:00:00Z",
        "tags": ["abc", "planning", "roadmap"],
        "body": (
            "## ABC Roadmap 2026-2027\n"
            "| Q | Theme | Milestone |\n"
            "|---|---|---|\n"
            "| Q3 2026 | Reg reporting refresh | MAS 610 line 34 rewrite |\n"
            "| Q4 2026 | UBO threshold prep | 10% threshold data model |\n"
            "| Q1 2027 | ETL modernisation | 40% Informatica mappings retired |\n"
            "| Q2 2027 | AI governance | MRM register extended for LLM copilots |"
        ),
    },
    {
        "id": "SP-ABC-PLAN-OKRS",
        "title": "ABC-2026-OKRs.docx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Planning/OKRs-2026.docx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-01-30T09:00:00Z",
        "tags": ["abc", "planning", "okr"],
        "body": (
            "## 2026 OKRs - ABC\n"
            "1. Cut ADHOC median turnaround from 4.2 days to 3.0 days\n"
            "2. 100% regulatory statutory deadlines met\n"
            "3. Zero SEV1/2 incidents attributable to ABC deliverables\n"
            "4. Snowflake compute cost <= 2025 baseline + 10%"
        ),
    },
    {
        "id": "SP-ABC-PLAN-CAPACITY",
        "title": "ABC-Capacity-Plan.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Planning/Capacity.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-07-08T09:00:00Z",
        "tags": ["abc", "planning", "capacity"],
        "body": (
            "## Capacity Plan - ABC\n"
            "| Role | Headcount (current) | Headcount (need) | Gap |\n"
            "|---|---|---|---|\n"
            "| Analyst | 5 | 6 | -1 |\n"
            "| ETL Dev | 2 | 3 | -1 |\n"
            "| Compliance Analyst | 1 | 2 | -1 |\n\n"
            "Hiring approvals with HR - two headcount released for Q4."
        ),
    },

    # -----------------------------------------------------------------
    # SSM (Shared Services & Migration) - Landing
    # -----------------------------------------------------------------
    {
        "id": "SP-SSM-HOME",
        "title": "SSM - Shared Services & Migration (Home)",
        "url": "https://sharepoint.bank.internal/sites/SSM/Home.aspx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-11T09:00:00Z",
        "tags": ["ssm", "home", "landing"],
        "body": (
            "## Welcome to SSM\n"
            "SSM (Shared Services & Migration) owns cross-domain services and the "
            "large-scale migration workstreams: hosting migrations, ETL modernisation, "
            "and DB platform consolidation.\n\n"
            "## Folders on this site\n"
            "- [ADHOC Requests](/doc/SP-SSM-ADHOC-INDEX)\n"
            "- [Analysis](/doc/SP-SSM-ANALYSIS-INDEX)\n"
            "- [Releases](/doc/SP-SSM-RELEASES-INDEX)\n"
            "- [Business Data Requirements](/doc/SP-SSM-BDR-INDEX)\n"
            "- [Onboarding New Member](/doc/SP-SSM-ONBOARDING-INDEX)\n"
            "- [Planning](/doc/SP-SSM-PLANNING-INDEX)\n\n"
            "## Team\n"
            "- Application Lead: Safaya, Sunita\n"
            "- Migration Lead: Sharma, Anil\n"
            "- On-call rota: `#ssm-support`\n\n"
            "## Active migrations\n"
            "- UCP -> ENT hosting\n"
            "- Teradata -> Snowflake\n"
            "- Informatica -> DBT rewrite (40% target)"
        ),
    },
    {
        "id": "SP-SSM-ADHOC-INDEX",
        "title": "SSM - ADHOC Requests",
        "url": "https://sharepoint.bank.internal/sites/SSM/ADHOC/Forms/AllItems.aspx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["ssm", "adhoc", "index"],
        "body": (
            "## ADHOC Requests - SSM\n"
            "Off-cycle migration and shared-service asks.\n\n"
            "## Documents in this folder\n"
            "- [SSM-Migration-Assessment-Form.docx](/doc/SP-SSM-ADHOC-ASSESS)\n"
            "- [SSM-Cross-Team-Support-Register.xlsx](/doc/SP-SSM-ADHOC-REGISTER)\n"
            "- [SSM-Migration-Waiver-Requests.docx](/doc/SP-SSM-ADHOC-WAIVER)"
        ),
    },
    {
        "id": "SP-SSM-ADHOC-ASSESS",
        "title": "SSM-Migration-Assessment-Form.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/ADHOC/Assessment-Form.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-20T09:00:00Z",
        "tags": ["ssm", "adhoc", "migration", "assessment"],
        "body": (
            "## Migration Assessment Form - SSM\n"
            "Use this before requesting migration effort from SSM.\n\n"
            "### Section 1 - Application profile\n"
            "- App name / ID:\n"
            "- Tier (1/2/3):\n"
            "- Current hosting (UCP / ENT / bare-metal / vendor):\n"
            "- Data classification (highest):\n\n"
            "### Section 2 - Migration ask\n"
            "- Target hosting:\n"
            "- RPO / RTO:\n"
            "- Downtime tolerance:\n\n"
            "### Section 3 - Dependencies\n"
            "- Upstream systems:\n"
            "- Downstream systems:\n"
            "- Regulatory / audit sensitivity:"
        ),
    },
    {
        "id": "SP-SSM-ADHOC-REGISTER",
        "title": "SSM-Cross-Team-Support-Register.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/ADHOC/Support-Register.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["ssm", "adhoc", "register"],
        "body": (
            "## SSM Cross-Team Support Register\n"
            "| ID | Requesting team | Ask | Status |\n"
            "|---|---|---|---|\n"
            "| SSM-ADH-330 | Payments | LDAP group cutover to new naming | Done |\n"
            "| SSM-ADH-331 | Finance BI | Snowflake replica for UAT | In progress |\n"
            "| SSM-ADH-332 | Retail Web | Vault namespace split | Scheduled |\n"
            "| SSM-ADH-333 | Compliance | RiskHub read replica | Scoping |"
        ),
    },
    {
        "id": "SP-SSM-ADHOC-WAIVER",
        "title": "SSM-Migration-Waiver-Requests.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/ADHOC/Waivers.docx",
        "author": "Verma, Rahul",
        "updated_at": "2026-08-04T09:00:00Z",
        "tags": ["ssm", "adhoc", "waiver"],
        "body": (
            "## Migration Waiver Requests\n"
            "Waivers to defer a scheduled migration beyond its target date.\n\n"
            "### Approvers\n"
            "- SSM Lead\n"
            "- Application Owner\n"
            "- InfoSec (for any Tier-1 waiver)\n\n"
            "### Standing rule\n"
            "No waiver may extend a migration beyond the regulator-mandated deadline "
            "(where applicable) without CIO sign-off."
        ),
    },

    {
        "id": "SP-SSM-ANALYSIS-INDEX",
        "title": "SSM - Analysis",
        "url": "https://sharepoint.bank.internal/sites/SSM/Analysis/Forms/AllItems.aspx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-30T09:00:00Z",
        "tags": ["ssm", "analysis", "index"],
        "body": (
            "## Analysis - SSM\n"
            "\n"
            "## Documents in this folder\n"
            "- [SSM-UCP-to-ENT-Wave2-Analysis.docx](/doc/SP-SSM-ANA-WAVE2)\n"
            "- [SSM-Teradata-to-Snowflake-Cost-Model.xlsx](/doc/SP-SSM-ANA-TERA)\n"
            "- [SSM-Informatica-to-DBT-Effort.xlsx](/doc/SP-SSM-ANA-INFA-DBT)"
        ),
    },
    {
        "id": "SP-SSM-ANA-WAVE2",
        "title": "SSM-UCP-to-ENT-Wave2-Analysis.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Analysis/UCP-Wave2.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-19T09:00:00Z",
        "tags": ["ssm", "analysis", "ucp", "ent", "migration"],
        "body": (
            "## UCP to ENT Migration - Wave 2 Analysis\n"
            "Scope: 14 applications in UAT, targeting cutover 2026-10-15.\n\n"
            "### Risks\n"
            "- Kafka MirrorMaker lag observed under dual-run load\n"
            "- Two Informatica agents still pinned to UCP-only network paths\n\n"
            "### Recommendation\n"
            "Cutover 12 of 14 apps on 2026-10-15; defer the two Informatica-pinned apps "
            "to Wave 2b (2026-11-05) after network paths are opened."
        ),
    },
    {
        "id": "SP-SSM-ANA-TERA",
        "title": "SSM-Teradata-to-Snowflake-Cost-Model.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Analysis/Teradata-Cost.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-07-25T09:00:00Z",
        "tags": ["ssm", "analysis", "teradata", "snowflake", "cost"],
        "body": (
            "## Teradata -> Snowflake Cost Model\n"
            "| Line item | Teradata (annual) | Snowflake (annual) |\n"
            "|---|---|---|\n"
            "| Compute | $2.1M | $1.4M |\n"
            "| Storage | $480k | $290k |\n"
            "| Support + license | $650k | $180k |\n"
            "| Total | $3.23M | $1.87M |\n\n"
            "### Payback\n"
            "Break-even at month 14 including one-time migration cost of $2.3M."
        ),
    },
    {
        "id": "SP-SSM-ANA-INFA-DBT",
        "title": "SSM-Informatica-to-DBT-Effort.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Analysis/Infa-DBT.xlsx",
        "author": "Burger, Hans",
        "updated_at": "2026-06-15T09:00:00Z",
        "tags": ["ssm", "analysis", "informatica", "dbt"],
        "body": (
            "## Informatica -> DBT Rewrite Effort\n"
            "| Domain | Mappings | Complexity | Estimated dev-days |\n"
            "|---|---|---|---|\n"
            "| Finance | 84 | Med | 220 |\n"
            "| Risk | 47 | High | 180 |\n"
            "| Ops | 61 | Low | 120 |\n"
            "| Customer | 38 | Med | 100 |\n"
            "\n"
            "40% target = ~92 mappings. Prioritise Ops (fast wins) and Risk (high defect rate)."
        ),
    },

    {
        "id": "SP-SSM-RELEASES-INDEX",
        "title": "SSM - Releases",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Forms/AllItems.aspx",
        "author": "Burger, Hans",
        "updated_at": "2026-09-11T09:00:00Z",
        "tags": ["ssm", "releases", "index"],
        "body": (
            "## Releases - SSM\n"
            "Cross-cutting release train for migrations and shared services.\n\n"
            "## Documents in this folder\n"
            "- [SSM-Release-Train-Calendar.xlsx](/doc/SP-SSM-REL-CAL)\n"
            "- [SSM-UCP-Wave2-Cutover-Runbook.docx](/doc/SP-SSM-REL-WAVE2)\n"
            "- [SSM-Post-Release-Retro-Template.docx](/doc/SP-SSM-REL-RETRO)"
        ),
    },
    {
        "id": "SP-SSM-REL-CAL",
        "title": "SSM-Release-Train-Calendar.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Calendar.xlsx",
        "author": "Burger, Hans",
        "updated_at": "2026-02-10T09:00:00Z",
        "tags": ["ssm", "releases", "calendar"],
        "body": (
            "## SSM Release Train 2026\n"
            "| Milestone | Date | Notes |\n"
            "|---|---|---|\n"
            "| UCP -> ENT Wave 1 | 2026-06-18 | DEV/SIT complete |\n"
            "| UCP -> ENT Wave 2 | 2026-10-15 | UAT + PROD |\n"
            "| UCP -> ENT Wave 2b | 2026-11-05 | Informatica-pinned apps |\n"
            "| Teradata -> Snowflake pilot | 2026-11-20 | Finance BI mart |\n"
            "| Informatica -> DBT batch 1 | 2026-12-04 | Ops mappings |"
        ),
    },
    {
        "id": "SP-SSM-REL-WAVE2",
        "title": "SSM-UCP-Wave2-Cutover-Runbook.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Wave2-Runbook.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["ssm", "releases", "runbook", "ucp"],
        "body": (
            "## UCP Wave 2 Cutover Runbook\n"
            "```\n"
            "T-30m   Freeze deployments cluster-wide\n"
            "T-15m   Take backups (Vault, LDAP, config)\n"
            "T0      DNS switch to ENT ingress\n"
            "T+15m   Smoke tests (login, health, sample transactions)\n"
            "T+30m   Reg-reporting jobs re-enabled\n"
            "T+45m   Downstream validation with FINBI + Payments\n"
            "T+60m   Freeze lifted or rollback declared\n"
            "```\n\n"
            "### Rollback\n"
            "DNS re-pointed to UCP; restart Autosys jobs pinned to UCP; alert #incident-bridge."
        ),
    },
    {
        "id": "SP-SSM-REL-RETRO",
        "title": "SSM-Post-Release-Retro-Template.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Retro-Template.docx",
        "author": "Burger, Hans",
        "updated_at": "2026-03-20T09:00:00Z",
        "tags": ["ssm", "releases", "retro", "template"],
        "body": (
            "## Post-Release Retro Template\n"
            "### What went well\n"
            "### What did not\n"
            "### Surprises\n"
            "### Action items (owner, due date)\n"
            "### Regulatory / audit implications"
        ),
    },

    {
        "id": "SP-SSM-BDR-INDEX",
        "title": "SSM - Business Data Requirements",
        "url": "https://sharepoint.bank.internal/sites/SSM/BDR/Forms/AllItems.aspx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-01T09:00:00Z",
        "tags": ["ssm", "bdr", "index"],
        "body": (
            "## Business Data Requirements - SSM\n"
            "## Documents in this folder\n"
            "- [BDR-SSM-2026-01-Snowflake-Replica.docx](/doc/SP-SSM-BDR-REPLICA)\n"
            "- [BDR-SSM-2026-02-Cross-Region-DR.docx](/doc/SP-SSM-BDR-DR)\n"
            "- [BDR-Template.docx](/doc/SP-SSM-BDR-TEMPLATE)"
        ),
    },
    {
        "id": "SP-SSM-BDR-REPLICA",
        "title": "BDR-SSM-2026-01-Snowflake-Replica.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/BDR/Snowflake-Replica.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-07-30T09:00:00Z",
        "tags": ["ssm", "bdr", "snowflake", "replica"],
        "body": (
            "## BDR: Snowflake read replica for UAT\n"
            "### Business context\n"
            "Finance BI UAT currently reads from PROD Snowflake via masked views. This "
            "creates cost bleed and audit friction. Need a dedicated UAT account replicated "
            "from PROD nightly.\n\n"
            "### Data impact\n"
            "- Account replication policy set on PROD -> UAT\n"
            "- Row-access policies mirrored\n"
            "- Cost target: <= $8k / month"
        ),
    },
    {
        "id": "SP-SSM-BDR-DR",
        "title": "BDR-SSM-2026-02-Cross-Region-DR.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/BDR/Cross-Region-DR.docx",
        "author": "Cloud Platform",
        "updated_at": "2026-06-25T09:00:00Z",
        "tags": ["ssm", "bdr", "dr", "resilience"],
        "body": (
            "## BDR: Cross-region DR for Tier-1 workloads\n"
            "### Business context\n"
            "MAS TRM 2026 update requires demonstrable 2-hour RTO for retail internet banking. "
            "Current design meets this; need explicit failover drill twice a year.\n\n"
            "### Data impact\n"
            "- Aurora cross-region read replica for CIF\n"
            "- Snowflake account replication for FINBI mart\n"
            "- Kafka MirrorMaker for payments topics"
        ),
    },
    {
        "id": "SP-SSM-BDR-TEMPLATE",
        "title": "BDR-Template.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/BDR/Template.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-01-15T09:00:00Z",
        "tags": ["ssm", "bdr", "template"],
        "body": (
            "## SSM BDR Template\n"
            "### 1. Business context\n"
            "### 2. Data impact\n"
            "### 3. Sign-offs (SSM Lead, App Owner, InfoSec)"
        ),
    },

    {
        "id": "SP-SSM-ONBOARDING-INDEX",
        "title": "SSM - Onboarding New Member",
        "url": "https://sharepoint.bank.internal/sites/SSM/Onboarding/Forms/AllItems.aspx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-04T09:00:00Z",
        "tags": ["ssm", "onboarding", "index"],
        "body": (
            "## Onboarding New Member - SSM\n"
            "## Documents in this folder\n"
            "- [SSM-Onboarding-Checklist.docx](/doc/SP-SSM-ONB-CHECKLIST)\n"
            "- [SSM-Migration-Primer.docx](/doc/SP-SSM-ONB-PRIMER)\n"
            "- [SSM-Access-Matrix.xlsx](/doc/SP-SSM-ONB-ACCESS)\n"
            "- [SSM-Team-Directory.pdf](/doc/SP-SSM-ONB-DIR)"
        ),
    },
    {
        "id": "SP-SSM-ONB-CHECKLIST",
        "title": "SSM-Onboarding-Checklist.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Onboarding/Checklist.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-30T09:00:00Z",
        "tags": ["ssm", "onboarding", "checklist"],
        "body": (
            "## SSM Onboarding Checklist\n"
            "- [ ] SailPoint request for `PNC-SSM-PROD-READER`\n"
            "- [ ] Confluence access to Migration space\n"
            "- [ ] AWS + Azure console (read-only) access\n"
            "- [ ] PowerCenter client + repo access\n"
            "- [ ] `#ssm-support` Slack channel\n"
            "- [ ] Read UCP-to-ENT Wave 2 Analysis"
        ),
    },
    {
        "id": "SP-SSM-ONB-PRIMER",
        "title": "SSM-Migration-Primer.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Onboarding/Primer.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-25T09:00:00Z",
        "tags": ["ssm", "onboarding", "primer", "migration"],
        "body": (
            "## SSM Migration Primer\n"
            "Everything a new joiner should know about our migration playbook in 15 minutes.\n\n"
            "### The three pillars\n"
            "- **Dual-run** - every migration runs old + new side by side for at least two weeks\n"
            "- **Reversible** - every cutover has a documented, rehearsed rollback\n"
            "- **Auditable** - CRQ, evidence pack, and PIR filed for every wave\n\n"
            "### Common patterns\n"
            "- Hosting migration -> DNS traffic manager cutover\n"
            "- DB platform -> account replication + shadow reads\n"
            "- ETL rewrite -> data diff harness comparing old vs new pipeline outputs"
        ),
    },
    {
        "id": "SP-SSM-ONB-ACCESS",
        "title": "SSM-Access-Matrix.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Onboarding/Access-Matrix.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-07-15T09:00:00Z",
        "tags": ["ssm", "onboarding", "access"],
        "body": (
            "## SSM Access Matrix\n"
            "| Role | AD group | SSM System |\n"
            "|---|---|---|\n"
            "| SSM Reader | PNC-SSM-PROD-READER | All read APIs |\n"
            "| SSM Migration Dev | PNC-SSM-DEV-DEVELOPER | Migration tools |\n"
            "| SSM Migration Deployer | PNC-SSM-PROD-DEPLOYER | Cutover console |\n"
            "| SSM Admin | PNC-SSM-PROD-ADMIN | All |"
        ),
    },
    {
        "id": "SP-SSM-ONB-DIR",
        "title": "SSM-Team-Directory.pdf",
        "url": "https://sharepoint.bank.internal/sites/SSM/Onboarding/Directory.pdf",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-20T09:00:00Z",
        "tags": ["ssm", "onboarding", "directory"],
        "body": (
            "## SSM Team Directory\n"
            "| Name | Role | Slack |\n"
            "|---|---|---|\n"
            "| Sharma, Anil | SSM Lead | @anils |\n"
            "| Burger, Hans | Release / Change | @hansb |\n"
            "| Lohar, Kavita | ABC liaison | @kavital |\n"
            "| Kowalski, Anna | Platform liaison | @annak |"
        ),
    },

    {
        "id": "SP-SSM-PLANNING-INDEX",
        "title": "SSM - Planning",
        "url": "https://sharepoint.bank.internal/sites/SSM/Planning/Forms/AllItems.aspx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["ssm", "planning", "index"],
        "body": (
            "## Planning - SSM\n"
            "## Documents in this folder\n"
            "- [SSM-Migration-Roadmap.xlsx](/doc/SP-SSM-PLAN-ROADMAP)\n"
            "- [SSM-2026-OKRs.docx](/doc/SP-SSM-PLAN-OKRS)\n"
            "- [SSM-Cross-Region-DR-Drill-Schedule.xlsx](/doc/SP-SSM-PLAN-DR)"
        ),
    },
    {
        "id": "SP-SSM-PLAN-ROADMAP",
        "title": "SSM-Migration-Roadmap.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Planning/Roadmap.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-08-28T09:00:00Z",
        "tags": ["ssm", "planning", "roadmap"],
        "body": (
            "## SSM Migration Roadmap 2026-2027\n"
            "| Q | Migration | Status |\n"
            "|---|---|---|\n"
            "| Q4 2026 | UCP -> ENT Wave 2 | In flight |\n"
            "| Q4 2026 | Teradata -> Snowflake pilot | Scoped |\n"
            "| Q1 2027 | Informatica -> DBT batch 1 | Planned |\n"
            "| Q2 2027 | Legacy DB (SQL Server 2016) sunset | Planned |"
        ),
    },
    {
        "id": "SP-SSM-PLAN-OKRS",
        "title": "SSM-2026-OKRs.docx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Planning/OKRs-2026.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-02-01T09:00:00Z",
        "tags": ["ssm", "planning", "okr"],
        "body": (
            "## SSM 2026 OKRs\n"
            "1. Decommission UCP by 2026-12-31\n"
            "2. Zero SEV1 incidents attributable to migration cutovers\n"
            "3. Teradata -> Snowflake pilot delivered under 90% of budget\n"
            "4. 100% CRQs filed with rollback evidence"
        ),
    },
    {
        "id": "SP-SSM-PLAN-DR",
        "title": "SSM-Cross-Region-DR-Drill-Schedule.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Planning/DR-Drill.xlsx",
        "author": "Cloud Platform",
        "updated_at": "2026-05-05T09:00:00Z",
        "tags": ["ssm", "planning", "dr", "drill"],
        "body": (
            "## DR Drill Schedule 2026\n"
            "| Date | Scenario | Scope |\n"
            "|---|---|---|\n"
            "| 2026-04-20 | Primary DC failure | Tabletop |\n"
            "| 2026-06-15 | Snowflake region outage | Live failover |\n"
            "| 2026-09-22 | Kafka MSK region outage | Tabletop |\n"
            "| 2026-11-17 | Full BCP - retail banking | Live failover |"
        ),
    },

    # -----------------------------------------------------------------
    # EPM (Enterprise Performance Management) - Landing
    # -----------------------------------------------------------------
    {
        "id": "SP-EPM-HOME",
        "title": "EPM - Enterprise Performance Management (Home)",
        "url": "https://sharepoint.bank.internal/sites/EPM/Home.aspx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-12T09:00:00Z",
        "tags": ["epm", "home", "landing"],
        "body": (
            "## Welcome to EPM\n"
            "EPM (Enterprise Performance Management) owns the P&L attribution stack, "
            "budgeting / forecasting cubes, and the executive scorecard on Tableau.\n\n"
            "## Folders on this site\n"
            "- [ADHOC Requests](/doc/SP-EPM-ADHOC-INDEX)\n"
            "- [Analysis](/doc/SP-EPM-ANALYSIS-INDEX)\n"
            "- [Releases](/doc/SP-EPM-RELEASES-INDEX)\n"
            "- [Business Data Requirements](/doc/SP-EPM-BDR-INDEX)\n"
            "- [Onboarding New Member](/doc/SP-EPM-ONBOARDING-INDEX)\n"
            "- [Planning](/doc/SP-EPM-PLANNING-INDEX)\n\n"
            "## Team\n"
            "- Application Lead: Safaya, Sunita\n"
            "- Reporting Lead: Menon, Priya\n"
            "- On-call rota: `#epm-support`"
        ),
    },

    {
        "id": "SP-EPM-ADHOC-INDEX",
        "title": "EPM - ADHOC Requests",
        "url": "https://sharepoint.bank.internal/sites/EPM/ADHOC/Forms/AllItems.aspx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-08T09:00:00Z",
        "tags": ["epm", "adhoc", "index"],
        "body": (
            "## ADHOC Requests - EPM\n"
            "## Documents in this folder\n"
            "- [EPM-ADHOC-Intake.docx](/doc/SP-EPM-ADHOC-INTAKE)\n"
            "- [EPM-ADHOC-Register.xlsx](/doc/SP-EPM-ADHOC-REGISTER)\n"
            "- [EPM-Board-Pack-Snapshots.pptx](/doc/SP-EPM-ADHOC-BOARD)"
        ),
    },
    {
        "id": "SP-EPM-ADHOC-INTAKE",
        "title": "EPM-ADHOC-Intake.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/ADHOC/Intake.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-08-25T09:00:00Z",
        "tags": ["epm", "adhoc", "template"],
        "body": (
            "## EPM ADHOC Intake\n"
            "### Requester\n"
            "### Business ask\n"
            "### Data required (cube / grain / period)\n"
            "### Deadline\n"
            "### Sensitivity"
        ),
    },
    {
        "id": "SP-EPM-ADHOC-REGISTER",
        "title": "EPM-ADHOC-Register.xlsx",
        "url": "https://sharepoint.bank.internal/sites/EPM/ADHOC/Register.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-05T09:00:00Z",
        "tags": ["epm", "adhoc", "register"],
        "body": (
            "## EPM ADHOC Register\n"
            "| ID | Title | Requester | Delivered |\n"
            "|---|---|---|---|\n"
            "| EPM-ADH-2010 | Board pack Q3 draft | CFO office | 2026-08-11 |\n"
            "| EPM-ADH-2011 | LOB P&L breakdown | Retail head | 2026-08-19 |\n"
            "| EPM-ADH-2012 | FX-neutral revenue view | CFO office | 2026-09-02 |"
        ),
    },
    {
        "id": "SP-EPM-ADHOC-BOARD",
        "title": "EPM-Board-Pack-Snapshots.pptx",
        "url": "https://sharepoint.bank.internal/sites/EPM/ADHOC/Board-Pack.pptx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-04T09:00:00Z",
        "tags": ["epm", "adhoc", "board"],
        "body": (
            "## Board Pack Snapshots - Q3 2026\n"
            "Curated slides for the quarterly board pack. Do not distribute outside "
            "the Finance leadership team.\n\n"
            "### Slide index\n"
            "- Slide 3 - Group revenue vs plan\n"
            "- Slide 5 - LOB contribution\n"
            "- Slide 8 - Cost-income ratio trend\n"
            "- Slide 11 - Capital ratios (CET1, T1, TC)\n"
            "- Slide 14 - Guidance vs consensus"
        ),
    },

    {
        "id": "SP-EPM-ANALYSIS-INDEX",
        "title": "EPM - Analysis",
        "url": "https://sharepoint.bank.internal/sites/EPM/Analysis/Forms/AllItems.aspx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["epm", "analysis", "index"],
        "body": (
            "## Analysis - EPM\n"
            "## Documents in this folder\n"
            "- [EPM-Variance-Analysis-Aug-2026.docx](/doc/SP-EPM-ANA-VAR)\n"
            "- [EPM-LOB-Attribution.xlsx](/doc/SP-EPM-ANA-LOB)\n"
            "- [EPM-FX-Neutral-Revenue.docx](/doc/SP-EPM-ANA-FX)"
        ),
    },
    {
        "id": "SP-EPM-ANA-VAR",
        "title": "EPM-Variance-Analysis-Aug-2026.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Analysis/Variance-Aug.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["epm", "analysis", "variance"],
        "body": (
            "## Variance Analysis - August 2026\n"
            "Actual vs plan variance, Group level.\n\n"
            "### Highlights\n"
            "- Revenue +2.3% vs plan (FX tailwind and stronger retail lending)\n"
            "- Cost +1.1% vs plan (contractor uplift on migration workstreams)\n"
            "- Cost-income ratio unchanged at 52.4%"
        ),
    },
    {
        "id": "SP-EPM-ANA-LOB",
        "title": "EPM-LOB-Attribution.xlsx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Analysis/LOB-Attribution.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-08-22T09:00:00Z",
        "tags": ["epm", "analysis", "lob"],
        "body": (
            "## LOB Attribution - YTD 2026\n"
            "| LOB | Revenue YTD | vs plan |\n"
            "|---|---|---|\n"
            "| Consumer | $4.1B | +1.8% |\n"
            "| CIB | $3.6B | +3.4% |\n"
            "| Wealth | $1.2B | -0.6% |\n"
            "| Global Markets | $2.9B | +5.1% |"
        ),
    },
    {
        "id": "SP-EPM-ANA-FX",
        "title": "EPM-FX-Neutral-Revenue.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Analysis/FX-Neutral.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-07-31T09:00:00Z",
        "tags": ["epm", "analysis", "fx"],
        "body": (
            "## FX-Neutral Revenue View\n"
            "Adjusting revenue for FX movement provides a cleaner view of underlying growth. "
            "Group FX-neutral revenue YTD is +1.4% vs plan (headline +2.3%)."
        ),
    },

    {
        "id": "SP-EPM-RELEASES-INDEX",
        "title": "EPM - Releases",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Forms/AllItems.aspx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-11T09:00:00Z",
        "tags": ["epm", "releases", "index"],
        "body": (
            "## Releases - EPM\n"
            "## Documents in this folder\n"
            "- [EPM-Cube-Refresh-Calendar.xlsx](/doc/SP-EPM-REL-CUBE)\n"
            "- [EPM-Model-Deployment-Runbook.docx](/doc/SP-EPM-REL-MODEL)\n"
            "- [EPM-Change-Log-2026.xlsx](/doc/SP-EPM-REL-CHANGES)"
        ),
    },
    {
        "id": "SP-EPM-REL-CUBE",
        "title": "EPM-Cube-Refresh-Calendar.xlsx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Cube-Refresh.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-01-25T09:00:00Z",
        "tags": ["epm", "releases", "cube"],
        "body": (
            "## Cube Refresh Calendar 2026\n"
            "| Cube | Cadence | Owner |\n"
            "|---|---|---|\n"
            "| P&L Attribution | Daily 04:00 | EPM |\n"
            "| Budget vs Actual | Monthly BD+2 | EPM |\n"
            "| Board scorecard | Quarterly | EPM + CFO office |"
        ),
    },
    {
        "id": "SP-EPM-REL-MODEL",
        "title": "EPM-Model-Deployment-Runbook.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Model-Runbook.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-08-15T09:00:00Z",
        "tags": ["epm", "releases", "model", "runbook"],
        "body": (
            "## Model Deployment Runbook\n"
            "### Pre-deploy\n"
            "- MRM review complete\n"
            "- Back-test vs 3 prior quarters\n"
            "- Approver: CFO office\n\n"
            "### Deploy\n"
            "- Promote model artifact to PROD\n"
            "- Rebuild all dependent cubes\n"
            "- Refresh Tableau extracts"
        ),
    },
    {
        "id": "SP-EPM-REL-CHANGES",
        "title": "EPM-Change-Log-2026.xlsx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Change-Log.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-11T09:00:00Z",
        "tags": ["epm", "releases", "changelog"],
        "body": (
            "## EPM Change Log 2026\n"
            "| Date | Change | CRQ |\n"
            "|---|---|---|\n"
            "| 2026-03-14 | Board scorecard v3 model | CRQ-72108 |\n"
            "| 2026-06-19 | LOB attribution refactor | CRQ-74551 |\n"
            "| 2026-09-11 | FX-neutral view GA | CRQ-88231 |"
        ),
    },

    {
        "id": "SP-EPM-BDR-INDEX",
        "title": "EPM - Business Data Requirements",
        "url": "https://sharepoint.bank.internal/sites/EPM/BDR/Forms/AllItems.aspx",
        "author": "Menon, Priya",
        "updated_at": "2026-08-05T09:00:00Z",
        "tags": ["epm", "bdr", "index"],
        "body": (
            "## Business Data Requirements - EPM\n"
            "## Documents in this folder\n"
            "- [BDR-EPM-2026-01-FX-Neutral.docx](/doc/SP-EPM-BDR-FX)\n"
            "- [BDR-EPM-2026-02-LOB-Attribution.docx](/doc/SP-EPM-BDR-LOB)"
        ),
    },
    {
        "id": "SP-EPM-BDR-FX",
        "title": "BDR-EPM-2026-01-FX-Neutral.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/BDR/FX-Neutral.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-07-15T09:00:00Z",
        "tags": ["epm", "bdr", "fx"],
        "body": (
            "## BDR: FX-neutral revenue view\n"
            "### Business context\n"
            "CFO office wants a standardised FX-neutral view for board presentation. "
            "Underlying method: constant-currency at YTD average vs prior year.\n\n"
            "### Data impact\n"
            "- New attribute in P&L cube: `revenue_fx_neutral`\n"
            "- FX rate source: fx-service published rates (Confluence: fx-service README)"
        ),
    },
    {
        "id": "SP-EPM-BDR-LOB",
        "title": "BDR-EPM-2026-02-LOB-Attribution.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/BDR/LOB-Attribution.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-06-10T09:00:00Z",
        "tags": ["epm", "bdr", "lob"],
        "body": (
            "## BDR: LOB attribution refactor\n"
            "### Business context\n"
            "Retail vs Wealth split of digital-channel revenue is currently allocated by "
            "product code only. Move to a segment-aware allocation using CIF segments.\n\n"
            "### Data impact\n"
            "- New attribute: `cif_segment` on P&L staging\n"
            "- New allocation logic in cube 'P&L Attribution'"
        ),
    },

    {
        "id": "SP-EPM-ONBOARDING-INDEX",
        "title": "EPM - Onboarding New Member",
        "url": "https://sharepoint.bank.internal/sites/EPM/Onboarding/Forms/AllItems.aspx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-04T09:00:00Z",
        "tags": ["epm", "onboarding", "index"],
        "body": (
            "## Onboarding New Member - EPM\n"
            "## Documents in this folder\n"
            "- [EPM-Onboarding-Checklist.docx](/doc/SP-EPM-ONB-CHECKLIST)\n"
            "- [EPM-Cube-Primer.docx](/doc/SP-EPM-ONB-CUBE)\n"
            "- [EPM-Tableau-Bookmarks.pdf](/doc/SP-EPM-ONB-TABLEAU)"
        ),
    },
    {
        "id": "SP-EPM-ONB-CHECKLIST",
        "title": "EPM-Onboarding-Checklist.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Onboarding/Checklist.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-08-30T09:00:00Z",
        "tags": ["epm", "onboarding", "checklist"],
        "body": (
            "## EPM Onboarding Checklist\n"
            "- [ ] SailPoint request for `PNC-EPM-PROD-READER`\n"
            "- [ ] Tableau access to `EPM` project\n"
            "- [ ] Read the Cube Primer\n"
            "- [ ] Shadow an ADHOC delivery\n"
            "- [ ] Attend one CFO office briefing (listener)"
        ),
    },
    {
        "id": "SP-EPM-ONB-CUBE",
        "title": "EPM-Cube-Primer.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Onboarding/Cube-Primer.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-08-25T09:00:00Z",
        "tags": ["epm", "onboarding", "primer", "cube"],
        "body": (
            "## Cube Primer - EPM\n"
            "The EPM stack lives on three cubes.\n\n"
            "### 1. P&L Attribution\n"
            "Grain: LOB x product x currency x day. Sources: GL curated.\n\n"
            "### 2. Budget vs Actual\n"
            "Grain: cost-centre x month. Sources: GL curated + Anaplan feed.\n\n"
            "### 3. Board scorecard\n"
            "Aggregated cube used by the CFO office for board packs."
        ),
    },
    {
        "id": "SP-EPM-ONB-TABLEAU",
        "title": "EPM-Tableau-Bookmarks.pdf",
        "url": "https://sharepoint.bank.internal/sites/EPM/Onboarding/Tableau-Bookmarks.pdf",
        "author": "Menon, Priya",
        "updated_at": "2026-07-30T09:00:00Z",
        "tags": ["epm", "onboarding", "tableau"],
        "body": (
            "## Tableau Bookmarks - EPM\n"
            "- `EPM_PnL_Daily`\n"
            "- `EPM_LOB_Contribution`\n"
            "- `EPM_Cost_Income_Trend`\n"
            "- `EPM_Board_Scorecard`\n"
            "- `EPM_FX_Neutral_Revenue`"
        ),
    },

    {
        "id": "SP-EPM-PLANNING-INDEX",
        "title": "EPM - Planning",
        "url": "https://sharepoint.bank.internal/sites/EPM/Planning/Forms/AllItems.aspx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-01T09:00:00Z",
        "tags": ["epm", "planning", "index"],
        "body": (
            "## Planning - EPM\n"
            "## Documents in this folder\n"
            "- [EPM-Roadmap-2026-2027.xlsx](/doc/SP-EPM-PLAN-ROADMAP)\n"
            "- [EPM-2026-OKRs.docx](/doc/SP-EPM-PLAN-OKRS)\n"
            "- [EPM-Board-Pack-Cadence.xlsx](/doc/SP-EPM-PLAN-BOARD)"
        ),
    },
    {
        "id": "SP-EPM-PLAN-ROADMAP",
        "title": "EPM-Roadmap-2026-2027.xlsx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Planning/Roadmap.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-08-20T09:00:00Z",
        "tags": ["epm", "planning", "roadmap"],
        "body": (
            "## EPM Roadmap 2026-2027\n"
            "| Q | Theme | Milestone |\n"
            "|---|---|---|\n"
            "| Q4 2026 | FX-neutral GA | Board pack Q3 uses new view |\n"
            "| Q1 2027 | Cube on Snowflake | Retire legacy MOLAP |\n"
            "| Q2 2027 | AI-assisted commentary | Draft variance narrative from cube |"
        ),
    },
    {
        "id": "SP-EPM-PLAN-OKRS",
        "title": "EPM-2026-OKRs.docx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Planning/OKRs-2026.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-02-05T09:00:00Z",
        "tags": ["epm", "planning", "okr"],
        "body": (
            "## EPM 2026 OKRs\n"
            "1. Board pack self-service - 3 fewer ADHOC per quarter\n"
            "2. Cube refresh SLA - 100% under 04:30 SGT\n"
            "3. Zero data-quality incidents on published board figures"
        ),
    },
    {
        "id": "SP-EPM-PLAN-BOARD",
        "title": "EPM-Board-Pack-Cadence.xlsx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Planning/Board-Cadence.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-06-01T09:00:00Z",
        "tags": ["epm", "planning", "board"],
        "body": (
            "## Board Pack Cadence 2026\n"
            "| Board meeting | Pack draft due | Final due |\n"
            "|---|---|---|\n"
            "| 2026-02-14 | 2026-02-07 | 2026-02-12 |\n"
            "| 2026-05-16 | 2026-05-09 | 2026-05-14 |\n"
            "| 2026-08-15 | 2026-08-08 | 2026-08-13 |\n"
            "| 2026-11-14 | 2026-11-07 | 2026-11-12 |"
        ),
    },

    # =========================================================================
    # 11 Release Documents / 61. Oct Release 2026
    # Migration + Unit Testing artefacts for ABC-1998, EPM-1998, SSM-1998.
    # Ingested from the Oct release SharePoint drop.
    # =========================================================================

    # -----------------------------------------------------------------
    # ABC-1998 - Oct Release 2026
    # -----------------------------------------------------------------
    {
        "id": "SP-ABC-1998-INDEX",
        "title": "11 Release Documents / 61. Oct Release 2026 / ABC-1998",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/",
        "author": "Lohar, Kavita",
        "updated_at": "2026-09-15T09:00:00Z",
        "tags": ["abc", "releases", "oct-2026", "abc-1998", "index"],
        "body": (
            "## ABC-1998 - October Release 2026\n"
            "Folder: `11 Release Documents / 61. Oct Release 2026 / ABC-1998`\n\n"
            "### Files in this folder\n"
            "- Backup files\n"
            "- EQFN\n"
            "- PROD Files\n"
            "- ABC Consolidated SQL_V2.xlsx\n"
            "- Changes done so far.txt\n"
            "- DML's.txt\n"
            "- ETL_Changes.xlsx\n"
            "- Final Data Requirement Updates 8.20.2026.xlsx\n"
            "- Final Data Requirement Updates.xlsx\n"
            "- Table Creation Script.txt\n"
            "- Unit Testing Doc.xlsx\n"
            "- Validation for ABC-1998.txt\n\n"
            "### Companion documents\n"
            "- [ABC-1998 Migration Scope & Areas](/doc/SP-ABC-1998-SCOPE)\n"
            "- [ABC-1998 Components List](/doc/SP-ABC-1998-COMPONENTS)\n"
            "- [ABC-1998 Components (Detailed)](/doc/SP-ABC-1998-COMPONENTS-DETAIL)\n"
            "- [ABC-1998 Changes](/doc/SP-ABC-1998-CHANGES)\n"
            "- [ABC-1998 Comments](/doc/SP-ABC-1998-COMMENTS)\n"
            "- [ABC-1998 Unit Testing Doc](/doc/SP-ABC-1998-UT)\n"
            "- [ABC-1998 Unit Testing (Detailed)](/doc/SP-ABC-1998-UT-DETAIL)\n"
            "- [ABC-1998 OIM Entitlement Register](/doc/SP-ABC-1998-ENTITLEMENTS)"
        ),
    },
    {
        "id": "SP-ABC-1998-SCOPE",
        "title": "ABC - Banking Application Scope, Migration Areas, Project Notes",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Scope.docx",
        "author": "Lohar, Kavita",
        "updated_at": "2026-09-12T09:00:00Z",
        "tags": ["abc", "releases", "oct-2026", "abc-1998", "scope", "migration"],
        "body": (
            "## ABC - Banking Application Scope, Migration Areas, Project Notes\n"
            "October Release 2026 - Ticket ABC-1998.\n\n"
            "### Application scope\n"
            "ABC (Analytics & Business Compliance) covers regulatory analytics, MAS/RBI/APRA "
            "extract generation, and the internal compliance dashboards. This release focuses "
            "on the ETL modernisation slice and prepares the data model for the UBO >=10% BDR.\n\n"
            "### Migration areas\n"
            "- Informatica PowerCenter -> DBT rewrite (in-scope: 6 mappings)\n"
            "- Snowflake curated additions for MAS 610 line 34\n"
            "- Unix scheduler cutover for `PNC_ABC_LOAD_UBO`\n\n"
            "### Project notes\n"
            "- CRQ: CRQ-88230 (already covered by release 2026.09 slot)\n"
            "- Blackout awareness: post month-end - clear window 2026-10-08 to 2026-10-24\n"
            "- Downstream teams: Compliance (Verma), Finance BI (SSM), Reg Reporting"
        ),
    },
    {
        "id": "SP-ABC-1998-COMPONENTS",
        "title": "ABC-1998 - Components List (Migration)",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Components.xlsx",
        "author": "Burger, Hans",
        "updated_at": "2026-09-13T09:00:00Z",
        "tags": ["abc", "releases", "oct-2026", "abc-1998", "components", "informatica", "etl"],
        "body": (
            "## ABC-1998 - Components List\n"
            "The 20 components in scope for the October release migration.\n\n"
            "| # | Component | Area |\n"
            "|---|---|---|\n"
            "| 1 | Informatica PowerCenter Repository | ETL |\n"
            "| 2 | Informatica Integration Service | ETL |\n"
            "| 3 | ETL Workflows | ETL |\n"
            "| 4 | ETL Mappings | ETL |\n"
            "| 5 | ETL Sessions | ETL |\n"
            "| 6 | Parameter Files | ETL |\n"
            "| 7 | Source Connections | ETL |\n"
            "| 8 | Target Connections | ETL |\n"
            "| 9 | Unix Application Server | Unix/Batch |\n"
            "| 10 | Shell Scripts | Unix/Batch |\n"
            "| 11 | Scheduler | Unix/Batch |\n"
            "| 12 | File System | Unix/Batch |\n"
            "| 13 | Database Schemas | Database |\n"
            "| 14 | Stored Procedures | Database |\n"
            "| 15 | DB Links | Database |\n"
            "| 16 | Indexes & Statistics | Database |\n"
            "| 17 | Data Validation | Database |\n"
            "| 18 | Security / Credentials | Security |\n"
            "| 19 | Monitoring & Logging | Ops |\n"
            "| 20 | Testing / Cutover / Rollback | Release |"
        ),
    },
    {
        "id": "SP-ABC-1998-CHANGES",
        "title": "ABC-1998 - Changes",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Changes.txt",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-14T09:00:00Z",
        "tags": ["abc", "releases", "oct-2026", "abc-1998", "changes"],
        "body": (
            "## ABC-1998 - Changes done so far\n"
            "| Component | Change |\n"
            "|---|---|\n"
            "| ETL Mappings | 6 mappings ported from PowerCenter to DBT |\n"
            "| ETL Workflows | Autosys BOX split into 3 smaller BOXes for parallelism |\n"
            "| Parameter Files | Business-date parameter moved into Vault-backed template |\n"
            "| Source Connections | GL CDC connection retargeted to MSK cluster v3 |\n"
            "| Target Connections | Snowflake WH_ETL_L role switched to `ROLE_ABC_ENGINEER` |\n"
            "| Shell Scripts | `run_load_ubo.sh` rewritten with strict-mode + trap |\n"
            "| Stored Procedures | `sp_refresh_mas610_l34` added |\n"
            "| Indexes & Statistics | Composite index on `fct_trading_exposure(product_family, txn_dt)` |\n"
            "| Data Validation | Row-count and null-rate checks in Great Expectations |\n"
            "| Monitoring & Logging | Argus dashboard `abc-1998` published |"
        ),
    },
    {
        "id": "SP-ABC-1998-COMMENTS",
        "title": "ABC-1998 - Comments",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Comments.txt",
        "author": "Verma, Rahul",
        "updated_at": "2026-09-14T09:00:00Z",
        "tags": ["abc", "releases", "oct-2026", "abc-1998", "comments"],
        "body": (
            "## ABC-1998 - Comments\n"
            "| Component | Comment |\n"
            "|---|---|\n"
            "| Informatica Repository | Snapshot backup taken before label promotion. |\n"
            "| ETL Mappings | DBT parity confirmed with 30-day replay. |\n"
            "| Parameter Files | Vault secret rotation window aligned with release T-24h. |\n"
            "| Source Connections | Requires firewall rule review from NetSec (raised INC-2210). |\n"
            "| Stored Procedures | Peer-reviewed by DBA on 2026-09-10. |\n"
            "| DB Links | No new DB links added - re-use of existing FIN_BI link. |\n"
            "| Security / Credentials | Break-glass account documented in Access Guide. |\n"
            "| Testing | UT sheet at UT-001..UT-010 attached. |\n"
            "| Cutover / Rollback | Rollback deployment group prepared and peer-signed. |"
        ),
    },
    {
        "id": "SP-ABC-1998-UT",
        "title": "ABC-1998 - Unit Testing Doc.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Unit-Testing.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-15T09:00:00Z",
        "tags": ["abc", "releases", "oct-2026", "abc-1998", "unit-testing", "ut"],
        "body": (
            "## ABC-1998 - Unit Testing Doc\n"
            "### Summary\n"
            "| Field | Value |\n"
            "|---|---|\n"
            "| Application | ABC |\n"
            "| Release | October Release 2026 |\n"
            "| Testing Type | Unit Testing |\n"
            "| Domain | Banking Application |\n"
            "| Scope | ETL/Informatica, Database, Unix/Batch, impacted regression |\n"
            "| Total Test Cases | 10 |\n"
            "| Pass | 0 |\n"
            "| Fail | 0 |\n"
            "| Blocked | 0 |\n"
            "| Not Executed | 10 |\n"
            "| Tester | Sharma, Anil |\n"
            "| Test Execution Date | (pending) |\n"
            "| Overall Comments | Not Executed |\n\n"
            "### Test cases\n"
            "| Test ID | Area | Test Steps | Expected Result | Test Data / Input | Actual Result | Status | Defect ID | Comments |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| UT-001 | Mapping Validation | Run m_LOAD_UBO with sample slice | Row counts match staging | 500-row extract | - | Not Executed | - | Not Executed |\n"
            "| UT-002 | Transformation Logic | Verify UBO >=10% flag derivation | `disclosed_at_10pct=Y` for 12 rows | Curated fixture | - | Not Executed | - | Not Executed |\n"
            "| UT-003 | Reject Handling | Feed row with null country | Row lands in DLQ, counter +1 | Malformed CSV | - | Not Executed | - | Not Executed |\n"
            "| UT-004 | Stored Procedure / SQL | Exec sp_refresh_mas610_l34 | Refresh completes < 90s | - | - | Not Executed | - | Not Executed |\n"
            "| UT-005 | Data Integrity | GL vs curated row counts | Delta <= 0.1% | T-1 snapshot | - | Not Executed | - | Not Executed |\n"
            "| UT-006 | Script Validation | Run run_load_ubo.sh --dry-run | Exit 0, no side effects | - | - | Not Executed | - | Not Executed |\n"
            "| UT-007 | Error Handling | Kill session mid-run | Autosys retries + alert fires | Simulate SIGTERM | - | Not Executed | - | Not Executed |\n"
            "| UT-008 | End-to-End Unit Flow | Full day slice DEV -> UAT | Tableau extract refreshes green | UAT fixture | - | Not Executed | - | Not Executed |\n"
            "| UT-009 | Unchanged Functionality | Regress fct_gl_txn | Same rowcount as baseline | Baseline extract | - | Not Executed | - | Not Executed |\n"
            "| UT-010 | Volume & Restart Check | Load 10x daily volume, kill, restart | Idempotent, no dup rows | Synthetic 20M rows | - | Not Executed | - | Not Executed |"
        ),
    },

    # -----------------------------------------------------------------
    # EPM-1998 - Oct Release 2026
    # -----------------------------------------------------------------
    {
        "id": "SP-EPM-1998-INDEX",
        "title": "11 Release Documents / 61. Oct Release 2026 / EPM-1998",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/",
        "author": "Menon, Priya",
        "updated_at": "2026-09-15T09:00:00Z",
        "tags": ["epm", "releases", "oct-2026", "epm-1998", "index"],
        "body": (
            "## EPM-1998 - October Release 2026\n"
            "Folder: `11 Release Documents / 61. Oct Release 2026 / EPM-1998`\n\n"
            "### Files in this folder\n"
            "- Backup files\n"
            "- EQFN\n"
            "- PROD Files\n"
            "- EPM Consolidated SQL_V2.xlsx\n"
            "- Changes done so far.txt\n"
            "- DML's.txt\n"
            "- ETL_Changes.xlsx\n"
            "- Final Data Requirement Updates 8.20.2026.xlsx\n"
            "- Final Data Requirement Updates.xlsx\n"
            "- Table Creation Script.txt\n"
            "- Unit Testing Doc.xlsx\n"
            "- Validation for EPM-1998.txt\n\n"
            "### Companion documents\n"
            "- [EPM-1998 Migration Scope & Areas](/doc/SP-EPM-1998-SCOPE)\n"
            "- [EPM-1998 Components List](/doc/SP-EPM-1998-COMPONENTS)\n"
            "- [EPM-1998 Components (Detailed)](/doc/SP-EPM-1998-COMPONENTS-DETAIL)\n"
            "- [EPM-1998 Changes](/doc/SP-EPM-1998-CHANGES)\n"
            "- [EPM-1998 Comments](/doc/SP-EPM-1998-COMMENTS)\n"
            "- [EPM-1998 Unit Testing Doc](/doc/SP-EPM-1998-UT)\n"
            "- [EPM-1998 Unit Testing (Detailed)](/doc/SP-EPM-1998-UT-DETAIL)\n"
            "- [EPM-1998 OIM Entitlement Register](/doc/SP-EPM-1998-ENTITLEMENTS)"
        ),
    },
    {
        "id": "SP-EPM-1998-SCOPE",
        "title": "EPM - Banking Application Scope, Migration Areas, Project Notes",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Scope.docx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-12T09:00:00Z",
        "tags": ["epm", "releases", "oct-2026", "epm-1998", "scope", "migration"],
        "body": (
            "## EPM - Banking Application Scope, Migration Areas, Project Notes\n"
            "October Release 2026 - Ticket EPM-1998.\n\n"
            "### Application scope\n"
            "EPM (Enterprise Performance Management) covers management-reporting cubes, board "
            "pack generation, and cost-allocation models used by Finance leadership. This "
            "release adjusts the cube refresh window and adds a new profitability grain.\n\n"
            "### Migration areas\n"
            "- Cube refresh moved from 03:00 to 02:00 SGT (30-min headroom vs SLA)\n"
            "- Snowflake mart addition: `mart.epm.profitability_by_desk_daily`\n"
            "- Unix cron cutover for `PNC_EPM_CUBE_REFRESH`\n\n"
            "### Project notes\n"
            "- Board pack cadence unaffected; watch for Nov 14 board meeting\n"
            "- Downstream: Finance leadership, Board Sec, Cost Allocation working group"
        ),
    },
    {
        "id": "SP-EPM-1998-COMPONENTS",
        "title": "EPM-1998 - Components List (Migration)",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Components.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-13T09:00:00Z",
        "tags": ["epm", "releases", "oct-2026", "epm-1998", "components", "informatica", "etl"],
        "body": (
            "## EPM-1998 - Components List\n"
            "The 20 components in scope for the October release migration.\n\n"
            "| # | Component | Area |\n"
            "|---|---|---|\n"
            "| 1 | Informatica PowerCenter Repository | ETL |\n"
            "| 2 | Informatica Integration Service | ETL |\n"
            "| 3 | ETL Workflows | ETL |\n"
            "| 4 | ETL Mappings | ETL |\n"
            "| 5 | ETL Sessions | ETL |\n"
            "| 6 | Parameter Files | ETL |\n"
            "| 7 | Source Connections | ETL |\n"
            "| 8 | Target Connections | ETL |\n"
            "| 9 | Unix Application Server | Unix/Batch |\n"
            "| 10 | Shell Scripts | Unix/Batch |\n"
            "| 11 | Scheduler | Unix/Batch |\n"
            "| 12 | File System | Unix/Batch |\n"
            "| 13 | Database Schemas | Database |\n"
            "| 14 | Stored Procedures | Database |\n"
            "| 15 | DB Links | Database |\n"
            "| 16 | Indexes & Statistics | Database |\n"
            "| 17 | Data Validation | Database |\n"
            "| 18 | Security / Credentials | Security |\n"
            "| 19 | Monitoring & Logging | Ops |\n"
            "| 20 | Testing / Cutover / Rollback | Release |"
        ),
    },
    {
        "id": "SP-EPM-1998-CHANGES",
        "title": "EPM-1998 - Changes",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Changes.txt",
        "author": "Menon, Priya",
        "updated_at": "2026-09-14T09:00:00Z",
        "tags": ["epm", "releases", "oct-2026", "epm-1998", "changes"],
        "body": (
            "## EPM-1998 - Changes done so far\n"
            "| Component | Change |\n"
            "|---|---|\n"
            "| ETL Mappings | New mapping m_LOAD_PROFIT_BY_DESK added |\n"
            "| ETL Workflows | Cube-refresh BOX rescheduled to 02:00 SGT |\n"
            "| Parameter Files | New `desk_grain` param exposed |\n"
            "| Target Connections | New Snowflake target `MART_EPM` |\n"
            "| Stored Procedures | `sp_epm_reallocate_cost_v3` deployed |\n"
            "| Indexes & Statistics | New index on `profitability_by_desk_daily(desk_id, business_dt)` |\n"
            "| Monitoring & Logging | Argus SLA alert `epm-cube-refresh-04-30` armed |\n"
            "| Testing | UT sheet UT-001..UT-010 prepared |"
        ),
    },
    {
        "id": "SP-EPM-1998-COMMENTS",
        "title": "EPM-1998 - Comments",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Comments.txt",
        "author": "Menon, Priya",
        "updated_at": "2026-09-14T09:00:00Z",
        "tags": ["epm", "releases", "oct-2026", "epm-1998", "comments"],
        "body": (
            "## EPM-1998 - Comments\n"
            "| Component | Comment |\n"
            "|---|---|\n"
            "| Cube-refresh window | Coordinated with SRE; no overlap with fx-service maintenance. |\n"
            "| Cost allocation SP | Reviewed by Finance CDO on 2026-09-11. |\n"
            "| New mart | Row-access policy scoped to `ROLE_EPM_READER`. |\n"
            "| Board pack | No board pack impact until 2026-11-14 cycle. |\n"
            "| Rollback | Cube snapshot retained for T+7 days post-cutover. |"
        ),
    },
    {
        "id": "SP-EPM-1998-UT",
        "title": "EPM-1998 - Unit Testing Doc.xlsx",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Unit-Testing.xlsx",
        "author": "Menon, Priya",
        "updated_at": "2026-09-15T09:00:00Z",
        "tags": ["epm", "releases", "oct-2026", "epm-1998", "unit-testing", "ut"],
        "body": (
            "## EPM-1998 - Unit Testing Doc\n"
            "### Summary\n"
            "| Field | Value |\n"
            "|---|---|\n"
            "| Application | EPM |\n"
            "| Release | October Release 2026 |\n"
            "| Testing Type | Unit Testing |\n"
            "| Domain | Banking Application |\n"
            "| Scope | ETL/Informatica, Database, Unix/Batch, impacted regression |\n"
            "| Total Test Cases | 10 |\n"
            "| Pass | 0 |\n"
            "| Fail | 0 |\n"
            "| Blocked | 0 |\n"
            "| Not Executed | 10 |\n"
            "| Tester | Menon, Priya |\n"
            "| Test Execution Date | (pending) |\n"
            "| Overall Comments | Not Executed |\n\n"
            "### Test cases\n"
            "| Test ID | Area | Test Steps | Expected Result | Test Data / Input | Actual Result | Status | Defect ID | Comments |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| UT-001 | Mapping Validation | Run m_LOAD_PROFIT_BY_DESK with slice | Row count matches staging | 1000-row fixture | - | Not Executed | - | Not Executed |\n"
            "| UT-002 | Transformation Logic | Verify desk-level P&L rollup | Sum equals fct_gl_txn total | T-1 slice | - | Not Executed | - | Not Executed |\n"
            "| UT-003 | Reject Handling | Feed unknown desk_id | Row lands in DLQ | Bad-desk CSV | - | Not Executed | - | Not Executed |\n"
            "| UT-004 | Stored Procedure / SQL | Exec sp_epm_reallocate_cost_v3 | Completes < 3 min | - | - | Not Executed | - | Not Executed |\n"
            "| UT-005 | Data Integrity | Cube total vs mart total | Delta = 0 | T-1 slice | - | Not Executed | - | Not Executed |\n"
            "| UT-006 | Script Validation | Cron run_cube_refresh.sh dry-run | Exit 0 | - | - | Not Executed | - | Not Executed |\n"
            "| UT-007 | Error Handling | Kill mid-cube-refresh | Alert fires; auto-restart | Simulate SIGKILL | - | Not Executed | - | Not Executed |\n"
            "| UT-008 | End-to-End Unit Flow | Full slice DEV -> UAT | Board pack extract green | UAT fixture | - | Not Executed | - | Not Executed |\n"
            "| UT-009 | Unchanged Functionality | Regress existing cube measures | Match baseline | Baseline extract | - | Not Executed | - | Not Executed |\n"
            "| UT-010 | Volume & Restart Check | 5x volume, kill, restart | Idempotent, no dup rows | Synthetic 5M rows | - | Not Executed | - | Not Executed |"
        ),
    },

    # -----------------------------------------------------------------
    # SSM-1998 - Oct Release 2026
    # -----------------------------------------------------------------
    {
        "id": "SP-SSM-1998-INDEX",
        "title": "11 Release Documents / 61. Oct Release 2026 / SSM-1998",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-15T09:00:00Z",
        "tags": ["ssm", "releases", "oct-2026", "ssm-1998", "index"],
        "body": (
            "## SSM-1998 - October Release 2026\n"
            "Folder: `11 Release Documents / 61. Oct Release 2026 / SSM-1998`\n\n"
            "### Files in this folder\n"
            "- Backup files\n"
            "- EQFN\n"
            "- PROD Files\n"
            "- SSM Consolidated SQL_V2.xlsx\n"
            "- Changes done so far.txt\n"
            "- DML's.txt\n"
            "- ETL_Changes.xlsx\n"
            "- Final Data Requirement Updates 8.20.2026.xlsx\n"
            "- Final Data Requirement Updates.xlsx\n"
            "- Table Creation Script.txt\n"
            "- Unit Testing Doc.xlsx\n"
            "- Validation for SSM-1998.txt\n\n"
            "### Companion documents\n"
            "- [SSM-1998 Migration Scope & Areas](/doc/SP-SSM-1998-SCOPE)\n"
            "- [SSM-1998 Components List](/doc/SP-SSM-1998-COMPONENTS)\n"
            "- [SSM-1998 Components (Detailed)](/doc/SP-SSM-1998-COMPONENTS-DETAIL)\n"
            "- [SSM-1998 Changes](/doc/SP-SSM-1998-CHANGES)\n"
            "- [SSM-1998 Comments](/doc/SP-SSM-1998-COMMENTS)\n"
            "- [SSM-1998 Unit Testing Doc](/doc/SP-SSM-1998-UT)\n"
            "- [SSM-1998 Unit Testing (Detailed)](/doc/SP-SSM-1998-UT-DETAIL)\n"
            "- [SSM-1998 OIM Entitlement Register](/doc/SP-SSM-1998-ENTITLEMENTS)"
        ),
    },
    {
        "id": "SP-SSM-1998-SCOPE",
        "title": "SSM - Banking Application Scope, Migration Areas, Project Notes",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Scope.docx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-12T09:00:00Z",
        "tags": ["ssm", "releases", "oct-2026", "ssm-1998", "scope", "migration"],
        "body": (
            "## SSM - Banking Application Scope, Migration Areas, Project Notes\n"
            "October Release 2026 - Ticket SSM-1998.\n\n"
            "### Application scope\n"
            "SSM (Shared Services & Migration) owns cross-domain services and the hosting/ETL "
            "migration workstreams. This release lands the first UCP -> ENT Wave 2 slice and "
            "retires the Teradata read replica in favour of Snowflake.\n\n"
            "### Migration areas\n"
            "- UCP -> ENT hosting cutover (Wave 2, 4 apps)\n"
            "- Teradata read replica decommissioned; Snowflake share promoted\n"
            "- Unix batch jobs re-parented from Autosys legacy calendar to new template\n\n"
            "### Project notes\n"
            "- CRQ: CRQ-89055 (needs CAB sign-off T-5)\n"
            "- Downstream: every consuming team - broad-comms sent 2026-09-10\n"
            "- Rollback: full ENT deprovision + Autosys revert JIL prepared"
        ),
    },
    {
        "id": "SP-SSM-1998-COMPONENTS",
        "title": "SSM-1998 - Components List (Migration)",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Components.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-13T09:00:00Z",
        "tags": ["ssm", "releases", "oct-2026", "ssm-1998", "components", "informatica", "etl"],
        "body": (
            "## SSM-1998 - Components List\n"
            "The 20 components in scope for the October release migration.\n\n"
            "| # | Component | Area |\n"
            "|---|---|---|\n"
            "| 1 | Informatica PowerCenter Repository | ETL |\n"
            "| 2 | Informatica Integration Service | ETL |\n"
            "| 3 | ETL Workflows | ETL |\n"
            "| 4 | ETL Mappings | ETL |\n"
            "| 5 | ETL Sessions | ETL |\n"
            "| 6 | Parameter Files | ETL |\n"
            "| 7 | Source Connections | ETL |\n"
            "| 8 | Target Connections | ETL |\n"
            "| 9 | Unix Application Server | Unix/Batch |\n"
            "| 10 | Shell Scripts | Unix/Batch |\n"
            "| 11 | Scheduler | Unix/Batch |\n"
            "| 12 | File System | Unix/Batch |\n"
            "| 13 | Database Schemas | Database |\n"
            "| 14 | Stored Procedures | Database |\n"
            "| 15 | DB Links | Database |\n"
            "| 16 | Indexes & Statistics | Database |\n"
            "| 17 | Data Validation | Database |\n"
            "| 18 | Security / Credentials | Security |\n"
            "| 19 | Monitoring & Logging | Ops |\n"
            "| 20 | Testing / Cutover / Rollback | Release |"
        ),
    },
    {
        "id": "SP-SSM-1998-CHANGES",
        "title": "SSM-1998 - Changes",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Changes.txt",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-14T09:00:00Z",
        "tags": ["ssm", "releases", "oct-2026", "ssm-1998", "changes"],
        "body": (
            "## SSM-1998 - Changes done so far\n"
            "| Component | Change |\n"
            "|---|---|\n"
            "| Unix Application Server | 4 apps re-hosted from UCP to ENT |\n"
            "| Scheduler | Autosys calendars migrated to new template `PNC_ENT_STD_V2` |\n"
            "| Shell Scripts | `env_bootstrap.sh` refactored for ENT paths |\n"
            "| File System | NFS mounts remapped to `/apps/ent/*` |\n"
            "| Database Schemas | Teradata read replica retired; Snowflake share promoted |\n"
            "| DB Links | Legacy Teradata DB link removed |\n"
            "| Security / Credentials | Vault namespace switched to `secret/ssm/ent/*` |\n"
            "| Monitoring & Logging | Splunk index alias `ssm-ent` added |\n"
            "| Testing | UT sheet UT-001..UT-010 attached |\n"
            "| Cutover / Rollback | Rollback JIL and Autosys revert playbook prepared |"
        ),
    },
    {
        "id": "SP-SSM-1998-COMMENTS",
        "title": "SSM-1998 - Comments",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Comments.txt",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-14T09:00:00Z",
        "tags": ["ssm", "releases", "oct-2026", "ssm-1998", "comments"],
        "body": (
            "## SSM-1998 - Comments\n"
            "| Component | Comment |\n"
            "|---|---|\n"
            "| UCP -> ENT | Wave 2 covers 4 apps; Wave 3 pushed to Nov release. |\n"
            "| Teradata retirement | Confirm no consumer still reading from replica (see Splunk audit). |\n"
            "| Autosys template | Peer-reviewed by Autosys admins on 2026-09-11. |\n"
            "| Vault namespace | Credential rotation completed 2026-09-12. |\n"
            "| Testing | Cross-team regression coordinated with ABC and EPM leads. |\n"
            "| Cutover / Rollback | CAB briefing scheduled for 2026-09-24. |"
        ),
    },
    {
        "id": "SP-SSM-1998-UT",
        "title": "SSM-1998 - Unit Testing Doc.xlsx",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Unit-Testing.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-15T09:00:00Z",
        "tags": ["ssm", "releases", "oct-2026", "ssm-1998", "unit-testing", "ut"],
        "body": (
            "## SSM-1998 - Unit Testing Doc\n"
            "### Summary\n"
            "| Field | Value |\n"
            "|---|---|\n"
            "| Application | SSM |\n"
            "| Release | October Release 2026 |\n"
            "| Testing Type | Unit Testing |\n"
            "| Domain | Banking Application |\n"
            "| Scope | ETL/Informatica, Database, Unix/Batch, impacted regression |\n"
            "| Total Test Cases | 10 |\n"
            "| Pass | 0 |\n"
            "| Fail | 0 |\n"
            "| Blocked | 0 |\n"
            "| Not Executed | 10 |\n"
            "| Tester | Sharma, Anil |\n"
            "| Test Execution Date | (pending) |\n"
            "| Overall Comments | Not Executed |\n\n"
            "### Test cases\n"
            "| Test ID | Area | Test Steps | Expected Result | Test Data / Input | Actual Result | Status | Defect ID | Comments |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| UT-001 | Mapping Validation | Re-point mapping to ENT source | Row count parity | Wave-2 fixture | - | Not Executed | - | Not Executed |\n"
            "| UT-002 | Transformation Logic | Verify env-agnostic path lookup | Path resolves under `/apps/ent` | ENT env | - | Not Executed | - | Not Executed |\n"
            "| UT-003 | Reject Handling | Feed missing param file | Session fails fast + alert | Missing PARAMS | - | Not Executed | - | Not Executed |\n"
            "| UT-004 | Stored Procedure / SQL | Exec against Snowflake share | Same output as Teradata baseline | Baseline slice | - | Not Executed | - | Not Executed |\n"
            "| UT-005 | Data Integrity | Cross-check ENT vs UCP totals | Delta = 0 | T-1 slice | - | Not Executed | - | Not Executed |\n"
            "| UT-006 | Script Validation | Run env_bootstrap.sh --check | Exit 0 | - | - | Not Executed | - | Not Executed |\n"
            "| UT-007 | Error Handling | Bad Vault path | Fail fast, do not log secret | Simulate 403 | - | Not Executed | - | Not Executed |\n"
            "| UT-008 | End-to-End Unit Flow | Full app slice UCP -> ENT | Downstream jobs green | Wave-2 fixture | - | Not Executed | - | Not Executed |\n"
            "| UT-009 | Unchanged Functionality | Regress non-migrated jobs | Match baseline | Baseline extract | - | Not Executed | - | Not Executed |\n"
            "| UT-010 | Volume & Restart Check | 2x nightly volume, restart | Idempotent, no dup rows | Synthetic 40M rows | - | Not Executed | - | Not Executed |"
        ),
    },

    # ================================================================
    # October Release 2026 - deep-detail companion docs for the demo:
    #   * Detailed Unit Testing (30 cases per app, tester + timings)
    #   * OIM Entitlement Register (Role display / description / requestable / app instance)
    #   * Migration Components - Detailed (per-component owner / cutover / rollback)
    # ================================================================

    # -----------------------------------------------------------------
    # ABC-1998 - Detailed Unit Testing
    # -----------------------------------------------------------------
    {
        "id": "SP-ABC-1998-UT-DETAIL",
        "title": "ABC-1998 - Unit Testing (Detailed) - October 2026.xlsx",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Unit-Testing-Detailed.xlsx",
        "author": "Sharma, Anil",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "abc", "releases", "oct-2026", "abc-1998",
            "unit-testing", "ut", "detailed", "qa",
        ],
        "body": (
            "## ABC-1998 - Detailed Unit Testing Doc\n"
            "This sheet is the extended UT for the October release. It supersedes the\n"
            "10-row summary sheet (see [ABC-1998 Unit Testing Doc](/doc/SP-ABC-1998-UT)).\n\n"
            "### Summary\n"
            "| Field | Value |\n"
            "|---|---|\n"
            "| Application | ABC (Analytics & Business Compliance) |\n"
            "| Release | October Release 2026 |\n"
            "| Ticket | ABC-1998 |\n"
            "| Testing Type | Unit Testing (Detailed) |\n"
            "| Environment | DEV -> UAT (fixture data) |\n"
            "| Scope | ETL/Informatica, DBT rewrite, Stored Procs, Batch, Regression |\n"
            "| Total Test Cases | 30 |\n"
            "| Pass | 22 |\n"
            "| Fail | 3 |\n"
            "| Blocked | 2 |\n"
            "| Not Executed | 3 |\n"
            "| Lead Tester | Sharma, Anil |\n"
            "| Peer Reviewer | Verma, Rahul |\n"
            "| Execution Window | 2026-09-14 to 2026-09-16 |\n"
            "| Overall Comments | 3 fails traced to fixture drift; retest scheduled 2026-09-18 |\n\n"
            "### Area coverage\n"
            "| Area | Cases | Pass | Fail | Blocked | Not Exec |\n"
            "|---|---|---|---|---|---|\n"
            "| Mapping Validation (Informatica) | 6 | 5 | 1 | 0 | 0 |\n"
            "| DBT Model Parity | 5 | 4 | 1 | 0 | 0 |\n"
            "| Transformation Logic | 4 | 3 | 0 | 1 | 0 |\n"
            "| Stored Procedure / SQL | 4 | 3 | 1 | 0 | 0 |\n"
            "| Reject / DLQ Handling | 3 | 2 | 0 | 1 | 0 |\n"
            "| Batch & Scheduling | 3 | 2 | 0 | 0 | 1 |\n"
            "| Data Integrity | 3 | 2 | 0 | 0 | 1 |\n"
            "| Volume / Restart | 2 | 1 | 0 | 0 | 1 |\n\n"
            "### Test cases\n"
            "| Test ID | Area | Test Steps | Expected Result | Test Data | Actual Result | Status | Defect ID | Executed By | Duration |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| UT-D-001 | Mapping Validation | Run m_LOAD_UBO with 500-row sample | Row counts match staging | GL slice 2026-09-01 | Match | Pass | - | Sharma | 42s |\n"
            "| UT-D-002 | Mapping Validation | Run m_LOAD_UBO with null country | Rows land in DLQ, counter +1 | Malformed CSV | Match | Pass | - | Sharma | 18s |\n"
            "| UT-D-003 | Mapping Validation | Run m_LOAD_CTPY with duplicate keys | Reject with UNIQUE_KEY_VIOL | Synthetic dup | Match | Pass | - | Sharma | 25s |\n"
            "| UT-D-004 | Mapping Validation | Run m_LOAD_TXN with 100k rows | Loads under 90s | GL 2026-08-30 | 132s | Fail | DEF-3120 | Verma | 132s |\n"
            "| UT-D-005 | Mapping Validation | Restart mid-session | Idempotent, no dup rows | SIGTERM at 60% | Match | Pass | - | Sharma | 84s |\n"
            "| UT-D-006 | Mapping Validation | End-to-end DEV -> UAT | All curated tables refresh | Full day slice | Match | Pass | - | Sharma | 12m |\n"
            "| UT-D-007 | DBT Model Parity | dim_customer parity vs Informatica | Delta = 0 | 30-day replay | Match | Pass | - | Verma | 4m |\n"
            "| UT-D-008 | DBT Model Parity | fct_trading_exposure parity | Delta = 0 | 30-day replay | Match | Pass | - | Verma | 6m |\n"
            "| UT-D-009 | DBT Model Parity | fct_gl_txn parity | Delta = 0 | 30-day replay | Match | Pass | - | Verma | 5m |\n"
            "| UT-D-010 | DBT Model Parity | dim_product_family parity | Delta = 0 | 30-day replay | +2 rows | Fail | DEF-3121 | Verma | 3m |\n"
            "| UT-D-011 | DBT Model Parity | fct_ubo_holding parity | Delta = 0 | 30-day replay | Match | Pass | - | Verma | 5m |\n"
            "| UT-D-012 | Transformation Logic | UBO >=10% flag derivation | 12 rows flagged | Curated fixture | 12 flagged | Pass | - | Sharma | 8s |\n"
            "| UT-D-013 | Transformation Logic | MAS 610 L34 aggregation | 4 rows per product_family | UAT slice | 4 rows | Pass | - | Sharma | 22s |\n"
            "| UT-D-014 | Transformation Logic | Currency FX at cutoff time | FX matches SOD rate | Rates 2026-08-30 | Match | Pass | - | Sharma | 6s |\n"
            "| UT-D-015 | Transformation Logic | Effective-date joins vs point-in-time | Point-in-time correct | AS-OF fixture | - | Blocked | BLK-540 | - | - |\n"
            "| UT-D-016 | Stored Procedure / SQL | sp_refresh_mas610_l34 | Refresh completes < 90s | - | 71s | Pass | - | Verma | 71s |\n"
            "| UT-D-017 | Stored Procedure / SQL | sp_apply_ubo_flag | Flag set for 12 rows | Fixture | 12 rows | Pass | - | Verma | 14s |\n"
            "| UT-D-018 | Stored Procedure / SQL | sp_reconcile_gl_txn | Zero delta | T-1 slice | 4 rows off | Fail | DEF-3122 | Verma | 55s |\n"
            "| UT-D-019 | Stored Procedure / SQL | sp_purge_stale_ubo | Purges > 400d rows | Historical fixture | Match | Pass | - | Verma | 9s |\n"
            "| UT-D-020 | Reject / DLQ Handling | Bad country ISO | Row -> DLQ, alert fires | Malformed CSV | Match | Pass | - | Sharma | 12s |\n"
            "| UT-D-021 | Reject / DLQ Handling | Missing party_id | Row -> DLQ, counter +1 | Malformed CSV | Match | Pass | - | Sharma | 10s |\n"
            "| UT-D-022 | Reject / DLQ Handling | DLQ replay CLI | Replayed rows land curated | DLQ snapshot | - | Blocked | BLK-541 | - | - |\n"
            "| UT-D-023 | Batch & Scheduling | Autosys BOX cascade | 3 children fire in order | - | Match | Pass | - | Sharma | 4m |\n"
            "| UT-D-024 | Batch & Scheduling | Autosys hold + release | Held job resumes | - | Match | Pass | - | Sharma | 90s |\n"
            "| UT-D-025 | Batch & Scheduling | Calendar rollover (month-end) | Runs on last-biz-day | Simulated 2026-10-31 | - | Not Executed | - | - | - |\n"
            "| UT-D-026 | Data Integrity | Row counts GL vs curated | Delta <= 0.1% | T-1 snapshot | Match | Pass | - | Verma | 2m |\n"
            "| UT-D-027 | Data Integrity | Null-rate check | No new nulls | T-1 snapshot | Match | Pass | - | Verma | 90s |\n"
            "| UT-D-028 | Data Integrity | FK integrity fct -> dim | 0 orphans | T-1 snapshot | - | Not Executed | - | - | - |\n"
            "| UT-D-029 | Volume / Restart | 10x nightly, kill, restart | Idempotent, no dup rows | Synthetic 20M | Match | Pass | - | Sharma | 22m |\n"
            "| UT-D-030 | Volume / Restart | 20x nightly, cold restart | No cluster panic | Synthetic 40M | - | Not Executed | - | - | - |\n\n"
            "### Defect log\n"
            "| Defect ID | Test | Severity | Owner | Status |\n"
            "|---|---|---|---|---|\n"
            "| DEF-3120 | UT-D-004 | S3 (performance) | Burger | Investigating - index missing on `product_family` |\n"
            "| DEF-3121 | UT-D-010 | S3 (data) | Verma | Fixture drift - dim_product_family had 2 stale rows |\n"
            "| DEF-3122 | UT-D-018 | S2 (reconciliation) | Verma | Root cause in `sp_reconcile_gl_txn` currency rounding |\n\n"
            "### Sign-offs\n"
            "- Lead Tester: **Sharma, Anil** (2026-09-16)\n"
            "- Peer Reviewer: **Verma, Rahul** (pending retest)\n"
            "- Delivery Lead: **Lohar, Kavita** (pending)"
        ),
    },

    # -----------------------------------------------------------------
    # ABC-1998 - OIM Entitlement Register
    # -----------------------------------------------------------------
    {
        "id": "SP-ABC-1998-ENTITLEMENTS",
        "title": "ABC-1998 - OIM Entitlement Register - October 2026.xlsx",
        "author": "Verma, Rahul",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Entitlements.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "abc", "releases", "oct-2026", "abc-1998",
            "entitlements", "oim", "access", "roles", "sod",
        ],
        "body": (
            "## ABC-1998 - OIM Entitlement Register\n"
            "Access model for the ABC application (Analytics & Business Compliance).\n"
            "Requests raise via **OIM Access Portal** -> app instance `ABC-PROD` /\n"
            "`ABC-UAT`. All Tier-1 roles require Delivery Lead + InfoSec approval.\n\n"
            "### Register\n"
            "| OIM Entitlement / Role Display Name | Description | Requestable | App Instance |\n"
            "|---|---|---|---|\n"
            "| ABC_ANALYST_RO | Read-only on curated ABC schemas in Snowflake (`SF_ABC_CURATED_*`). Analyst self-service. | Yes | ABC-PROD |\n"
            "| ABC_ANALYST_RW | Read/write on curated ABC schemas. Peer review required for DDL. | Yes | ABC-PROD |\n"
            "| ABC_COMPLIANCE_STEWARD | Elevated read on `fct_ubo_holding`, `fct_trading_exposure`. Compliance stewards only. | Yes | ABC-PROD |\n"
            "| ABC_COMPLIANCE_STEWARD_UAT | UAT twin of the compliance steward role. | Yes | ABC-UAT |\n"
            "| ABC_ETL_DEV | DBT + Informatica developer role. RW on `SF_ABC_STAGING_*` + repo push to `abc-etl`. | Yes | ABC-UAT |\n"
            "| ABC_ETL_SUPPORT | On-call troubleshooting - read logs, restart Autosys jobs, run job holds. | Yes | ABC-PROD |\n"
            "| ABC_DBA_RO | DDL viewer + query profile access on Snowflake WH_ETL_L / WH_ADHOC_S. | Yes | ABC-PROD |\n"
            "| ABC_DBA_ADMIN | Full DBA - schema owner, warehouse resize, resource monitors. Tier-1. | No | ABC-PROD |\n"
            "| ABC_TABLEAU_VIEWER | View executive Tableau dashboards under `ABC/Executive`. | Yes | TABLEAU-PROD |\n"
            "| ABC_TABLEAU_PUBLISHER | Publish/edit dashboards under `ABC/*`. | Yes | TABLEAU-PROD |\n"
            "| ABC_MAS610_APPROVER | Sign-off on MAS 610 L34 extract before submission. Segregated from developer role. | No | ABC-PROD |\n"
            "| ABC_ADHOC_REQUESTOR | File ADHOC requests via `SSM-ADHOC` intake. | Yes | SSM-ADHOC |\n"
            "| ABC_BREAK_GLASS | Time-boxed prod DDL - 4h auto-revoke, dual-approval, logged. Tier-1. | No | ABC-PROD |\n"
            "| ABC_SUPPORT_READ | Support engineer read on curated + audit logs. | Yes | ABC-PROD |\n"
            "| ABC_AUDIT_READ | Auditor role - read on `AUDIT_LOG_*` and lineage catalog. | Yes | ABC-PROD |\n\n"
            "### SoD (segregation of duties) conflicts\n"
            "| Role A | Conflicts with | Reason |\n"
            "|---|---|---|\n"
            "| ABC_ETL_DEV | ABC_MAS610_APPROVER | Developer cannot approve their own extract. |\n"
            "| ABC_DBA_ADMIN | ABC_COMPLIANCE_STEWARD | DBA cannot self-approve steward view. |\n"
            "| ABC_BREAK_GLASS | ABC_ANALYST_RW | Break-glass is time-boxed; standard write must be revoked first. |\n\n"
            "### Ownership & approval\n"
            "| Role | Owner | Approver | Review Cadence |\n"
            "|---|---|---|---|\n"
            "| ABC_ANALYST_* | Lohar, Kavita | Delivery Lead | Quarterly |\n"
            "| ABC_ETL_* | Burger, Hans | Delivery Lead + Peer | Quarterly |\n"
            "| ABC_COMPLIANCE_STEWARD | Verma, Rahul | InfoSec + Compliance | Quarterly |\n"
            "| ABC_DBA_ADMIN | Burger, Hans | InfoSec (Tier-1) | Monthly |\n"
            "| ABC_BREAK_GLASS | Lohar, Kavita | InfoSec (Tier-1) | Per use |\n\n"
            "### Notes\n"
            "- All requests flow through the OIM Access Portal - do not raise SNOW tickets directly.\n"
            "- Tier-1 (`Requestable: No`) roles are provisioned only via change-controlled JIT flow (see [Access & Entitlements](/doc/CONF-ONB-ACCESS-002)).\n"
            "- Recertification runs the first Friday of each quarter."
        ),
    },

    # -----------------------------------------------------------------
    # ABC-1998 - Migration Components (Detailed)
    # -----------------------------------------------------------------
    {
        "id": "SP-ABC-1998-COMPONENTS-DETAIL",
        "title": "ABC-1998 - Migration Components (Detailed) - October 2026.xlsx",
        "author": "Burger, Hans",
        "url": "https://sharepoint.bank.internal/sites/ABC/Releases/Oct-2026/ABC-1998/Components-Detailed.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "abc", "releases", "oct-2026", "abc-1998",
            "components", "migration", "informatica", "etl", "detailed",
        ],
        "body": (
            "## ABC-1998 - Migration Components (Detailed)\n"
            "Deep-detail companion to the 20-row summary at\n"
            "[ABC-1998 Components List](/doc/SP-ABC-1998-COMPONENTS). Each row here\n"
            "carries owner, downstream impact, cutover window, and rollback trigger.\n\n"
            "### Per-component detail\n"
            "| # | Component | Area | From | To | Owner | Downstream Impact | Cutover Window | Rollback Trigger |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| 1 | Informatica PowerCenter Repository | ETL | PC 10.4 (Linux) | Repository label `ABC_1998` | Burger | ETL Dev team | T-24h freeze | Restore label `ABC_PRE_1998` |\n"
            "| 2 | Informatica Integration Service | ETL | IS `IS_ABC_01` | IS `IS_ABC_02` (new node) | Burger | Autosys BOX | T-4h switch | Autosys revert JIL |\n"
            "| 3 | ETL Workflows (Autosys BOX) | ETL | `abc_daily_box` (single) | 3 child BOXes | Sharma | Reg Reporting | T0 window | Revert `abc_daily_box.jil` |\n"
            "| 4 | ETL Mappings (Informatica -> DBT) | ETL | 6 PowerCenter mappings | DBT models `abc.*` | Burger | Curated schemas | Included in T0 | Point DBT profile at `PRE` |\n"
            "| 5 | ETL Sessions | ETL | 12 sessions | Autotuned pool | Burger | Batch SLA | T-2h test-run | Retire new sessions |\n"
            "| 6 | Parameter Files | ETL | Flat `.prm` on NFS | Vault-templated | Verma | Session bootstrap | T-8h | Restore NFS `.prm` |\n"
            "| 7 | Source Connections | ETL | GL DB (jdbc) | MSK v3 CDC topic | Sharma | Realtime feeds | T-1h validation | Fail back to jdbc |\n"
            "| 8 | Target Connections | ETL | Snowflake WH_ETL_L (RO) | WH_ETL_L (RW via `ROLE_ABC_ENGINEER`) | Burger | Curated tables | T0 | Revert role grant |\n"
            "| 9 | Unix Application Server | Unix/Batch | ETL app node `abc01` | Rehosted on `abc02` (ENT) | Sharma | Batch, ADHOC | T-3h | DNS revert |\n"
            "| 10 | Shell Scripts | Unix/Batch | `run_load_ubo.sh` (unhardened) | Strict-mode + trap | Sharma | Autosys job | T0 | Restore prior script |\n"
            "| 11 | Scheduler | Unix/Batch | Autosys `PNC_STD_V1` cal | `PNC_ENT_STD_V2` cal | Sharma | Every child job | T-24h JIL swap | Restore `V1` JIL |\n"
            "| 12 | File System | Unix/Batch | `/apps/abc` (legacy) | `/apps/ent/abc` | Sharma | Log paths, drops | T-6h symlink | Symlink revert |\n"
            "| 13 | Database Schemas | Database | Snowflake `SF_ABC_CURATED_V1` | `SF_ABC_CURATED_V2` | Burger | All BI consumers | T-2h clone | Alias swap back |\n"
            "| 14 | Stored Procedures | Database | 4 existing | +2 new (`sp_refresh_mas610_l34`, `sp_apply_ubo_flag`) | Verma | Reg Reporting | Included in T0 | Drop new SPs |\n"
            "| 15 | DB Links | Database | FIN_BI link (reused) | (unchanged) | - | Finance BI | n/a | n/a |\n"
            "| 16 | Indexes & Statistics | Database | Missing on `product_family` | Composite `(product_family, txn_dt)` | Burger | Query perf | T-1h ANALYZE | Drop new index |\n"
            "| 17 | Data Validation | Database | Row-count only | Great Expectations suite | Verma | QA gate | T-30m | Skip GE gate + revert |\n"
            "| 18 | Security / Credentials | Security | ETL svc `svc_abc_etl` (long-lived pw) | Vault-issued short-lived | Verma | Autosys, ETL | T-8h rotate | Restore long-lived pw |\n"
            "| 19 | Monitoring & Logging | Ops | Splunk index `abc` | + Argus dashboard `abc-1998` | Sharma | On-call | T-24h | Disable Argus |\n"
            "| 20 | Testing / Cutover / Rollback | Release | (n/a) | UT sheet + rollback deploy group | Lohar | All | Release window | Fire rollback DG |\n\n"
            "### Cutover window\n"
            "```\n"
            "T-24h  Repository backup + Autosys JIL freeze\n"
            "T-8h   Vault secret rotation + parameter template load\n"
            "T-6h   File system symlink swap\n"
            "T-4h   Integration Service switch to IS_ABC_02\n"
            "T-2h   Snowflake schema clone `SF_ABC_CURATED_V2`\n"
            "T-1h   Source connection retarget + ANALYZE new index\n"
            "T-30m  Great Expectations dry-run\n"
            "T0     Autosys BOX split live; DBT models materialise\n"
            "T+30m  Smoke tests: `abc_smoke_v2` workflow\n"
            "T+2h   Post-deploy validation with Reg Reporting\n"
            "T+24h  Retire prior IS_ABC_01\n"
            "```\n\n"
            "### Rollback triggers\n"
            "- Curated row-count delta > 1% vs baseline\n"
            "- Great Expectations suite failure > 5 checks\n"
            "- Autosys BOX cascade fails within 30m of T0\n"
            "- Any Tier-1 downstream (Reg Reporting, Compliance) reports blocker\n\n"
            "### Sign-offs\n"
            "- Delivery Lead: Lohar, Kavita\n"
            "- ETL Lead: Burger, Hans\n"
            "- Compliance Steward: Verma, Rahul\n"
            "- Peer Review: Sharma, Anil"
        ),
    },

    # -----------------------------------------------------------------
    # SSM-1998 - Detailed Unit Testing
    # -----------------------------------------------------------------
    {
        "id": "SP-SSM-1998-UT-DETAIL",
        "title": "SSM-1998 - Unit Testing (Detailed) - October 2026.xlsx",
        "author": "Sharma, Anil",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Unit-Testing-Detailed.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "ssm", "releases", "oct-2026", "ssm-1998",
            "unit-testing", "ut", "detailed", "qa",
        ],
        "body": (
            "## SSM-1998 - Detailed Unit Testing Doc\n"
            "Extended UT for the UCP -> ENT Wave 2 cutover. Supersedes the summary\n"
            "sheet at [SSM-1998 Unit Testing Doc](/doc/SP-SSM-1998-UT).\n\n"
            "### Summary\n"
            "| Field | Value |\n"
            "|---|---|\n"
            "| Application | SSM (Shared Services & Migration) |\n"
            "| Release | October Release 2026 |\n"
            "| Ticket | SSM-1998 |\n"
            "| Testing Type | Unit Testing (Detailed) |\n"
            "| Environment | ENT (staging) with UCP shadow |\n"
            "| Scope | Hosting cutover, Autosys template, Vault rotation, Snowflake share |\n"
            "| Total Test Cases | 30 |\n"
            "| Pass | 20 |\n"
            "| Fail | 4 |\n"
            "| Blocked | 3 |\n"
            "| Not Executed | 3 |\n"
            "| Lead Tester | Sharma, Anil |\n"
            "| Peer Reviewer | Menon, Priya (EPM cross-team) |\n"
            "| Execution Window | 2026-09-13 to 2026-09-16 |\n"
            "| Overall Comments | 2 fails traced to residual UCP DNS records; retest 2026-09-18 |\n\n"
            "### Area coverage\n"
            "| Area | Cases | Pass | Fail | Blocked | Not Exec |\n"
            "|---|---|---|---|---|---|\n"
            "| Host Cutover (UCP -> ENT) | 8 | 5 | 2 | 1 | 0 |\n"
            "| Autosys Template Migration | 6 | 4 | 1 | 0 | 1 |\n"
            "| Snowflake Share Promotion | 5 | 4 | 0 | 1 | 0 |\n"
            "| Vault Namespace Rotation | 4 | 3 | 1 | 0 | 0 |\n"
            "| File System / Path Remap | 3 | 2 | 0 | 1 | 0 |\n"
            "| Rollback Rehearsal | 4 | 2 | 0 | 0 | 2 |\n\n"
            "### Test cases\n"
            "| Test ID | Area | Test Steps | Expected Result | Test Data | Actual Result | Status | Defect ID | Executed By | Duration |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| UT-D-101 | Host Cutover | Cutover `app-payments-01` UCP->ENT | DNS resolves ENT | dry-run cutover | Match | Pass | - | Sharma | 6m |\n"
            "| UT-D-102 | Host Cutover | Cutover `app-cards-01` | DNS resolves ENT | dry-run | Match | Pass | - | Sharma | 7m |\n"
            "| UT-D-103 | Host Cutover | Cutover `app-treasury-01` | DNS resolves ENT | dry-run | Stale UCP | Fail | DEF-3201 | Sharma | 9m |\n"
            "| UT-D-104 | Host Cutover | Cutover `app-adhoc-01` | DNS resolves ENT | dry-run | Match | Pass | - | Sharma | 6m |\n"
            "| UT-D-105 | Host Cutover | Rollback rehearsal `app-payments-01` | DNS reverts to UCP | dry-run | Match | Pass | - | Sharma | 5m |\n"
            "| UT-D-106 | Host Cutover | Rollback rehearsal `app-treasury-01` | DNS reverts | dry-run | Half-revert | Fail | DEF-3202 | Sharma | 8m |\n"
            "| UT-D-107 | Host Cutover | Certificate presented on ENT | Wildcard `*.ent.bank.internal` | curl | Match | Pass | - | Sharma | 30s |\n"
            "| UT-D-108 | Host Cutover | Latency SLA post-cutover | p95 < 120ms | 5m load | 138ms | - | Blocked | BLK-620 | - |\n"
            "| UT-D-109 | Autosys Template | New template `PNC_ENT_STD_V2` load | Loads cleanly | Template file | Match | Pass | - | Sharma | 40s |\n"
            "| UT-D-110 | Autosys Template | Migrate 12 jobs to new template | 12/12 migrated | JIL batch | 12/12 | Pass | - | Sharma | 3m |\n"
            "| UT-D-111 | Autosys Template | Calendar rollover month-end | Runs last-biz-day | Simulated | Match | Pass | - | Sharma | 12s |\n"
            "| UT-D-112 | Autosys Template | Blackout window respected | Skips window | Simulated | Match | Pass | - | Sharma | 8s |\n"
            "| UT-D-113 | Autosys Template | Job hold + release | Held job resumes | - | Match | Pass | - | Sharma | 30s |\n"
            "| UT-D-114 | Autosys Template | Cross-app dep on `abc_daily_box` | Fires only after ABC | Simulated | Fired early | Fail | DEF-3203 | Verma | 45s |\n"
            "| UT-D-115 | Autosys Template | JIL revert playbook | Rolls back cleanly | dry-run | - | Not Executed | - | - | - |\n"
            "| UT-D-116 | Snowflake Share | Promote share `SSM_ENT_SHARE` | Consumers see share | - | Match | Pass | - | Burger | 15s |\n"
            "| UT-D-117 | Snowflake Share | Grant share to ABC account | Grant applies | - | Match | Pass | - | Burger | 8s |\n"
            "| UT-D-118 | Snowflake Share | Grant share to EPM account | Grant applies | - | Match | Pass | - | Burger | 8s |\n"
            "| UT-D-119 | Snowflake Share | Retire Teradata read replica | Replica offline | - | Match | Pass | - | Burger | 20s |\n"
            "| UT-D-120 | Snowflake Share | Confirm no consumer still on Teradata | Splunk audit zero hits | 24h window | - | Blocked | BLK-621 | - | - |\n"
            "| UT-D-121 | Vault Rotation | Rotate `secret/ssm/ent/db` | New secret issued | - | Match | Pass | - | Verma | 12s |\n"
            "| UT-D-122 | Vault Rotation | Restart Autosys svc after rotate | Reconnects cleanly | - | Match | Pass | - | Verma | 30s |\n"
            "| UT-D-123 | Vault Rotation | Old secret revoked | 403 on old creds | - | 200 OK | Fail | DEF-3204 | Verma | 10s |\n"
            "| UT-D-124 | Vault Rotation | Break-glass path documented | Runbook link ok | Runbook | Match | Pass | - | Verma | 5s |\n"
            "| UT-D-125 | File System | NFS remap `/apps/ent/*` | Mounts on all ENT nodes | - | Match | Pass | - | Sharma | 90s |\n"
            "| UT-D-126 | File System | Symlink from `/apps/ucp/*` | Reads redirect | - | Match | Pass | - | Sharma | 15s |\n"
            "| UT-D-127 | File System | Write via legacy path fails | 403 | - | - | Blocked | BLK-622 | - | - |\n"
            "| UT-D-128 | Rollback Rehearsal | Full ENT deprovision | Restores UCP host | dry-run | Match | Pass | - | Sharma | 22m |\n"
            "| UT-D-129 | Rollback Rehearsal | Autosys JIL revert | Restores V1 calendar | - | Match | Pass | - | Sharma | 5m |\n"
            "| UT-D-130 | Rollback Rehearsal | Vault namespace revert | Restores old path | - | - | Not Executed | - | - | - |\n\n"
            "### Defect log\n"
            "| Defect ID | Test | Severity | Owner | Status |\n"
            "|---|---|---|---|---|\n"
            "| DEF-3201 | UT-D-103 | S2 (hosting) | Sharma | Stale UCP DNS record - flushed 2026-09-15, retest pending |\n"
            "| DEF-3202 | UT-D-106 | S2 (rollback) | Sharma | DNS revert partial; playbook step 4 clarified |\n"
            "| DEF-3203 | UT-D-114 | S3 (scheduler) | Verma | Cross-app dep expression missing calendar constraint |\n"
            "| DEF-3204 | UT-D-123 | S2 (security) | Verma | Vault TTL not honoured on legacy engine; upgrade tracked |\n\n"
            "### Sign-offs\n"
            "- Lead Tester: **Sharma, Anil** (2026-09-16)\n"
            "- Peer Reviewer: **Menon, Priya** (pending retest)\n"
            "- SSM Lead: **Sharma, Anil** (pending)"
        ),
    },

    # -----------------------------------------------------------------
    # SSM-1998 - OIM Entitlement Register
    # -----------------------------------------------------------------
    {
        "id": "SP-SSM-1998-ENTITLEMENTS",
        "title": "SSM-1998 - OIM Entitlement Register - October 2026.xlsx",
        "author": "Sharma, Anil",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Entitlements.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "ssm", "releases", "oct-2026", "ssm-1998",
            "entitlements", "oim", "access", "roles", "sod",
        ],
        "body": (
            "## SSM-1998 - OIM Entitlement Register\n"
            "Access model for the SSM cross-domain services and the ENT hosting\n"
            "estate. Requests raise via **OIM Access Portal** -> app instance\n"
            "`SSM-PROD` / `ENT-PROD`. Tier-1 roles are JIT-only.\n\n"
            "### Register\n"
            "| OIM Entitlement / Role Display Name | Description | Requestable | App Instance |\n"
            "|---|---|---|---|\n"
            "| SSM_HOSTING_OPERATOR | Provision + retire ENT hosts, manage JIL. Standard operator. | Yes | ENT-PROD |\n"
            "| SSM_HOSTING_OPERATOR_UAT | UAT twin of the operator role. | Yes | ENT-UAT |\n"
            "| SSM_HOSTING_ADMIN | Full estate admin - Tier-1, break-glass only. | No | ENT-PROD |\n"
            "| SSM_AUTOSYS_ADMIN | Autosys template + calendar edits. | Yes | AUTOSYS-PROD |\n"
            "| SSM_AUTOSYS_OPERATOR | On-call - restart, hold, release jobs. | Yes | AUTOSYS-PROD |\n"
            "| SSM_MIGRATION_LEAD | Sign-off on migration CRQs; SoD-fenced from operators. | No | SSM-PROD |\n"
            "| SSM_VAULT_ROTATOR | Rotate secrets under `secret/ssm/ent/*`. | Yes | VAULT-PROD |\n"
            "| SSM_VAULT_READER | Read metadata (not secret material) - dashboards + audit. | Yes | VAULT-PROD |\n"
            "| SSM_SNOWFLAKE_SHARE_ADMIN | Manage `SSM_ENT_SHARE` grants. | Yes | SNOWFLAKE-PROD |\n"
            "| SSM_UCP_DECOMM | Retire UCP hosts + revoke UCP DNS. Time-limited campaign role. | Yes | UCP-PROD |\n"
            "| SSM_ADHOC_INTAKE | File and triage cross-team ADHOC requests. | Yes | SSM-ADHOC |\n"
            "| SSM_ADHOC_APPROVER | Approve ADHOC requests - SSM Lead + App Owner. | No | SSM-ADHOC |\n"
            "| SSM_BREAK_GLASS | Time-boxed prod admin - 4h auto-revoke, dual-approval. | No | ENT-PROD |\n"
            "| SSM_AUDIT_READ | Read audit logs across ENT + Vault + Autosys. | Yes | ENT-PROD |\n\n"
            "### SoD (segregation of duties) conflicts\n"
            "| Role A | Conflicts with | Reason |\n"
            "|---|---|---|\n"
            "| SSM_MIGRATION_LEAD | SSM_HOSTING_OPERATOR | Lead cannot self-execute a cutover they approve. |\n"
            "| SSM_AUTOSYS_ADMIN | SSM_ADHOC_APPROVER | Scheduler edits cannot be self-approved as ADHOC. |\n"
            "| SSM_BREAK_GLASS | SSM_HOSTING_OPERATOR | Break-glass supersedes standard operator; standard must be revoked first. |\n\n"
            "### Ownership & approval\n"
            "| Role | Owner | Approver | Review Cadence |\n"
            "|---|---|---|---|\n"
            "| SSM_HOSTING_* | Sharma, Anil | SSM Lead + Peer | Quarterly |\n"
            "| SSM_AUTOSYS_* | Sharma, Anil | SSM Lead | Quarterly |\n"
            "| SSM_VAULT_* | Verma, Rahul (InfoSec sponsor) | InfoSec | Quarterly |\n"
            "| SSM_MIGRATION_LEAD | Sharma, Anil | InfoSec (Tier-1) | Monthly |\n"
            "| SSM_BREAK_GLASS | Sharma, Anil | InfoSec (Tier-1) | Per use |\n\n"
            "### Notes\n"
            "- Time-limited campaign roles (`SSM_UCP_DECOMM`) auto-expire at campaign end.\n"
            "- All Vault-scoped roles enforce short-lived credential issuance.\n"
            "- Recertification runs the first Friday of each quarter, cross-checked with the\n"
            "  ADHOC register at [SSM ADHOC Register](/doc/SP-SSM-ADHOC-REGISTER)."
        ),
    },

    # -----------------------------------------------------------------
    # SSM-1998 - Migration Components (Detailed)
    # -----------------------------------------------------------------
    {
        "id": "SP-SSM-1998-COMPONENTS-DETAIL",
        "title": "SSM-1998 - Migration Components (Detailed) - October 2026.xlsx",
        "author": "Sharma, Anil",
        "url": "https://sharepoint.bank.internal/sites/SSM/Releases/Oct-2026/SSM-1998/Components-Detailed.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "ssm", "releases", "oct-2026", "ssm-1998",
            "components", "migration", "hosting", "autosys", "detailed",
        ],
        "body": (
            "## SSM-1998 - Migration Components (Detailed)\n"
            "Deep-detail companion to the 20-row summary at\n"
            "[SSM-1998 Components List](/doc/SP-SSM-1998-COMPONENTS). This release\n"
            "covers the UCP -> ENT Wave 2 hosting cutover and the Autosys template\n"
            "migration.\n\n"
            "### Per-component detail\n"
            "| # | Component | Area | From | To | Owner | Downstream Impact | Cutover Window | Rollback Trigger |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| 1 | UCP Host `app-payments-01` | Hosting | UCP data center | ENT `payments-01.ent` | Sharma | Payments API | T-3h DNS TTL | DNS revert + service restart |\n"
            "| 2 | UCP Host `app-cards-01` | Hosting | UCP | ENT `cards-01.ent` | Sharma | Cards issuing | T-3h | DNS revert |\n"
            "| 3 | UCP Host `app-treasury-01` | Hosting | UCP | ENT `treasury-01.ent` | Sharma | Treasury feeds | T-3h | DNS revert |\n"
            "| 4 | UCP Host `app-adhoc-01` | Hosting | UCP | ENT `adhoc-01.ent` | Sharma | SSM ADHOC intake | T-3h | DNS revert |\n"
            "| 5 | Autosys Template `PNC_STD_V1` | Scheduler | V1 calendar | `PNC_ENT_STD_V2` | Sharma | 12 jobs across SSM | T-24h JIL swap | Restore V1 JIL |\n"
            "| 6 | Autosys Calendar (Month-end) | Scheduler | `MEND_V1` | `MEND_V2` | Sharma | Reg Reporting | Included above | Restore `MEND_V1` |\n"
            "| 7 | Autosys Cross-App Dep | Scheduler | Implicit | Explicit `success(abc_daily_box)` | Verma | ABC + EPM boxes | Included above | Drop new dep |\n"
            "| 8 | Autosys Blackout Windows | Scheduler | Per-app config | Central template | Sharma | All jobs | Included above | Revert per-app |\n"
            "| 9 | Snowflake Share `SSM_ENT_SHARE` | Data platform | (n/a) | Promoted | Burger | ABC + EPM Snowflake accounts | T-2h | Revoke share |\n"
            "| 10 | Teradata Read Replica | Data platform | Live | Decommissioned | Burger | Legacy BI dashboards | T+24h retire | Re-enable replica (24h grace) |\n"
            "| 11 | Vault Namespace `secret/ssm/*` | Security | Legacy engine | KV v2 `secret/ssm/ent/*` | Verma | Autosys svc, ETL svc | T-8h rotate | Restore prior namespace |\n"
            "| 12 | Vault Role Bindings | Security | Long-lived tokens | Short-lived (`ttl=1h`) | Verma | All consumers | T-8h | Restore long-lived (audit only) |\n"
            "| 13 | NFS Mount `/apps/ucp/*` | File system | UCP mount | Symlink -> `/apps/ent/*` | Sharma | Log paths, batch drops | T-6h | Remove symlinks |\n"
            "| 14 | NFS Mount `/apps/ent/*` | File system | (n/a) | Live on all ENT nodes | Sharma | All apps | T-6h | Unmount (breaks ENT nodes - rollback via host cutover) |\n"
            "| 15 | Splunk Index Alias | Ops | `ssm-ucp` | `ssm-ent` (aliased) | Sharma | On-call dashboards | T-1h | Restore alias |\n"
            "| 16 | Argus Dashboard `ssm-ent` | Ops | (n/a) | Published | Sharma | On-call | T-24h | Disable dashboard |\n"
            "| 17 | Certificate `*.ent.bank.internal` | Security | (n/a) | Issued via internal CA | Verma | All ENT services | T-24h | (leave in place) |\n"
            "| 18 | Firewall Rules | Network | UCP FW zone | ENT FW zone | Sharma | All inbound + outbound | T-24h | Restore UCP rules |\n"
            "| 19 | Load Balancer VIP | Network | UCP LB pool | ENT LB pool | Sharma | Payments, Cards, Treasury | T-3h | Repoint VIP |\n"
            "| 20 | Testing / Cutover / Rollback | Release | (n/a) | Rehearsal + rollback DG | Sharma | All | Release window | Fire rollback DG |\n\n"
            "### Cutover window\n"
            "```\n"
            "T-24h  Autosys JIL freeze + template load (`PNC_ENT_STD_V2`)\n"
            "T-24h  Argus dashboard published; Splunk alias staged\n"
            "T-24h  Firewall rule staging; certificates issued\n"
            "T-8h   Vault namespace rotation + credential re-issue\n"
            "T-6h   NFS symlink swap `/apps/ucp/*` -> `/apps/ent/*`\n"
            "T-3h   DNS cutover for 4 UCP hosts (TTL warmed 60s)\n"
            "T-2h   Snowflake share promoted; grants applied to ABC / EPM\n"
            "T-1h   Splunk alias flipped to `ssm-ent`\n"
            "T0     Load balancer VIP repointed; new Autosys template goes live\n"
            "T+30m  Smoke tests: hosting, scheduler, share, vault\n"
            "T+2h   Cross-team validation with ABC + EPM leads\n"
            "T+24h  Teradata read replica decommission\n"
            "```\n\n"
            "### Rollback triggers\n"
            "- Any Tier-1 downstream (Payments, Cards, Treasury) reports 5xx > 1% for > 5 min\n"
            "- Autosys template migration blocks > 3 jobs simultaneously\n"
            "- Vault rotation causes credential exhaustion across > 1 consumer\n"
            "- Snowflake share consumers cannot read within 30m of promotion\n"
            "- Firewall rule change denies any Tier-1 flow\n\n"
            "### Sign-offs\n"
            "- SSM Lead: Sharma, Anil\n"
            "- InfoSec: Verma, Rahul\n"
            "- Cross-team (ABC): Lohar, Kavita\n"
            "- Cross-team (EPM): Menon, Priya"
        ),
    },

    # -----------------------------------------------------------------
    # EPM-1998 - Detailed Unit Testing
    # -----------------------------------------------------------------
    {
        "id": "SP-EPM-1998-UT-DETAIL",
        "title": "EPM-1998 - Unit Testing (Detailed) - October 2026.xlsx",
        "author": "Menon, Priya",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Unit-Testing-Detailed.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "epm", "releases", "oct-2026", "epm-1998",
            "unit-testing", "ut", "detailed", "qa",
        ],
        "body": (
            "## EPM-1998 - Detailed Unit Testing Doc\n"
            "Extended UT for the P&L attribution + cube-refresh scope. Supersedes\n"
            "the summary sheet at [EPM-1998 Unit Testing Doc](/doc/SP-EPM-1998-UT).\n\n"
            "### Summary\n"
            "| Field | Value |\n"
            "|---|---|\n"
            "| Application | EPM (Enterprise Performance Management) |\n"
            "| Release | October Release 2026 |\n"
            "| Ticket | EPM-1998 |\n"
            "| Testing Type | Unit Testing (Detailed) |\n"
            "| Environment | UAT (with prod-shaped fixture) |\n"
            "| Scope | Model deployment, cube refresh, Tableau extracts, DBT parity |\n"
            "| Total Test Cases | 30 |\n"
            "| Pass | 24 |\n"
            "| Fail | 2 |\n"
            "| Blocked | 1 |\n"
            "| Not Executed | 3 |\n"
            "| Lead Tester | Menon, Priya |\n"
            "| Peer Reviewer | Verma, Rahul |\n"
            "| Execution Window | 2026-09-14 to 2026-09-16 |\n"
            "| Overall Comments | MRM sign-off pending on Model v2.4 |\n\n"
            "### Area coverage\n"
            "| Area | Cases | Pass | Fail | Blocked | Not Exec |\n"
            "|---|---|---|---|---|---|\n"
            "| Model Deployment (MRM path) | 6 | 5 | 0 | 1 | 0 |\n"
            "| Cube Refresh (Essbase) | 5 | 4 | 1 | 0 | 0 |\n"
            "| Tableau Extract | 5 | 4 | 0 | 0 | 1 |\n"
            "| DBT Parity | 5 | 4 | 1 | 0 | 0 |\n"
            "| Attribution Logic | 5 | 4 | 0 | 0 | 1 |\n"
            "| Regression (unchanged) | 4 | 3 | 0 | 0 | 1 |\n\n"
            "### Test cases\n"
            "| Test ID | Area | Test Steps | Expected Result | Test Data | Actual Result | Status | Defect ID | Executed By | Duration |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| UT-D-201 | Model Deployment | Load Model v2.4 into UAT | Model registers | Model v2.4 pkg | Match | Pass | - | Menon | 90s |\n"
            "| UT-D-202 | Model Deployment | Back-test 30 days vs baseline | Delta <= 0.05% | 30-day fixture | 0.03% | Pass | - | Menon | 22m |\n"
            "| UT-D-203 | Model Deployment | MRM sign-off gate | Sign-off recorded | - | - | Blocked | BLK-720 | - | - |\n"
            "| UT-D-204 | Model Deployment | Rollback to v2.3 | Model v2.3 restored | - | Match | Pass | - | Menon | 90s |\n"
            "| UT-D-205 | Model Deployment | Feature-store consistency | Features consistent | Store snapshot | Match | Pass | - | Menon | 45s |\n"
            "| UT-D-206 | Model Deployment | Cold-cache warm-up | Warm-up < 5m | - | 4m | Pass | - | Menon | 4m |\n"
            "| UT-D-207 | Cube Refresh | Full cube refresh | Refresh completes < 30m | Full cube | 28m | Pass | - | Menon | 28m |\n"
            "| UT-D-208 | Cube Refresh | Incremental refresh | Incremental < 5m | Delta | 4m | Pass | - | Menon | 4m |\n"
            "| UT-D-209 | Cube Refresh | Cube reconcile to Snowflake | Delta = 0 | UAT fixture | Match | Pass | - | Menon | 3m |\n"
            "| UT-D-210 | Cube Refresh | Slow-changing dimension load | SCD2 tracked | Curated | Match | Pass | - | Menon | 2m |\n"
            "| UT-D-211 | Cube Refresh | Bad member ID | Reject to DLQ | Malformed | Silent pass | Fail | DEF-3301 | Verma | 90s |\n"
            "| UT-D-212 | Tableau Extract | Executive scorecard refresh | Extract green | Live | Match | Pass | - | Menon | 6m |\n"
            "| UT-D-213 | Tableau Extract | CFO daily view refresh | Extract green | Live | Match | Pass | - | Menon | 4m |\n"
            "| UT-D-214 | Tableau Extract | Row-level security policy | Non-priv user sees redacted | UAT user | Match | Pass | - | Verma | 45s |\n"
            "| UT-D-215 | Tableau Extract | Publisher can overwrite | Publisher role works | Publisher | Match | Pass | - | Menon | 30s |\n"
            "| UT-D-216 | Tableau Extract | Scheduled refresh (nightly) | Runs 03:00 | - | - | Not Executed | - | - | - |\n"
            "| UT-D-217 | DBT Parity | dim_book parity vs cube | Delta = 0 | 30-day | Match | Pass | - | Verma | 5m |\n"
            "| UT-D-218 | DBT Parity | fct_pnl_attribution parity | Delta = 0 | 30-day | Match | Pass | - | Verma | 6m |\n"
            "| UT-D-219 | DBT Parity | fct_forecast parity | Delta = 0 | 30-day | +3 rows | Fail | DEF-3302 | Verma | 6m |\n"
            "| UT-D-220 | DBT Parity | dim_scenario parity | Delta = 0 | 30-day | Match | Pass | - | Verma | 4m |\n"
            "| UT-D-221 | DBT Parity | Snapshot regen | Snapshot matches | - | Match | Pass | - | Verma | 3m |\n"
            "| UT-D-222 | Attribution | Book-level P&L reconcile | Sum matches GL | GL slice | Match | Pass | - | Menon | 90s |\n"
            "| UT-D-223 | Attribution | Trader-level attribution | Trader totals sum to book | UAT | Match | Pass | - | Menon | 60s |\n"
            "| UT-D-224 | Attribution | Factor-level attribution | Factors sum to trader | UAT | Match | Pass | - | Menon | 90s |\n"
            "| UT-D-225 | Attribution | Zero-P&L day | Handles cleanly | Zero-day | Match | Pass | - | Menon | 30s |\n"
            "| UT-D-226 | Attribution | Cross-currency attribution | FX applied at cutoff | Multi-ccy fixture | - | Not Executed | - | - | - |\n"
            "| UT-D-227 | Regression | Legacy scorecard unchanged | Same numbers | Baseline | Match | Pass | - | Menon | 3m |\n"
            "| UT-D-228 | Regression | Legacy Essbase views unchanged | Same numbers | Baseline | Match | Pass | - | Menon | 3m |\n"
            "| UT-D-229 | Regression | Legacy report PDF pixel-diff | Same layout | Baseline | Match | Pass | - | Menon | 45s |\n"
            "| UT-D-230 | Regression | Legacy Tableau workbook | Same numbers | Baseline | - | Not Executed | - | - | - |\n\n"
            "### Defect log\n"
            "| Defect ID | Test | Severity | Owner | Status |\n"
            "|---|---|---|---|---|\n"
            "| DEF-3301 | UT-D-211 | S2 (data) | Verma | Cube loader swallowed reject; DLQ hook missing |\n"
            "| DEF-3302 | UT-D-219 | S3 (data) | Verma | Fixture drift; 3 stale forecast rows in baseline |\n\n"
            "### Sign-offs\n"
            "- Lead Tester: **Menon, Priya** (2026-09-16)\n"
            "- Peer Reviewer: **Verma, Rahul** (pending)\n"
            "- Model Risk (MRM): pending (BLK-720)\n"
            "- Delivery Lead: **Menon, Priya** (pending)"
        ),
    },

    # -----------------------------------------------------------------
    # EPM-1998 - OIM Entitlement Register
    # -----------------------------------------------------------------
    {
        "id": "SP-EPM-1998-ENTITLEMENTS",
        "title": "EPM-1998 - OIM Entitlement Register - October 2026.xlsx",
        "author": "Menon, Priya",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Entitlements.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "epm", "releases", "oct-2026", "epm-1998",
            "entitlements", "oim", "access", "roles", "sod",
        ],
        "body": (
            "## EPM-1998 - OIM Entitlement Register\n"
            "Access model for EPM - the P&L attribution stack, Essbase cubes, and\n"
            "the executive Tableau scorecard. Requests raise via **OIM Access Portal**\n"
            "-> app instance `EPM-PROD` / `EPM-UAT`. Model-risk roles are SoD-fenced\n"
            "from developer roles.\n\n"
            "### Register\n"
            "| OIM Entitlement / Role Display Name | Description | Requestable | App Instance |\n"
            "|---|---|---|---|\n"
            "| EPM_ANALYST_RO | Read-only on curated EPM schemas + Tableau viewer. | Yes | EPM-PROD |\n"
            "| EPM_ANALYST_RW | Read/write on curated EPM schemas; peer review for DDL. | Yes | EPM-PROD |\n"
            "| EPM_MODEL_DEVELOPER | Author and deploy P&L attribution models to UAT. | Yes | EPM-UAT |\n"
            "| EPM_MODEL_APPROVER | Sign-off on production model deploys. SoD-fenced from developer. | No | EPM-PROD |\n"
            "| EPM_MODEL_MRM | Model Risk Management review + approve. | No | EPM-PROD |\n"
            "| EPM_CUBE_ADMIN | Essbase cube admin - refresh, dim edits, calc scripts. | Yes | ESSBASE-PROD |\n"
            "| EPM_CUBE_OPERATOR | On-call - restart refresh, kick incremental. | Yes | ESSBASE-PROD |\n"
            "| EPM_TABLEAU_VIEWER | View scorecards under `EPM/*`. Broad. | Yes | TABLEAU-PROD |\n"
            "| EPM_TABLEAU_PUBLISHER | Publish/edit workbooks under `EPM/*`. | Yes | TABLEAU-PROD |\n"
            "| EPM_CFO_VIEWER | Restricted CFO daily view - row-level policy applies. | Yes | TABLEAU-PROD |\n"
            "| EPM_FORECAST_APPROVER | Approve forecast cube publishes to prod. | No | EPM-PROD |\n"
            "| EPM_BREAK_GLASS | Time-boxed prod admin - 4h auto-revoke, dual-approval. | No | EPM-PROD |\n"
            "| EPM_AUDIT_READ | Read audit + lineage across models, cubes, Tableau. | Yes | EPM-PROD |\n"
            "| EPM_SUPPORT_READ | Support engineer read + Splunk index `epm`. | Yes | EPM-PROD |\n\n"
            "### SoD (segregation of duties) conflicts\n"
            "| Role A | Conflicts with | Reason |\n"
            "|---|---|---|\n"
            "| EPM_MODEL_DEVELOPER | EPM_MODEL_APPROVER | Developer cannot approve own deploy. |\n"
            "| EPM_MODEL_DEVELOPER | EPM_MODEL_MRM | MRM review must be independent. |\n"
            "| EPM_CUBE_ADMIN | EPM_FORECAST_APPROVER | Cube admin cannot self-approve forecast publish. |\n"
            "| EPM_BREAK_GLASS | EPM_ANALYST_RW | Break-glass supersedes standard write; revoke standard first. |\n\n"
            "### Ownership & approval\n"
            "| Role | Owner | Approver | Review Cadence |\n"
            "|---|---|---|---|\n"
            "| EPM_ANALYST_* | Menon, Priya | Delivery Lead | Quarterly |\n"
            "| EPM_MODEL_DEVELOPER | Menon, Priya | Delivery Lead + Peer | Quarterly |\n"
            "| EPM_MODEL_APPROVER | Menon, Priya | MRM + InfoSec | Monthly |\n"
            "| EPM_MODEL_MRM | Verma, Rahul (Compliance sponsor) | InfoSec (Tier-1) | Monthly |\n"
            "| EPM_CUBE_* | Menon, Priya | Delivery Lead | Quarterly |\n"
            "| EPM_TABLEAU_PUBLISHER | Menon, Priya | Delivery Lead | Quarterly |\n"
            "| EPM_CFO_VIEWER | Menon, Priya | CFO office | Quarterly |\n"
            "| EPM_BREAK_GLASS | Menon, Priya | InfoSec (Tier-1) | Per use |\n\n"
            "### Notes\n"
            "- Model roles enforce independence: no user may hold Developer + Approver + MRM.\n"
            "- CFO viewer role enforces row-level Tableau policy - test coverage in UT-D-214.\n"
            "- Recertification runs the first Friday of each quarter."
        ),
    },

    # -----------------------------------------------------------------
    # EPM-1998 - Migration Components (Detailed)
    # -----------------------------------------------------------------
    {
        "id": "SP-EPM-1998-COMPONENTS-DETAIL",
        "title": "EPM-1998 - Migration Components (Detailed) - October 2026.xlsx",
        "author": "Menon, Priya",
        "url": "https://sharepoint.bank.internal/sites/EPM/Releases/Oct-2026/EPM-1998/Components-Detailed.xlsx",
        "updated_at": "2026-09-16T09:00:00Z",
        "tags": [
            "epm", "releases", "oct-2026", "epm-1998",
            "components", "migration", "essbase", "tableau", "model", "detailed",
        ],
        "body": (
            "## EPM-1998 - Migration Components (Detailed)\n"
            "Deep-detail companion to the 20-row summary at\n"
            "[EPM-1998 Components List](/doc/SP-EPM-1998-COMPONENTS). This release\n"
            "lands the P&L attribution Model v2.4, refactors the forecast cube, and\n"
            "moves the executive Tableau scorecard onto DBT-materialised sources.\n\n"
            "### Per-component detail\n"
            "| # | Component | Area | From | To | Owner | Downstream Impact | Cutover Window | Rollback Trigger |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| 1 | P&L Attribution Model | Model | v2.3 | v2.4 (feature `factor_beta_v2`) | Menon | Trader attribution | T-2h load | Restore v2.3 |\n"
            "| 2 | Model Package | Model | Legacy tarball | Signed pkg via Vault-cosign | Verma | Deploy pipeline | T-8h | Restore legacy tarball |\n"
            "| 3 | Feature Store | Model | Snowflake `EPM_FEATURES_V1` | `EPM_FEATURES_V2` | Menon | Model + backtest | T-4h clone | Alias swap back |\n"
            "| 4 | Backtest Job | Model | Weekly | Nightly | Menon | On-call | T-24h JIL swap | Revert to weekly |\n"
            "| 5 | MRM Review Artefact | Model | (n/a) | Signed off in `MRM-EPM-24` | Verma | MRM gate | Independent of T0 | (blocker if missing) |\n"
            "| 6 | Essbase Cube (Actuals) | Cube | Cube v1.9 | Cube v2.0 (new dim `Scenario`) | Menon | CFO daily view | T-3h freeze | Restore cube v1.9 |\n"
            "| 7 | Essbase Cube (Forecast) | Cube | Cube v1.4 | Cube v1.5 (SCD2) | Menon | Forecast dashboards | T-3h | Restore cube v1.4 |\n"
            "| 8 | Cube Calc Scripts | Cube | 8 scripts | 10 scripts | Menon | Cube refresh | T-3h | Restore prior 8 |\n"
            "| 9 | Cube Refresh Schedule | Cube | Full nightly | Incremental every 4h | Menon | Freshness SLA | T-24h JIL swap | Revert to nightly |\n"
            "| 10 | Cube DLQ Hook | Cube | Silent drop | Route to DLQ + alert | Verma | Data quality | T-3h | Restore silent path (audit only) |\n"
            "| 11 | Tableau Extract - Scorecard | Tableau | From Essbase | From Snowflake `fct_pnl_attribution` | Menon | Exec scorecard | T-2h refresh | Repoint to Essbase |\n"
            "| 12 | Tableau Extract - CFO view | Tableau | From Essbase | From Snowflake + RLS policy | Verma | CFO office | T-2h | Repoint + drop RLS |\n"
            "| 13 | Tableau Row-Level Security | Tableau | (n/a) | Policy `epm.cfo.view` | Verma | CFO viewer role | T-2h | Drop policy |\n"
            "| 14 | DBT Models (EPM) | ETL | (n/a) | `epm.fct_pnl_attribution` + 6 dim | Menon | Tableau, downstream BI | T-2h | Point workbook back to Essbase |\n"
            "| 15 | DBT Snapshots | ETL | (n/a) | Nightly SCD2 on `dim_book` | Menon | Historical query | T-2h | Drop snapshots |\n"
            "| 16 | Snowflake Warehouse | Data platform | WH_EPM_M | +WH_EPM_ADHOC_S | Menon | ADHOC users | T-2h | Retire ADHOC WH |\n"
            "| 17 | Reporting Cache | Ops | Filesystem cache | Redis (elasticache) | Menon | Refresh perf | T-2h | Fall back to filesystem |\n"
            "| 18 | Security / Roles | Security | Broad `EPM_RW` | Split (`ANALYST_RW`, `MODEL_DEVELOPER`, `MODEL_APPROVER`) | Verma | All EPM users | T-24h role provision | Restore broad role (audit only) |\n"
            "| 19 | Monitoring & Logging | Ops | Splunk index `epm` | + Argus dashboard `epm-1998` | Menon | On-call | T-24h | Disable Argus |\n"
            "| 20 | Testing / Cutover / Rollback | Release | (n/a) | UT sheet + rollback DG | Menon | All | Release window | Fire rollback DG |\n\n"
            "### Cutover window\n"
            "```\n"
            "T-24h  Argus dashboard published; Autosys JIL freeze\n"
            "T-24h  OIM role provisioning for split roles\n"
            "T-8h   Model package rebuilt + Vault-cosigned\n"
            "T-4h   Feature store clone `EPM_FEATURES_V2`\n"
            "T-3h   Essbase cube freeze; calc scripts staged\n"
            "T-2h   Tableau extracts repointed to Snowflake\n"
            "T-2h   Tableau row-level security policy `epm.cfo.view` applied\n"
            "T-2h   Warehouse ADHOC WH_EPM_ADHOC_S live\n"
            "T-2h   Redis cache warmed\n"
            "T-2h   Model v2.4 loaded to UAT\n"
            "T0     Model v2.4 promoted to prod (MRM sign-off required)\n"
            "T+30m  Smoke tests: cube refresh, scorecard, CFO view\n"
            "T+2h   Cross-team validation with ABC + SSM leads\n"
            "T+24h  Retire Feature Store V1\n"
            "```\n\n"
            "### Rollback triggers\n"
            "- Model v2.4 back-test delta > 0.1% vs v2.3 baseline\n"
            "- Cube refresh > 45m (SLA breach)\n"
            "- Tableau scorecard numbers do not reconcile to GL (any book)\n"
            "- CFO row-level policy leaks any restricted row (Sev-1)\n"
            "- MRM sign-off not present at T0 (hard block, not rollback)\n\n"
            "### Sign-offs\n"
            "- Delivery Lead: Menon, Priya\n"
            "- Model Risk (MRM): Verma, Rahul\n"
            "- InfoSec (roles + RLS): Verma, Rahul\n"
            "- Cross-team (ABC): Lohar, Kavita\n"
            "- Cross-team (SSM): Sharma, Anil"
        ),
    },
]


ALL_DOCS = []
for d in CONFLUENCE_DOCS:
    ALL_DOCS.append({**d, "source": "confluence"})
for d in GITHUB_DOCS:
    ALL_DOCS.append({**d, "source": "github"})
for d in SHAREPOINT_DOCS:
    ALL_DOCS.append({**d, "source": "sharepoint"})
