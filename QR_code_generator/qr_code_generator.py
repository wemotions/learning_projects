import qrcode
import os
import PIL.Image


class QRCodeGenerator:
    """Класс для создания и сохранения QR-кодов.

        Атрибуты:
            box_size (int): Размер одного модуля QR-кода в пикселях.
            border (int): Размер границы вокруг QR-кода в модулях.
        """
    def __init__(self):
        """Инициализирует генератор QR-кодов и создает папку для хранения."""
        self.box_size = 10
        self.border = 4
        os.makedirs('qrcodes', exist_ok=True)

    def create_qr_code(self, data: str, filename: str) -> bool:
        """Создает QR-код на основе переданных данных и сохраняет его.

        Args:
            data (str): Данные для генерации QR кода.
            filename (str): Имя файла для сохранения QR-кода (с путем).

        Returns:
            bool: True, если QR-код успешно создан и сохранен, False в случае ошибки.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        return self._save(img, filename)

    def _save(self, img: PIL.Image.Image, filename: str) -> bool:
        """Сохраняет изображение QR-кода в указанный файл.

        Args:
            img (PIL.Image.Image): Объект изображения QR-кода.
            filename (str): Имя файла для сохранения.

        Returns:
            bool: True, если сохранение успешно, False в случае ошибки.
        """
        try:
            img.save(filename)
            return True
        except OSError:
            return False

    def run(self) -> None:
        """Запускает консольное меню генератора QR-кодов."""
        print('Добро пожаловать в генератор QR-кодов!')
        while True:
            print('1. Создать QR-код\n2. Выход')
            choice = input('Выберите опцию (1-2): ')
            if choice not in ['1', '2']:
                print('Ошибка: Выберите опцию 1 или 2.')
                continue
            if choice == '1':
                data = input('Введите данные для QR-кода: ').strip()
                if not data:
                    print('Ошибка: Введите данные для QR-кода.')
                    continue
                filename = input('Введите имя файла (оставьте пустым для имени по умолчанию): ')
                filename = filename.strip() or 'qr_code'
                if len(filename) > 50:
                    print('Ошибка: Имя файла слишком длинное (максимум 50 символов).')
                    continue
                filename = ''.join(c if c.isalnum() or c in '-_' else '_' for c in filename)
                filepath = os.path.join('qrcodes', f'{filename}.png')
                if os.path.exists(filepath):
                    overwrite = input(f'Файл {filename}.png уже существует. Перезаписать? (да/нет): ').lower()
                    if overwrite != 'да':
                        continue
                if self.create_qr_code(data, filepath):
                    print(f'QR-код успешно сохранен как {filename}.png.')
                else:
                    print('Ошибка: Не удалось сохранить QR-код.')
            elif choice == '2':
                print('До свидания!')
                break


if __name__ == '__main__':
    qr_generator = QRCodeGenerator()
    qr_generator.run()
