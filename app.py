from fastapi import FastAPI, HTTPException
import requests
import xml.etree.ElementTree as ET

app = FastAPI()
XML_URL = "https://explore.com.my/wp-content/Properties-Export-2024-December-18-1223.xml"

# # Database connection
# def get_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host="host.keyspacerealty.com",
#             user="exploretest1@explore.com.my",
#             password="Test@123!!",
#             database="explore-my-db"
#         )
#         if connection.is_connected():
#             print("Successfully connected to the database")
#         return connection
#     except Error as e:
#         print(f"Error while connecting to the database: {e}")
#         return None

# @app.get("/fetch-data")
# def fetch_data():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM wp_posts")
#     data = cursor.fetchall()
#     conn.close()
#     return data

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get-properties")
async def get_properties():
    try:
        # Fetch the XML content from the URL
        response = requests.get(XML_URL)
        response.raise_for_status()  # Raise an HTTP error if occurred
        # Parse the XML content
        root = ET.fromstring(response.content)
        print(root)
        
        # Extract data from the XML
        posts = []
        for post in root.findall('.//post'):  # Adjust the tag based on the XML structure
            post_data = {
                "ID": post.find('ID').text if post.find('ID') is not None else None,
                "Title": post.find('Title').text if post.find('Title') is not None else None,
                "Content": post.find('Content').text if post.find('Content') is not None else None
            }
            posts.append(post_data)

        # Return the parsed data as JSON
        return {"posts": posts}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching the XML file: {str(e)}")
    except ET.ParseError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing the XML file: {str(e)}")
