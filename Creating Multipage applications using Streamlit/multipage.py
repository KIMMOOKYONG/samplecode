"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
이 파일은 객체 지향 프레임워크를 통해 여러 Streamlit 애플리케이션을 생성하기 위한 프레임워크입니다. 
"""

# Import necessary libraries 
import streamlit as st

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project

        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append(
            {
                "title": title, 
                "function": func
            }
        )

    def run(self):
        # Drodown to select the page to run  
        # 실행할 페이지를 선택한다.
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page.get('title', "")
        )

        # run the app function 
        # () 는 함수를 실행한다는 의미이다.
        page.get('function')()
