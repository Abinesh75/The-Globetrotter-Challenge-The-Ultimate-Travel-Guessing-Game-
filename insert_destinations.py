import json
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin@123",
        database="globetrotter_db"
    )

def insert_destinations(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        destinations = json.load(f)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    inserted_count = 0
    
    for i, dest in enumerate(destinations):
        if "city" not in dest or "country" not in dest or "clues" not in dest or "fun_fact" not in dest or "trivia" not in dest:
            continue
        
        try:
            cursor.execute(
                """
                INSERT INTO destinations (city, country, clues, fun_fact, trivia)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    dest["city"],
                    dest["country"],
                    json.dumps(dest["clues"], ensure_ascii=False),
                    json.dumps(dest["fun_fact"], ensure_ascii=False),
                    json.dumps(dest["trivia"], ensure_ascii=False)
                )
            )
            inserted_count += 1
        except mysql.connector.Error:
            continue
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Successfully inserted {inserted_count} destinations!")

if __name__ == "__main__":
    insert_destinations("expanded_travel_dataset.json")
