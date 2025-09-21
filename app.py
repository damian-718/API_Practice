from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flightdb",
        user="postgres",
        password="password"
    )
    return conn


@app.route("/flights", methods=["GET"])
def get_cheapest_flight():
    origin = request.args.get("origin")
    dest = request.args.get("dest")
    date = request.args.get("date")

    conn = get_db_connection() # this connects to the database
    cur = conn.cursor() # this is the actual worker which can point to rows

    # triple qoutes best for SQL syntax
    cur.execute("""
        SELECT id, airline, origin, destination, departure_time, arrival_time, price, available_seats
        FROM flights
        WHERE origin=%s AND destination=%s AND departure_time >= %s;
    """, (origin, dest, date))
    
    rows = cur.fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "airline": r[1],
            "origin": r[2],
            "destination": r[3],
            "departure_time": r[4],
            "arrival_time": r[5],
            "price": r[6],
            "available_seats": r[7]
        })

    # clean up resources, we dont need worker holding onto memory or locking rows
    cur.close()
    conn.close()

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)