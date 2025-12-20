import streamlit as st
import restaurant
st.set_page_config(page_title="Nigerian Fusion Generator", page_icon="🇳🇬")

st.title("🇳🇬 Nigerian Fusion Food Name Generator")

# sidebar selection for the user
country = st.sidebar.selectbox(
    "Pick a Country",
    ("India", "Italy", "Mexico", "Saudi Arabia", "USA",
     "China", "Japan", "Brazil", "South Africa", "Australia")
)

# when a country is selected, generate the content
if country:
    # use the function from your restaurant.py file
    with st.spinner(f"Creating a Nigerian-fusion concept for {country}..."):
        response = restaurant.generate_restaurant_name_and_items(country)

    # display the Restaurant Name
    # result['restaurant_name'] comes from your helper
    st.header(response['restaurant_name'].strip())

    # process and display menu Items
    # result['menu_items'] is a comma-separated string from your helper
    menu_items = response['menu_items'].strip().split(",")

    st.write("### **Gourmet Fusion Menu**")

    # create a nice layout for the menu items
    for item in menu_items:
        st.write(f"🍴 {item.strip()}")

    # display the country name for confirmation
    st.sidebar.info(f"Currently viewing: {response.get('country')}")