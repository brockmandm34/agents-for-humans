# Enterprise Change Impact Agent

An AI-powered cross-platform change impact and blast-radius analysis agent built with **AWS Strands Agents** and **Amazon Bedrock**.

Built for the **Agents for Humans Hackathon**.

**Track:** Pro Agents

## Problem

Enterprise systems rarely operate in isolation.

A change that appears small inside one platform can create unexpected problems elsewhere.

For example, changing a Salesforce field could affect:

* Power Automate workflows
* Power BI dashboards
* Power Apps applications
* Business processes
* Integrations
* Data handling
* System owners and stakeholders

The challenge is that dependency information is often fragmented across platforms, teams, and technical owners.

Individual enterprise platforms may understand parts of their own ecosystem, but organizations still need a way to understand the **cross-platform blast radius** of a proposed change before it reaches production.

## Solution

The **Enterprise Change Impact Agent** investigates a proposed system change and identifies what else may be affected.

The agent uses AWS Strands Agents to gather evidence from available tools and reason across dependencies spanning multiple enterprise platforms.

The goal is to answer questions such as:

* What systems depend on the component being changed?
* Which workflows or automations may be affected?
* Which reports or dashboards rely on the current configuration?
* Which applications consume the data?
* Who owns the affected systems?
* What risks should be validated before deployment?
* Where is human review or approval required?

The agent does **not** approve or deploy changes.

It identifies the potential blast radius, separates known evidence from potential risks, and gives human decision-makers better information before a change is made.

## Current Demo Scenario

The current prototype evaluates a proposed change to:

**Salesforce → Membership Status**

Proposed change:

> Change the `Membership Status` field from a picklist to a calculated field.

The agent discovers that the field has known dependencies across Microsoft Power Platform:

### Power Automate

**Membership Renewal Workflow**

Uses Membership Status to determine when renewal communications are sent.

### Power BI

**Membership Dashboard**

Uses Membership Status for membership reporting and filtering.

### Power Apps

**Membership Administration App**

Uses membership information as part of the staff administration experience.

The agent then evaluates the potential impact of the proposed Salesforce change across all three downstream systems.

## Architecture

```text
             Proposed Enterprise Change
                        |
                        v
              AWS Strands Agent
                        |
                        v
            Amazon Bedrock / Claude
                        |
                        v
              Investigation Tools
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     Salesforce    Power Platform   Enterprise
      Metadata      Dependencies      Data
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
    Power Automate   Power BI      Power Apps
       Workflows     Reports       Applications
          |             |             |
          +-------------+-------------+
                        |
                        v
               Evidence Collection
                        |
                        v
              Blast Radius Analysis
                        |
                        v
             Human Review / Decision
```

## Why This Is Different

This project is not intended to replace Salesforce, Power Platform, or existing enterprise administration tools.

Its purpose is to reason **across platforms**.

A change may originate in Salesforce while its consequences appear in Power Automate, Power BI, Power Apps, or another connected system.

The agent is designed to bring those dependencies together into a single change-impact assessment.

## Current Capabilities

The prototype currently supports:

* AWS Strands Agent running locally
* Amazon Bedrock integration
* Anthropic Claude through Bedrock
* Custom Python tools using Strands
* External enterprise dependency data stored separately from the agent
* Salesforce component lookup
* Cross-platform dependency discovery
* Power Automate impact identification
* Power BI impact identification
* Power Apps impact identification
* Business-owner identification
* Blast-radius analysis
* Human-review recommendations

## Evidence-Aware Analysis

The agent is designed to distinguish between different levels of certainty.

### Known Impact

Information directly discovered from enterprise data or tools.

### Potential Risk

A plausible consequence of the proposed change that should be investigated.

### Needs Validation

Information the agent does not currently have enough evidence to confirm.

### Human Review

Decisions or technical validations that should remain with system owners or other responsible humans.

This prevents the agent from presenting assumptions as established facts.

## Human-in-the-Loop Design

The agent supports human judgment rather than replacing it.

It can:

* Gather evidence
* Discover dependencies
* Identify affected systems
* Surface risks
* Identify missing information
* Recommend testing
* Identify relevant system owners

It does not:

* Approve production changes
* Deploy changes
* Modify enterprise systems autonomously
* Treat uncertain risks as confirmed facts

High-risk or ambiguous findings are escalated for human review.

## Technology

* **AWS Strands Agents**
* **Amazon Bedrock**
* **Anthropic Claude**
* **Python**
* **Salesforce**
* **Microsoft Power Automate**
* **Microsoft Power BI**
* **Microsoft Power Apps**
* **Git**
* **GitHub**

## Current Project Structure

```text
agents-for-humans/
|
|-- agent.py
|-- enterprise_data.json
|-- README.md
|-- LICENSE
|-- .gitignore
```

## Current Data Model

For the prototype, `enterprise_data.json` represents the organization's known enterprise architecture and dependencies.

This allows the agent to demonstrate cross-platform investigation without requiring access to production enterprise systems.

Future versions can replace or supplement the synthetic data layer with live APIs and metadata sources.

## Planned Capabilities

Planned development includes:

* Multiple investigation tools
* Deeper Salesforce metadata inspection
* Power Automate dependency analysis
* Power BI dependency analysis
* Power Apps dependency analysis
* Cross-system dependency traversal
* Security and authentication impact analysis
* Data-classification checks
* Missing-owner detection
* Change-risk scoring
* Structured blast-radius reports
* Human approval workflows
* Interactive user interface
* AWS AgentCore deployment
* Architecture visualization
* Additional enterprise-system connectors

## Example Output

A completed assessment may look like:

```text
CHANGE IMPACT ASSESSMENT

Proposed Change:
Salesforce Membership Status
Picklist -> Calculated Field

Overall Risk:
HIGH

Known Dependencies:
- Power Automate: Membership Renewal Workflow
- Power BI: Membership Dashboard
- Power Apps: Membership Administration App

Potential Impact:
- Workflow conditions may require validation
- Reporting logic may need regression testing
- Application behavior may need to be reviewed

Human Review:
- Salesforce Administrator
- Power Platform Administrator
- Reporting Owner

Recommended Action:
Test the change and all known downstream dependencies
in a non-production environment before deployment.
```

## Roadmap

### Phase 1 — Working Agent

* [x] Configure AWS
* [x] Install Strands Agents
* [x] Connect to Amazon Bedrock
* [x] Invoke Claude successfully
* [x] Create first custom Strands tool
* [x] Add external enterprise dependency data
* [x] Perform first cross-platform blast-radius analysis

### Phase 2 — Multi-Step Investigation

* [ ] Add Salesforce metadata tool
* [ ] Add Power Automate investigation tool
* [ ] Add Power BI investigation tool
* [ ] Add Power Apps investigation tool
* [ ] Allow the agent to choose investigation paths dynamically

### Phase 3 — Risk Intelligence

* [ ] Separate known evidence from inferred risk
* [ ] Add structured risk scoring
* [ ] Detect missing owners and undocumented dependencies
* [ ] Generate recommended validation plans
* [ ] Add human approval checkpoints

### Phase 4 — Deployment and Demo

* [ ] Deploy using AWS AgentCore
* [ ] Build demo interface
* [ ] Create architecture diagram
* [ ] Record hackathon demonstration
* [ ] Publish final repository documentation

## License

This project is released under the **MIT License**.

## Hackathon

Built for the **Agents for Humans Hackathon** using AWS Strands Agents.

The project demonstrates how an AI agent can help humans understand the potential consequences of enterprise technology changes before those changes reach production.
