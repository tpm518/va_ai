import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize Streamlit app with a title
st.title("🤖 AI Chatbot")

# Define system prompt
SYSTEM_PROMPT = """You are a virtual assistant, whose job it is to manage an AirBnB property and answer all guest messages.
You are friendly, precise, and helpful in your responses. Here is some information about the property:

Address: 700 Hume St, Apt 700, Nashville, TN 37208
Check-in time: 4:00 PM
Check-out time: 10:00 AM
Cohost Names: Tom Murray, Gordon Wolf, Cortlandt Schuyler, Michelle King
Amenities: Pool (seasonal), Fitness Center, Free Private Parking, Fast Free WiFi, Smart TV, Washer/Dryer,
Central A/C, Mixology Kit, Fully Stocked Kitchen, Coffee Maker, and Heat
Nearby Attractions: Broadway, The Ryman Auditorium, The Grand Ole Opry,
Hattie B's Hot Chicken, Biscuit Love, Husk, Martin's BBQ, Biscuit
Check-in Instructions: You will be provited with the complex gate code on the day of your arrival, in addition
to the access code for the elctric lock. Once you are in the apartment, you can grab the key fob off the kitchen counter and use that to open the private parking lot gate.
Please remember to lock the door(s) when you are out. The Wifi is "Repeat Rentals Guest".
Please do not hesitate to reach out if you need ANYTHING at all! Safe Travels in!
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat history (excluding system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Prepare messages for API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                temperature=0.2,  # Hardcoded temperature value
            )
            response_content = response.choices[0].message.content
            
            st.markdown(response_content)
            
            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": response_content}
            )

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.experimental_rerun()
