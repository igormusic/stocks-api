DowJonesIndex

Welcome to the RBC Coding challenge!

Please timebox your efforts to 2 - 4 hours for the following challenge.

Problem Background

As a programmer with a fascination for stock markets, you got excited about a new data set that you discovered

that there is a collection of records from the [Dow Jones Index from 2011](http://archive.ics.uci.edu/ml/datasets/Dow+Jones+Index#) that caught your attention.


You decided you'd like to build an application server (Spring Boot) that would allow multiple users to perform the following operations concurrently:

- upload a bulk data set

- query for data by stock ticker (e.g. input: AA, would return 12 elements if the only data uploaded were the single data set above)

- add a new record

Requirements

- Your solution source code should be publicly available to share via a github / gitlab / bitbucket link

- Solution should be able to run locally (e.g. no dependencies on managed services), but you are encouraged to leverage open source technologies (e.g. Docker, spring boot, mongo, postgresql, mysql etc) for your solution.

- The solution does not need to be perfect. Please complete what you deem necessary and prioritize accordingly. Most importantly, you should be prepared to discuss how you would potentially enhance the solution given more time, and decisions / tradeoffs that you made.

Final Thoughts

Some aspects of this challenge have been left intentionally vague. Have fun! Build a solution you would be proud to show off :slightly_smiling_face:


Usage

- mvn clean package
- docker-compose up -d

- goto http://localhost:8080/swagger-ui/index.html

OR

- curl -F "file=@dow_jones_index.data" -H "X-Client_Id: abc123" http://127.0.0.1:8080/api/stock-data/bulk-insert
- curl -H "X-Client_Id: abc123" http://127.0.0.1:8080/api/stock-data/AA
- curl -H "Content-Type: application/json" -H "X-Client_Id: abc123" -X POST -d @dow_jones_missing.json http://127.0.0.1:8080/api/stock-data/