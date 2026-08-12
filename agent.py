import json
from strands import Agent, tool


@tool
def get_system_dependencies(system_name: str, component_name: str) -> str:
    """
    Retrieve known dependencies, owners, and data classification
    for a component in an enterprise system.
    """

    with open("enterprise_data.json", "r") as file:
        enterprise_data = json.load(file)

    try:
        component = enterprise_data["systems"][system_name]["components"][component_name]
        return json.dumps(component, indent=2)

    except KeyError:
        return (
            f"No dependency information was found for "
            f"{component_name} in {system_name}."
        )


agent = Agent(
    tools=[get_system_dependencies],
    system_prompt="""
    You are an Enterprise Change Impact Agent.

    Your purpose is to evaluate proposed changes to enterprise systems
    before those changes are deployed.

    When evaluating a proposed change:

    1. Use available tools to gather evidence about the affected system
       and component.

    2. Identify:
       - downstream systems
       - automations
       - integrations
       - reports and dashboards
       - data classification
       - business owners
       - potential operational impacts

    3. Determine the potential blast radius of the proposed change.

    4. Explain:
       - what could be affected
       - why it could be affected
       - what could fail
       - which teams or owners should be involved

    5. Recommend testing, review, or mitigation steps.

    You must not approve or deploy enterprise changes yourself.

    Clearly identify situations where human review or approval is required.

    Base your conclusions on evidence returned from tools.
    If information is missing, say what additional information would
    be needed rather than inventing dependencies.
    """
)


agent("""
We are considering changing the Salesforce Membership Status field
from a picklist to a calculated field.

Assess the potential blast radius of this change.

Tell me:
- what systems or processes may be affected
- why they may be affected
- what could potentially break
- which owners should review the change
- what should be tested before deployment
""")