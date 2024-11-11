import streamlit as st, yaml
from pageFiles.module.general import get_file, write_file

def admin_edit_roles():
    st.markdown('## Edit User Roles')

    # Load credentials
    config = get_file('user_config.yaml')
    usernames = config['credentials']['usernames']
    
    # Select the user to edit
    user_to_edit = st.selectbox("Select a user to edit", list(usernames.keys()))

    if user_to_edit:
        user_info = usernames[user_to_edit]

        st.write(f"Current roles for {user_to_edit}: {user_info.get('roles', [])}")
        
        available_roles = {role for user in config['credentials']['usernames'].values() for role in user.get('roles', [])}

        with st.form("edit_roles_form"):
            selected_roles = st.multiselect(
                "Select roles for the user",
                options=available_roles,
                default=user_info.get('roles', [])
            )
            submitted = st.form_submit_button("Save Changes")

            if submitted:
                # Update roles in the credentials data
                user_info['roles'] = selected_roles
                write_file(config, 'user_config.yaml')
                st.success(f"Roles for {user_to_edit} updated successfully!")

st.divider()
admin_edit_roles()
