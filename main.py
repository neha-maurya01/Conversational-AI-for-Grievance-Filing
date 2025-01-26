import streamlit as st
from engine import predict_category

# Multi-threaded conversation handling
def add_to_conversation(grievance, category, score):
    conversation_item = {
        'grievance': grievance,
        'category': category,
        'score': score
    }
    st.session_state.conversation.append(conversation_item)


if __name__ == '__main__':
    # Sample data for demonstration (both English and Hindi grievances)
    sample_grievances = [
        "There's a broken streetlight on Elm Street.",
        "सड़क पर गड्ढा है, कृपया इसे ठीक करें।",
        "The garbage bins in Market Street are overflowing.",
        "पानी की पाइपलाइन में लीकेज हो रहा है, कृपया इसे ठीक करें।",
        "The local water supply has been contaminated with harmful chemicals, making it unsafe for consumption.",
        "सड़कों पर कचरा पड़ा हुआ है, इसे तुरंत साफ किया जाए।"
    ]

    # Initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Streamlit UI
    st.title("Grievance Filing System")

    # Select language
    language = st.radio("Select Language", ("English", "Hindi"))

    # Get user grievance input
    grievance_input = st.text_area("Enter your grievance:")

    # File grievance button
    if st.button("File Grievance"):
        if grievance_input:
            # Detect language
            p_dept, p_cat, p_score = predict_category(grievance_input)
            add_to_conversation(grievance_input, p_dept, p_score)
            
            st.success("Grievance filed successfully!")
            st.write(f"Predicted Category: {p_dept}")
            st.write(f"Similarity Score: {p_score:.4f}")
                
        else:
            st.error("Please enter a grievance.")

    # Display conversation history
    if st.session_state.conversation:
        st.subheader("Previous Grievances")
        for i, item in enumerate(st.session_state.conversation):
            st.write(f"Grievance {i+1}: {item['grievance']}")
            st.write(f"Category: {item['category']}")
            st.write(f"Similarity Score: {item['score']:.4f}")
            st.write("-" * 50)

    # Display sample grievances
    st.subheader("Sample Grievances")
    for grievance in sample_grievances:
        st.write(f"- {grievance}")

