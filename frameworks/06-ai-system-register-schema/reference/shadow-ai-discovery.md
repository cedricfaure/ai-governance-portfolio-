> Component of the [AI System Register Schema](../README.md) framework.

# Shadow AI discovery

The systems you already know about are the easy half. The register's credibility rests on the half nobody declared.

**Scale of the problem.** IBM's 2025 Cost of a Data Breach report found shadow AI was a factor in roughly one in five breaches, adding an average of USD 670,000 to breach cost, largely because most affected organisations had no AI governance policy. UpGuard's State of Shadow AI reporting puts unapproved AI tool use above 80% of workers.

## The five discovery layers

No single technique gives coverage. Fuse at least three.

| Layer | Mechanism | What it catches | What it misses | Effort |
|---|---|---|---|---|
| 1, Declared | Structured team survey; ask what tools they use to decide or sort anything about a person | Context, purpose, ownership, spreadsheets, intent | Anything people forget, hide, or do not think of as AI | Low cost, high time |
| 2, Network | DNS, egress, proxy, firewall, SWG logs for first-seen connections to model provider and AI domains | Breadth; server-side API calls; volume trends | Personal devices; encrypted tunnels; new providers not yet catalogued; what happened inside the session | Low, uses data you already hold |
| 3, Identity | OAuth grant enumeration across the workspace suite; SSO and audit logs filtered against an AI tool catalogue; service account audit; secrets scanning in code repositories for embedded API keys | Which account authorised what, and with which scopes; agent connections; API keys in code | Browser tools that need no enterprise identity; personal-account usage | Low to medium |
| 4, Endpoint and browser | Managed browser extension telemetry; endpoint agent inventory of AI desktop apps, local model runtimes, MCP servers and package installs | The broadest single layer, catches tools that bypass every other layer, including personal-account sign-ins and local agentic components | Unmanaged and personal devices | Medium; privacy consultation required |
| 5, Commercial | Expense and corporate card data; procurement and renewal records for the last 12 to 24 months; email scanning for sign-up confirmations and invoices | Paid subscriptions bought outside procurement; embedded features arriving via renewal | Free tiers; anything not paid for | Low |

**Correlation beats any single source.** Network logs alone miss most of it, because so much AI usage is browser-based and embedded in approved SaaS. Identity logs answer "which account authorised this" far better than raw network data. Expense data finds what nobody logged. Run at least three, then reconcile.

## Two mechanisms most programmes omit

**Approved-SaaS feature sweep.** Read the admin console of every significant SaaS platform and list the AI features available and which are enabled. AI capability arriving inside a renewal is the highest-volume source of unregistered systems, and it never passes a procurement gate because nothing was procured.

**Local agentic sweep.** Inventory MCP servers, local model runtimes, agent frameworks and IDE agents with tool access on developer machines. This is the fastest-growing blind spot and appears in no traditional inventory. Prioritise devices with privileged data access.

## The amnesty, a process mechanism, not a technical one

Technical discovery finds connections. It does not find purpose, ownership or the spreadsheet on someone's desktop. Run a time-boxed declaration amnesty alongside it:

- Announce a fixed window, four to six weeks
- State plainly that the objective is visibility, not enforcement, and that nothing declared in the window will be withdrawn or disciplined
- Provide a form that takes under five minutes and uses plain language, "anything that helps you decide, sort, rank, score, draft or answer", never the word "model"
- Make declaration the path of least resistance and provide a route to keep using the tool
- Publish what was found, in aggregate, and what happened next

Then close the loop: anything found by technical discovery after the amnesty closes that was not declared becomes a conversation with the team, not a sanction, but the register entry is created either way.

**On blocking.** Blocking traffic without addressing the underlying demand drives usage onto personal devices, removing all corporate visibility. A programme that reduces detected usage while demand is unchanged has made the problem invisible, not smaller. The register exists to see. Enforcement decisions come after, informed by the tier.

## The discovery_source field

Record how each entry was found: `declared_by_team`, `amnesty`, `network_log`, `identity_oauth`, `endpoint_browser`, `saas_admin_sweep`, `expense_procurement`, `local_agentic_sweep`, `incident`, `audit`, `intake_process`.

This field is the register's own quality metric. If 95% of entries are `declared_by_team`, discovery has not run. A healthy mature register shows most new entries arriving through `intake_process`, because the front door is working, and continues to show a trickle from technical layers, because it always will.
