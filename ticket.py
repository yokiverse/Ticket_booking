import smtplib
import mysql.connector

class RohitCinimas:
    def __init__(self):
        self.movies = ['garudan', 'aharaja', 'ookuthi amman']
        self.classes = {"first class": 150, "second class": 200}
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="rohit_theater"
        )
        self.cursor = self.db.cursor()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS rohit_theater")
        self.db.commit()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_name VARCHAR(255),
                email VARCHAR(255),
                total DECIMAL(10, 2)
            )
        """)
        self.db.commit()

    def display_movies(self):
        print("ROHIT CINIMAS")
        print("Available movies:")
        for movie in self.movies:
            print(movie)

    def get_movie_details(self):
        Enter_movie = input("Enter movie name: ")
        if Enter_movie in self.movies:
            print("Movie is available")
            return Enter_movie
        else:
            print("Movie is not available")
            return None

    def get_class_details(self):
        enter_class = input("Enter your class: ")
        if enter_class in self.classes:
            print("Your ticket price is", self.classes[enter_class])
            return enter_class
        else:
            print("Class is not available")
            return None

    def calculate_total(self, enter_class, how_many):
        total = self.classes[enter_class] * int(how_many)
        print("Your total price is", total)
        return total

    def make_payment(self, cm, pay):
        if cm == "on hand" and pay == "paid":
            print("Your ticket is booked")
            return True
        elif cm == "online" and pay == "paid":
            print("Your ticket is booked")
            return True
        else:
            print("Your ticket is not booked")
            return False

    def send_email(self, bill, total):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("yokeshrajasekaran01@gmail.com", "ytzm rgsr bpvs nswn")
            msg = f"Your Total price: {total}"
            s.sendmail("yokeshrajasekaran01@gmail.com", bill, msg)
            s.quit()
            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print("Error sending email:", e)
        except Exception as e:
            print("An error occurred:", e)

    def book_ticket(self):
        self.display_movies()
        Enter_movie = self.get_movie_details()
        if Enter_movie:
            enter_class = self.get_class_details()
            if enter_class:
                how_many = int(input("How many tickets: "))
                total = self.calculate_total(enter_class, how_many)
                cm = input("Is cash pay in online or on hand: ")
                pay = input("paid/unpaid? ")
                if self.make_payment(cm, pay):
                    bill = input("Enter your mail for bill: ")
                    self.send_email(bill, total)
                    self.cursor.execute("""INSERT INTO movies (movie_name, email, total)VALUES (%s, %s, %s)""", (Enter_movie, bill, total))
                    self.db.commit()
                    print("Ticket booked successfully!")

if __name__ == "__main__":
    rohit_cinimas = RohitCinimas()
    rohit_cinimas.create_database()
    rohit_cinimas.create_table()
    while True:
        command = input("Type 'book' to book a ticket or 'exit' to exit: ")
        if command.lower() == 'exit':
            break
        elif command.lower() == 'book':
            rohit_cinimas.book_ticket()
        else:
            print("Invalid command. Please try again.")