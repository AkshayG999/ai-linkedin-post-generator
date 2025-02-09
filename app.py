import time
import os
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from exa_py import Exa
import clipboard
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
METAPHOR_API_KEY = os.getenv('METAPHOR_API_KEY')

def main():
    # Set page configuration without theme parameter
    st.set_page_config(
        page_title="AI LinkedIn Post Generator",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Add custom theme settings
    st.markdown("""
        <style>
            /* Override default theme to dark */
            .stApp {
                background-color: #0E1117;
                color: #E0E0E0;
            }
            
            /* Override default streamlit elements for dark theme */
            .stTextInput, .stSelectbox {
                color: #E0E0E0;
            }
            
            .stMarkdown {
                color: #E0E0E0;
            }
            
            /* Make sure text inputs are visible in dark mode */
            .stTextInput > div > div > input {
                color: #E0E0E0 !important;
                background-color: rgba(17, 17, 17, 0.7) !important;
            }
            
            /* Make select boxes visible in dark mode */
            .stSelectbox > div > div {
                background-color: rgba(17, 17, 17, 0.7) !important;
                color: #E0E0E0 !important;
            }
            
            /* Style select box options */
            .stSelectbox > div > div > div {
                background-color: #1E1E1E !important;
                color: #E0E0E0 !important;
            }
            
            /* Error message styling for dark theme */
            .stAlert > div {
                background-color: rgba(255, 76, 76, 0.2);
                border-color: #FF4C4C;
                color: #E0E0E0;
            }
            
            /* Success message styling for dark theme */
            .element-container > div.stAlert > div[data-baseweb="notification"] {
                background-color: rgba(45, 183, 66, 0.2);
                border-color: #2DB742;
                color: #E0E0E0;
            }
        </style>
    """, unsafe_allow_html=True)

    # Updated CSS styling for dark theme
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            
            /* Main container styling */
            .main {
                padding: 2rem;
                font-family: 'Inter', sans-serif;
                color: #E0E0E0;
            }
            
            /* Card styling */
            .stExpander {
                background: rgba(17, 17, 17, 0.7);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                margin-bottom: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Input fields styling */
            .stTextInput > div > div > input {
                background: rgba(17, 17, 17, 0.7) !important;
                border-radius: 10px;
                border: 2px solid rgba(255, 255, 255, 0.1);
                padding: 10px 15px;
                font-size: 16px;
                color: #E0E0E0;
            }
            
            .stSelectbox > div > div {
                background: rgba(17, 17, 17, 0.7) !important;
                border-radius: 10px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Button styling */
            div.stButton > button:first-child {
                background: linear-gradient(45deg, #0077B5, #00A0DC);
                color: white;
                padding: 12px 24px;
                border-radius: 10px;
                font-weight: 600;
                font-size: 16px;
                border: none;
                box-shadow: 0 4px 6px rgba(0, 123, 255, 0.2);
                transition: all 0.3s ease;
            }
            
            /* Post preview styling */
            .post-preview {
                background: rgba(17, 17, 17, 0.7);
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #0077B5;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                color: #E0E0E0;
            }
            
            /* Headers styling */
            h1, h2, h3 {
                color: #E0E0E0;
                font-family: 'Inter', sans-serif;
                font-weight: 600;
            }
            
            /* Success message styling */
            .success-message {
                padding: 15px;
                border-radius: 10px;
                background-color: rgba(40, 167, 69, 0.2);
                border-left: 5px solid #28a745;
                margin: 10px 0;
                color: #E0E0E0;
            }

            /* Custom elements for dark theme */
            .dark-card {
                background: rgba(17, 17, 17, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 20px;
                color: #E0E0E0;
            }

            .gradient-header {
                background: linear-gradient(45deg, rgba(0, 119, 181, 0.8), rgba(0, 160, 220, 0.8));
                backdrop-filter: blur(10px);
            }
        </style>
    """, unsafe_allow_html=True)

    # Updated header with dark theme
    st.markdown("""
        <div class='gradient-header' style='padding: 20px; border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: #E0E0E0; text-align: center; font-family: Inter, sans-serif;'>
                🤖 AI LinkedIn Post Generator
            </h1>
            <p style='color: #E0E0E0; text-align: center; font-size: 18px;'>
                Transform tech trends into engaging LinkedIn content with AI!
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Hide top header and footer for a cleaner UI
    hide_elements = """
        <style>
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_elements, unsafe_allow_html=True)

    # Initialize session state for generated post
    if "linkedin_post" not in st.session_state:
        st.session_state.linkedin_post = ""

    # Updated Pro Tips section
    with st.expander("💡 Pro Tips for Better Results", expanded=True):
        st.markdown("""
            <div class='dark-card'>
                <h4 style='color: #00A0DC;'>Follow these guidelines:</h4>
                <ul style='list-style-type: none; padding-left: 0; color: #E0E0E0;'>
                    <li>✨ Use specific keywords related to your topic</li>
                    <li>🎯 Choose a post type that aligns with your message</li>
                    <li>🌍 Select appropriate language and length for your audience</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        # Input fields for the LinkedIn post generator
        input_blog_keywords = st.text_input(
            '🔑 **Enter main keywords for your post**', 
            placeholder='e.g., Marketing Trends, Leadership Tips...', 
            help="Use relevant keywords that define the topic of your LinkedIn post."
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            input_linkedin_type = st.selectbox('📝 **Post Type**', (
                'General','How to implements/build', 'How-to Guides', 'Polls', 'Listicles', 
                'Reality Check Posts', 'Job Posts', 'FAQs', 'Checklists/Cheat Sheets'), 
                index=0, help="Choose the format that suits the message you want to deliver.")
        with col2:
            input_linkedin_length = st.selectbox('📏 **Post Length**', 
                # ('1000 words', 'Long Form', 'Short Form'),
                ('Short Form (300-500 words)','Standard 1000 words','Long Form (1500-2000 words)'),
                index=0, 
                help="Decide the length of your post based on its complexity and target audience.")
        with col3:
            input_linkedin_language = st.selectbox('🌐 **Choose Language**', 
                ('English', 'Vietnamese', 'Chinese', 'Hindi', 'Spanish'), 
                index=0, help="Pick the language that resonates best with your audience.")

    # Button to generate the LinkedIn post
    if st.button('🚀 **Generate LinkedIn Post**'):
        if not input_blog_keywords:
            st.error('🚫 **Please provide keywords to generate a LinkedIn post!**')
        else:
            with st.spinner('🤖 Crafting your LinkedIn post...'):
                # Progress bar for user feedback
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(percent_complete + 1)

                # Generate the LinkedIn post
                st.session_state.linkedin_post = generate_linkedin_post(
                    input_blog_keywords, input_linkedin_type, 
                    input_linkedin_length, input_linkedin_language)

    if st.session_state.get("linkedin_post"):
        st.markdown("""
            <div class='post-preview'>
                <h3 style='color: #0077B5;'>📄 LinkedIn Post Preview</h3>
            </div>
        """, unsafe_allow_html=True)
        st.write(st.session_state.linkedin_post)

        # Enhanced action buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button('📋 Copy to Clipboard', key='copy'):
                clipboard.copy(st.session_state.linkedin_post)
                st.markdown("""
                    <div class='success-message'>
                        ✅ Copied to clipboard!
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.download_button(
                label="💾 Download Post",
                data=st.session_state.linkedin_post,
                file_name="linkedin_post.txt",
                mime="text/plain",
                key="download_2"  # Added unique key here
            )


def generate_linkedin_post(input_blog_keywords, input_linkedin_type, input_linkedin_length, input_linkedin_language):
    """ Function to call upon LLM to get the work done. """

    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")

    # If keywords and content both are given.
    if serp_results:
        
        # prompt = f"""As a expert and experienced linkedin content writer, 
        # I will provide you with my 'blog keywords' and 'google search results'.
        # Your task is to write a detailed linkedin post, using given keywords and search results.

        # Follow below guidelines for generating the linkedin post:
        # 1). Write a title, introduction, sections, faqs and a conclusion for the post.
        # 2). Demostrate Experience, Expertise, Authoritativeness, and Trustworthiness with your post.
        # 3). Maintain consistent voice of tone, keep the sentence short and simple for professional audience.
        # 4). Make sure to include important results from the given google serp results.
        # 5). Optimise your response for blog type of {input_linkedin_type}.
        # 6). Important to provide your response in {input_linkedin_language} language.\n

        # blog keywords: '{input_blog_keywords}'\n
        # google serp results: '{serp_results}'
        # """
        
        prompt = f"""As a senior LinkedIn content strategist with expertise in viral business content, 
        I will transform the provided 'blog keywords' and 'google search results' into an engaging LinkedIn post 
        that drives meaningful engagement.

        Primary Inputs:
        - Blog Keywords: '{input_blog_keywords}'
        - Search Results: '{serp_results}'
        - Post Type: {input_linkedin_type}
        - Language: {input_linkedin_language}
        - Post Length: {input_linkedin_length}

        Content Adaptation Based on Length:
        1. Format for {input_linkedin_length}:
        if input_linkedin_length == 'Short Form':
            - Focus on single key message
            - 300-500 words
            - Crisp, direct writing style
            - 2-3 key points maximum
        elif input_linkedin_length == '1000 words':
            - Balanced depth and engagement
            - 1000 words approximately
            - 3-4 detailed sections
            - Complete topic coverage
        else:  # Long Form
            - In-depth analysis
            - 1500-2000 words
            - Multiple detailed sections
            - Comprehensive coverage

        Content Structure:
        1. Hook (Visible Preview)
        - Attention-grabbing opener
        - Problem statement or insight
        - Curiosity generator

        2. Main Content:
        - Title
        - Introduction
        - Core Sections
        - Expert Tips
        - FAQs (if applicable to length)
        - Conclusion with CTA

        Writing Guidelines:
        1. Voice & Style:
        - Professional yet conversational
        - Active voice
        - Clear and concise sentences
        - Industry-appropriate tone

        2. Content Enhancement:
        - Data from search results
        - Industry examples
        - Social proof
        - Engagement elements

        3. Formatting:
        - Strategic line breaks
        - Appropriate emojis
        - Clear section breaks
        - Emphasis on key points

        4. Engagement Elements:
        - Discussion questions
        - Relevant hashtags
        - Call for interactions
        - Value proposition

        Technical Requirements:
        1. Deliver in {input_linkedin_language}
        2. Match {input_linkedin_type} style
        3. Optimize for LinkedIn algorithm
        4. Include proper citations

        Quality Assurance:
        1. E-E-A-T principles
        2. Fact verification
        3. LinkedIn best practices
        4. Global audience consideration
        """
        
        linkedin_post = generate_text_with_exception_handling(prompt)
        return linkedin_post


# Metaphor search function
def metaphor_search_articles(query):
    if not METAPHOR_API_KEY:
        raise ValueError("METAPHOR_API_KEY environment variable not set!")

    metaphor = Exa(METAPHOR_API_KEY)

    try:
        search_response = metaphor.search_and_contents(query, use_autoprompt=True, num_results=5)
        return search_response.results
    except Exception as err:
        st.error(f"Failed in metaphor.search_and_contents: {err}")
        return None


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the LangChain ChatOpenAI model with exception handling.

    Args:
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """
    try:
        chat = ChatOpenAI(
            model="gpt-3.5-turbo",
            # temperature=0.5,
            # top_p=0.95  
        )
        
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=prompt)
        ]
        
        response = chat.invoke(messages)
        return response.content.strip()

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()