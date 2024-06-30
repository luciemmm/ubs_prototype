import streamlit as st
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import altair as alt
import sqlite3
import arrow
import os
def add_post(title, user, content,path, db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("INSERT INTO posts (title, user, content, profile_image_url) VALUES (?, ?, ?, ?)", (title, user, content, path))
            conn.commit()
            conn.close()

def show_posts(db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT id, title, content, user, profile_image_url, timestamp FROM posts ORDER BY timestamp DESC")
            posts = c.fetchall()
            conn.close()
            return posts

def add_comment(post_id, user, content,path,db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("INSERT INTO comments (post_id, user, comment, profile_image_url) VALUES (?, ?, ?, ?)", (post_id, user, content, path))
            conn.commit()
            conn.close()

def get_comments(post_id,path,db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT user, comment,profile_image_url, timestamp FROM comments WHERE post_id = ? ORDER BY timestamp", (post_id,))
            comments = c.fetchall()
            conn.close()
            return comments

def add_upvote(post_id, user,db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("INSERT INTO upvotes (post_id, user) VALUES (?, ?)", (post_id, user))
            conn.commit()
            conn.close()

def get_upvote_count(post_id,db):
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM upvotes WHERE post_id = ?", (post_id,))
            count = c.fetchone()[0]
            conn.close()
            return count
def discuss_app(text,db):
            st.title('Discussion Forum')
            
            #post_button=st.button("Write a Post")
            #if post_button:
            post_expander = st.expander(text)
            with post_expander:
                with st.form("post_form"):
                        title = st.text_input("Title")
                        user = st.session_state['username']
                        query = "SELECT profile_image_url FROM users WHERE username = ?"
                        conn = sqlite3.connect(db)
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
                            add_post(title, user, content,user_path,db)

            posts = show_posts(db)
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
                upvotes = get_upvote_count(post[0],db)
                if st.button(f'Upvote ({upvotes})', key=f"upvote{post[0]}"):
                    add_upvote(post[0], post[3],db)  

                comments_expander = st.expander("Comments")
                with comments_expander:
                    comments = get_comments(post[0],post[4],db)
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
                                    col1_1, col1_2 = st.columns([0.09, 0.9])  
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
                                add_comment(post[0], user, comment_content,user_path,db)
                                st.experimental_rerun()
                            
                st.write("---")

def learn():
                st.session_state["choice"]= st.sidebar.selectbox("Choose your category:", ["Name Learning", "DEI Terms","Understanding Gender", "Facts in History"])
                if st.session_state["choice"]== "Name Learning":
                    # Load your CSV data
                    @st.cache_data
                    def load_data():
                        return pd.read_csv("/Users/moemmyat/Downloads/ubs_prototype/names.csv")

                    data = load_data()

                    # Title of the site
                    st.title('Learn Names and Pronunciations')

                    # Display Name of the Day
                    name_of_the_day = data.sample(1)
                    st.header('Name of the Day')
                    st.subheader(name_of_the_day.iloc[0]['Name'])
                    st.write(f"Country: {name_of_the_day.iloc[0]['Country']}")

                    # Play the pronunciation audio
                    audio_file = name_of_the_day.iloc[0]['Pronunciation_Audio']
                    audio_bytes = open(audio_file, 'rb').read()
                    st.audio(audio_bytes, format='audio/m4a')  # Changed format to 'audio/m4a'

                    # Search bar functionality
                    st.header('Search for a Name')
                    name_query = st.text_input("Enter a name to find its pronunciation:")

                    if name_query:
                        # Filter data based on the name
                        results = data[data['Name'].str.lower() == name_query.lower()]
                        if not results.empty:
                            for _, row in results.iterrows():
                                st.write(f"Name: {row['Name']}, Country: {row['Country']}")
                                audio_file = row['Pronunciation_Audio']
                                audio_bytes = open(audio_file, 'rb').read()
                                st.audio(audio_bytes, format='audio/m4a')
                        else:
                            st.write("Name not found. Please try another name.")
                elif st.session_state["choice"]== "DEI Terms":
                    dei_categories = [
                        "Microaggressions",
                        "Inclusion",
                        "Diversity",
                        "Equity",
                        "Accessibility",
                        "Unconscious Bias",
                        "Cultural Competence",
                        "Social Justice",
                        "Intersectionality",
                        "Belonging"
                    ]

                    st.session_state["choice"]= st.sidebar.selectbox("Choose your category:", dei_categories)

                    # Process the choice
                    if st.session_state["choice"]== "Microaggressions":
                            st.session_state["choice"]= st.selectbox("I would like to see:", ["Overview","Stories","Videos","Discussions"])
                            if st.session_state["choice"]== "Overview":
                                st.header("Understanding Microaggressions")
                                st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">Read Maria's Story</h2>
                                        <p>Maria, a talented computer science graduate, was excited when she secured a position at a renowned tech firm that was actively promoting diversity. Her interview had gone exceptionally well, particularly when she discussed her advanced AI project, which impressed the interviewers.

                                    However, on her first day, while setting up her workstation, she overheard a colleague whisper, "She's probably just a diversity hire." The comment stung, especially since the colleague hadn't yet seen her work or knew about her strong academic background.</p>
                                    </div>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">YouTube: Understanding Microaggressions</h2>
                                        <iframe width="560" height="315" src="https://www.youtube.com/embed/ASWL6jIQbrQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                                    </div>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">Podcast: Discussing Microaggressions</h2>
                                        <audio controls>
                                            <source src="full_audio.mp3" type="audio/mpeg">
                                            Your browser does not support the audio element.
                                        </audio>
                                    </div>
                                    """, unsafe_allow_html=True)
                            elif st.session_state["choice"]=="Stories":
                                    st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">Read Maria's Story</h2>
                                        <p>Maria, a talented computer science graduate, was excited when she secured a position at a renowned tech firm that was actively promoting diversity. Her interview had gone exceptionally well, particularly when she discussed her advanced AI project, which impressed the interviewers.

                                    However, on her first day, while setting up her workstation, she overheard a colleague whisper, "She's probably just a diversity hire." The comment stung, especially since the colleague hadn't yet seen her work or knew about her strong academic background.</p>
                                    </div>""", unsafe_allow_html=True)
                                    with st.expander("Learn more about Maria's situation"):
                                        st.write("""
                                        **Question: How should Maria respond to the comment?**
                                        
                                        **Answer:** Maria might consider addressing the comment directly with the colleague or seek support from HR or a mentor within the company to discuss her feelings and the appropriate steps to take.
                                        
                                        **Question: What can the company do to prevent such situations?**
                                        
                                        **Answer:** The company should enforce a positive workplace culture that values all employees equally, with training on diversity, inclusion, and sensitivity.

                                        **Question: Why is the concept of a 'diversity hire' a misconception and why is diversity important in the workplace?**
                                        
                                        **Answer:** The term 'diversity hire' often carries a negative implication that individuals are selected based on their demographics rather than their qualifications. This is a misconception because:
                                        
                                        - **Merit and Diversity**: Organizations that emphasize diversity still base hiring decisions on qualifications. The goal is to ensure that hiring practices are fair and inclusive, giving qualified candidates of all backgrounds equal opportunity.
                                        
                                        - **Enhanced Creativity and Innovation**: Diverse teams bring a range of perspectives and experiences, which can lead to more creative solutions and innovations. This can be crucial in problem-solving and adapting to new market trends.
                                        
                                        - **Reflecting the Customer Base**: A diverse workforce can better understand and connect with a varied customer base, thus improving service and increasing customer satisfaction.
                                        
                                        - **Improved Employee Satisfaction and Retention**: Cultivating an inclusive environment where everyone feels valued can lead to higher job satisfaction, lower turnover rates, and a more positive company culture.
                                        """)
                                    st.markdown("""
                                        <style>
                                            .card {
                                                margin: 10px;
                                                padding: 20px;
                                                background-color: #ffcccc; /* light red background */
                                                border: 2px solid #ff0000; /* red border */
                                                border-radius: 8px;
                                                box-shadow: 2px 2px 5px grey;
                                                color: #800000; /* dark red text color */
                                            }
                                        </style>
                                        <div class="card">
                                            <h2 style="color: #ff0000;">Read Ethan's Story</h2>
                                            <p>Ethan, a bright young man with a passion for graphic design, had recently graduated from a top art school. Despite his congenital muscular dystrophy, which required him to use a wheelchair, Ethan's creativity and skill with digital tools were unparalleled. His portfolio was filled with innovative designs and brand strategies that had already won several academic awards. On his first day at a prestigious advertising agency, Ethan overheard some colleagues whispering 'I guess they needed to check off another box on the diversity list'.The words hit Ethan hard. He had always strived to be recognized for his talent and not his disability.</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    with st.expander("Learn more about Ethan's situation"):
                                        st.write("""
                                        - **Empathy and Support**: Colleagues should show empathy and support, recognizing the unique perspectives and strengths each individual brings.
                                        - **Educate Themselves**: It's important for individuals to educate themselves about different disabilities and the proper etiquette when interacting with colleagues who have disabilities.
                                        - **Inclusive Communication**: Ensure that communication within the team is inclusive, avoiding assumptions and stereotypes.
                                        - **Speak Up**: If comfortable, address the situation directly with the individuals involved, explaining how their comments may be hurtful or inappropriate.
                                        - **Seek Support**: Reach out to a manager, HR, or a trusted colleague for support and to discuss potential resolutions.
                                        - **Focus on Your Strengths**: Continue to demonstrate your skills and capabilities, reinforcing your value to the team beyond any physical or other attributes.
                                        - **Educate Others**: Use the opportunity to educate others, helping to prevent similar situations in the future.
                                        """)

                                    st.markdown("""
                                        <style>
                                            .card {
                                                margin: 10px;
                                                padding: 20px;
                                                background-color: #ffcccc; /* light red background */
                                                border: 2px solid #ff0000; /* red border */
                                                border-radius: 8px;
                                                box-shadow: 2px 2px 5px grey;
                                                color: #800000; /* dark red text color */
                                            }
                                        </style>
                                        <div class="card">
                                            <h2 style="color: #ff0000;">Read Alyanna's Story</h2>
                                            <p>Alyanna, a dedicated business student from the Philippines, landed an internship at a prestigious multinational corporation. Eager to showcase her skills, she soon encountered subtle, yet persistent, challenges in the form of microaggressions from her boss, Mr. Thompson.In team meetings, when Alyanna offered her insights, they were frequently ignored or swiftly dismissed. Conversely, similar suggestions from her peers were met with approval and enthusiasm. Confused and seeking support, she turned to her colleagues, only to be met with dismissive comments. "That's just how Mr. Thompson is," they said, suggesting she shouldn't take it personally.These microaggressions began to weigh on Alyanna, making her question both her belonging and her value within the team.</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    with st.expander("Why Alyanna’s Experience Matters"):
                                        st.write("""
                                        **Understanding Microaggressions**: Alyanna's story sheds light on microaggressions in the workplace—subtle, indirect, or unintentional discriminations—that can significantly impact an individual's professional and personal well-being.
                                        
                                        **Cultural Sensitivity and Awareness**: This story serves as a reminder of the importance of cultural sensitivity and awareness in a globalized workplace. Recognizing and addressing these issues is essential for fostering an inclusive and supportive work environment.
                                        
                                        **Mental Health Considerations**: Persistent microaggressions can deteriorate one's mental health, leading to decreased job satisfaction, reduced work performance, and even withdrawal from professional opportunities.
                                        
                                        **Legal and Ethical Implications**: Ignoring such behaviors can contribute to a toxic work culture and might even pose legal risks concerning workplace discrimination and harassment laws.
                                        """)

                                    with st.expander("How People Should React to Microaggressions"):
                                        st.write("""
                                        - **Acknowledge and Address**: It is crucial for both colleagues and management to acknowledge and address microaggressions when they occur. Ignoring them can perpetuate a culture of exclusion.
                                        
                                        - **Supportive Environment**: Creating a supportive environment where everyone feels safe to express their concerns and experiences is essential.
                                        
                                        - **Training and Education**: Regular training sessions on diversity, equity, and inclusion can help educate employees about microaggressions and their impact, promoting a more empathetic workplace culture.
                                        
                                        - **Open Dialogue**: Encourage open dialogue about microaggressions, allowing those affected to share their experiences without fear of retribution or dismissal.
                                        """)

                                    with st.expander("What to Do If You Experience Microaggressions"):
                                        st.write("""
                                        - **Document the Incidents**: Keep a record of what was said or done, including dates and times. Documentation can be crucial for discussing these issues with HR or your supervisor.
                                        
                                        - **Seek Allies**: Find colleagues who understand and support you. Allies can help advocate for changes and provide emotional support.
                                        
                                        - **Communicate Effectively**: When comfortable, address the behavior directly with the person involved, explaining how their actions or words affect you.
                                        
                                        - **Utilize Resources**: Many organizations have policies and resources in place to handle such issues. Contact your HR department for guidance on how to proceed.
                                        
                                        - **Professional Guidance**: Consider seeking support from a mentor or a professional counselor to navigate the emotional and professional complexities of the situation.
                                        """)
                            elif st.session_state["choice"]=="Videos":
                                st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">The What, How and Why of Microaggressions
                                        </h2>
                                        <iframe width="560" height="315" src="https://www.youtube.com/embed/ASWL6jIQbrQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                                    </div>
                                    """, unsafe_allow_html=True)
                                st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">How to get serious about diversity and inclusion in the workplace
                                        </h2>
                                        <iframe width="560" height="315" src="https://www.youtube.com/embed/kvdHqS3ryw0?si=gAZbUq8Ca7uBESZ1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>                                    </div>
                                    """, unsafe_allow_html=True)
                                st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">Conversation on speaking up (Get Comfortable with being Uncomfortable)
                                        </h2>
                                        <iframe width="560" height="315" src="https://www.youtube.com/embed/QijH4UAqGD8?si=wn_PUx_Bz3p57IOE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                                    """, unsafe_allow_html=True)
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
    st.session_state["menu_choice"]= st.sidebar.selectbox("Main Menu", ["Learning of the Day","My Profile","FAQ", "Forum","Calendar", "Admin Portal", "Learning","DE&I Chatbot", "Assessment"], index=0)
    if st.session_state.get("menu_choice") == "Learning of the Day":
        st.title("Let's talk about microaggressions today!")
        st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">Read Maria's Story</h2>
                                        <p>Maria, a talented computer science graduate, was excited when she secured a position at a renowned tech firm that was actively promoting diversity. Her interview had gone exceptionally well, particularly when she discussed her advanced AI project, which impressed the interviewers.

                                    However, on her first day, while setting up her workstation, she overheard a colleague whisper, "She's probably just a diversity hire." The comment stung, especially since the colleague hadn't yet seen her work or knew about her strong academic background.</p>
                                    </div>""", unsafe_allow_html=True)
        with st.expander("Learn more about Maria's situation"):
                                        st.write("""
                                        **Question: How should Maria respond to the comment?**
                                        
                                        **Answer:** Maria might consider addressing the comment directly with the colleague or seek support from HR or a mentor within the company to discuss her feelings and the appropriate steps to take.
                                        
                                        **Question: What can the company do to prevent such situations?**
                                        
                                        **Answer:** The company should enforce a positive workplace culture that values all employees equally, with training on diversity, inclusion, and sensitivity.

                                        **Question: Why is the concept of a 'diversity hire' a misconception and why is diversity important in the workplace?**
                                        
                                        **Answer:** The term 'diversity hire' often carries a negative implication that individuals are selected based on their demographics rather than their qualifications. This is a misconception because:
                                        
                                        - **Merit and Diversity**: Organizations that emphasize diversity still base hiring decisions on qualifications. The goal is to ensure that hiring practices are fair and inclusive, giving qualified candidates of all backgrounds equal opportunity.
                                        
                                        - **Enhanced Creativity and Innovation**: Diverse teams bring a range of perspectives and experiences, which can lead to more creative solutions and innovations. This can be crucial in problem-solving and adapting to new market trends.
                                        
                                        - **Reflecting the Customer Base**: A diverse workforce can better understand and connect with a varied customer base, thus improving service and increasing customer satisfaction.
                                        
                                        - **Improved Employee Satisfaction and Retention**: Cultivating an inclusive environment where everyone feels valued can lead to higher job satisfaction, lower turnover rates, and a more positive company culture.
                                        """)
 
        st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">Conversation on speaking up (Get Comfortable with being Uncomfortable)
                                        </h2>
                                        <iframe width="560" height="315" src="https://www.youtube.com/embed/QijH4UAqGD8?si=wn_PUx_Bz3p57IOE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                                    """, unsafe_allow_html=True)
        discuss_app("Would you like to share your thoughts?",'/Users/moemmyat/Downloads/ubs_prototype/forum.db')
        
    elif st.session_state["menu_choice"]=="My Profile":
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
                                border: 2px solid #696969;
                                padding: 20px;
                                border-radius: 10px;
                                margin-bottom: 20px;
                                background-color: #ADD8E6; 
                                font-size: 18px; 
                                color: #333; 
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
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

            load_css()
            # Button to fetch the profile
            user_data = get_user_data(st.session_state['username'])
            if user_data:
                    print(user_data)
                    username, role, profile_image_url, fun_fact, gender, hobbies = user_data
                    if profile_image_url:
                        col1, col2 = st.columns([0.13, 0.9]) 

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
    elif st.session_state["menu_choice"]== "FAQ":
        st.title("Frequently Asked Questions")
        for faq in faqs:
            st.subheader(faq["question"])
            st.write(faq["answer"])

    elif st.session_state["menu_choice"]== "Calendar":

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
        #st.write(calendar)
        if calendar["callback"]=="eventChange":
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')  
            add_update_event(calendar["eventChange"]["oldEvent"]["id"], calendar["eventChange"]["event"]["title"], calendar["eventChange"]["event"]["start"],calendar["eventChange"]["event"]["end"], calendar["eventChange"]["event"]["extendedProps"]["avenue"], conn)
        def load_events():
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')
            c = conn.cursor()
            c.execute("SELECT id, title, start, end, avenue FROM events")
            events = c.fetchall()
            conn.close()
            return events

        def register_for_event(event_id, user_name, user_email):
            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')
            c = conn.cursor()
            c.execute("INSERT INTO registrations (event_id, user_name, user_email) VALUES (?, ?, ?)",
                    (event_id, user_name, user_email))
            conn.commit()
            conn.close()
        import pytz
        def format_datetime(iso_datetime):
            """Convert ISO 8601 string to a more readable format."""
            local_timezone = pytz.timezone("Asia/Yangon")  # Adjust to the event's local timezone
            datetime_obj = datetime.fromisoformat(iso_datetime.replace('Z', '+00:00'))
            local_datetime = datetime_obj.astimezone(local_timezone)
            return local_datetime.strftime("%B %d, %Y at %H:%M %Z")  # E.g., "June 11, 2024 at 14:57 MYT"

        def app():
            st.title('Event Registration')
            
            events = load_events()
            if events:
                # Create a select box for choosing an event
                event_options = [(event[1], event[0]) for event in events]  # List of tuples (event name, event ID)
                chosen_event_name, chosen_event_id = st.selectbox("Choose an event:", event_options, format_func=lambda x: x[0])

                # Find the chosen event details
                chosen_event = next(event for event in events if event[0] == chosen_event_id)
                
                # Display details of the chosen event
                st.subheader(f"{chosen_event[1]}")
                start_formatted = format_datetime(chosen_event[2])
                end_formatted = format_datetime(chosen_event[3])
                st.text(f"Start: {start_formatted} - End: {end_formatted}")
                st.text(f"Avenue: {chosen_event[4]}")
                
                # Input fields for user registration
                user_name = st.text_input("Your Name", key=f"name_{chosen_event_id}")
                user_email = st.text_input("Your Email", key=f"email_{chosen_event_id}")
                
                # Register button
                if st.button("Register", key=chosen_event_id):
                    register_for_event(chosen_event_id, user_name, user_email)
                    st.success(f"You have successfully registered for {chosen_event[1]}. You will sent an email soon by the admin!")
            else:
                st.write("No events available.")

        def suggest_event():
            st.title("Suggest an Event to Admin")

            # Form for event suggestion
            with st.form("event_form"):
                event_name = st.text_input("Event Name")
                event_date = st.date_input("Event Date")
                event_description = st.text_area("Learn More History")
                has_celebrated_before = st.selectbox("Has you ever celebrated this before/Is this a tradition that you know well?", ["Yes", "No"])
                available_to_help = st.selectbox("Will you be able to help out? Don't worry. Just give us some ideas!", ["Yes", "No"])
                submit_button = st.form_submit_button("Submit Event")

                if submit_button:
                    # Connect to SQLite database
                    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')
                    c = conn.cursor()
                    # Insert the data into the event_suggestions table
                    c.execute('''
                        INSERT INTO event_suggestions (event_name, event_date, event_description, has_celebrated_before, available_to_help)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (event_name, event_date, event_description, has_celebrated_before, available_to_help))
                    conn.commit()
                    conn.close()
                    st.success("Your event suggestion has been submitted successfully!")
        st.session_state["choice"]=st.radio("Choose an option:",["Event Registration","Suggest an event to admin"])
        if st.session_state["choice"]=="Event Registration":
            app()
        else:
            suggest_event()
    elif st.session_state["menu_choice"]== 'Assessment':
            st.header("Diversity & Inclusion Assessments")

            # Function to retrieve surveys
            def get_surveys(conn):
                c = conn.cursor()
                query = "SELECT * FROM surveys"
                c.execute(query)
                rows = c.fetchall()
                df = pd.DataFrame(rows, columns=[desc[0] for desc in c.description])
                return df

            # Function to retrieve questions for a given survey_id
            def get_questions(conn, survey_id):
                c = conn.cursor()
                c.execute("SELECT * FROM questions WHERE survey_id = ?", (survey_id,))
                rows = c.fetchall()
                df = pd.DataFrame(rows, columns=[desc[0] for desc in c.description])
                return df

                    # Function to insert a response into the database
            def insert_response(conn, survey_id, question_id, response):
                query = f"INSERT INTO responses (survey_id, question_id, response) VALUES (?, ?, ?)"
                cur = conn.cursor()
                cur.execute(query, (survey_id, question_id, response))
                conn.commit()

            def insert_survey_id( title, reminder):
                conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
                c = conn.cursor()
                c.execute("INSERT INTO surveys (title,reminder) VALUES (?,?)", (title,reminder))
                conn.commit()
                survey_id = c.lastrowid
                print(survey_id)
                
                conn.close()
                return survey_id
                # Function to insert survey data into the database

            def insert_assessment_id( title, reminder):
                conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/assessment.db')
                c = conn.cursor()
                c.execute("INSERT INTO surveys (title,reminder) VALUES (?,?)", (title,reminder))
                conn.commit()
                survey_id = c.lastrowid
                print(survey_id)
                
                conn.close()
                return survey_id
                # Function to insert survey data into the database

            def insert_survey_q(survey_id, question, option1, option2, option3, option4):

                conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
                c = conn.cursor()
                c.execute("INSERT INTO questions (survey_id, question, option1, option2, option3, option4) VALUES (?, ?, ?, ?, ?, ?)",
                            (survey_id, question, option1, option2, option3, option4))
                conn.commit()
            
            def insert_assessment_q(survey_id, question, option1,score1, option2,score2, option3,score3, option4,score4):

                conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/assessment.db')
                c = conn.cursor()
                c.execute("INSERT INTO questions (survey_id, question, option1,score1, option2,score2, option3,score3, option4,score4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (survey_id, question, option1,score1, option2,score2, option3,score3, option4,score4))
                conn.commit()
                conn.close()

            if st.session_state["role"]=="Admin":
                # Connect to SQLite database
                
                app_mode = st.sidebar.radio(
                "Choose the mode:",
                ("Survey Management", "User Engagement Tracker")
    )
                if app_mode=="Survey Management":
                    st.title("Survey Management")

                    st.session_state["choice"]= st.selectbox("Choose an option", ["Create a survey","Create Assessments","Check the surveys","Check the questions"])

                    if st.session_state["choice"]== 'Create a survey':
                        title= st.text_input("What is the survey topic?")
                        st.header("Upload a CSV file for the new survey")
                        uploaded_file = st.file_uploader("Choose a file")
                        submit_button = st.button('Submit Survey')
                        reminder=st.radio("Send notification to users:",("YES","NO"))

                        if submit_button and uploaded_file is not None:
                            if uploaded_file is not None:
                                df = pd.read_csv(uploaded_file)
                                insert_survey_id( title, reminder)
                                survey_id=1
                                for index, row in df.iterrows():
                                    insert_survey_q(survey_id,row['question'], row['option1'], row['option2'], row['option3'], row['option4'])
                                st.success("Survey uploaded successfully!")

                                st.subheader("Take a look at the survey:")
                                for index, row in df.iterrows():
                                    options = [row['option1'], row['option2'], row['option3'], row['option4']]
                                    response = st.radio(row['question'], options)
                    
                    elif st.session_state["choice"]== "Create Assessments":
                        title= st.text_input("What is the Assessment topic?")
                        st.header("Upload a CSV file for the new assessment")
                        uploaded_file = st.file_uploader("Choose a file")
                        submit_button = st.button('Submit Survey')
                        reminder=st.radio("Send notification to users:",("YES","NO"))
                        if submit_button and uploaded_file is not None:
                            if uploaded_file is not None:
                                df = pd.read_csv(uploaded_file)
                                insert_assessment_id( title, reminder)
                                survey_id=1
                                for index, row in df.iterrows():
                                    insert_assessment_q(survey_id,row['question'], row['option1'], row['score1'], row['option2'],row['score2'], row['option3'], row['score3'],row['option4'],row['score4'])
                                st.success("Survey uploaded successfully!")

                                st.subheader("Take a look at the assessment:")
                                for index, row in df.iterrows():
                                    options = [row['question'], row['option1'],  row['option2'], row['option3'],row['option4']]
                                    response = st.radio(row['question'], options)  

                    elif st.session_state["choice"]=="Check the surveys":   

                        # Function to get surveys
                        def get_surveys():
                            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
                            cur = conn.cursor()
                            cur.execute("SELECT survey_id, title FROM surveys")
                            surveys = cur.fetchall()
                            conn.close()
                            return surveys

                        # Function to get questions for a survey
                        def get_questions(survey_id):
                            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
                            cur = conn.cursor()
                            cur.execute("SELECT question, option1, option2, option3, option4 FROM questions WHERE survey_id=?", (survey_id,))
                            questions = cur.fetchall()
                            conn.close()
                            return questions
                        
                        def load_css():
                            css = """
                            .custom-container {
                                border: 2px solid #696969;
                                padding: 20px;
                                border-radius: 10px;
                                margin-bottom: 20px;
                                background-color: #ADD8E6; 
                                font-size: 18px; 
                                color: #333; 
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
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

                        load_css()

                        # Streamlit UI
                        def main():
                            
                            st.markdown(f"<div class='custom-container'>All created surveys are displayed here. For tracking user responses, please go to User Engagement Tracker. <span style='color: #1E3566;'></span></div>", unsafe_allow_html=True)                    


                            surveys = get_surveys()
                            survey_id = st.selectbox('Choose a survey:', [s[0] for s in surveys], format_func=lambda x: f"{x} - {dict(surveys)[x]}")

                            if survey_id:
                                st.header('Questions')
                                questions = get_questions(survey_id)
                                for q in questions:
                                    st.subheader(q[0])
                                    for i in range(1, 5):
                                        if q[i]:
                                            st.radio(f"Answer[{i}]:", options=[q[i]], key=f"{survey_id}_{q[0]}_{i}")

                        main()    

                    elif st.session_state["choice"]=="Check the questions":   

                        # Function to get surveys
                        def get_surveys():
                            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/assessment.db')
                            cur = conn.cursor()
                            cur.execute("SELECT survey_id, title FROM surveys")
                            surveys = cur.fetchall()
                            conn.close()
                            return surveys

                        # Function to get questions for a survey
                        def get_questions(survey_id):
                            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/assessment.db')
                            cur = conn.cursor()
                            cur.execute("SELECT question, option1, option2, option3, option4 FROM questions WHERE survey_id=?", (survey_id,))
                            questions = cur.fetchall()
                            conn.close()
                            return questions
                        
                        def load_css():
                            css = """
                            .custom-container {
                                border: 2px solid #696969;
                                padding: 20px;
                                border-radius: 10px;
                                margin-bottom: 20px;
                                background-color: #ADD8E6; 
                                font-size: 18px; 
                                color: #333; 
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
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

                        load_css()

                        # Streamlit UI
                        def main():
                            
                            st.markdown(f"<div class='custom-container'>All created surveys are displayed here. For tracking user responses, please go to User Engagement Tracker. <span style='color: #1E3566;'></span></div>", unsafe_allow_html=True)                    


                            surveys = get_surveys()
                            survey_id = st.selectbox('Choose a survey:', [s[0] for s in surveys], format_func=lambda x: f"{x} - {dict(surveys)[x]}")

                            if survey_id:
                                st.header('Questions')
                                questions = get_questions(survey_id)
                                for q in questions:
                                    st.subheader(q[0])
                                    for i in range(1, 5):
                                        if q[i]:
                                            st.radio(f"Answer[{i}]:", options=[q[i]], key=f"{survey_id}_{q[0]}_{i}")

                        main()                          
                elif app_mode=="User Engagement Tracker":
                    def get_questions(survey_id):
                        conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
                        cur = conn.cursor()
                        cur.execute("SELECT id, question FROM questions WHERE survey_id=?", (survey_id,))
                        questions = cur.fetchall()
                        conn.close()
                        return questions
   
                    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
                    c = conn.cursor()

                    def get_questions(survey_id):
                        c.execute("SELECT id, question FROM questions WHERE survey_id = ?", (survey_id,))
                        return c.fetchall()

                    def get_response_counts(question_id):
                        c.execute("""
                            SELECT response, COUNT(*) as count 
                            FROM responses 
                            WHERE question_id = ? 
                            GROUP BY response
                            """, (question_id,))
                        return c.fetchall()

                    def main():
                        st.subheader("User Engagement Tracker")

                        survey_id = st.number_input("Enter Survey ID", value=1, step=1)

                        questions = get_questions(survey_id)
                        if questions:
                            st.subheader('Select Questions:')
                            selected_questions = []
                            for q_id, question in questions:
                                if st.checkbox(question, key=q_id):
                                    selected_questions.append(q_id)
                            print(selected_questions)
                            if selected_questions:
                                st.text(f'You selected questions with IDs: {selected_questions}')

                                for q_id in selected_questions:
                                    st.write(f"Question: {questions[q_id-1]}")
                                    response_counts = get_response_counts(q_id)
                                    
                                    if response_counts:
                                        chart_data = {}
                                        
                                        # Aggregate response counts into chart_data
                                        for response, count in response_counts:
                                            chart_data[response] = count
                                        
                                        # Create DataFrame from the aggregated data
                                        data = pd.DataFrame(list(chart_data.items()), columns=['Response', 'Count'])
                                        
                                        # Create an Altair chart object
                                        chart = alt.Chart(data).mark_bar().encode(
                                            x='Response',
                                            y='Count',
                                            color='Response'  # Colors bars by category
                                        ).properties(
                                            width='container',  # Use the full width of the container
                                            height=300          # Set the height of the chart
                                        )
                                        
                                        # Display the chart in Streamlit
                                        st.altair_chart(chart, use_container_width=True)
                                    else:
                                        st.write("No responses yet for this question.")
                        else:
                            st.error("No survey available")

                    if __name__ == "__main__":
                        main()

            else:
                st.session_state["choice"]= st.selectbox("Choose a category:", ["Take a survey", "Take a self-Assessment"])
                if st.session_state["choice"]=="Take a survey":

                    # Streamlit app
                    def main():
                        # Database connection
                            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
                            surveys = get_surveys(conn)
                            if len(surveys['survey_id']) == 0:
                                st.write("No survey available")
                                
                            else:
                                st.write("Your admin has published some surveys.")
                            survey_id = st.selectbox('Choose a survey:', surveys['survey_id'])
                            
                            if survey_id:
                                questions = get_questions(conn, survey_id)
                                responses = []
                                printed_questions = set()
                                for idx, question in questions.iterrows():
                                    current_question = question['question']
                                    
                                    if current_question not in printed_questions:
                                        options = [question['option1'], question['option2'], question['option3'], question['option4']]
                                        # Generate a unique key for each question
                                        key = f"question_{idx}"
                                        
                                        # Display the question using st.radio
                                        response = st.radio(current_question, options, key=key)
                                    responses.append(response)
                                
                                if st.button('Submit'):
                                    for idx, question in questions.iterrows():
                                        print(responses[idx])
                                        insert_response(conn, survey_id, question['id'], responses[idx])
                                    st.success("Thank you for your responses!")
                    main()
                else:
                        # Database connection
                            conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/assessment.db')
                            surveys = get_surveys(conn)
                            if len(surveys['survey_id']) == 0:
                                st.write("No assessment available")
                                
                            else:
                                st.write("Your admin has published some assessments.Feel free to take the assessments.Your responses and participation are kept anonymous.")
                            survey_id = st.selectbox('Choose a assessment:', surveys['survey_id'])
                            
                            if survey_id:
                                questions = get_questions(conn, survey_id)
                                printed_questions = set()
                                total_score=0
                                # Assume questions is a DataFrame loaded previously
                                for idx, question in questions.iterrows():
                                    current_question = question['question']
                                    
                                    # Check if the current question has already been printed
                                    if current_question not in printed_questions:
                                        options = [question['option1'], question['option2'], question['option3'], question['option4']]
                                        scores = [question['score1'], question['score2'], question['score3'], question['score4']]
                                        # Generate a unique key for each question
                                        key = f"question_{idx}"
                                        
                                        # Display the question using st.radio
                                        response = st.radio(current_question, options, key=key)
                                        selected_index = options.index(response)
                                        total_score += scores[selected_index]
                                        
                                        # Add the question to the set of printed questions
                                        printed_questions.add(current_question)
                                
                                if st.button('Submit'):
                                    st.success("Thank you for your responses!")
                                    card_html = f"""
                                    <div style="border-radius: 10px; padding: 20px; background-color: lightblue; box-shadow: 0 2px 4px rgba(0,0,0,0.1); color: white;">
                                        <h2 style="color: black;">{"Limited Understanding of Microaggressions" if total_score <= 70 else "Good Understanding of Microaggressions"}</h2>
                                        <p style="color: black;">{"According to your total score, your understanding of microaggressions is limited. You are not alone, and we are glad that you are here to learn more. Let us help you with it." if total_score <= 70 else "Your understanding of microaggressions is quite good! However, there's always room for improvement and deeper understanding."}</p>
                                        <a href="https://www.youtube.com/watch?v=ASWL6jIQbrQ" target="_blank" style="color: darkblue; text-decoration: none; font-weight: bold;">Watch this video on Microaggressions</a>
                                    </div>
                                    """
                                    # Display the card using markdown
                                    st.markdown(card_html, unsafe_allow_html=True)
                                    st.write("")
                                    event_html = f"""
                                    <div style="border-radius: 10px; padding: 20px; background-color: #ffcccb; box-shadow: 0 4px 8px rgba(0,0,0,0.2); color: black;">
                                        <h2 style="color: darkred;">Join Our Understanding Workplace Inclusion!</h2>
                                        <p>Join us at "Understanding Workplace Inclusion," an enriching event designed to explore the vast spectrum of cultures and perspectives that make up our workplace. This celebration is a wonderful opportunity for everyone to learn from each other, share diverse experiences, and collaborate towards fostering a more inclusive environment. Don't miss out on the chance to expand your horizons and contribute to our collective growth in understanding and inclusion.</p>                                        
                                        <p>Date: <strong>July 30, 2024</strong></p>
                                        <p>Location: <strong>Hall 1, UBS Building</strong></p>
                                        <a href="link_to_event_details" target="_blank" style="color: white; background-color: darkred; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px;">Register in Calendar</a>
                                        <h3 style="color: darkred;">Fun Activities Include:</h3>
                                        <ul>
                                            <li>Interactive Workshops</li>
                                            <li>Cultural Performances</li>
                                            <li>Food Tasting from around the world</li>
                                        </ul>
                                        <p>Don't miss out on the fun and learning. Everyone is welcome!</p>
                                    </div>
                                    """
                                    st.markdown(event_html, unsafe_allow_html=True)

                                st.write("")
                                ans=st.radio("Thanks for your participation!Would you like to improve your understanding?",["Not sure yet","Yes","No need"],index=0)
                                if ans=="Yes":
                                        st.header("Understanding Microaggressions")
                                        st.markdown("""
                                            <style>
                                                .card {
                                                    margin: 10px;
                                                    padding: 20px;
                                                    background-color: #ffcccc; /* light red background */
                                                    border: 2px solid #ff0000; /* red border */
                                                    border-radius: 8px;
                                                    box-shadow: 2px 2px 5px grey;
                                                    color: #800000; /* dark red text color */
                                                }
                                            </style>
                                            <div class="card">
                                                <h2 style="color: #ff0000;">Read Maria's Story</h2>
                                                <p>Maria, a talented computer science graduate, was excited when she secured a position at a renowned tech firm that was actively promoting diversity. Her interview had gone exceptionally well, particularly when she discussed her advanced AI project, which impressed the interviewers.

                                            However, on her first day, while setting up her workstation, she overheard a colleague whisper, "She's probably just a diversity hire." The comment stung, especially since the colleague hadn't yet seen her work or knew about her strong academic background.</p>
                                            </div>
                                            """, unsafe_allow_html=True)
                                            
                                        with st.expander("Learn more about Maria's situation"):
                                            st.write("""
                                        **Question: How should Maria respond to the comment?**
                                        
                                        **Answer:** Maria might consider addressing the comment directly with the colleague or seek support from HR or a mentor within the company to discuss her feelings and the appropriate steps to take.
                                        
                                        **Question: What can the company do to prevent such situations?**
                                        
                                        **Answer:** The company should enforce a positive workplace culture that values all employees equally, with training on diversity, inclusion, and sensitivity.

                                        **Question: Why is the concept of a 'diversity hire' a misconception and why is diversity important in the workplace?**
                                        
                                        **Answer:** The term 'diversity hire' often carries a negative implication that individuals are selected based on their demographics rather than their qualifications. This is a misconception because:
                                        
                                        - **Merit and Diversity**: Organizations that emphasize diversity still base hiring decisions on qualifications. The goal is to ensure that hiring practices are fair and inclusive, giving qualified candidates of all backgrounds equal opportunity.
                                        
                                        - **Enhanced Creativity and Innovation**: Diverse teams bring a range of perspectives and experiences, which can lead to more creative solutions and innovations. This can be crucial in problem-solving and adapting to new market trends.
                                        
                                        - **Reflecting the Customer Base**: A diverse workforce can better understand and connect with a varied customer base, thus improving service and increasing customer satisfaction.
                                        
                                        - **Improved Employee Satisfaction and Retention**: Cultivating an inclusive environment where everyone feels valued can lead to higher job satisfaction, lower turnover rates, and a more positive company culture.""")
                                        st.markdown("""
                                            <style>
                                                .card {
                                                    margin: 10px;
                                                    padding: 20px;
                                                    background-color: #ffcccc; /* light red background */
                                                    border: 2px solid #ff0000; /* red border */
                                                    border-radius: 8px;
                                                    box-shadow: 2px 2px 5px grey;
                                                    color: #800000; /* dark red text color */
                                                }
                                            </style>
                                            <div class="card">
                                                <h2 style="color: #ff0000;">YouTube: Understanding Microaggressions</h2>
                                                <iframe width="560" height="315" src="https://www.youtube.com/embed/ASWL6jIQbrQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                                            </div>
                                            <div class="card">
                                                <h2 style="color: #ff0000;">Podcast: Discussing Microaggressions</h2>
                                                <audio controls>
                                                    <source src="full_audio.mp3" type="audio/mpeg">
                                                </audio>
                                            </div>
                                            """, unsafe_allow_html=True)
                                else:
                                    st.write("No worries, You can always check out the learning session on your own!")
                                                                       
    elif st.session_state["menu_choice"]== "Forum":
       discuss_app("Anything to share today?","/Users/moemmyat/Downloads/ubs_prototype/blog.db")
    
    elif st.session_state["menu_choice"]== "Learning":
        learn()

    elif st.session_state["menu_choice"]=="DE&I Chatbot":
        from hugchat import hugchat
        from hugchat.login import Login

        # Hugging Face Credentials
        with st.sidebar:
                st.title('🤗💬 HugChat')
                hf_email = st.text_input('Enter E-mail:', type='password')
                hf_pass = st.text_input('Enter password:', type='password')
                if not (hf_email and hf_pass):
                    st.warning('Please enter your credentials!', icon='⚠️')
                else:
                    st.success('Proceed to entering your prompt message!', icon='👉')
            
        # Store LLM generated responses
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Function for generating LLM response
        def generate_response(prompt_input, email, passwd):
            sign = Login(email, passwd)
            cookies = sign.login()
            cookie_path_dir = "./cookies_snapshot"
            sign.saveCookiesToDir(cookie_path_dir)
            # Create ChatBot                        
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            return chatbot.chat(prompt_input)

        # User-provided prompt
        if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt, hf_email, hf_pass) 
                    st.write(response) 
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)


    elif st.session_state["menu_choice"]== "Admin Portal" and st.session_state['role'] == "Admin":
        import plotly.express as px
        answers = ["Laugh Along", "Confront Privately", "Report to HR", "Suggest Training"]
        responses = [80, 10, 5, 5]  # Assuming these are the numbers of responses

        def plot_responses_with_plotly(answers, responses):
            # Custom pastel-like color scale
            custom_color_scale = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']
            fig = px.bar(
                x=answers, 
                y=responses, 
                text=responses,
                title="Responses to Inappropriate Jokes",
                labels={'x': 'Responses', 'y': 'Number of People'},
                color=responses,
                color_continuous_scale=custom_color_scale  # Using a custom color scale
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')  # Transparent background
            return fig

        # Streamlit application layout
        st.title('Survey Response Visualization')
        st.subheader("This visualization generally represents how survey takers responded as a bystander when faced with inappropriate jokes.")
        st.write("""
        Question: A team member frequently makes jokes that stereotype certain ethnicities. 
        How would you respond? 
        """)

        # Radio button options
        options = [
            "You laugh along to fit in, despite feeling uncomfortable.",
            "You confront them privately, explaining why the jokes are inappropriate.",
            "You report the behavior to HR.",
            "You suggest a team training session on cultural sensitivity."
        ]

        # Create a radio selector for the responses
        response = st.radio("Responses:", options)
        # Plot
        fig = plot_responses_with_plotly(answers, responses)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
                                    <style>
                                        .card {
                                            margin: 10px;
                                            padding: 20px;
                                            background-color: #ffcccc; /* light red background */
                                            border: 2px solid #ff0000; /* red border */
                                            border-radius: 8px;
                                            box-shadow: 2px 2px 5px grey;
                                            color: #800000; /* dark red text color */
                                        }
                                    </style>
                                    <div class="card">
                                        <h2 style="color: #ff0000;">Suggested Actions</h2>
                                        <p>The recent survey highlights a concerning trend: many employees choose to ignore inappropriate jokes, potentially due to fears about job security or a belief that such behavior is normal. To better understand these responses, HR should consider proposing a detailed follow-up survey. Additionally, one should consider publishing a blog post discussing a similar situation and outlining suggested actions. This will not only educate our workforce but also emphasize the importance of maintaining a respectful and safe workplace. It's crucial that all employees feel empowered and responsible for upholding our company's values.</p>
                                    </div>""", unsafe_allow_html=True)
        
        answers_preferential = [
    "Ignore the behavior, assuming it's unintentionial",
    "Gather evidence and discuss with manager",
    "Openly question the fairness in a meeting",
    "Request an anonymous feedback tool"
]

        responses_preferential = [25, 40, 20, 15]  # Hypothetical response counts

        def plot_preferential_treatment_responses(answers, responses):
            custom_color_scale = ['#8da0cb', '#fc8d62', '#e78ac3', '#a6d854']  # Different color scale
            fig = px.bar(
                x=answers,
                y=responses,
                text=responses,
                title="Responses to Preferential Treatment",
                labels={'x': 'Responses', 'y': 'Number of Responses'},
                color=responses,
                color_continuous_scale=custom_color_scale
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            return fig

        # Streamlit application layout
        st.title('Preferential Treatment Response Visualization')
        st.subheader("This visualization shows how survey participants responded to a leader's preferential treatment based on gender and ethnicity.")
        st.write("""
        Question: A project leader openly gives preferential treatment to team members of the same gender and ethnicity. How would you respond?
        """)

        # Create a radio selector for the new scenario
        response_preferential = st.radio("Select your response:", answers_preferential)

        # Plot the new data
        fig_preferential = plot_preferential_treatment_responses(answers_preferential, responses_preferential)
        st.plotly_chart(fig_preferential, use_container_width=True)

    else:
        st.error("Unauthorized Access. Admin only.")
        st.error("Please contact the admin to access the portal!")

# Logout button
if 'username' in st.session_state:
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):  # modified to avoid RuntimeError
            del st.session_state[key]
        st.experimental_rerun()