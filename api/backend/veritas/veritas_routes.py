from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db 
from mysql.connector import Error

# Create a Blueprint for the Veritas Patissier API routes
# NOTE - Don't forget to register it with the main Flask App -- OK
veritas_api = Blueprint("veritas_api", __name__)



# --- Table Setup Route (for testing/initialization) ---
@veritas_api.route("/setup_tables", methods=["GET"]) # Using GET for simplicity in browser testing
def setup_tables():
    conn = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        current_app.logger.info("Attempting to create database tables for Veritas API.")

        # Drop tables if they exist (for easy re-running during development)
        cursor.execute("DROP TABLE IF EXISTS Clues;")
        cursor.execute("DROP TABLE IF EXISTS Artifacts;")
        cursor.execute("DROP TABLE IF EXISTS Locations;")
        cursor.execute("DROP TABLE IF EXISTS HistoricalFigures;") # Basic for FK reference
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        current_app.logger.info("Dropped existing tables (if any).")

        # Create Locations Table
        cursor.execute("""
            CREATE TABLE Locations (
                LocationID INT AUTO_INCREMENT PRIMARY KEY,
                SiteName VARCHAR(255) NOT NULL,
                City VARCHAR(100),
                Country VARCHAR(100),
                Latitude DECIMAL(9,6),
                Longitude DECIMAL(9,6),
                Description TEXT,
                ParentLocationID INT,
                FOREIGN KEY (ParentLocationID) REFERENCES Locations(LocationID) ON DELETE SET NULL
            );
        """)
        current_app.logger.info("Locations table created successfully.")

        # -----------------------------------------------------------------------
        # NOTE - OH NOte - Tydney didn't finish this table.  Quick - add in 
        # the missing attributes! Don't forget any foreign keys!
        cursor.execute("""
            CREATE TABLE HistoricalFigures (
                FigureID INT AUTO_INCREMENT PRIMARY KEY,
                FigName VARCHAR(100) NOT NULL,
                BirthYear INT NOT NULL,
                DeathYear INT,
                PrimaryCulinaryArt VARCHAR(100),
                SocietyRank VARCHAR(100)
            );
        """)
        current_app.logger.info("HistoricalFigures table created successfully.")

        # -----------------------------------------------------------------------
        # NOTE - What?? Tydney didn't finish Artifacts either - Help!
        # And don't forget those FKs. 
        cursor.execute("""
            CREATE TABLE Artifacts (
                ArtifactID INT AUTO_INCREMENT PRIMARY KEY,
                ArtName VARCHAR(100) NOT NULL,
                Material VARCHAR(100),
                ToolType VARCHAR(100),
                EstDateOfOrigin DATE,
                HistFigID INT,
                LocID INT,
                FOREIGN KEY (HistFigID) REFERENCES HistoricalFigures(FigureID),
                FOREIGN KEY (LocID) REFERENCES Locations(LocationID)

            );
        """)
        current_app.logger.info("Artifacts table created successfully.")

        # -----------------------------------------------------------------------
        # NOTE - Wow - Tydney was really smelling the spiced Cocoa and didn't finish the
        # Clues table either.  Quick - Rescue the data model! 
        cursor.execute("""
            CREATE TABLE Clues (
                ClueID INT AUTO_INCREMENT PRIMARY KEY,
                Description TEXT,
                DateDiscovered DATE,
                DiscoveredAtLocationID INT,
                HistFigID INT,
                ArtID INT,
                FollowClueID INT,
                FOREIGN KEY (DiscoveredAtLocationID) REFERENCES Locations(LocationID),
                FOREIGN KEY (HistFigID) REFERENCES HistoricalFigures(FigureID),
                FOREIGN KEY (FollowClueID) REFERENCES Clues(ClueID)

            );
        """)
        current_app.logger.info("Clues table created successfully.")
        
        # -----------------------------------------------------------------------
        # NOTE - Add a couple different Locations and clues to the DB for testing purposes
        cursor.execute("""
            INSERT INTO Locations (SiteName, City, Country, Latitude, Longitude, Description, ParentLocationID)
            VALUES
            ("Nihoul Pastry Shop", "Brussels", "Belgium", 50.8260, 4.3802, "Nihoul Pastry Shop is the oldest patisserie/chocolaterie in Belgium!", NULL),
            ("Chocolatte", "Leuven", "Belgium", 50.8791, 4.7025, "Chocolatte is a coffee shop with multiple locations, one being in Leuven", NULL);
        """)

        cursor.execute("""
            INSERT INTO HistoricalFigures (FigName, BirthYear, DeathYear, PrimaryCulinaryArt, SocietyRank)
            VALUES ("Barno", 1962, 2020, "Chocolate", "King");
        """)
            
        cursor.execute("""
            INSERT INTO Artifacts (ArtName, Material, ToolType, EstDateOfOrigin, HistFigID, LocID)
            VALUES ("Spatula", "Metal", "Spatula", "1979-11-02", 1, 2);
            
        """)  
        
        cursor.execute("""
            INSERT INTO Clues (Description, DateDiscovered, DiscoveredAtLocationID, HistFigID, ArtID, FollowClueID)
            VALUES
            ("This is a cryptic recipe note", "2024-01-10", 1, 1, 1, 1),
            ("This is a local legend about a spatula", "2025-04-27", 2, 1, 1, 1);
        """)

        conn.commit()
        cursor.close()
        return jsonify({"message": "Veritas tables created (or reset) successfully!"}), 200
    except Error as e:
        current_app.logger.error(f"Database error during table setup: {str(e)}")
        if conn:
            conn.rollback() # Rollback in case of error
        return jsonify({"error": f"Database error: {str(e)}"}), 500


