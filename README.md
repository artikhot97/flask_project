# flask_project


1. Insall Above all Requirements 
 `python -m pip freeze > requirements.txt`
3. Run python3 app.py 

Create DB :
- mysql -u root -p :- Enter Password 
- Cretae database <db_name> ;
- show databases;
- use <db_name>;
- show tables;
- cretae tables user, movies;



1. Register User : http://0.0.0.0:9000/api/register/
2. Login User : http://0.0.0.0:9000/api/login_user/
3. Get User List : http://0.0.0.0:9000/api/user_list/
4. Add Movie : http://0.0.0.0:9000/api/movies_curd/
5. Get Movie List : http://0.0.0.0:9000/api/movies_curd/
6. Single Movie Data : http://0.0.0.0:9000/single_movies/2
7. Edit Movie : http://0.0.0.0:9000/single_movies/11



# Handling the Scaling Problem
While We design any architecture to solve scaling problem then following some points need to consider 
1. Technical Debt
- Technical debt accumulates interests over time and increases software entropy. To effectively measure technical debt, we need to express it as a ratio of the cost it takes to fix the software system to the cost it took to build the system. This quantity is called the Technical Debt Ratio [TDR]

2. Single Point of Failures
- Break it down into smaller components that make up the system. If the failure of one of those components would shut down the system or destroy it, then you have identified a single point of failure.

3. Bottleneck accross multiple services
- A process bottleneck is a work stage that gets more work requests than it can process at its maximum throughput capacity. That causes an interruption to the flow of work and delays across the production process.

With Respective above all points Following are some of solution to scale up system 

DB : 
- Optimmizing Query for retrive data
- Indexing some of tables column 
- Reduce server load by moving image and video to some third -party content delivery network (CDN) like CloudFront.
- We can use AWS service for like RDS for DB or any other for database service 
- Horizontal scaling the databases using sharding and replication

Server Load: 
- We can use Elastic Serach for Cacheing data 
- Creating Multiple instance for reduce lataency 
- We can use Load Balancing techince
- Use multiple different servers for procssing data like we can use media , files s3 service , for cacheing elastic search , Kibana or RDS etc.
- Apply some of scaling Technicq  

Code :
- Trying to write code into different modules
- Writing code for minimum time conusing 
- minimizing Looping Part for data storage 
- We can use Synchronus or asynchronuos as per requirment 
- Trying to use some of python libaryies 
- Avoiding Repeation of Code 
- Writing Reuable Compoent 
- Reviewing Otheres code because sometimes we have better approch to do things 
- Minimizing API Calls or DB calles (As per Requirements)
- Use differnt coding approch for reduce time consuming for server 
- Dyanmic Programming 


Some Other Things we can imporve :
- Attending Differnt Seminars or Sessions for architecture Dsign
- Always Learning for architecture improvemt 
- Course on Architecture Design 


Thanks You :)


