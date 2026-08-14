import json
import shutil
import subprocess
from pathlib import Path

from strands import Agent, tool

DATA_FILE = Path(__file__).parent / "enterprise_data.json"


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def load_enterprise_data():
    """
    Load the enterprise dependency catalog from JSON.
    """

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def find_catalog_component(
    system_name: str,
    field_api_name: str
) -> str | None:
    """
    Resolve a catalog component name from a field API name.
    """

    components = (
        load_enterprise_data()
        .get("systems", {})
        .get(system_name, {})
        .get("components", {})
    )

    for component_name, component in components.items():
        if component.get("api_name") == field_api_name:
            return component_name

    return None


# =========================================================
# TOOL 1: FIND DOWNSTREAM DEPENDENCIES
# =========================================================

@tool
def get_system_dependencies(
    system_name: str,
    component_name: str
) -> str:
    """
    Find known downstream dependencies for a component
    in an enterprise system.

    Use this tool to discover which systems, applications,
    reports, or automations depend on a component.
    """

    enterprise_data = load_enterprise_data()

    try:
        component = (
            enterprise_data["systems"]
            [system_name]
            ["components"]
            [component_name]
        )

        result = {
            "source": "Enterprise Dependency Catalog",
            "system": system_name,
            "component": component_name,
            "type": component.get("type"),
            "data_classification": component.get(
                "data_classification"
            ),
            "owner": component.get("owner"),
            "dependencies": component.get(
                "dependencies",
                []
            )
        }

        return json.dumps(
            result,
            indent=2
        )

    except KeyError:
        return (
            f"No dependency information was found for "
            f"{component_name} in {system_name}."
        )


# =========================================================
# TOOL 2: INVESTIGATE AN ENTERPRISE COMPONENT
# =========================================================

@tool
def get_component_details(
    system_name: str,
    component_name: str
) -> str:
    """
    Investigate a specific enterprise component.

    Returns known information including:
    - component type
    - owner
    - criticality
    - purpose
    - fields used
    - human review requirements
    """

    enterprise_data = load_enterprise_data()

    try:
        component = (
            enterprise_data["systems"]
            [system_name]
            ["components"]
            [component_name]
        )

        result = {
            "source": "Enterprise Dependency Catalog",
            "system": system_name,
            "component": component_name,
            "type": component.get("type"),
            "owner": component.get("owner"),
            "criticality": component.get(
                "criticality"
            ),
            "purpose": component.get(
                "purpose"
            ),
            "uses_fields": component.get(
                "uses_fields",
                []
            ),
            "human_review_required": component.get(
                "human_review_required",
                False
            )
        }

        return json.dumps(
            result,
            indent=2
        )

    except KeyError:
        return (
            f"No detailed information was found for "
            f"{component_name} in {system_name}."
        )


# =========================================================
# TOOL 3: LIVE SALESFORCE FIELD METADATA
# =========================================================

