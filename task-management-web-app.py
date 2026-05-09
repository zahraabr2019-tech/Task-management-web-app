import streamlit as st
import sqlite3


# Connect to SQLite database
def create_connection():
    conn = sqlite3.connect('D:/python projects/new_db.db')
    return conn


def verify_user(user_id, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_pass FROM user WHERE user_id=?", (user_id,))
    result = cursor.fetchone()

    if result:
        if result[0] == password:
            return "success"
        else:
            return "wrong_password"
    else:
        return "no_user"


def login_form():
    st.title("Login Form")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login_result = verify_user(user_id, password)

        if login_result == "success":
            st.info("Successful login!")
            st.session_state.current_user = user_id
            st.session_state.page = "Define Task"
            st.session_state["logged_in"] = True
            st.session_state["login_action"] = True
        elif login_result == "wrong_password":
            st.error("Incorrect password. Please try again.")
        elif login_result == "no_user":
            st.error("User ID does not exist. Please check your User ID or sign up.")


def create_user(user_id, password, email):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO user (user_id, user_pass, email) VALUES (?, ?, ?)", (user_id, password, email))
        conn.commit()
        return "User created successfully!"
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            return "User ID or email already exists. Please try a different one."
        else:
            return f"An error occurred: {e}"
    finally:
        conn.close()


def signup_form():
    st.title("Signup Form")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")

    if st.button("Sign Up"):
        if not user_id or not password or not email:
            st.error("All fields are required!")
        else:
            result = create_user(user_id, password, email)
            if "successfully" in result:
                st.success(result)
                st.session_state.current_user = user_id
                st.session_state.page = "Define Task"  
                st.session_state["logged_in"] = True  
            else:
                st.error(result)


def get_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM user")
    users = cursor.fetchall()
    conn.close()
    return users


def get_next_task_id():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM task")
    count = cursor.fetchone()[0]
    conn.close()
    return str(count + 1)


def create_task(task_id, task_name, description, priority, assigned_user, creator):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO task (task_id, task_name, description, priority, assigned_user, creator, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (task_id, task_name, description, priority, assigned_user, creator, 'new'))  # Default status is 'new'
        conn.commit()
        return "Task created successfully!"
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            return "Task ID already exists. Please try a different one."
        else:
            return f"An error occurred: {e}"
    finally:
        conn.close()


def define_task_form():
    st.title("Define Task")    
    st.sidebar.write("in this form you can define tasks for yourself or other users.")

    task_id = get_next_task_id()
    task_name = st.text_input("Task Name")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["1", "2", "3", "4", "5"])
    users = get_users()
    user_names = [user[0] for user in users]
    assigned_user = st.selectbox("Assign to User", user_names)
    creator = st.session_state.get("current_user")

    if st.button("Create Task"):
        result = create_task(task_id, task_name, description, priority, assigned_user, creator)
        if "successfully" in result:
            st.success(result)
        else:
            st.error(result)


