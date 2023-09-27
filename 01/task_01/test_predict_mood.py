import unittest
from unittest import mock

from predict_mood import predict_message_mood


class TestPredictMood(unittest.TestCase):

    @mock.patch("predict_mood.SomeModel")
    def test_positive_prediction(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.9

        value = predict_message_mood("Чапаев и пустота", mock_model)
        self.assertEqual(value, "отл")

    @mock.patch("predict_mood.SomeModel")
    def test_negative_prediction(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0

        value = predict_message_mood("Вулкан", mock_model)
        self.assertEqual(value, "неуд")

    @mock.patch("predict_mood.SomeModel")
    def test_neutral_prediction(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Вулкан", mock_model)
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_zero_left_border(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Вулкан", mock_model, 0)
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_one_left_border(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Вулкан", mock_model, good_thresholds=1)
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_empty_string(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("", mock_model)
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_left_threshold(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.3

        value = predict_message_mood("", mock_model)
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_right_threshold(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.8

        value = predict_message_mood("", mock_model)
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_neutral_bad_threshold(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        with self.assertRaises(Exception) as context:
            predict_message_mood("aboba", mock_model, 1, 0)

        self.assertTrue('Bad threshold' in str(context.exception))
