import streamlit as st
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import sqlite3
import arrow
import os

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role, path):
    hashed_password = hash_password(password)
    try:
        conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, role, profile_image_url) VALUES (?, ?, ?, ?)",
                  (username, hashed_password, role, path))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        print("Username already exists")
        return False
        

# Sample FAQs
faqs = [
    {"question": "How to reset my password?", "answer": "Go to settings to reset your password."},
    {"question": "Where can I find the user manual?", "answer": "The user manual is available in the help section."}
]

# Authentication
def authenticate(username, password):
    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

# User session management
def user_login(role):
    st.title("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(login_username, login_password):
            st.session_state['username'] = login_username
            st.session_state['role'] = role
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid username or password")

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('/Users/moemmyat/Downloads/ubs_prototype/images', uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join('/Users/moemmyat/Downloads/ubs_prototype/images', uploaded_file.name)
    except Exception as e:
        return None

if 'username' not in st.session_state:
    st.title('User Registration System')
    user_status = st.radio("Are you a new user or a registered user?", ('New User', 'Registered User'))       
    if user_status == 'New User':
        # Streamlit interface for registration
        st.title("User Registration")
        with st.form("user_registration_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                uploaded_file = st.file_uploader("Upload Profile Image", type=['png', 'jpg', 'jpeg'])
                role = st.selectbox("Role", ["User", "Admin"])
                submit_button = st.form_submit_button("Register")

                if submit_button:
                    file_path = save_uploaded_file(uploaded_file)
                    #if uploaded_file==None:
                    #    file_path="/Users/moemmyat/Downloads/ubs_prototype/8.png"
                    if register_user(username, password, role, file_path)==True:
                        st.success("You have successfully registered! Please login again")
                    else:
                        st.error("Registration failed. Please login (username already exists).")

    else:
        role = st.selectbox("Role", ["User", "Admin"])
        user_login(role)

else:
    # Main app
    st.sidebar.title("Welcome to the UBS Diversity, Equity and Inclusion Forum!")
    st.sidebar.write(f"You are now logged in as {st.session_state['role']}.")

    # Navigation
    choice = st.sidebar.selectbox("Main Menu", ["My Profile","FAQ", "Forum","Calendar", "Admin Portal", "Learning","DE&I Chatbot", "Accessment"], index=0)

    if choice =="My Profile":
        st.title("My Profile")
        # Function to fetch user data from the database
        def get_user_data(username):
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')  # Ensure the database path is correct
            c = conn.cursor()
            c.execute("SELECT username, role, profile_image_url, fun_fact, gender, hobbies FROM users WHERE username=?", (username,))
            user_data = c.fetchone()
            conn.close()
            return user_data

        # Streamlit user interface
        def main():
            def load_css():
                    css = """
                            .custom-container {
                                border: 2px solid #696969; /* Green border */
                                padding: 20px;
                                border-radius: 10px;
                                margin-bottom: 20px;
                                background-color: #ADD8E6; /* Light green background */
                                font-size: 18px; /* Larger text */
                                color: #333; /* Darker text color for better readability */
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
                            }
                            .author-style {
                                color: navy;
                                font-size: 24px; /* Larger font size for author */
                            }
                            .time-style {
                                color: #555; /* Darker gray for timestamp */
                                font-size: 16px;
                                text-align: right;
                            }
                            """
                    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

                        # Call this function at the start of your app to load the styles
            load_css()
            # Button to fetch the profile
            user_data = get_user_data(st.session_state['username'])
            if user_data:
                    print(user_data)
                    username, role, profile_image_url, fun_fact, gender, hobbies = user_data
                    if profile_image_url:
                        col1, col2 = st.columns([0.13, 0.9])  # Adjust the ratio as needed for your layout

                        # Display image in the second column (right column)
                        with col2:
                            st.image(profile_image_url)
                    else:
                        st.write("No profile image available.")
                    
                    contributions = "N/A"
                    def profile_update(fun_fact,gender, hobbies,contributions):
                        # Update the profile in the session state
                        st.session_state['fun_fact'] = fun_fact
                        st.session_state['gender'] = gender
                        st.session_state['hobbies'] = hobbies
                        st.session_state['contributions'] = contributions
                        st.success("Profile updated!")
                    # Initialize default values in session state if not already set
                    if 'fun_fact' not in st.session_state:
                        st.session_state['fun_fact'] = fun_fact
                    if 'gender' not in st.session_state:
                        st.session_state['gender'] = gender
                    if 'hobbies' not in st.session_state:
                        st.session_state['hobbies'] = hobbies
                    if 'contributions' not in st.session_state:
                        st.session_state['contributions'] = "Your contributions here"

                    st.write("---")
                    st.subheader(f"Welcome to the app, {username}!")
                    st.markdown(f"<div class='custom-container'><strong>Role:</strong> <span style='color: #1E3566;'>{st.session_state['role']}</span></div>", unsafe_allow_html=True)                    
                    st.markdown(f"<div class='custom-container'><strong>Fun Fact:</strong> <span style='color: #1E3566;'>{st.session_state['fun_fact']}</span></div>", unsafe_allow_html=True)                    
                    st.markdown(f"<div class='custom-container'><strong>Gender:</strong> <span style='color: #1E3566;'>{st.session_state['gender']}</span></div>", unsafe_allow_html=True)                    
                    st.markdown(f"<div class='custom-container'><strong>Hobbies:</strong> <span style='color: #1E3566;'>{st.session_state['hobbies']}</span></div>", unsafe_allow_html=True)                    

                    if 'form_open' not in st.session_state:
                        st.session_state.form_open = False

                    if st.button('Update Profile'):
                        st.session_state.form_open = not st.session_state.form_open

                    if st.session_state.form_open:
                        with st.form("profile_form"):
                            new_fun_fact = st.text_input("What is your fun fact?", st.session_state['fun_fact'])
                            new_gender = st.text_input("What is your gender?", st.session_state['gender'])
                            new_hobbies = st.text_input("What are your hobbies?", st.session_state['hobbies'])
                            submitted = st.form_submit_button("Submit")
                            if submitted:
                                profile_update(new_fun_fact,new_gender,new_hobbies,contributions)
                                conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
                                c = conn.cursor()
                                c.execute('''
                                    UPDATE users SET
                                    fun_fact = ?,
                                    gender = ?,
                                    hobbies = ?
                                    WHERE username = ?
                                ''', (new_fun_fact, new_gender, new_hobbies, st.session_state["username"]))

                                conn.commit()
                                st.session_state.form_open = False

            else:
                    st.error("User not found!")
        main()
    elif choice == "FAQ":
        st.title("Frequently Asked Questions")
        for faq in faqs:
            st.subheader(faq["question"])
            st.write(faq["answer"])

    elif choice == "Calendar":

        if st.session_state['role'] == "Admin":
            edit_bool = True
        else:
            edit_bool = False
        calendar_options = {
            "editable": edit_bool,
            "selectable": "true",
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timeGridWeek,timeGridDay,listWeek",
            },
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "initialView": "dayGridMonth",
            "resourceGroupField": "building",
            "resources": [
                {"id": "a", "building": "Building A", "title": "Building A"},
                {"id": "b", "building": "Building A", "title": "Building B"},
                {"id": "c", "building": "Building B", "title": "Building C"},
                {"id": "d", "building": "Building B", "title": "Building D"},
                {"id": "e", "building": "Building C", "title": "Building E"},
                {"id": "f", "building": "Building C", "title": "Building F"},
            ],
        }
        # Function to add or update an event
        def add_update_event(id, title, start, end, avenue, conn):
            if id is None:  # New event
                conn.execute('INSERT INTO events (title, start, end, avenue) VALUES (?, ?, ?, ?)',
                            (title, start, end, avenue))
            else:  # Update existing event
                conn.execute('UPDATE events SET title=?, start=?, end=?, avenue=? WHERE id=?',
                            (title, start, end,avenue,  id))
            conn.commit()

        # Streamlit UI
        st.title('Event Calendar')

        if 'form_open' not in st.session_state:
            st.session_state.form_open = False

        if st.session_state['role'] == "Admin" and st.button('Add Event'):
            st.session_state.form_open = not st.session_state.form_open

        if st.session_state.form_open:
            with st.form("event_form"):
                id = 0
                title = st.text_input('Event Title')
                start_date = st.date_input("Start Date")
                start_time = st.time_input("Start Time")
                end_date = st.date_input("End Date")
                end_time = st.time_input("End Time")
                avenue = st.text_input("Where is the event taking place?")

                # Combine date and time into a single datetime object if needed
                start = datetime.combine(start_date, start_time)
                end = datetime.combine(end_date, end_time)
                #allDay = st.checkbox('All Day Event')
                submitted = st.form_submit_button('Submit Event')
                if submitted:
                    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')  # Replace 'your_database.db' with your database file
                    add_update_event(None if id == 0 else id, title, start, end, avenue, conn)
                    st.success('Event saved!')
                    st.session_state.form_open = False  # Optionally close the form upon submission
        
        def fetch_events():
            # Connect to the SQLite database
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')  # Replace 'your_database.db' with your database file
            conn.row_factory = sqlite3.Row  # This enables column access by name
            cursor = conn.cursor()

            # Execute a query to fetch all events
            cursor.execute("SELECT id, title, start, end, avenue FROM events")
            
            # Convert fetched rows to a list of dictionaries
            events = []
            for row in cursor:
                event = {
                    "id":row["id"],
                    "title": row["title"],
                    "start": row["start"],  
                    "end": row["end"],
                    "avenue": row["avenue"]
                }
                events.append(event)

            # Close the connection
            conn.close()

            return events

        # Retrieve events from the database
        calendar_events = fetch_events()
        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """

        calendar = calendar(events=st.session_state.get("events", calendar_events), options=calendar_options, custom_css=custom_css)
        st.write(calendar)
        if calendar["callback"]=="eventChange":
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')  
            add_update_event(calendar["eventChange"]["oldEvent"]["id"], calendar["eventChange"]["event"]["title"], calendar["eventChange"]["event"]["start"],calendar["eventChange"]["event"]["end"], calendar["eventChange"]["event"]["extendedProps"]["avenue"], conn)
        
    elif choice == 'Accessment':
            st.header("Diversity & Inclusion Quiz")


    elif choice == "Forum":
        def add_post(title, user, content,path):
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
            c = conn.cursor()
            c.execute("INSERT INTO posts (title, user, content, profile_image_url) VALUES (?, ?, ?, ?)", (title, user, content, path))
            conn.commit()
            conn.close()

        def show_posts():
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
            c = conn.cursor()
            c.execute("SELECT id, title, content, user, profile_image_url, timestamp FROM posts ORDER BY timestamp DESC")
            posts = c.fetchall()
            conn.close()
            return posts

        def add_comment(post_id, user, content,path):
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
            c = conn.cursor()
            c.execute("INSERT INTO comments (post_id, user, comment, profile_image_url) VALUES (?, ?, ?, ?)", (post_id, user, content, path))
            conn.commit()
            conn.close()

        def get_comments(post_id,path):
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
            c = conn.cursor()
            c.execute("SELECT user, comment,profile_image_url, timestamp FROM comments WHERE post_id = ? ORDER BY timestamp", (post_id,))
            comments = c.fetchall()
            conn.close()
            return comments

        def add_upvote(post_id, user):
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
            c = conn.cursor()
            c.execute("INSERT INTO upvotes (post_id, user) VALUES (?, ?)", (post_id, user))
            conn.commit()
            conn.close()

        def get_upvote_count(post_id):
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM upvotes WHERE post_id = ?", (post_id,))
            count = c.fetchone()[0]
            conn.close()
            return count

        def app():
            st.title('Discussion Forum')
            
            #post_button=st.button("Write a Post")
            #if post_button:
            post_expander = st.expander("Anything to share today?")
            with post_expander:
                with st.form("post_form"):
                        title = st.text_input("Title")
                        user = st.session_state['username']
                        query = "SELECT profile_image_url FROM users WHERE username = ?"
                        conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
                        c = conn.cursor()
                        # Execute the query
                        c.execute(query, (user,))
                        # Fetch the result
                        result = c.fetchone()
                        if result != None:
                            user_path= result[0]
                        else:
                            user_path="/Users/moemmyat/Downloads/ubs_prototype/8.png"
                        # Close the connection to the database
                        conn.close()
                        content = st.text_area("Content")
                        submitted = st.form_submit_button("Post")
                        if submitted and title and user and content:
                            add_post(title, user, content,user_path)

            posts = show_posts()
            for post in posts:
                def load_css():
                    css = """
                    .custom-container {
                        border: 2px solid #4CAF50; /* Green border */
                        padding: 20px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                        background-color: #ebf5eb; /* Light green background */
                        font-size: 18px; /* Larger text */
                        color: #333; /* Darker text color for better readability */
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
                    }
                    .author-style {
                        color: navy;
                        font-size: 24px; /* Larger font size for author */
                    }
                    .time-style {
                        color: #555; /* Darker gray for timestamp */
                        font-size: 16px;
                        text-align: right;
                    }
                    """
                    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

                # Call this function at the start of your app to load the styles
                load_css()
                
                author = post[3]
                timestamp = post[5]
                timestamp = arrow.get(timestamp)
                human_stamp = timestamp.humanize()
                content=post[2]
                st.write("---")
                with st.container():
                    col1, col2 = st.columns([4, 0.5])
                    with col1:
                        col1_1, col1_2 = st.columns([0.09, 0.9])  # Adjust these ratios based on desired layout
        
                        with col1_1:
                            st.image(post[4], width=40)
        
                        with col1_2:
                            st.markdown(f"<span style='color: black; font-size: 20px;'><b>{author}</b></span>", unsafe_allow_html=True)
                            
                    with col2:
                            st.markdown(f"<span style='color: dimgray; font-size: 15px;'><b>{human_stamp}</b></span>", unsafe_allow_html=True)
                st.subheader(post[1])
                st.markdown(f"<div class='custom-container'>{content}</div>", unsafe_allow_html=True)
                upvotes = get_upvote_count(post[0])
                if st.button(f'Upvote ({upvotes})', key=f"upvote{post[0]}"):
                    add_upvote(post[0], post[3])  

                comments_expander = st.expander("Comments")
                with comments_expander:
                    comments = get_comments(post[0],post[4])
                    for comment in comments:
                            if comment[2] == None:
                                st.image("/Users/moemmyat/Downloads/ubs_prototype/8.png", width=40)

                            def custom_css():
                                st.markdown("""
                                    <style>
                                    .custom-container {
                                        background-color: #F4F7F4;
                                        border: 1px solid #ccc;
                                        padding: 10px;
                                        border-radius: 5px;
                                        margin: 10px 0px;
                                    }
                                    </style>
                                """, unsafe_allow_html=True)

                            custom_css()
                            
                            author = comment[0]
                            timestamp = comment[3]
                            timestamp = arrow.get(timestamp)
                            human_stamp = timestamp.humanize()
                            content=comment[1]
                            with st.container():
                                col1, col2 = st.columns([4, 0.5])
                                with col1:
                                    col1_1, col1_2 = st.columns([0.09, 0.9])  # Adjust these ratios based on desired layout
                                    with col1_1:
                                        st.image(comment[2], width=40)
                    
                                    with col1_2:
                                        st.markdown(f"<span style='color: black; font-size: 20px;'><b>{author}</b></span>", unsafe_allow_html=True)
                                        
                                with col2:
                                        st.markdown(f"<span style='color: dimgray; font-size: 15px;'><b>{human_stamp}</b></span>", unsafe_allow_html=True)
                            st.markdown(f"<div class='custom-container'>{content}</div>", unsafe_allow_html=True)

                    with st.form(f"comment_form{post[0]}"):
                            comment_content = st.text_area("Add a comment", key=f"comment{post[0]}")
                            comment_button = st.form_submit_button("Post Comment")
                            if comment_button and comment_content:
                                add_comment(post[0], user, comment_content,user_path)
                                st.experimental_rerun()
                            
                st.write("---")

        app()
    
    elif choice == "Learning":
        choice = st.selectbox("Choose your category:", ["Name Learning", "DEI Terms","Understanding Gender", "Fact in History"])
    
    elif choice =="DE&I Chatbot":
        st.title("🤗💬 Ask any questions!")
        # Hugging Face Credentials
        # with st.sidebar:
        #     st.title('🤗💬 HugChat')

        #     hf_email = st.text_input('Enter E-mail:', type='password') #lolajane205@gmail.com
        #     hf_pass = st.text_input('Enter password:', type='password') #t&Ld~i6VDXtVvy4
        #     if not (hf_email and hf_pass):
        #             st.warning('Please enter your credentials!', icon='⚠️')
        #     else:
        #             st.success('Proceed to entering your prompt message!', icon='👉')
            
        # # Store LLM generated responses
        # if "messages" not in st.session_state.keys():
        #     st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

        # # Display chat messages
        # for message in st.session_state.messages:
        #     with st.chat_message(message["role"]):
        #         st.write(message["content"])

        # # Function for generating LLM response
        # def generate_response(prompt_input, email, passwd):
        #     # Hugging Face Login
        #     sign = Login(email, passwd)
        #     cookies = sign.login()
        #     # Create ChatBot                        
        #     chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        #     return chatbot.chat(prompt_input)

        # # User-provided prompt
        # if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
        #     st.session_state.messages.append({"role": "user", "content": prompt})
        #     with st.chat_message("user"):
        #         st.write(prompt)

        # # Generate a new response if last message is not from assistant
        # if st.session_state.messages[-1]["role"] != "assistant":
        #     with st.chat_message("assistant"):
        #         with st.spinner("Thinking..."):
        #             response = generate_response(prompt, hf_email, hf_pass) 
        #             st.write(response) 
        #     message = {"role": "assistant", "content": response}
        #     st.session_state.messages.append(message)

    elif choice == "Admin Portal" and st.session_state['role'] == "Admin":

        # Function to create a connection to the database
        def get_db_connection():
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
            return conn

        # Function to fetch posts
        def fetch_posts():
            conn = get_db_connection()
            posts = pd.read_sql_query("SELECT * FROM posts", conn)
            conn.close()
            return posts

        # Function to fetch comments
        def fetch_comments():
            conn = get_db_connection()
            comments = pd.read_sql_query("SELECT * FROM comments", conn)
            conn.close()
            return comments

        # Function to fetch upvotes
        def fetch_upvotes():
            conn = get_db_connection()
            upvotes = pd.read_sql_query("SELECT post_id, COUNT(*) as upvote_count FROM upvotes GROUP BY post_id", conn)
            conn.close()
            return upvotes

        st.title('Admin Portal')

        # Display Posts
        st.header('Display Posts')
        posts = fetch_posts()
        st.write(posts)

        # Display Comments
        st.header('Display Comments')
        comments = fetch_comments()
        st.write(comments)

        # Display Upvotes
        st.header('Display Upvotes')
        upvotes = fetch_upvotes()
        
        st.write(upvotes)

        st.title('Admin Dashboard for User Engagement')

        # Date filter
        start_date = st.sidebar.date_input("Start date", datetime(2023, 1, 1))
        end_date = st.sidebar.date_input("End date", datetime.now())
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date) + timedelta(days=1) - timedelta(seconds=1)

        # Fetch data
        posts = fetch_posts()
        comments = fetch_comments()
        upvotes = fetch_upvotes()
        posts['timestamp'] = pd.to_datetime(posts['timestamp'])
        comments['timestamp'] = pd.to_datetime(comments['timestamp'])

        # Filter data based on the timeframe
        posts = posts[(posts['timestamp'] >= start_date) & (posts['timestamp'] <= end_date)]
        comments = comments[(comments['timestamp'] >= start_date) & (comments['timestamp'] <= end_date)]

        # Display data
        st.write("## Posts", posts)
        st.write("## Comments", comments)
        st.write("## Upvotes", upvotes)

        # Visualization (example using matplotlib or plotly)
        import matplotlib.pyplot as plt

        posts_by_date = posts.groupby(posts['timestamp'].dt.date).size()
        plt.figure(figsize=(10, 5))
        plt.plot(posts_by_date.index, posts_by_date.values, marker='o')
        plt.title('Number of Posts Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Posts')
        plt.grid(True)
        st.pyplot(plt)

        popular_posts = pd.merge(posts, upvotes, left_on='id', right_on='post_id', how='left')
        popular_posts.sort_values(by='upvote_count', ascending=False, inplace=True)
        st.write("## Most Popular Posts", popular_posts.head())

    else:
        st.error("Unauthorized Access. Admin only.")
        st.error("Please contact the admin to access the portal!")

# Logout button
if 'username' in st.session_state:
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):  # modified to avoid RuntimeError
            del st.session_state[key]
        st.experimental_rerun()