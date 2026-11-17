import pymysql
from pymysql.err import MySQLError



GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "film_kolleksiyasi_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}


def get_connection():
    """MySQL ma'lumotlar bazasiga ulanishni ta'minlaydi."""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except MySQLError as e:
        print(f"{RED}❌ Ma'lumotlar bazasiga ulanishda xatolik: {e}{RESET}")
        return None


def create_table():
    """movies jadvali mavjud bo'lmasa, uni yaratadi."""
    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS movies (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            director VARCHAR(255),
            year INT
        )
        """
        cursor.execute(sql)
        connection.commit()
    except MySQLError as e:
        print(f"{RED}❌ Jadval yaratishda xatolik: {e}{RESET}")
    finally:
        if cursor:
            cursor.close()
        connection.close()


def add_movie():
    """Yangi film ma'lumotlarini tekshiradi va bazaga qo'shadi."""
    print(f"\n{CYAN}--- 🎬 Yangi film qo'shish ---{RESET}")
    
    
    while True:
        title = input("Film nomi (majburiy): ").strip()
        if title:
            break
        print(f"{YELLOW}⚠️ Film nomi bo'sh bo'lishi mumkin emas!{RESET}")

    genre = input("Janri: ").strip() or None
    director = input("Rejissyor: ").strip() or None

    
    year = None
    while True:
        year_input = input("Chiqgan yili (masalan, 2024): ").strip()
        if not year_input:
            break
        if year_input.isdigit():
            year = int(year_input)
            break
        print(f"{YELLOW}⚠️ Yil faqat butun sondan iborat bo'lishi kerak!{RESET}")

    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO movies (title, genre, director, year) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (title, genre, director, year))
        connection.commit()
        print(f"{GREEN}✅ '{title}' filmi kolleksiyaga muvaffaqiyatli qo'shildi!{RESET}")
    except MySQLError as e:
        print(f"{RED}❌ Film qo'shishda xatolik yuz berdi: {e}{RESET}")
    finally:
        if cursor:
            cursor.close()
        connection.close()


def list_movies():
    """Barcha filmlar ro'yxatini jadval ko'rinishida chiqaradi."""
    print(f"\n{CYAN}--- 🎞️ Filmlar ro'yxati ---{RESET}")
    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY id ASC")
        movies = cursor.fetchall()

        if not movies:
            print(f"{YELLOW}📭 Hali filmlar yo'q.{RESET}")
            return

        print("-" * 78)
        print(f"{'ID':<5} | {'Nomi':<25} | {'Janr':<15} | {'Rejissyor':<18} | {'Yil':<6}")
        print("-" * 78)
        for m in movies:
            genre = m['genre'] if m['genre'] else "-"
            director = m['director'] if m['director'] else "-"
            year = str(m['year']) if m['year'] else "-"
            print(f"{m['id']:<5} | {m['title'][:24]:<25} | {genre[:14]:<15} | {director[:17]:<18} | {year:<6}")
        print("-" * 78)
    except MySQLError as e:
        print(f"{RED}❌ Ro'yxatni olishda xatolik: {e}{RESET}")
    finally:
        if cursor:
            cursor.close()
        connection.close()


def update_movie():
    """Tanlangan ID bo'yicha film ma'lumotlarini yangilaydi."""
    print(f"\n{CYAN}--- ✏️ Film ma'lumotlarini yangilash ---{RESET}")
    movie_id_input = input("Yangilamoqchi bo'lgan film ID sini kiriting: ").strip()
    
    if not movie_id_input.isdigit():
        print(f"{YELLOW}⚠️ ID butun son bo'lishi kerak!{RESET}")
        return

    movie_id = int(movie_id_input)
    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
        movie = cursor.fetchone()

        if not movie:
            print(f"{RED}❌ ID={movie_id} bo'lgan film topilmadi.{RESET}")
            return

        print(f"{YELLOW}Eslatma: O'zgartirmaslik uchun maydonni bo'sh qoldiring (Enter bosing).{RESET}")
        
        new_title = input(f"Yangi nomi [{movie['title']}]: ").strip() or movie['title']
        
        curr_genre = movie['genre'] or ""
        new_genre_in = input(f"Yangi janri [{curr_genre}]: ").strip()
        new_genre = new_genre_in if new_genre_in else movie['genre']

        curr_dir = movie['director'] or ""
        new_dir_in = input(f"Yangi rejissyor [{curr_dir}]: ").strip()
        new_director = new_dir_in if new_dir_in else movie['director']

        curr_year = str(movie['year']) if movie['year'] else ""
        new_year = movie['year']
        while True:
            year_in = input(f"Yangi yili [{curr_year}]: ").strip()
            if not year_in:
                break
            if year_in.isdigit():
                new_year = int(year_in)
                break
            print(f"{YELLOW}⚠️ Yil butun son bo'lishi kerak!{RESET}")

        sql = """
        UPDATE movies 
        SET title = %s, genre = %s, director = %s, year = %s 
        WHERE id = %s
        """
        cursor.execute(sql, (new_title, new_genre, new_director, new_year, movie_id))
        connection.commit()
        print(f"{GREEN}✅ Film ma'lumotlari muvaffaqiyatli yangilandi!{RESET}")
    except MySQLError as e:
        print(f"{RED}❌ Yangilashda xatolik yuz berdi: {e}{RESET}")
    finally:
        if cursor:
            cursor.close()
        connection.close()


def delete_movie():
    """Tanlangan ID bo'yicha filmni bazadan o'chiradi."""
    print(f"\n{CYAN}--- 🗑️ Filmni o'chirish ---{RESET}")
    movie_id_input = input("O'chirmoqchi bo'lgan film ID sini kiriting: ").strip()

    if not movie_id_input.isdigit():
        print(f"{YELLOW}⚠️ ID butun son bo'lishi kerak!{RESET}")
        return

    movie_id = int(movie_id_input)
    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM movies WHERE id = %s", (movie_id,))
        movie = cursor.fetchone()

        if not movie:
            print(f"{RED}❌ ID={movie_id} bo'lgan film topilmadi.{RESET}")
            return

        cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
        connection.commit()
        print(f"{GREEN}✅ '{movie['title']}' (ID={movie_id}) kolleksiyadan o'chirildi.{RESET}")
    except MySQLError as e:
        print(f"{RED}❌ O'chirishda xatolik yuz berdi: {e}{RESET}")
    finally:
        if cursor:
            cursor.close()
        connection.close()