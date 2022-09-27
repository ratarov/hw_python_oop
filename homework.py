from dataclasses import dataclass, asdict
from typing import List, Dict, Type
from abc import abstractmethod


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    H_IN_M: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    RUN_CAL_COEF1: int = 18
    RUN_CAL_COEF2: int = 20

    def get_spent_calories(self) -> float:
        calories = ((self.RUN_CAL_COEF1 * self.get_mean_speed()
                    - self.RUN_CAL_COEF2) * self.weight
                    / self.M_IN_KM * self.duration * self.H_IN_M)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_CAL_COEF1: float = 0.035
    WLK_CAL_COEF2: int = 2
    WLK_CAL_COEF3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.WLK_CAL_COEF1 * self.weight
                    + (self.get_mean_speed()
                     ** self.WLK_CAL_COEF2 // self.height)
                    * self.WLK_CAL_COEF3
                    * self.weight) * self.duration * self.H_IN_M)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWM_CAL_COEF1: float = 1.1
    SWM_CAL_COEF2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.SWM_CAL_COEF1)
                    * self.SWM_CAL_COEF2 * self.weight)
        return calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workouts:
        return workouts[workout_type](*data)
    else:
        raise ValueError(
            f'{workout_type} отсутствует в списке доступных тренировок')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