def update_task_status(task_id, new_status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE task SET status = ? WHERE task_id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
    st.success(f"Status for Task ID {task_id} updated to {new_status}.")
    st.session_state['last_task_updated'] = task_id


def view_tasks_form():
    st.title("View Tasks")
    st.sidebar.write("in this form you can see the tasks you should do!")
    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("You need to log in to view tasks.")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, task_name, description, priority, status FROM task WHERE assigned_user = ?", (current_user,))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        st.info("No tasks assigned to you.")
        return

    for i, task in enumerate(tasks):
        task_id, task_name, description, priority, status = task

        if status == "done":
            st.markdown(f"### ~~Task ID: {task_id} - {task_name}~~")
            st.markdown(f"**Description**: ~~{description}~~")
            st.markdown(f"**Priority**: ~~{priority}~~")
            st.markdown(f"**Status**: ~~{status}~~")
        else:
            st.subheader(f"Task ID: {task_id} - {task_name}")
            st.write(f"**Description**: {description}")
            st.write(f"**Priority**: {priority}")
            st.write(f"**Status**: {status}")

        if status != "done":
            new_status = st.selectbox(
                f"Update status for Task ID {task_id}",
                options=["waiting", "done"],
                index=["waiting", "done"].index(status) if status in ["waiting", "done"] else 0,
                key=f"status_{task_id}"
            )

            if st.button(f"Update Status for Task {task_id}", key=f"update_{task_id}"):
                update_task_status(task_id, new_status)

        st.markdown("---")


def check_tasks_form():
    st.title("Check Tasks")
    
    st.sidebar.write("in this form you can check the status of tasks you have defined.")
    
    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("You need to log in to check tasks.")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, task_name, description, priority, status FROM task WHERE creator = ?", (current_user,))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        st.info("No tasks created by you.")
        return

    for task in tasks:
        task_id, task_name, description, priority, status = task
        if status == "done":
            st.markdown(f"### ~~Task ID: {task_id} - {task_name}~~")
            st.markdown(f"**Description**: ~~{description}~~")
            st.markdown(f"**Priority**: ~~{priority}~~")
            st.markdown(f"**Status**: ~~{status}~~")
        else:
            st.subheader(f"Task ID: {task_id} - {task_name}")
            st.write(f"**Description**: {description}")
            st.write(f"**Priority**: {priority}")
            st.write(f"**Status**: {status}")

        st.markdown("---")


def update_task_field(task_id, field, new_value):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"UPDATE task SET {field} = ? WHERE task_id = ?"
    cursor.execute(query, (new_value, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM task WHERE task_id = ?", (task_id,))
    conn.commit()
    conn.close()


def change_task_form():
    st.title("Change Task")
    
    st.sidebar.write("in this form you can change or delete tasks you have defined.")
    st.sidebar.write("!! but only is it not done yet!!")

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("You need to log in to change tasks.")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, task_name, description, priority, status FROM task WHERE creator = ? AND status = 'new'", (current_user,))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        st.info("No tasks with status 'new' created by you.")
        return

    selected_task_id = st.selectbox("Select Task to Modify", [task[0] for task in tasks])
    selected_task = next((task for task in tasks if task[0] == selected_task_id), None)

    if selected_task:
        task_id, task_name, description, priority, status = selected_task

        new_task_name = st.text_input("Task Name", task_name)
        new_description = st.text_area("Description", description)
        new_priority = st.selectbox("Priority", ["1", "2", "3", "4", "5"], index=["1", "2", "3", "4", "5"].index(priority))

        if st.button("Update Task"):
            update_task_field(task_id, "task_name", new_task_name)
            update_task_field(task_id, "description", new_description)
            update_task_field(task_id, "priority", new_priority)
            st.success("Task updated successfully!")

        if st.button("Delete Task"):
            delete_task(task_id)
            st.success("Task deleted successfully!")


def main():
    if "page" not in st.session_state:
        st.session_state.page = "Login"
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state.page == "Login":
        login_form()
    elif st.session_state.page == "Sign Up":
        signup_form()
    elif st.session_state.page == "Define Task":
        define_task_form()
    elif st.session_state.page == "View Tasks":
        view_tasks_form()
    elif st.session_state.page == "Check Tasks":
        check_tasks_form()
    elif st.session_state.page == "Change Task":
        change_task_form()

    
    st.sidebar.title("Navigation")

    if st.session_state["logged_in"]:
        form_selection = st.sidebar.selectbox(
            "Select Form",
            options=["Define Task", "View Tasks", "Check Tasks", "Change Task", "Login", "Sign Up"],
            key="form_selection"
        )
        st.session_state.page = form_selection  
    else:
        nav_selection = st.sidebar.selectbox(
            "Select Page",
            options=["Login", "Sign Up"],
            key="nav_selection"
        )
        st.session_state.page = nav_selection


if __name__ == "__main__":
    main()
