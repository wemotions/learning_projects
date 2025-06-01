class QuickSort:
    """Класс для реализации алгоритма быстрой сортировки (QuickSort)."""

    def sort(self, numbers: list[int], pivot_type: str) -> list[int]:
        """Сортирует список чисел с использованием QuickSort.

        Создает копию исходного списка и сортирует ее,
        чтобы не изменять оригинальный список.

        Args:
            numbers (list[int]): Список чисел для сортировки.
            pivot_type (str): Выбор опорного элемента (1 - первый, 2 - последний).
        Returns:
            list[int]: Отсортированный список.
        """
        if not numbers:
            return []
        data = numbers.copy()
        self._quicksort(data, 0, len(data) - 1, pivot_type)
        return data

    def _quicksort(self, numbers: list[int], start: int, end: int, pivot_type: str):
        """Рекурсивно сортирует подсписок массива.

        Функция использует рекурсию для применения алгоритма QuickSort
        к подмассивам слева и справа от опорного элемента.

        Args:
            numbers (List[int]): Список для сортировки.
            start (int): Начальный индекс.
            end (int): Конечный индекс.
            pivot_type (str): Выбор опорного элемента.
        """
        if start < end:
            pivot_index = self._partition(numbers, start, end, pivot_type)
            self._quicksort(numbers, start, pivot_index - 1, pivot_type)
            self._quicksort(numbers, pivot_index + 1, end, pivot_type)

    def _partition(self, arr: list[int], start: int, end: int, pivot_type: str) -> int:
        """Разделяет список относительно опорного элемента.

        Args:
            arr (List[int]): Список для разделения.
            start (int): Начальный индекс.
            end (int): Конечный индекс.
            pivot_type (str): Выбор опорного элемента (1 - первый, 2 - последний).

        Returns:
            int: Индекс опорного элемента после разделения.
        """
        if pivot_type == '1':
            arr[start], arr[end] = arr[end], arr[start]
        pivot = arr[end]
        i = start - 1
        for j in range(start, end):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[end] = arr[end], arr[i + 1]
        return i + 1


def get_pivot() -> str:
    """Запрашивает у пользователя тип опорного элемента для QuickSort.

    Пользователь должен выбрать '1' (первый элемент) или '2' (последний элемент).
    Функция повторяет запрос до тех пор, пока не будет введен корректный ответ.

    Returns:
        str: Выбранный тип опорного элемента ('1' или '2').
    """
    while True:
        pivot_choice = input('Выберите опорный элемент (1 - первый, 2 - последний): ').strip()
        if pivot_choice in {'1', '2'}:
            return pivot_choice
        print('Ошибка: опорный элемент должен быть 1 или 2.')


def sorted_again_answer() -> str:
    """Запрашивает у пользователя, хочет ли он отсортировать другой список.

    Функция повторяет запрос до тех пор, пока не будет введен 'да' или 'нет'.

    Returns:
        str: Ответ пользователя ('да' или 'нет').
    """
    while True:
        answer = input('Хотите отсортировать другой список? (да/нет): ').lower()
        if answer in ['да', 'нет']:
            return answer
        print('Ошибка: Введите "да" или "нет".')


def main():
    """Основная функция для запуска программы QuickSort.

    Позволяет пользователю вводить списки чисел для сортировки,
    выбирать тип опорного элемента и повторять процесс.
    """
    while True:
        try:
            numbers = list(map(int, input('Введите числа через пробел: ').split()))
            if not numbers:
                print('Список пуст.')
                continue
        except ValueError:
            print('Ошибка: Введите корректные числа.')
            continue

        pivot_choice = get_pivot()
        sorter = QuickSort()
        sorted_numbers = sorter.sort(numbers, pivot_choice)
        print(f'Исходный список: {numbers}')
        print(f'Отсортированный список: {sorted_numbers}')

        answer = sorted_again_answer()
        if answer == 'да':
            continue
        else:
            print('До свидания!')
            break


if __name__ == '__main__':
    main()
