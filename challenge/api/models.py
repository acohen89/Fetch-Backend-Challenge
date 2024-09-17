from curses.ascii import isalnum
from django.db import models
import json
import uuid

import math

# Create your models here.
class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    retailer = models.CharField(max_length=255)
    purchaseDate = models.DateField(null=False)
    purchaseTime = models.TimeField(null=False)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    # no array field in SQLite so using string as items field 
    items = models.TextField()

    def __str__(self) -> str:
        return self.retailer
    
    def calculatePoints(self) -> float:
        # convert items back to List<Dict> 
        # needs to replace ' with " in order to decode string 
        convertedItems = [json.loads(i.replace("'", '"')) for i in self.splitWithoutRemovingDelimiter("}", self.items)]
        alphaNumericCharCount = self.getAlphaNumCount(self.retailer)
        roundDollarPoints = 50 if float(self.total).is_integer() else 0
        multipleOfZeroTwoFivePoint = 25 if float(self.total) % 0.25 == 0 else 0
        numItemsPoints = 5 * (len(convertedItems) // 2)
        itemDescPoints = self.calcItemDescPoint(convertedItems)
        oddDatePoints = 6 if self.purchaseDate.day % 2 == 1 else 0
        purchaseTimePoints = 10 if self.purchaseTime.hour >= 14 and self.purchaseTime.minute > 0 and self.purchaseTime.hour < 16 else 0
        return alphaNumericCharCount + roundDollarPoints + numItemsPoints + itemDescPoints + oddDatePoints + purchaseTimePoints + multipleOfZeroTwoFivePoint

    
    def splitWithoutRemovingDelimiter(self, delimiter, items) -> list:
        newItems = items.split(delimiter)
        itemsWithDelim = [item + "}" for item in newItems]
        # need to remove last element cause it adds an extra delimiter 
        return itemsWithDelim[:-1]
        
    def calcItemDescPoint(self, convertedItems) -> float:
        points = 0.0
        for item in convertedItems:
            desc = item["shortDescription"].strip()
            price = float(item["price"])
            if len(desc) % 3 == 0:
                points += math.ceil(price * 0.2)
        return points
    
    def getAlphaNumCount(self, retailer):
        # remove spaces
        retailer.replace(" ", "")
        count = 0
        for c in retailer:
            if c.isalpha() or c.isdigit(): count += 1
        return count