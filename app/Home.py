import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (LoginError)
from datetime import datetime
import yaml, os
from yaml.loader import SafeLoader
from pageFiles.module.general import get_file, write_file

config = get_file('user_config.yaml')

authenticator = stauth.Authenticate(
config['credentials'],
config['cookie']['name'],
config['cookie']['key'],
config['cookie']['expiry_days']
)

try:
    authenticator.login(single_session = True)
except LoginError as e:
    st.error(e)

if 'roles' not in st.session_state: ROLES = []
else: ROLES = st.session_state['roles'] 


if st.session_state["authentication_status"]: ## Renders Navigation once logged in
    ROLES = st.session_state['roles'] 

    ## Defining all pages

    Manage_Users = st.Page("pageFiles/manage_users.py",title="Manage Users",icon=":material/library_add:")
        
    ManageAccount = st.Page("pageFiles/Manage_account.py",title="Mange Account",icon=":material/settings:",)
            
    ## Creating Navigation

    page_dict = {} # Dict to hold all pages

    page_dict["General"] = [ManageAccount]

    # Adding Pages based on Role:

    if 'admin' in ROLES:
        page_dict["Admin Tools"] = [Manage_Users]

    pg = st.navigation(page_dict)

    ## Rendering dynamic objects based on page selected:

    if pg == ManageAccount: 
        st.title('Manage Your Account')

        if authenticator.reset_password(st.session_state['username'],fields={'Form name':'Change Password'},):
            write_file('user_config.yaml', config)

    if pg == Manage_Users:
        try:
            email_of_registered_user, \
            username_of_registered_user, \
            name_of_registered_user = authenticator.register_user(domains=['rehabpath.com','recovery.com'],clear_on_submit=True,captcha=False,roles=['default'])
            if email_of_registered_user:
                st.success('User registered successfully')
                st.session_state["authentication_status"] = True
                
                write_file('user_config.yaml', config)
        except Exception as e:
            st.error(e)

    pg.run() # Renders selected page