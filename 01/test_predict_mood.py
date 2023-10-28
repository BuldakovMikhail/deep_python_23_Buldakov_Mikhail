import unittest
from unittest import mock

from predict_mood import predict_message_mood


class TestPredictMood(unittest.TestCase):
    @mock.patch("predict_mood.SomeModel")
    def test_positive_prediction(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.9

        value = predict_message_mood("Чапаев и пустота", mock_model)
        self.assertEqual(mock_model.predict.call_args.args, ("Чапаев и пустота",))
        self.assertEqual(value, "отл")

    @mock.patch("predict_mood.SomeModel")
    def test_negative_prediction(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0

        value = predict_message_mood("Вулкан", mock_model)
        self.assertEqual(mock_model.predict.call_args.args, ("Вулкан",))
        self.assertEqual(value, "неуд")

    @mock.patch("predict_mood.SomeModel")
    def test_neutral_prediction(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Вулкан", mock_model)
        self.assertEqual(mock_model.predict.call_args.args, ("Вулкан",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_zero_left_border(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Вулкан", mock_model, 0)
        self.assertEqual(mock_model.predict.call_args.args, ("Вулкан",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_one_left_border(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Вулкан", mock_model, good_thresholds=1)
        self.assertEqual(mock_model.predict.call_args.args, ("Вулкан",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_empty_string(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Not this time", mock_model)
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_left_threshold(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.3

        value = predict_message_mood("Not this time", mock_model)
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_right_threshold(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.8

        value = predict_message_mood("Not this time", mock_model)
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_neutral_bad_threshold(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        with self.assertRaises(Exception) as context:
            predict_message_mood("aboba", mock_model, 1, 0)

        self.assertTrue("Bad threshold" in str(context.exception))

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_thin(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.66

        value = predict_message_mood(
            "Not this time", mock_model, bad_thresholds=0.65, good_thresholds=0.70
        )
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_wide(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 9.9

        value = predict_message_mood(
            "Not this time", mock_model, bad_thresholds=-10, good_thresholds=10
        )
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_сlose_to_left_from_right(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 5.0001

        value = predict_message_mood(
            "Not this time", mock_model, bad_thresholds=5, good_thresholds=10
        )
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_сlose_to_left_from_left(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 4.999

        value = predict_message_mood(
            "Not this time", mock_model, bad_thresholds=5, good_thresholds=10
        )
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "неуд")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_сlose_to_right_from_left(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 9.999

        value = predict_message_mood(
            "Not this time", mock_model, bad_thresholds=5, good_thresholds=10
        )
        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "норм")

    @mock.patch("predict_mood.SomeModel")
    def test_model_return_сlose_to_right_from_right(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 10.0001

        value = predict_message_mood(
            "Not this time", mock_model, bad_thresholds=5, good_thresholds=10
        )

        self.assertEqual(mock_model.predict.call_args.args, ("Not this time",))
        self.assertEqual(value, "отл")

    @mock.patch("predict_mood.SomeModel")
    def test_equal_threshold(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        with self.assertRaises(Exception) as context:
            predict_message_mood("aboba", mock_model, 0.5, 0.5)

        self.assertTrue("Bad threshold" in str(context.exception))

    @mock.patch("predict_mood.SomeModel")
    def test_passed_message(self, mock_model_constructor):
        mock_model = mock_model_constructor.return_value
        mock_model.predict.return_value = 0.5

        value = predict_message_mood("Вулкан", mock_model, good_thresholds=1)

        self.assertEqual(mock_model.predict.call_args.args, ("Вулкан",))

        self.assertEqual(value, "норм")
