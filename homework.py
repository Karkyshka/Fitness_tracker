class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: int,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f'Длительность: {self.duration} ч.;'
                f'Дистанция: {self.distance}км;'
                f'Ср. скорость: {self.speed} км/ч;'
                f'Потрачено ккал: {self.calories}.'
                )


class Training:

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_CH: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration: duration
        self.weigth = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    KH_IN_MS: float = 3.6

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weigth / self.M_IN_KM
                * (self.duration * self.MIN_IN_CH))


class SportsWalking(Training):

    CALORIES_MEAN_WALKING_MULTIPLIER: float = 0.035
    CALORIES_MEAN_WALKING_SHIFT: float = 0.029
    KH_IN_MS: float = 3.6

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_WALKING_MULTIPLIER * self.weigth
                + ((self.get_mean_speed() / self.KH_IN_MS)**2 / self.height)
                * self.CALORIES_MEAN_WALKING_SHIFT
                * self.duration) * self.MIN_IN_CH
                )


class Swimming(Training):

    MEAN_SWIM_MULTIPLIER: float = 1.1
    MEAN_SWIM_SHIFT: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.MEAN_SWIM_MULTIPLIER)
                * self.MEAN_SWIM_SHIFT * self.weigth * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    training_type: dict = {'SWM': Swimming,
                           'RUN': Running,
                           'WLK': SportsWalking
                           }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    message = training.show_training_info()
    print(message.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
