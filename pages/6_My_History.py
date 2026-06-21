import streamlit as st
import json
from supabase import create_client, ClientOptions

# --- SECURITY: Redirect if not logged in ---
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("app.py")

st.title("🗄️ Database Records & History")

# --- SUPABASE INIT ---
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"], options=ClientOptions(postgrest_client_timeout=10))
except:
    st.error("Database connection failed.")
    st.stop()

def get_history(user_id):
    try:
        res = supabase.table("users_history").select("id, created_at, work_data").eq("user_id", user_id).order("created_at", desc=True).execute()
        return res.data
    except: return []

def delete_session(session_id):
    try:
        supabase.table("users_history").delete().eq("id", session_id).execute()
        return True
    except: return False

def update_session_name(session_id, current_data, new_name):
    try:
        current_data["Session_Name"] = new_name
        supabase.table("users_history").update({"work_data": json.dumps(current_data)}).eq("id", session_id).execute()
        return True
    except: return False

hist = get_history(st.session_state.user.id)

if len(hist) == 0:
    st.info("No records found in database. Save an analysis from the Corporate Analysis tab first.")
else:
    for item in hist:
        session_id = item['id']
        date_str = item['created_at'][:10]
        data = json.loads(item['work_data'])
        session_name = data.get('Session_Name', f"Session: {date_str}")
        
        with st.expander(f"📊 {session_name}"):
            st.write(f"**Date Recorded:** {data.get('Date', 'N/A')}")
            st.write(f"**Revenue:** {data.get('Revenue', 0):,.2f} MAD")
            st.write(f"**Net Margin:** {data.get('Net Margin', 0)}%")
            st.write(f"**ROE:** {data.get('ROE', 0)}%")
            
            st.markdown("---")
            col_ren, col_del = st.columns([3, 1])
            
            with col_ren:
                new_name = st.text_input("Rename Session", value=session_name, key=f"rename_{session_id}", label_visibility="collapsed")
                if st.button("✏️ Update Name", key=f"btn_ren_{session_id}"):
                    if update_session_name(session_id, data, new_name):
                        st.success("Renamed successfully!")
                        st.rerun()
                        
            with col_del:
                if st.button("🗑️ Delete", key=f"btn_del_{session_id}", type="primary", use_container_width=True):
                    if delete_session(session_id):
                        st.success("Deleted!")
                        st.rerun()
