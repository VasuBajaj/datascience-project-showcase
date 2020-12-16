# Introduction:
## Product Recommendation System

The aim of this project is to generate the recommendation based on 
1. Collaborative Filtering ( User to User Match )
2. Content-Based Filtering ( Item to Item Match )

### Model:

The application architecture is in recommendation_application.png

### Learnings

Apart from the recommendation logic, I could found out that packing the model for deployment for pickel makes a big deployment file, hence we can use BZ2 and "_pickle" libraries that would make the model files pretty small.
Below are the stats I observed for this project.

|Model| size with pickle (in MB) | size with BZ2 (in MB)|
|:---:|:---:|:----:|
| User2User|||
| Item2Item|||


### Issues:

Below are the list of issues I faced during this project

https://stackoverflow.com/questions/65326155/recommendation-model-server-deployment