@tool
def get_salesforce_field_metadata(
    object_name: str,
    field_api_name: str
) -> str:
    """
    Retrieve live Salesforce metadata for a field.

    Use this tool when investigating a Salesforce field.

    Returns live metadata including:
    - field label
    - API name
    - field type
    - updateable status
    - createable status
    - nullability
    - calculated status
    - restricted picklist status
    - current picklist values
    """

    sf_path = shutil.which("sf")

    if not sf_path:
        return (
            "Salesforce CLI could not be found on PATH. "
            "Live Salesforce metadata is unavailable."
        )

    command = [
        sf_path,
        "sobject",
        "describe",
        "--sobject",
        object_name,
        "--target-org",
        "hackathon",
        "--json"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        metadata = json.loads(
            result.stdout
        )

        fields = metadata["result"]["fields"]

        for field in fields:

            if field.get("name") == field_api_name:

                picklist_values = []

                for value in field.get(
                    "picklistValues",
                    []
                ):
                    if value.get("active"):
                        picklist_values.append(
                            value.get("value")
                        )

                field_metadata = {
                    "source": (
                        "Live Salesforce "
                        "Developer Edition Metadata"
                    ),
                    "object": object_name,
                    "label": field.get("label"),
                    "api_name": field.get("name"),
                    "type": field.get("type"),
                    "custom": field.get("custom"),
                    "updateable": field.get(
                        "updateable"
                    ),
                    "createable": field.get(
                        "createable"
                    ),
                    "nillable": field.get(
                        "nillable"
                    ),
                    "calculated": field.get(
                        "calculated"
                    ),
                    "restricted_picklist": field.get(
                        "restrictedPicklist"
                    ),
                    "picklist_values": picklist_values
                }

                return json.dumps(
                    field_metadata,
                    indent=2
                )

        return (
            f"Field {field_api_name} was not found "
            f"on Salesforce object {object_name}."
        )

    except subprocess.CalledProcessError as error:
        return (
            "Salesforce CLI returned an error:\n"
            f"{error.stderr}"
        )

    except json.JSONDecodeError:
        return (
            "Salesforce CLI returned output that "
            "could not be parsed as JSON."
        )

    except KeyError:
        return (
            "Salesforce metadata was returned, but "
            "the expected field information was missing."
        )


# =========================================================
# CREATE THE STRANDS AGENT
# =========================================================

agent = Agent(

    tools=[
        get_system_dependencies,
        get_component_details,
        get_salesforce_field_metadata
    ],

    system_prompt="""
You are an Enterprise Change Impact Agent.

Your purpose is to investigate proposed changes to
enterprise systems before those changes are deployed.

Your primary objective is to identify the potential
cross-platform blast radius of a proposed change.

You have access to multiple evidence sources:

1. Live Salesforce metadata.
2. An enterprise dependency catalog.
3. Detailed information about downstream enterprise
   components.

==================================================
INVESTIGATION PROCESS
==================================================

When a proposed change involves Salesforce:

1. Use get_salesforce_field_metadata to retrieve
   live metadata about the Salesforce field.

2. Use get_system_dependencies to identify known
   downstream dependencies.

3. Use get_component_details to investigate each
   relevant downstream component.

4. Check downstream components for additional known
   dependencies when appropriate.

5. Combine the evidence into a structured
   change-impact assessment.

Live Salesforce metadata should take precedence over
synthetic catalog data when determining the CURRENT
properties of a Salesforce field.

Examples include:

- current field type
- current updateability
- current createability
- current nullability
- current picklist values
- current calculated status

==================================================
EVIDENCE RULES
==================================================

Separate findings into the following categories.

--------------------------------------------------
1. KNOWN IMPACT
--------------------------------------------------

Include ONLY facts explicitly returned by tools.

Examples of known evidence include:

- Salesforce reports the current field as a picklist.
- Salesforce reports the current field as updateable.
- The enterprise catalog lists a Power Automate flow
  as a downstream dependency.
- The enterprise catalog lists a component as High
  criticality.
- The enterprise catalog identifies an owner.

Do NOT include:

- assumptions
- predictions
- typical platform behavior
- inferred failure modes
- properties of a proposed future state that have
  not been confirmed by tools

If a statement uses reasoning such as:

- may
- might
- could
- likely
- typically
- generally

it normally belongs under POTENTIAL RISK or
NEEDS VALIDATION rather than KNOWN IMPACT.

IMPORTANT:

If Salesforce metadata reports a field as
"updateable" or "createable", state exactly that.

Do not automatically conclude that every user,
automation, or integration can write to the field.

Actual write access may also depend on:

- permissions
- field-level security
- profiles
- permission sets
- integration configuration
- runtime context

--------------------------------------------------
2. POTENTIAL RISK
--------------------------------------------------

Include reasonable consequences that could result
from the proposed change.

These are hypotheses, NOT confirmed failures.

Use conditional language such as:

- may
- might
- could
- if
- potentially

For example:

If a proposed calculated field becomes non-writable,
a workflow that currently writes to the field could
require redesign.

Do not say that such a workflow WILL fail unless
tool evidence confirms the relevant behavior.

--------------------------------------------------
3. NEEDS VALIDATION
--------------------------------------------------

Clearly identify information that cannot be confirmed
using currently available evidence.

Examples include:

- undocumented dependencies
- unknown workflow conditions
- whether a Power Automate flow reads or writes
- whether a Power Apps control edits a field
- unknown proposed formulas
- unknown proposed field behavior
- missing owners
- incomplete dependency-catalog coverage
- Salesforce-native dependencies not yet inspected

When comparing the current state to a proposed future
state, only the CURRENT state may be treated as known
evidence unless a tool explicitly confirms properties
of the proposed state.

Do not place predicted properties of a proposed
configuration under KNOWN IMPACT.

--------------------------------------------------
4. HUMAN REVIEW
--------------------------------------------------

Identify owners or teams that should evaluate the
change before production deployment.

Use owners returned by tools whenever available.

Do not approve the change on their behalf.

==================================================
COMPLETENESS RULES
==================================================

Never claim:

- every dependency has been discovered
- the entire enterprise has been investigated
- no other dependencies exist
- the investigation is universally complete

Instead use wording such as:

"All known dependencies returned by available tools
have been investigated."

The assessment status should use wording such as:

"Known dependency investigation complete —
this change has not been approved or deployed."

Always acknowledge that:

- undocumented dependencies may exist
- metadata sources may have incomplete coverage
- systems outside the available catalog may exist
- additional investigation may be necessary

==================================================
SAFETY AND HUMAN CONTROL
==================================================

You MAY:

- investigate
- retrieve metadata
- gather evidence
- discover known dependencies
- identify affected systems
- surface potential risks
- identify uncertainty
- recommend testing
- recommend mitigation
- identify human reviewers

You MUST NOT:

- approve production changes
- deploy changes
- modify enterprise systems
- claim uncertain information is confirmed
- present inferred technical behavior as fact

Important changes require human review.

==================================================
OUTPUT FORMAT
==================================================

Produce a clear structured assessment containing:

CHANGE IMPACT ASSESSMENT

Proposed Change

Assessment Status:
"Known dependency investigation complete —
this change has not been approved or deployed."

Current State / Change Summary

1. KNOWN IMPACT

Only confirmed tool evidence.

2. POTENTIAL RISK

Clearly labeled reasoned hypotheses.

3. NEEDS VALIDATION

Unknowns and missing evidence.

4. HUMAN REVIEW REQUIRED

Owners and relevant responsibilities.

5. RECOMMENDED TESTING BEFORE DEPLOYMENT

Practical validation steps.

6. SCOPE OF INVESTIGATION

Explicitly state:

"All known dependencies returned by available tools
have been investigated. Systems, integrations, or
components not represented in available evidence
remain explicit uncertainty."

End by clearly stating that the assessment does not
constitute approval to deploy.
"""
)


# =========================================================
# DEMO CHANGE REQUEST
# =========================================================

def analyze_change(
    object_name: str,
    field_api_name: str,
    proposed_change: str,
    system_name: str = "Salesforce",
    catalog_component_name: str | None = None
) -> str:
    """
    Run a change-impact investigation and return
    the final agent response as text.
    """

    catalog_name = (
        catalog_component_name
        or find_catalog_component(
            system_name,
            field_api_name
        )
    )

    if catalog_name:
        catalog_instruction = (
            f"For the enterprise dependency catalog, "
            f"look up the component named:\n\n"
            f"{catalog_name}\n\n"
            f"in system:\n\n"
            f"{system_name}"
        )
    else:
        catalog_instruction = (
            f"No catalog mapping was found for "
            f"{field_api_name} in {system_name}. "
            f"Use get_system_dependencies with the "
            f"best matching component name if one "
            f"exists in the catalog."
        )

    prompt = f"""
We are considering a change to the following
Salesforce field:

Object:
{object_name}

API Name:
{field_api_name}

Proposed Change:
{proposed_change}

Investigate the potential cross-platform blast
radius of this proposed change.

Use live Salesforce metadata wherever available.

Investigate:

- current Salesforce field metadata
- known downstream dependencies
- purpose of affected components
- criticality of affected components
- known component owners
- potential risks
- information that still requires validation
- required human review
- recommended testing before deployment

{catalog_instruction}

Do not approve or deploy the proposed change.
"""

    result = agent(prompt)

    return str(result)


if __name__ == "__main__":
    print(
        analyze_change(
            object_name="Contact",
            field_api_name="Membership_Status__c",
            proposed_change=(
                "Change Membership Status from a "
                "picklist to a calculated field."
            )
        )
    )