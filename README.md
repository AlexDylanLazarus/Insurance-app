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
[Alex Dylan Lazarus Insurance App](https://github.com/AlexDylanLazarus/Insurance-app)


# Run this sql commands in your database named "ipmsdb"
```sql


CREATE TABLE insurance_policies (
    policy_id INT PRIMARY KEY,
    policy_name VARCHAR(255),
    coverage VARCHAR(255),
    premium DECIMAL(10, 2),
    deductible DECIMAL(10, 2),
    details TEXT,
    image_url VARCHAR(255)
);


INSERT INTO insurance_policies (policy_id, policy_name, coverage, premium, deductible, details, image_url) 
VALUES 
    (1, 'Car Insurance', 'Accident, Theft, Liability', 1000.00, 500.00, 'Sanlam offers comprehensive car insurance solutions tailored to meet the diverse needs of drivers. With a focus on providing peace of mind and financial security, Sanlam''s car insurance policies cover a wide range of risks, including accidents, theft, and liability. Whether you''re a new driver or a seasoned road veteran, Sanlam''s offerings are designed to protect both you and your vehicle from unforeseen circumstances on the road. With competitive premiums and flexible deductible options, Sanlam ensures that you''re adequately covered without breaking the bank. Additionally, their responsive customer service and efficient claims process strive to minimize the hassle and inconvenience often associated with car insurance claims, allowing you to get back on the road with confidence. Whether you''re commuting to work, embarking on a road trip, or simply running errands, Sanlam''s car insurance provides the security and support you need for a worry-free driving experience.', 'http://surl.li/rymyw'),
    (2, 'Home Insurance', 'Fire, Theft, Flood, Liability', 1500.00, 1000.00, 'Sanlam offers comprehensive house insurance solutions designed to safeguard your home and its contents against a variety of risks. Whether you own a house, apartment, or condominium, Sanlam''s house insurance policies provide protection for your property''s structure, as well as your personal belongings inside. With coverage for events such as fire, theft, natural disasters, and liability, Sanlam ensures that you''re prepared for unexpected incidents that could damage or jeopardize your home. Their flexible policies allow you to customize coverage based on your specific needs and budget, ensuring that you have the right level of protection without overpaying. Additionally, Sanlam''s experienced team of insurance professionals provides personalized assistance throughout the policy selection process, making it easy to understand your coverage options and choose the best policy for your home. With Sanlam''s house insurance, you can have peace of mind knowing that your most valuable asset is protected against life''s uncertainties.', 'http://surl.li/rymzi'),
    (3, 'Health Insurance', 'Hospitalization, Surgery, Prescription drugs', 2000.00, 750.00, 'Sanlam''s health insurance plans offer comprehensive coverage to protect you and your family''s well-being. With rising healthcare costs and unforeseen medical emergencies, having reliable health insurance is essential for peace of mind. Sanlam''s health insurance policies provide coverage for a wide range of medical expenses, including hospitalization, doctor visits, prescription medications, and diagnostic tests. Additionally, their plans often include benefits such as wellness programs, preventive care services, and access to a network of healthcare providers. Whether you''re looking for individual coverage or a family plan, Sanlam offers flexible options to suit your needs and budget. Their commitment to customer service means that you''ll receive personalized support every step of the way, from selecting the right plan to filing claims and accessing healthcare services. With Sanlam''s health insurance, you can focus on your health and well-being knowing that you''re protected financially against unexpected medical costs.', 'http://surl.li/rynac');


CREATE TABLE users (
    id VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(255),
    Last_name VARCHAR(255),
    Date_of_birth DATE,  -- Change data type to DATE
    Password VARCHAR(255),
    Email VARCHAR(255),
    Phone_number VARCHAR(20),
    Credits INT,
    Street_Address VARCHAR(255),
    Zip_code VARCHAR(20),
    Suburb VARCHAR(255),
    City VARCHAR(255),
    Country VARCHAR(255),
    sex VARCHAR(10)
);


CREATE TABLE user_insurance (
    user_id VARCHAR(50),
    policy_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (policy_id) REFERENCES insurance_policies(policy_id),
    PRIMARY KEY (user_id, policy_id)
);


```