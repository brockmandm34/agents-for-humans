# Enterprise Change Impact Agent

An AI-powered enterprise change impact and blast-radius analysis agent built with **AWS Strands Agents** and **Amazon Bedrock**.

Built for the **Agents for Humans Hackathon**.

**Track:** Pro Agents

## Problem

Enterprise systems rarely operate in isolation.

A seemingly small change to a field, API, workflow, data source, authentication method, or business rule can affect:

* Downstream automations
* Reports and dashboards
* Integrations
* AI agents
* Security controls
* Business processes
* Data handling
* Other teams and system owners

The challenge is that these dependencies are often spread across multiple platforms and understood by different people.

Before a change is deployed, teams may not know its full **blast radius**.

## Solution

The **Enterprise Change Impact Agent** investigates a proposed system change before deployment.

The agent uses tools to gather information about the affected system and then evaluates potential downstream consequences.

It is designed to answer questions such as:

* What systems depend on the component being changed?
* Which automations could fail?
* Which dashboards or reports could be affected?
* Are integrations dependent on the current configuration?
* Who owns the affected systems?
* Does the change introduce security or data-handling concerns?
* Which risks require human review before deployment?

The agent does **not** approve enterprise changes.

Its purpose is to gather evidence, identify risk, explain the potential blast radius, and help a human make a better-informed decision.

## Example

A user proposes:

> Change the Salesforce `Membership Status` field from a picklist to a calculated field.

The agent can investigate known dependencies and identify potential impacts such as:

* A Power Automate renewal workflow that depends on existing field values
* A Power BI membership dashboard that filters on the field
* A Zapier integration that uses membership status to synchronize community access
* Business owners who should review the proposed change

The result is a structured change-impact assessment showing the potential blast radius and recommended next steps.

## How It Works

```text
Proposed Enterprise Change
          |
          v
 Enterprise Change Impact Agent
          |
          v
   Strands Agent Tool Calls
          |
          +--> System Dependencies
          |
          +--> Automations
          |
          +--> Integrations
          |
          +--> Data Classification
          |
          +--> Security Controls
          |
          +--> Business Owners
          |
          v
   Evidence + AI Reasoning
          |
          v
 Change Impact Assessment
          |
          v
     Human Decision
```

## Current Capabilities

The current prototype can:

* Run a Strands agent locally
* Connect to Amazon Bedrock
* Invoke Anthropic Claude through Bedrock
* Define custom Python tools for the agent
* Allow the agent to autonomously select and use tools
* Retrieve known enterprise dependencies
* Analyze the potential downstream impact of a proposed change
* Identify areas requiring human review

## Planned Capabilities

Development will expand the agent to support:

* Multiple enterprise systems
* External enterprise configuration data
* Dependency discovery
* Automation impact analysis
* Data classification checks
* Security and authentication impact analysis
* Business-owner identification
* Risk scoring
* Structured blast-radius reports
* Human approval and escalation workflows
* AWS AgentCore deployment
* A demonstration interface

## Technology

* **AWS Strands Agents**
* **Amazon Bedrock**
* **Anthropic Claude**
* **Python**
* **Git / GitHub**

## Human-in-the-Loop Design

The agent is intended to support human judgment, not replace it.

It can:

* Investigate
* Identify dependencies
* Surface risks
* Explain potential consequences
* Recommend next actions

It does not independently approve or deploy enterprise changes.

High-risk or ambiguous findings are surfaced for human review.

## Project Status

🚧 **In active development**

Current milestone:

* AWS environment configured
* Strands Agents installed
* Amazon Bedrock connected
* Claude successfully invoked
* First custom Strands tool working
* Initial enterprise dependency analysis prototype working
* Source code tracked in GitHub

## Hackathon

Built for **Agents for Humans**, using AWS Strands Agents to create an AI-powered agent that helps humans make better enterprise change decisions.
