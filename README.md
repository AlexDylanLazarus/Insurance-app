# What is my app?
- I created an insurance web app that expands upon what Sanlam currently has in place. It makes use of `session management` and `user authentication` to dynamically change this state of itself depending on the user's authentication and platform. 

## Guide
- It is built from the customer's perspective where they may:
    1. Register `/register`
    2. Login `/login`
    3. View Sanlam's policies `/pol`
    4. View their own policies `/profile` 
    5. Update their account details `/update_details`  
    6. Get a quote on car insurance `/calculate_quote`
    7. Win rewards from the [Sanlam Reality website](https://www.sanlamreality.co.za/join/?gad_source=1&gclid=EAIaIQobChMInN2C07G1hQMV6URBAh2KLARpEAAYASAAEgJ-0fD_BwE&gclsrc=aw.ds) `/try_again`
        - PLEASE NOTE: This was out of scope of this project and makes use of `javascript`
    8. Logout `/logout`
    9. and delete their account `/delete_account`

#### User Registration and Authentication:
 Users can create an account by entering details such as their name, email, password and date of birth etc. Passwords are securely encrypted before being stored in the database. Registered users can log in using their email and password.

#### User Profile Management:
 Logged in users have the ability to view and update their profiles. They can modify their email address, password directly on the profile page.
 Insurance Policies; The app provides information on insurance policies including details like cost and coverage.

 #### Get a Quote: 
 Users can receive insurance quotes by inputting information such as their age, email address and vehicle details. The app calculates the estimate based on criteria and Displays it to the user.

#### Insurance Management for Users:
My application allows users to manage their existing policies. 

### Components
In my app I have the option, to group routes and their corresponding functions using blueprints. These blueprints serve as modules, each for a particular part of the application such, as `users`, `insurance`, `userinsurance`,  `cards`, `potential_customers`. 
- `SQLAlchemy` is used to define database models, a powerful ORM tool, the models define database tables, and the relationships between them. 
- To handle forms, `Flask-WTF` is used. It is required for `profile.html`, `register.html` and `login.html` pages and uses the `RegistrationForm` and `LoginForm` required for user registration and login, while the `UpdateDetailsForm` is used to manage profile update forms. 
- Lastly, various Flask extensions are employed for user authentication and session management, one of the extensions used is `Flask-Login`.



## Project Management
### Scrum Board
- [Insurance App](https://trello.com/b/DixVxiKd/insurance-application)

## Login details for my website
| Email         | Password   |
|---------------|------------|
| alex@gmail.com | 12345678   |


## Link to my website
[Sanlam Insurance Web App]()

## Github link
[GitHub]()