# --- Location Routes ---
@veritas_api.route("/locations", methods=["GET"])
def get_all_locations():
    conn = None
    try:
        current_app.logger.info("Request received for get_all_locations.")
        conn = db.get_db()
        cursor = conn.cursor()

        query = "SELECT * FROM Locations"
        params = []
       
        # Optional filters could be added here, e.g., ?city=Brussels
        city_filter = request.args.get("city")
        if city_filter:
            query += " WHERE City = %s"
            params.append(city_filter)
        # -----------------------------------------------------------------------    
        # NOTE - Add an additional filter for country!!
        country_filter = request.args.get("country")
        if country_filter:
            query += " WHERE Country = %s"
            params.append(country_filter)

        
        cursor.execute(query, params)
        locations = cursor.fetchall()
        cursor.close()
        current_app.logger.info(f"Successfully retrieved {len(locations)} locations.")
        return jsonify(locations), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_locations: {str(e)}")
        return jsonify({"error": str(e)}), 500


@veritas_api.route("/locations/<int:location_id>", methods=["GET"])
def get_location(location_id):
    conn = None
    try:
        current_app.logger.info(f"Request received for get_location with ID: {location_id}.")
        conn = db.get_db()
        cursor = conn.cursor()

        # -----------------------------------------------------------------------
        # NOTE - OH NO - Tydney didn't get to write the query to retrieve a 
        # specific location's information.  
        # Quick add in a SELECT statement that will retrieve all the attributes 
        # about the location passed in as location_id
        cursor.execute("SELECT * FROM Locations WHERE LocationID = %s", (location_id,))
        location = cursor.fetchone() #returns first
        cursor.close()

        if not location:
            current_app.logger.warn(f"Location with ID {location_id} not found.")
            return jsonify({"error": "Location not found"}), 404
        
        locations = cursor.fetchall()

        current_app.logger.info(f"Successfully retrieved location with ID: {location_id}.")
        return jsonify(location), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_location: {str(e)}")
        return jsonify({"error": str(e)}), 500
    



# -----------------------------------------------------------------------
# NOTE - Looks like this route might be OK - but double check it for
# any potential issues. It should be returning any clues associated with
# a particular location. 

@veritas_api.route("/locations/<int:location_id>/clues", methods=["GET"])
def get_clues_at_location(location_id):
    conn = None
    try:
        current_app.logger.info(f"Request for clues at location ID: {location_id}.")
        conn = db.get_db()
        cursor = conn.cursor()

        # -----------------------------------------------------------------------
        # First, check if location exists in the database.  If it doesn't,
        # Return a message stating that marked up as JSON. 
        cursor.execute("SELECT * FROM Locations WHERE LocationID = %s", (location_id,))
        if not cursor.fetchone():
            #current_app.logger.warn(f"Location with ID {location_id} not found for fetching clues.")
            return jsonify({"error": "Location not found in the database"}), 404

        # -----------------------------------------------------------------------
        # If we get past that, get any clues associated with that location id
        # and return them to the client. 
        cursor.execute("SELECT * FROM Clues WHERE DiscoveredAtLocationID = %s", (location_id,))
        clues = cursor.fetchall()
        
        cursor.close()
        
        current_app.logger.info(f"Successfully retrieved {len(clues)} clues for location ID: {location_id}.")
        return jsonify(clues), 200
    
    except Error as e:
        current_app.logger.error(f"Database error in get_clues_at_location: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    


# -----------------------------------------------------------------------
# NOTE - HELP - We desperately need a POST route to add a new Clue to the Database.
# Can you add one please??  Ferber provided the decorator for you but it
# is commented out!! 
@veritas_api.route("/clues", methods=["POST"])
def add_clue():
    try:
        data = request.json()

        # Validate required fields
        required_fields = ["Description", "DateDiscovered", "DiscoveredAtLocationID", "HistFigID", "ArtID", "FollowClueID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()

        # Insert new Clue
        query = """
        INSERT INTO Clues (Description, DateDiscovered, DiscoveredAtLocationID, HistFigID, ArtID, FollowClueID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query, 
            (
                data["Description"],
                data["DateDiscovered"],
                data["DiscoveredAtLocationID"],
                data["HistFigID"],
                data["ArtID"],
                data["FollowClueID"]
            )
        )

        db.get_db().commit()
        new_clue_id = cursor.lastrowid
        cursor.close()

        return (
            jsonify({"message": "Clue created successfully", "clue_id": new_clue_id}),
            201,
        )

    except Error as e:
        return jsonify({"error": str(e)}), 500
 

