from db import (
    create_table,
    add_movie,
    list_movies,
    update_movie,
    delete_movie,
    CYAN,
    YELLOW,
    GREEN,
    RESET
)


def menu():
    """Asosiy menyu va foydalanuvchi tanlovlarini boshqaradi."""
    create_table()

    while True:
        print(f"\n{CYAN}===================================={RESET}")
        print(f"{CYAN}     🎬 FILM KOLLEKSIYASI (1)       {RESET}")
        print(f"{CYAN}===================================={RESET}")
        print("1. ➕ Film qo'shish")
        print("2. 📋 Filmlar ro'yxatini ko'rish")
        print("3. ✏️  Film ma'lumotlarini yangilash")
        print("4. 🗑️  Filmni o'chirish")
        print("0. 🚪 Chiqish")
        print(f"{CYAN}===================================={RESET}")

        choice = input("Amalni tanlang (0-4): ").strip()

        if choice == "1":
            add_movie()
        elif choice == "2":
            list_movies()
        elif choice == "3":
            update_movie()
        elif choice == "4":
            delete_movie()
        elif choice == "0":
            print(f"\n{GREEN}👋 Dastur yakunlandi. Xayr!{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Noto'g'ri tanlov! Iltimos, 0 dan 4 gacha son kiriting.{RESET}")


if __name__ == "__main__":
    menu()
