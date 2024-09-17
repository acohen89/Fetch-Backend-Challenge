import requests
import unittest
import json


endPoint = "http://localhost:8001/api/receipts/"

class TestReceiptProcess(unittest.TestCase):
    goodHeaders = {"Content-Type": "application/json"}
    goodBody = {
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": 35.35
}
    def test_good_receipt(self):
         
      response = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(self.goodBody))
      self.assertTrue("id" in json.loads(response.text))
        
    def test_missing_retailer(self):
        body = self.goodBody.copy()
        del body["retailer"]
        response = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)
    
    def test_missing_purchase_date(self):
        body = self.goodBody.copy()
        del body["purchaseDate"]
        response = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)
    
    def test_missing_purchase_time(self):
        body = self.goodBody.copy()
        del body["purchaseTime"]
        response = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)
    
    def test_missing_items(self):
        body = self.goodBody.copy()
        del body["items"]
        response = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)
        
    def test_missing_total(self):
        body = self.goodBody.copy()
        del body["total"]
        response = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)
    
    def test_empty_items_list(self):
        body = self.goodBody.copy()
        body["items"] = []
        response = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        self.assertEqual(response.status_code, 400)
    