import unittest

from fastapi.testclient import TestClient

from main import app


class LoanRiskDemoAPITests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.sample = {
            "person_age": 25,
            "person_income": 50000,
            "person_emp_length": 3,
            "loan_amnt": 15000,
            "loan_int_rate": 10.5,
            "loan_percent_income": 0.3,
            "cb_person_cred_hist_length": 4,
            "person_home_ownership": "RENT",
            "loan_intent": "EDUCATION",
            "loan_grade": "B",
            "cb_person_default_on_file": "N",
        }

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertTrue(payload["models_loaded"])

    def test_xgboost_prediction_endpoint(self):
        response = self.client.post(
            "/api/predict",
            json={"model": "xgboost", "customer": self.sample},
        )
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertEqual(payload["model"], "XGBoost")
        self.assertEqual(payload["strategy"], "SAFE")
        self.assertIn("risk_probability", payload)
        self.assertIn("risk_level", payload)
        self.assertIn("recommendation", payload)

    def test_catboost_prediction_endpoint(self):
        response = self.client.post(
            "/api/predict",
            json={"model": "catboost", "customer": self.sample},
        )
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertEqual(payload["model"], "CatBoost")
        self.assertEqual(payload["strategy"], "SWEEP")
        self.assertIn("risk_probability", payload)
        self.assertIn("risk_level", payload)

    def test_compare_endpoint(self):
        response = self.client.post("/api/compare", json=self.sample)
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertIn("xgboost", payload)
        self.assertIn("catboost", payload)
        self.assertEqual(payload["xgboost"]["strategy"], "SAFE")
        self.assertEqual(payload["catboost"]["strategy"], "SWEEP")

    def test_invalid_input_rejected(self):
        response = self.client.post(
            "/api/predict",
            json={"model": "xgboost", "customer": {**self.sample, "person_age": 17}},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
