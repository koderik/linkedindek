import re
import os
import psycopg2
from flask import Flask, render_template, request
import qrcode
import qrcode.image.svg
import io




app = Flask(__name__)

# Get PostgreSQL configuration from environment variables
# from dotenv import load_dotenv

# # Load environment variables from .env.local file during development
# load_dotenv(dotenv_path=".env.local")
db_config = {
    "host": os.environ.get("POSTGRES_HOST"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "dbname": os.environ.get("POSTGRES_DATABASE"),
}


def connect_to_database():
    try:
        connection = psycopg2.connect(**db_config)
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


def check_linkedin_url_exists(linkedin_url):
    connection = connect_to_database()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM submissions WHERE linkedin_url = %s"
            cursor.execute(query, (linkedin_url,))
            count = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            return count > 0
        except psycopg2.Error as e:
            print(f"Error executing the query: {e}")
    return False


def add_linkedin_url(name, year, linkedin_url):
    connection = connect_to_database()
    if connection is not None:
        try:
            # create table if it doesn't exist

            cursor = connection.cursor()

            # create table if it doesn't exist
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS submissions (id SERIAL PRIMARY KEY, name VARCHAR(255), year VARCHAR(255), linkedin_url VARCHAR(255))"
            )

            query = (
                "INSERT INTO submissions (name, year, linkedin_url) VALUES (%s, %s, %s)"
            )
            cursor.execute(query, (name, year, linkedin_url))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except psycopg2.Error as e:
            print(f"Error executing the query: {e}")
    return False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        year = request.form["year"]
        linkedin_url = request.form["linkedin_url"]
        valid, error = validate_linkedin_url(linkedin_url)

        if "skip" in request.form:  # Check if the skip button was clicked
            return result()
        if valid:
            if check_linkedin_url_exists(linkedin_url):
                error = "LinkedIn URL has already been submitted"
                return render_template(
                    "form.html",
                    name=name,
                    year=year,
                    linkedin_url=linkedin_url,
                    error=error,
                )
            else:
                add_linkedin_url(name, year, linkedin_url)
                return result()
        else:
            return render_template(
                "form.html",
                name=name,
                year=year,
                linkedin_url=linkedin_url,
                error=error,
            )
    return render_template(
        "form.html",
        linkedin_url="https://www.linkedin.com/in/sandlov/",
        name="Erik",
        year="2021",
    )


def validate_linkedin_url(linkedin_url):
    pattern = r"^https?://www.linkedin.com/in/[\w-]+/?$"
    if re.match(pattern, linkedin_url):
        return True, None
    else:
        return False, "Invalid LinkedIn URL format"


# Add a new route to display all entries in the database
@app.route("/result", methods=["GET"])
def result():
    connection = connect_to_database()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "SELECT name, year, linkedin_url FROM submissions"
            cursor.execute(query)
            entries = cursor.fetchall()
            # convert the list of tuples to a list of lists
            entries = [list(entry) for entry in entries]

            cursor.close()
            connection.close()
            # for each entry, generate a QR code to the LinkedIn URL to svg format and add it to the list
            for entry in entries:
                # resize the QR code to 40 mm
                factory = qrcode.image.svg.SvgPathImage
                img = qrcode.make(entry[2], image_factory=factory, box_size=20)
                
                stream = io.BytesIO()
                img.save(stream)

                data = stream.getvalue().decode()
                # replace width="Xmm" with width="40mm"
                data = re.sub(r'width="\d+mm"', 'width="40mm"', data)
                # replace height="Xmm" with height="40mm"
                data = re.sub(r'height="\d+mm"', 'height="40mm"', data)

                # append the path to the svg image to the entry
                

                
                entry.append(data)
                

            


            return render_template("result.html", entries=entries)
        except psycopg2.Error as e:
            print(f"Error executing the query: {e}")
    return render_template("result.html", entries=None)






if __name__ == "__main__":
    # try to connect to the database
    app.run()
