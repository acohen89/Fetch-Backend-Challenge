import requests
import unittest
import json


endPoint = "http://localhost:8001/api/receipts/"

class TestReceiptPoints(unittest.TestCase):
    goodHeaders = {"Content-Type": "application/json"}
    bodyOne = {
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
    bodyTwo = {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}    
    def test_good_receipt_one(self):  
      processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(self.bodyOne))
      id = json.loads(processResponse.text)["id"]
      pointsResponse = requests.get(f"{endPoint}{id}/points",)
      self.assertEqual(json.loads(pointsResponse.text)["points"], 28.0)
      
    def test_good_receipt_two(self):  
      processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(self.bodyTwo))
      id = json.loads(processResponse.text)["id"]
      pointsResponse = requests.get(f"{endPoint}{id}/points",)
      self.assertEqual(json.loads(pointsResponse.text)["points"], 109)
      
    def test_no_alpha_in_retailer(self):  
        body = self.bodyOne.copy()
        body["retailer"] = "   #$ %% #@!     "
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 22)
        
    def test_round_dollar_amount_and_25_multiple(self):  
        body = self.bodyOne.copy()
        body["total"] = 12
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 103)
        
    def test_total_25_multiple(self):  
        body = self.bodyOne.copy()
        body["total"] = 12.50
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 53)
        
    def test_eight_items(self):  
        body = self.bodyTwo.copy()
        body["items"] = [{
      "shortDescription": "Not multiple of 3",
      "price": "6.49"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "12.25"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "1.26"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "3.35"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "12.00"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "2.25"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "2.25"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "2.25"
    }
    ]
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 119)
        
    def test_seven_items(self):  
        body = self.bodyTwo.copy()
        body["items"] = [{
      "shortDescription": "Not multiple of 3",
      "price": "6.49"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "12.25"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "1.26"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "3.35"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "12.00"
    }, {
      "shortDescription": "Not multiple of 3",
      "price": "2.25"
    },{
      "shortDescription": "Not multiple of 3",
      "price": "2.25"
    }
    ]
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 114)
      
    def test_item_desc_multiple_of_3(self):  
        body = self.bodyTwo.copy()
        body["items"] = [{
      "shortDescription": "Multiple of three3",
      "price": "6.49"
    },{
      "shortDescription": "Multiple of three3",
      "price": "12.25"
    },{
      "shortDescription": "Multiple of three3",
      "price": "1.26"
    }
    ]
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 110)
        
    def test_purchase_date_not_odd(self):  
        body = self.bodyOne.copy()
        body["purchaseDate"] = "2022-01-02"
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 22)
        
    def test_purchase_time_between_2_and_4(self):  
        body = self.bodyOne.copy()
        body["purchaseTime"] = "15:59"
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 38)
        
    def test_purchase_time_exactly_2(self):  
        body = self.bodyOne.copy()
        body["purchaseTime"] = "14:00"
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 28)
        
    def test_purchase_time_exactly_4(self):  
        body = self.bodyOne.copy()
        body["purchaseTime"] = "16:00"
        processResponse = requests.post(f"{endPoint}process", headers=self.goodHeaders, data=json.dumps(body))
        id = json.loads(processResponse.text)["id"]
        pointsResponse = requests.get(f"{endPoint}{id}/points",)
        self.assertEqual(json.loads(pointsResponse.text)["points"], 28)
        
      
        
      
        
      
        
      