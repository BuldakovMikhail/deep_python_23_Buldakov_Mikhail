# Реализовать функцию predict_message_mood, которая приниамает
# на вход строку, экземпляр модели SomeModel и пороги хорошести.
# Функция возвращает:
#
#     "неуд", если предсказание модели меньше bad_threshold
#     "отл", если предсказание модели больше good_threshold
#     "норм" в остальных случаях


import random


class SomeModel:
    def predict(self, message: str) -> float:
        return random.random()


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if not bad_thresholds < good_thresholds:
        raise Exception("Bad threshold")

    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return "неуд"
    elif prediction > good_thresholds:
        return "отл"
    else:
        return "норм"


# assert predict_message_mood("Чапаев и пустота", model) == "отл"
# assert predict_message_mood("Вулкан", model) == "неуд"
