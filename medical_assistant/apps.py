import streamlit as st
import uuid
import json

# Assuming these imports are available and properly set.
from rag import rag
import db

def main():
    st.title("Question Handling Application")

    # Section for asking questions
    st.header("Ask a Question")
    question = st.text_input("Enter your question here:")

    if st.button("Submit Question"):
        if not question:
            st.error("No question provided.")
        else:
            conversation_id = str(uuid.uuid4())
            answer_data = rag(question)

            # Display the result
            st.success("Question Submitted Successfully!")
            st.write("Conversation ID:", conversation_id)
            st.write("Question:", question)
            st.write("Answer:", answer_data.get("answer"))

            # Save the conversation to the database
            db.save_conversation(
                conversation_id=conversation_id,
                question=question,
                answer_data=answer_data,
            )

            st.session_state.conversation_id = conversation_id
            st.session_state.question = question

    # Section for providing feedback
    if 'conversation_id' in st.session_state:
        feedback = st.radio("How would you rate the answer?", (1, -1), index=0)

        if st.button("Submit Feedback"):
            if feedback not in [1, -1]:
                st.error("Invalid feedback.")
            else:
                conversation_id = st.session_state.conversation_id
                db.save_feedback(
                    conversation_id=conversation_id,
                    feedback=feedback,
                )
                st.success(f"Feedback received for conversation {conversation_id}: {feedback}")

if __name__ == "__main__":
    main()