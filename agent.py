import json
from strands import Agent, tool


def load_enterprise_data():
    """Load enterprise architecture data from the JSON file."""
    with open("enterprise_data.json", "r") as file:
        return json.load(file)


@tool
def get_system_dependencies(system_name: str, component_name: str) -> str:
    """
    Find known downstream dependencies for a component
    in an enterprise system.
    """

    enterprise_data = load_enterprise_data()

    try:
        component = enterprise_data["systems"][system_name]["components"][component_name]

        result = {
            "system": system_name,
            "component": component_name,
            "type": component.get("type"),
            "data_classification": component.get("data_classification"),
            "owner": component.get("owner"),
            "dependencies": component.get("dependencies", [])
        }

        return json.dumps(result, indent=2)

    except KeyError:
        return (
            f"No dependency information was found for "
            f"{component_name} in {system_name}."
        )


@tool
def get_component_details(system_name: str, component_name: str) -> str:
    """
    Investigate a specific enterprise component and return its
    owner, purpose, criticality, fields used, and human-review requirements.
    """

    enterprise_data = load_enterprise_data()

    try:
        component = enterprise_data["systems"][system_name]["components"][component_name]

        result = {
            "system": system_name,
            "component": component_name,
            "type": component.get("type"),
            "owner": component.get("owner"),
            "criticality": component.get("criticality"),
            "purpose": component.get("purpose"),
            "uses_fields": component.get("uses_fields", []),
            "human_review_required": component.get(
                "human_review_required",
                False
            )
        }

        return json.dumps(result, indent=2)

    except KeyError:
        return (
            f"No detailed information was found for "
            f"{component_name} in {system_name}."
        )


agent = Agent(
    tools=[
        get_system_dependencies,
        get_component_details
    ],
    system_prompt="""
    You are an Enterprise Change Impact Agent.

    Your job is to investigate proposed changes to enterprise systems
    before those changes are deployed.

    You should perform a multi-step investigation.

    First, identify the component being changed and use available tools
    to discover its known downstream dependencies.

    Then investigate relevant downstream components using available tools
    before producing your final assessment.

    Separate your findings into:

    1. KNOWN IMPACT
        Include ONLY facts explicitly returned by tools.
        Do not include assumptions, typical platform behavior,
        predictions, or inferred failure modes in this section.
        If a statement uses reasoning such as "may", "might",
        "likely", "typically", or "could", place it under
        POTENTIAL RISK or NEEDS VALIDATION instead.

    2. POTENTIAL RISK
       Reasonable risks created by the proposed change.
       Clearly identify these as potential rather than confirmed failures.

    3. NEEDS VALIDATION
       Questions or unknowns that cannot be confirmed using available evidence.
       Do not claim that an investigation is "complete" or that all dependencies
        have been discovered.

        Instead, state that all KNOWN dependencies returned by available tools
        have been investigated.

        Undocumented dependencies, missing metadata, or systems outside the
        available enterprise catalog must be identified as remaining uncertainty.

        When describing platform behavior that was not returned by a tool,
        use conditional language such as "may", "could", or "if".
        Do not state inferred technical behavior as confirmed fact.

    4. HUMAN REVIEW
       Owners or teams that should review the proposed change.

    Do not invent enterprise dependencies that are not returned by tools.

    Do not approve or deploy changes yourself.

    Recommend appropriate testing and validation steps before production.
    """
)


agent("""
We are considering changing the Salesforce Membership Status field
from a picklist to a calculated field.

Investigate the potential blast radius of this change.

Identify:
- known downstream dependencies
- the purpose and criticality of affected components
- known owners
- potential risks
- items that still need validation
- required human review
- recommended testing before deployment

Use your tools to investigate the affected components before answering.
""")