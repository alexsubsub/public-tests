"""
Test app for get_user_email() function on Streamlit Cloud
This is a simple standalone app to test if user email detection works.
"""

import streamlit as st
import sys
from datetime import datetime

def get_user_email() -> str:
    """
    Get the email of the logged-in user from Streamlit Cloud. 
    This function only works when the app is deployed on Streamlit Cloud
    
    Returns:
        str: The user's email address if available, otherwise "Unknown User"
    
    """
    try:
        # Try to get user info from st.experimental_user (Streamlit 1.36.0)
        if hasattr(st, 'experimental_user'):
            user_info = st.experimental_user
            return user_info.get('email', 'Unknown User')
        # Fallback to st.user for newer versions
        elif hasattr(st, 'user'):
            user_info = st.user
            return user_info.get('email', 'Unknown User')
        else:
            return "Unknown User"
    except Exception as e:
        # If there's any error accessing user info, return Unknown
        st.warning(f"Could not retrieve user information: {e}")
        return "Unknown User"

def main():
    st.set_page_config(
        page_title="User Email Test",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 User Email Detection Test")
    st.markdown("---")
    
    st.markdown("""
    This app tests the `get_user_email()` function to see if it can detect user emails 
    when deployed on Streamlit Cloud.
    
    **Note:** This function only works when deployed on Streamlit Cloud, not in local development.
    """)
    
    # Test the function
    st.subheader("🔍 Test Results")
    
    with st.spinner("Testing user email detection..."):
        user_email = get_user_email()
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Detected Email", user_email)
    
    with col2:
        if user_email != "Unknown User":
            st.success("✅ Email detection working!")
        else:
            st.error("❌ Email detection not working")
    
    # Show detailed information
    st.subheader("📊 Detailed Information")
    
    # Check which method is available
    st.write("**Available Streamlit user methods:**")
    
    experimental_user_available = hasattr(st, 'experimental_user')
    user_available = hasattr(st, 'user')
    
    st.write(f"- `st.experimental_user`: {'✅ Available' if experimental_user_available else '❌ Not available'}")
    st.write(f"- `st.user`: {'✅ Available' if user_available else '❌ Not available'}")
    
    # Show raw user info if available
    if experimental_user_available:
        try:
            user_info = st.experimental_user
            st.write("**Raw user info from `st.experimental_user`:**")
            st.json(user_info)
        except Exception as e:
            st.write(f"Error accessing `st.experimental_user`: {e}")
    
    if user_available:
        try:
            user_info = st.user
            st.write("**Raw user info from `st.user`:**")
            st.json(user_info)
        except Exception as e:
            st.write(f"Error accessing `st.user`: {e}")
    
    # Environment information
    st.subheader("🌍 Environment Information")
    
    env_info = {
        "Streamlit Version": st.__version__,
        "Python Version": sys.version,
        "Current Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "Deployment": "Streamlit Cloud" if "streamlit.app" in st.get_option("server.baseUrlPath") else "Local Development"
    }
    
    for key, value in env_info.items():
        st.write(f"**{key}:** {value}")
    
    # Instructions
    st.subheader("📝 Instructions")
    st.markdown("""
    1. **Deploy this app to Streamlit Cloud** as a public app
    2. **Access the app** from Streamlit Cloud (not locally)
    3. **Check if your email is detected** in the test results above
    4. **Share the results** - if it works, you'll see your email address
    5. **If it doesn't work**, you'll see "Unknown User" and error messages
    
    **Important:** This test only works when the app is deployed on Streamlit Cloud, 
    not when running locally with `streamlit run`.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("*This is a test app for the `get_user_email()` function.*")

if __name__ == "__main__":
    main()
