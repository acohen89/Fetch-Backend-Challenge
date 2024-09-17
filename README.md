
# Fetch Backend Challenge

Please follow these steps:   
1. Start up docker destkop 
2. Go to a desired folder and clone repository: ```git clone https://github.com/acohen89/Fetch-Backend-Challenge.git```
3. Now change directory to created folder (usually ```cd Fetch-Backend-Challenge```)
4. Enter ``` docker-compose up -d --build ```
5. Requests can now be made to http://localhost:8001/api/receipts/   
For processing, hit http://localhost:8001/api/receipts/process
For points, hit http://localhost:8001/api/receipts/{id}/points 


If you would like to use the unit tests provided please complete steps 1-6 above and then begin here:   
1. Change directory to ```challenge``` folder (```cd challenge/```)
2. Install python at the following link: https://www.python.org/downloads/
3. Once installed, install the required packages 
4. Type ```pip install requests```
5. Once completed type ```python -m unittest```




