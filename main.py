import setup

if __name__ == "__main__":
    print("Запуск приложения\n")

    setup.create_app()

    print("\nОстановка приложения")

    setup.close_app()
