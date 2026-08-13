import streamlit as st

from agent import analyze_change


st.set_page_config(
    page_title="Enterprise Change Impact Agent",
    page_icon="🔍",
    layout="wide"
)


st.title("🔍 Enterprise Change Impact Agent")

st.write(
    "Analyze the potential cross-platform blast radius "
    "of a proposed enterprise system change."
)

st.info(
    "The agent investigates known dependencies and risks. "
    "It does not approve or deploy changes."
)


with st.form("change_request_form"):

    system = st.selectbox(
        "Source System",
        ["Salesforce"]
    )

    object_name = st.text_input(
        "Object",
        value="Contact"
    )

    component_name = st.text_input(
        "Field / Component",
        value="Membership_Status__c"
    )

    proposed_change = st.text_area(
        "Proposed Change",
        value=(
            "Change Membership Status from a "
            "picklist to a calculated field."
        ),
        height=120
    )

    submitted = st.form_submit_button(
        "Analyze Change",
        type="primary"
    )


if submitted:

    st.divider()

    st.subheader("Change Request")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Source System",
            system
        )

    with col2:
        st.metric(
            "Object",
            object_name
        )

    with col3:
        st.metric(
            "Component",
            component_name
        )

    st.write(
        f"**Proposed Change:** {proposed_change}"
    )

    with st.spinner(
        "Investigating Salesforce metadata and "
        "cross-platform dependencies..."
    ):

        try:

            assessment = analyze_change(
                object_name=object_name,
                field_api_name=component_name,
                proposed_change=proposed_change
            )

            st.divider()

            st.subheader(
                "Change Impact Assessment"
            )

            st.markdown(
                assessment
            )

        except Exception as error:

            st.error(
                "The change-impact investigation "
                "could not be completed."
            )

            st.exception(error)