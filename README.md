# Token transaction history Web3 App✨

This repository contains the Full-Stack web3 app. Provides the last 100 token transactions on the Ethereum Goerli testnet, with multiple filters by transaction method. Which is built using React frontend and Django Backend(Django Rest Framework, Celery, Redis, Cache)


### Setup

1. Clone of the repo

2. Check 'token_monitor/settings.py' Redis, Celery, Cors, Caches and change ETHERSCAN_API_KEY in celery.py

3. Create a virtual environment and Install the pip packages in the requiremets.txt
    > `pip install -r requirements.txt`

4. Run django 
    > `python manage.py runserver` 

5. Run Redis
    > `redis-server`

6. Run Celery and wait beat starting
    > `celery -A token_monitor worker -l INFO -B`

7. Install all the npm packages
    > `npm install`

8. Run the code
    > `npm start`



   