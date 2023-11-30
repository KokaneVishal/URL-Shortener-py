import string
import random
import sqlite3


class URLShortener:
    def __init__(self, db_name="url_shortener.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT NOT NULL
            )
        """
        )
        self.connection.commit()

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        short_code = "".join(
            random.choice(characters) for _ in range(6)
        )  # You can adjust the length of the short code
        return short_code

    def shorten_url(self, original_url):
        short_code = self.generate_short_code()
        self.cursor.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, short_code),
        )
        self.connection.commit()
        return short_code

    def get_original_url(self, short_code):
        self.cursor.execute(
            "SELECT original_url FROM urls WHERE short_code = ?", (short_code,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def close(self):
        self.connection.close()


# Example usage
if __name__ == "__main__":
    url_shortener = URLShortener()
    # Add your original URLs here
    original_url = "https://www.example.com"
    short_code = url_shortener.shorten_url(original_url)
    print(f"Shortened URL: http://short.url/{short_code}")

    retrieved_url = url_shortener.get_original_url(short_code)
    if retrieved_url:
        print(f"Original URL: {retrieved_url}")
    else:
        print("Short code not found.")

    url_shortener.close()
