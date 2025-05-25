import json
import random


class PasswordManager:
    """Класс для управления паролями"""
    def __init__(self, shift: int = 3) -> None:
        """Инициализирует менеджер паролей.

        Args:
            shift (int): Сдвиг для шифрования (шифр Цезаря). По умолчанию 3.
        """
        self.passwords: list[dict[str, str]] = []
        self.shift = shift
        self._load()

    def add_password(self, service_name: str, login: str, password: str) -> None:
        """Добавляет новый пароль в базу.

        Args:
            service_name (str): Название сервиса.
            login (str): Логин для сервиса.
            password (str): Пароль (незашифрованный).
        """
        encrypted = self.encrypt_password(password)
        self.passwords.append({'service': service_name.lower(), 'login': login.lower(), 'password': encrypted})
        self._save()

    def remove_password(self, service: str, login: str) -> bool:
        """Удаляет пароль по названию сервиса и логину.

        Args:
            service (str): Название сервиса.
            login (str): Логин для сервиса.

        Returns:
            bool: True, если запись удалена, False, если не найдена.
        """
        if self.passwords:
            for n, i in enumerate(self.passwords):
                if service == i['service'].lower() and login == i['login'].lower():
                    self.passwords.pop(n)
                    self._save()
                    return True
            else:
                return False

    def encrypt_password(self, password: str) -> str:
        """Шифрует пароль с помощью шифра Цезаря.

        Args:
            password (str): Пароль для шифрования.

        Returns:
            str: Зашифрованный пароль.
        """
        index_chars = [(ord(char) - 32 + self.shift) % 95 + 32 for char in password]
        encrypt_password = ''.join(chr(char) for char in index_chars)
        return encrypt_password

    def decrypt_password(self, password: str) -> str:
        """Расшифровывает пароль, зашифрованный шифром Цезаря.

        Args:
            password (str): Зашифрованный пароль.

        Returns:
            str: Расшифрованный пароль.
        """
        index_chars = [(ord(char) - 32 - self.shift) % 95 + 32 for char in password]
        encrypt_password = ''.join(chr(char) for char in index_chars)
        return encrypt_password

    def _save(self) -> None:
        """Сохраняет базу паролей в JSON-файл.
        Сохраняет данные в файл 'passwords.json'.
         """
        try:
            with open('passwords.json', 'w', encoding='utf-8') as file:
                json.dump(self.passwords, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Не удалось сохранить данные, ошибка: {e}')

    def _load(self) -> None:
        """Загружает базу паролей из JSON-файла.
        Загружает данные из файла 'passwords.json'.
        Если файл отсутствует или поврежден, инициализирует пустую базу.
        """
        try:
            with open('passwords.json', 'r', encoding='utf-8') as file:
                self.passwords = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.passwords = []


class PasswordGenerator:
    """Класс для генерации случайных паролей.
    Генерирует пароли из символов в диапазоне ASCII 32–126.
    """
    def __init__(self, length: int = 12) -> None:
        """Инициализирует генератор паролей.

        Args:
            length (int): Длина генерируемого пароля. По умолчанию 12.
        """
        self.length: int = length
        self.char_range: list[str] = [chr(i) for i in range(32, 127)]

    def generate_password(self) -> str:
        """Генерирует случайный пароль длиной 12 символов.

        Returns:
            str: Сгенерированный пароль.
        """
        generated_password = random.choices(self.char_range, k=self.length)
        return ''.join(generated_password)


def get_user_data(pattern: str) -> bool | str:
    """Запрашивает данные у пользователя и возвращает их.

    Args:
        pattern (str): Сообщение для пользователя.

    Returns:
        str: Введенные пользователем данные (в нижнем регистре).
        bool: False, если пользователь ввел пустую строку или только пробелы.
    """
    request = input(f'{pattern}').lower()
    if not request.strip():
        return False
    return request


def main() -> None:
    """Запускает консольное приложение для управления паролями.
    Предоставляет меню для добавления, просмотра, удаления паролей и выхода.
    """
    print('Добро пожаловать в менеджер паролей!')
    manager = PasswordManager()
    generator = PasswordGenerator()

    while True:
        print(
            '1. Добавить новый пароль\n'
            '2. Показать все пароли\n'
            '3. Удалить пароль\n'
            '4. Выход')
        try:
            choice = int(input('Выберите операцию (1-4): '))
            if choice < 0 or choice > 4:
                raise ValueError

        except ValueError:
            print('Ошибка: Выберите операцию от 1 до 4.')
            continue

        if choice == 1:
            service = get_user_data('Введите название сервиса: ')
            if not service:
                print('Ошибка: Значение сервиса не может быть пустым')
                continue
            login = get_user_data('Введите логин: ')
            if not login:
                print('Ошибка: Значение логина не может быть пустым')
                continue

            auto_password = get_user_data('Сгенерировать пароль автоматически? (да/нет): ').lower()
            if not auto_password:
                print('Ошибка: Значение выбора авто-генерации пароля не может быть пустым')
                continue

            if auto_password in ['да', 'д', 'yes', 'y']:
                password = generator.generate_password()
                print(f"Сгенерированный пароль: {password}")
            else:
                password = get_user_data('Введите пароль: ')
                if not password:
                    print('Ошибка: Значение пароля не может быть пустым')
                    continue

            manager.add_password(service, login, password)
            print(f"Пароль для {service} добавлен.")

        elif choice == 2:
            if manager.passwords:
                for password_entry in manager.passwords:
                    password = manager.decrypt_password(password_entry['password'])
                    print(
                        f'Сервис: {password_entry["service"]} |'
                        f' Логин: {password_entry["login"]} |'
                        f' Пароль: {password}')
            else:
                print('Список паролей пуст.')

        elif choice == 3:
            if manager.passwords:
                service = get_user_data('Введите название сервиса: ')
                if not service:
                    print('Ошибка: Значение сервиса не может быть пустым')
                    continue
                login = get_user_data('Введите логин: ')
                if not login:
                    print('Ошибка: Значение логина не может быть пустым')
                    continue
                if manager.remove_password(service, login):
                    print(f"Пароль для сервиса {service} (логин: {login}) удален.")
                else:
                    print(f"Запись для сервиса {service} с логином {login} не найдена.")
            else:
                print('Список паролей пуст.')

        elif choice == 4:
            print('До свидания!')
            break


if __name__ == '__main__':
    main()
