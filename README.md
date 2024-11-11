# Railway Streamlit Template

This is a template for deploying a streamlit app on [Railway](https://railway.app/) that has built-in user authentication. 

## Project Layout

```plaintext
revops_streamlit_tool/
├── app/                        # Assets and Python scripts for site
│   ├── .streamlit              # Streamlit configuration  
│   ├── local/                  # Sample verion of production files
│   └── pageFiles/              
│     └── module/               # Python module
│       └── general.py          
│   ├── Home.py                 # .py file that creates site
├── railway.json                # Defines build instructions for railway
├── python-version.txt          # Defines python version used in production
├── requirements.txt            # Dependencies for the project
└── README.md                   # Project overview and instructions
```

#### Home.py

This python file is the heart of the streamlit app and performs several crutial functions:

First, it manages user authentication and login using the [streamlit-authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) package.

Second, it generates the navigation system based on user's roles and permissions. As such, all [Page objects](https://docs.streamlit.io/develop/api-reference/navigation/st.page) are defined here.

# FAQ

## How does Page Rendering Work?

You may have noticed that some streamlit items are rendered on the Home.py page in the navigation system section. This is because of how the streamlit app is rendered.

Technically, this is a one page app were all pages are rendered on Home.py based on which page is selected by the user in the navigation bar. This means that anything added to Home.py (i.e. a title like "Home") would show up on every page on the top before the page specific items.

Having a one-page design allows us to have a centralized authentication system that can be used across all pages. Individal pages can be defined by a python file and are only loaded/painted onto the screen when selected by the user. However, some items related to the authenticaion system need to remain on Home.py so that they can access the authentical object. To acomplish this, The reset password widget, register user widget, and loggout button are all dynamically rendered on the Home.py page itself the user has selected a specific page (e.g. **Change Passsword** widget is loaded if page is **Manage Account**)

**Anything that doesn't need to be on Home.py should be defined on the Page.py file that needs**


```python
Render order:
-----------------------
|    Home.py Items     |
-----------------------
|    Page.py Items     |
-----------------------
```

## Creating New Pages

1. Create a .py file in the `pageFiles/ ` directory
2. On Home.py, create a new Page Object like this -- P.s. check out the [material icons](https://fonts.google.com/icons)

```python
MyPage = st.Page("pageFiles/my_page.py",
                title="Edit Customer Access",
                icon=":material/group:")
```
3. Sections in the navigation panel are defined by a dictionary of lists, so add your page to the appropriate list for it to show up. Make sure to consider roles, topic, etc. when choosing a propper location.

```python
# Adding MyPage to pages in "My Folder" section
page_dict["My Folder"] = [Page1,Page2,MyPage]

# Adding page based on defined role/permissions
if 'admin' in ROLES:
    page_dict["Admin Pages"].append(MyPage)
```