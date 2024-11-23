# MyVault

MyVault is a secure and feature-rich application designed to help users manage their finances with ease and confidence. 
It offers features like sending and receiving money with unique addresses, deposits and withdrawals through Stripe, private key authentication, and detailed transaction history. Additional functionalities include email notifications, login location tracking with Google Maps, and complete account deletion. MyVault prioritizes privacy and user responsibility<br>
<strong>"Your vault, your responsibility."</strong>

The live deployed site can be found [here](https://my-vault-cb8eb703ab63.herokuapp.com/)

## Contents

- [Agile Development](#agile-development)
- [User Experience(UX)](#user-experienceux)
  - [Project Goals](#project-goals)
  - [User Stories](#user-stories)
- [Design](#design)
  - [Structure](#structure)
  - [Colour Scheme](#colour-scheme)
  - [Typography](#typography)
  - [Features](#features)
    - [Home](#home)
    - [FAQ](#faq)
    - [Ask](#ask)
    - [Profile](#profile)
    - [Update Profile](#update-profile)
    - [Delete Profile](#delete-profile)
    - [Validate private key/Unlock account](#validate-private-keyunlock-account)
    - [Dashboard](#dashboard)
    - [Transactions](#transactions)
    - [Top Up](#top-up)
    - [Send Payment](#send-payment)
    - [Withdraw](#withdraw)
    - [Transactions History](#transactions-history)
    - [Future Implementation](#future-implementations)
- [Technologies, Languages, and Programs used](#technologies-languages-and-programs-used)
  - [Stripe](#stripe)
- [Deployment & Local Development](#deployment--local-development)
  - [Local Deployment](#local-deployment)
  - [Testing](#testing)
    - [HTML](#html)
    - [CSS](#css)
    - [JavaScript](#javascript)
    - [Python](#python)
    - [Lighthouse](#lighthouse)
    - [Wave](#wave)
    - [Automated Testing](#automated-testing)
    - [Manual Testing](#manual-testing)
    - [Full Testing](#full-testing)
    - [Bugs](#bugs)
- [Credits](#credits)
  - [Media](#media)
  - [Content](#content)

## Agile Development

User stories were prioritized using MoSCoW.
The Agile process emphasizes incremental development and user-focused delivery. The following flowchart outlines how key application features and workflows, such as user validation, transaction handling, and account management, were prioritized and developed across sprints:<br>
![flowchart](/docs/screenshots/project-4.png)<br>
This workflow guided the sprint planning and ensured seamless integration of essential features.

## User Experience(UX)

### Project Goals

The primary goals of the app is to ensure robust security and provide a seamless and secure platform for handling payments. With features like private key authentication, unique addresses for sending and receiving funds, the app prioritizes user privacy and control. Additionally, the app facilitates transparent financial management by offering a detailed transaction history and the app empowers users to keep track of their finances through interactive charts and visual insights, promoting better financial management.

### User Stories

User Stories were tracked throughout the project as [GitHub issues](https://github.com/users/Tamas-Gavlider/projects/5/views/1).

## Design

### Structure

The ERD represents the database structure for the application. Due to the data being used for the project I have opted to use a relational database as this will best suit my requirements.
 - Profile - Stores user-specific details such as balance, notification preferences, and unique sending/receiving addresses. The model has full CRUD (Create, Read, Update, Delete) functionality to manage user information securely and efficiently.Each profile is linked to a user account via a Foreign Key.
 - Transactions - Tracks all financial activities, including deposits, withdrawals, and transfers between users, with fields for transaction type, status, and amounts. The model is designed for integrity and security. Even if a Profile is deleted, related transaction records are retained for compliance and audit purposes.
 - Deleted profile - Maintains a record of deleted user profiles, preserving details like username, email, and deletion date for audit purposes.
 - User questions - Captures questions submitted by users in the FAQ section, including the question text and submission date.

![Models](/docs/screenshots/erd.png)

### Colour Scheme

![colour](/docs/screenshots/colout%20palette.png)

- #333333 (Dark Gray): This color provides a modern and professional look, acting as a neutral and calming base. It ensures good contrast with lighter colors, enhancing readability while giving the app a sophisticated, minimalistic feel.
- #FFFFFF (White): White symbolizes simplicity and cleanliness, creating a bright and open interface. It balances the darker tones, improving visual clarity and making the app feel user-friendly and inviting.
- #E1F4F3 (Soft Aqua): This soft, refreshing color adds a subtle touch of warmth and energy to the interface. It symbolizes trust and innovation, complementing the darker and lighter tones to create a cohesive, elegant, and approachable design.
- #706C61: This muted, earthy tone adds depth and warmth to the overall design, creating a subtle contrast against the darker #333333 and the bright #FFFFFF. Its neutral yet sophisticated appearance evokes stability, reliability, and professionalism. It serves as a grounding element, tying the color palette together and softening the overall visual experience.
This color palette was chosen to achieve a clean, minimalistic, and modern aesthetic, emphasizing usability and professionalism.
- #00FFFF: color was used on the V letter on the navbar due to contrast errors in Wave.

### Typography

The Nanum Myeongjo font, available via Google Fonts, is a sophisticated serif typeface inspired by traditional Korean calligraphy. The font’s graceful curves and sharp serifs make it stand out, giving your design a distinctive and memorable quality.

### Features

All pages feature a fully responsive navbar that transforms into a hamburger menu on smaller screens and a [favicon](/static/images/android-chrome-192x192.png) in the browser tab.<br>
Navbar if user logged in
![Logged in](/docs/screenshots/home-logged-in.png)

Navbar is user logged out/not registered
![Logged out](/docs/screenshots/home-logged-out.png)

#### Home

The home page of MyVault features a sleek design to leave a lasting impression on first-time visitors. At the top, the navigation bar provides easy access to key sections of the app. The background showcases a captivating image of a door with a key, symbolizing security and empowerment. The slogan "Be the Key" is prominently displayed on the right, while "Be Your Vault" appears on the left, reinforcing the app’s theme of personal responsibility and financial security.

At the bottom, the footer includes the tagline "Great Wealth, Greater Responsibility," emphasizing MyVault's focus on managing and safeguarding your finances responsibly.

![Backgorund](/docs/screenshots/home-page-bg.png)

#### FAQ

The FAQ page provides answers to the 10 most frequently asked questions about MyVault.
![FAQ](/docs/screenshots/faq.png)
Users can click on a question to expand and view its detailed answer. 
![faq-example](/docs/screenshots/faq-question.png)
If users don’t find the information they need or require further assistance, a button at the bottom of the page directs them to the Ask page, where they can submit their queries for personalized support.
![faq-btn](/docs/screenshots/faq-btn-ask.png)

#### Ask

The Ask page in MyVault leverages the Gemini API to provide instant answers to user queries. To streamline the process, the page includes predefined prompts to guide users in framing their questions. All submitted questions are logged and stored, ensuring they are accessible for review and management via the admin panel.
![Ask page](/docs/screenshots/ask-page.png)

#### Profile

The Profile page is the first destination for users after registration or login. For new users, their private key will be displayed on this page with a clear warning to store it securely, as it cannot be recovered later. 
![Private-key](/docs/screenshots/secret-private-key.png)
The page also displays user details such as username and email address. By default, features like email notifications and location tracking are enabled, but users can conveniently manage these settings from the Edit Profile page.
The Profile page also provides users with essential account management options. Users can:
- Delete their profile if they wish to close their account permanently.
- Reset their password for enhanced security.
- Validate their private key, a mandatory step to access the Transactions section.


Every time a user logs in, private key validation is required to ensure secure access to transaction-related features. Without validation, the features will remain inaccessible.
![Profile](/docs/screenshots/profile-not-validated.png)
Validated profile:<br>
![Valid-Profile](/docs/screenshots/profile-validated.png)
If an account is suspended by the user or admin, it can only be unlocked using the private key. While the account is in a suspended state, all other buttons and functionalities on the Profile page are disabled, ensuring that no changes or actions can be performed until the account is reactivated.
![Suspended](/docs/screenshots/suspended-account.png)

#### Update Profile

The Edit Profile page allows users to manage and update their account details conveniently. Users can:

 - Change their email address.
 - Add their first name and last name.
 - Enable or disable email notifications and location tracking.
 - Suspend their account if needed.


These options ensure users have full control over their account preferences and settings.
![Update profile](/docs/screenshots/update-profile.png)

Email notifications:

| Type    |  Example    |
|---------|-------------|
| Login   | [login](/docs/email-notification/login-email.png)  |
| Payment | [payment](/docs/email-notification/payment-email.png) |
| Changes | [profile changes](/docs/email-notification/profile-change-email.png) |
| Password reset | [password reset](/docs/email-notification/pwd-reset-email.png) |
| Top Up  | [top-up](/docs/email-notification/top-up-email.png) |
| Withdraw | [withdraw](/docs/email-notification/withdraw-email.png)

#### Delete Profile

Users can delete their profile; however, all funds will be forfeited upon deletion. A warning message will be displayed to inform users of this outcome before they confirm the deletion.
![delete](/docs/screenshots/delete-profile.png)

#### Validate private key/Unlock account
The Validate Key and Unlock Account functionalities in MyVault use the same underlying logic for security and access control:

- Validate Key: When the user clicks the Validate Key button, it ensures that the private key is correctly validated. Once validated, the user gains access to sensitive sections, such as the Transactions and Dashboard pages, account deletion and profile update, which require this validation for security.

- Unlock Account: The Unlock Account functionality works in a similar way. It removes the suspension from the account by validating the user's private key, restoring access to all features and functionalities that were previously disabled due to the suspension.


In both cases, the user must provide the private key to proceed. This ensures that only the rightful account holder can access and manage their sensitive information.
![Validate PK](/docs/screenshots/validate-private-key.png)

#### Dashboard
The Dashboard provides users with a comprehensive overview of their financial activity, featuring three insightful charts.
Page before validation:
![Dashboard](/docs/screenshots/dashboard-not%20validated.png)
The first pie chart visualizes the distribution of the user’s transactions, breaking them down by type—Withdrawals, Deposits, Sent, and Received. It helps users understand their transaction habits at a glance.
![Pie](/docs/screenshots/dashboard-chart-one.png)
The bar chart displays the total number of transactions for the current month. This gives users a clear view of their activity over time, helping them track trends and patterns in their transactions.
![Bar](/docs/screenshots/dashboard-chart-2.png)
The third chart shows the total sum of inflows (deposits and money received) versus outflows (withdrawals and money sent) for the current month. It provides a quick overview of the user's financial balance for the month, highlighting any surplus or deficit.
![pie chart](/docs/screenshots/dashboard-chart-3.png)
#### Transactions
The Transactions page is designed to ensure that sensitive financial data is protected.
Private Key Validation: After login, if the user's private key is not validated, the transaction page will remain empty, preventing access to any sensitive information.
![Transaction no validation](/docs/screenshots/transactions-not-validated.png)
If the account is suspended, a clear and informative message displayed to the user, explaining the situation and the steps they need to take.
![Transaction suspension](/docs/screenshots/transaction-suspended.png)
Access After Validation: Once the private key is validated, the user gains full access to the transaction features:
- Balance: The user's current balance will be displayed.
- Sending and Receiving Addresses: The unique addresses for sending and receiving money will be shown.
- Action Buttons: Users will have the ability to perform actions such as:
   - Withdraw funds.
   - Top up their balance.
   - Send money to other users.
- Transaction History: Users can check their transaction history, giving them insights into past deposits, withdrawals, and transfers.


![Transactions](/docs/screenshots/transactions.png)

#### Top Up

For the Top Up process, users can follow these steps:

- Enter Amount: The user needs to enter the desired top-up amount on the Transactions page.
- Click on Top Up Button: After entering the amount, the user clicks the Top Up button to proceed.
- Redirect to Checkout Page: Upon clicking the top-up button, the user is redirected to the Checkout page.
- Enter Card and User Details: On the Checkout page, the user will need to enter their card details and user information to complete the transaction.
- Stripe Testnet: The payment system is powered by Stripe, but only the testnet environment is used, meaning no real payments will be processed. This allows users to simulate transactions for testing purposes without any actual financial transfer.


This process ensures that users can top up their accounts securely while using Stripe's test environment for validation and testing purposes.
If the payment is successful, a confirmation message will be displayed to the user.<br>
![topup](/docs/screenshots/checkout.gif)

#### Send Payment

The Send Payment form in MyVault includes validation to ensure secure and accurate transactions. Here’s how it works:

- Input Fields:

  - Amount: The user specifies the amount they wish to send.
  - Optional Note: An optional note can be added (e.g., "For dinner").
  - Receiver's Unique Address: The user enters the recipient's unique address.
- Validation Checks:

  - Receiver Address: If the address is invalid or does not exist, an error message will appear.
  - Sufficient Balance: If the entered amount exceeds the user's current balance, an error message will be displayed.

If all validations are passed, the payment will be processed, and the user will be redirected to the Transactions page.
This ensures that users can only send valid payments within their account limits, enhancing security and preventing errors.

![form](/docs/screenshots/send-payment.gif)

#### Withdraw

The user enters an amount and clicks the withdraw button. Since the page operates on a testnet, this function will simply deduct the withdrawal amount from the user's balance. Validation ensures that the withdrawal amount does not exceed the available balance and that the remaining balance is at least $1 USD. After the user clicks the withdraw button, they are redirected to either a withdraw success page or a withdraw failed page, depending on the outcome of the transaction.

#### Transactions history

The Transaction History page provides a user-friendly interface for reviewing financial activities, featuring pagination and advanced filtering options:

- Users can see all their Completed and Failed transactions.
- Each entry includes details such as the transaction type (e.g., Deposit, Withdraw, Sent, Received), amount, date, and status.
- 6 records per page, allowing users to navigate through their history without overwhelming the interface.
![Transactions history](/docs/screenshots/transactions-history.png)
- Users can move between pages using Next and Previous buttons or jump to specific pages.
- Users can filter transactions based on a specified range of amounts.
- Transactions can be filtered within a specific date range to focus on relevant periods.
- Users can refine results by selecting a specific type of transaction:
  - Withdraw
  - Deposit
  - Sent
  - Received

![filter](/docs/screenshots/history-filter.png)
When viewing details of a Sent transaction, the sender's unique address (only visible to the sender).
![sender view](/docs/screenshots/sent-history.png)
When viewing details of a Received transaction, the receiver can see the name of the sender for clarity.
![receiver view](/docs/screenshots/received-history.png)
The Pending status is part of the transaction model but will only be implemented and visible after integrating the testnet environment. This will allow users to track transactions that are awaiting confirmation.
This design ensures transparency and keeps users informed about the status of their financial activities, with room for future expansion to include pending transactions once the testnet is fully utilized.
#### Future Implementations
- Real Payments and Withdrawals: Enable live payment and withdrawal functionalities using Stripe.
- Historical Charts: Introduce a historical view to the charts, allowing users to compare transactions across different months.
- Profile Picture Upload: Add functionality for users to upload a profile picture, which will be displayed in the transaction history.
- Payment Requests: Allow users to request payments from others. When a payment request is made, a notification message will appear on the profile of the recipient.

## Technologies, Languages, and Programs used

- HTML - Markup language for creating web pages.
- CSS - Stylesheet language for styling the appearance of web pages.
- Bootstrap - A framework for building responsive, mobile-first sites.
- Python - The programming language used for the project.
- Django - A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- Djano Allauth - Used for authentication, registration, login & password reset.
- gunicorn - a Python WSGI HTTP Server
- psycopg2 - allow us to connect with a postgres database
- PostgreSQL - The database used to store transactions data, user information, and other relevant data for the application.
- Google Dev Tools - To troubleshoot, test features and solve issues with responsiveness and styling.
- JavaScript - for Stripe and Google Maps.
- GitHub - Web-based platform for version control and collaboration on software projects.
- Google Fonts - Library of free and open-source web fonts.
- Heroku - Used to deploy the project for hosting and managing the live application.
- Favicon.io - To create Favicon.
- [DBDiagram](https://dbdiagram.io/d) - To create ER Diagram
- [FreeConvert](https://www.freeconvert.com/convert/video-to-gif) - to convert screenrecordings to GIF
- Stripe - used for implementing test payments to showcase how the page will function when it goes live.
- Google Maps API: Used for tracking and displaying the user's location based on their IP address, enhancing features like login location tracking and visualization on a map.
- IpInfo: Used to obtain the user's IP address and retrieve location details (e.g., city, region, country) for features like login location tracking.
- Gemini API: An AI API integrated into the "Ask" page, enabling the application to answer user questions dynamically.
- [Toolsaday](https://toolsaday.com/writing/faq-generator) - to generate FAQ questions.
### Stripe

Stripe for the website is currently in developer mode, which allows us to be able to process test payments to check the function of the site.

| Type               | Card No                | Expiry               | CVC         | ZIP        |
|--------------------|------------------------|----------------------|-------------|------------|
| Success            | Visa 4242 4242 4242 4242 | A date in the future  | Any 3 digits | Any 5 digits |
| Require authorisation | 4000 0027 6000 3184  | A date in the future  | Any 3 digits | Any 5 digits |
| Declined           | 4000 0000 0000 0002    | A date in the future  | Any 3 digits | Any 5 digits |

## Deployment & Local Development

The project is deployed using Heroku. To deploy the project:

1. Create a live database - The database used in this project was provided by Code Institute.
2. Heroku app setup:
   1. From the Heroku dashboard, click the new button in the top right corner and select create new app.
   2. Give your app a name (this must be unique), select the region that is closest to you and then click the create app button bottom left.
   3. Open the settings tab and create a new config var of DATABASE_URL and paste the database URL(the value should not have quotation marks around it).
3. Prepare for deployment in GitPod:
   1. Install dj_database_url and psycopg2 (they are both needed for connecting to the external database you've just set up)<br>
   -- pip3 install dj-database-url==2.2.0 psycopg2 -- 
   2. Update your requirements.txt file with the installed packages.<br>
   -- pip3 freeze --local > requirements.txt --
   3. In settings.py underneath import os, add -- import dj_database_url --.
   4. To prevent your database URL from being misused, you can store it in the env.py file and add this file to .gitignore to keep it secure. Using the os library, you can then retrieve the database URL in your code instead of directly including it in settings.py.
   ![database](/docs/screenshots/settings-ss.png)
   5. In the terminal, run the show migrations command to confirm connection to the external database.<br>
   -- python3 manage.py runserver --
   6. If you have to the database correctly, you can now run migrations to migrate the models to the new database.<br>
   -- python3 manage.py migrate -- 
   7. Create a superuser for the new database.<br>
   -- python3 manage.py createsuperuser -- 
   8. Install gunicorn which will act as our webserver and freeze this to the requirements.txt file.<br>
   -- pip3 install gunicorn -- 
   9. Create a Procfile in the root directory. This tells Heroku to create a web dyno which runs gunicorn and serves our django app. Add the following to the file:<br>
   -- web: gunicorn my_vault.wsgi -- 
   10. Add the Heroku app and localhost (which will allow GitPod to still work) to ALLOWED_HOSTS = [] in settings.py:<br>
   ![hosts](/docs/screenshots/allowed-host.png)
   11. Install whitenoise. It will allow your Heroku app to serve its own static files without relying on any external file hosting services like a content delivery network (CDN). Then add it to the requirements.txt.
   <br>
   -- pip3 install whitenoise~=5.3.0 -- 
   <br>
   The WhiteNoise middleware must be placed directly after the Django SecurityMiddleware in settings.py<br>
   -- 'whitenoise.middleware.WhiteNoiseMiddleware', --
   12. Add the following path to settings.py<br>
     -- STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') --
   13. Collect static files -- python3 manage.py collectstatic -- and add a runtime.txt file to your app's root directory. Check your Python version and copy the runtime closest to the one used in your IDE.
   [Supported runtimes](https://devcenter.heroku.com/articles/python-support#specifying-a-python-version)
   14. Save, add, commit and push the changes to GitHub. 
   15. To enable automatic deploys on Heroku, go to the deploy tab and click the connect to GitHub button in the deployment method section. Search for the projects repository and then click connect. Click enable automatic deploys at the bottom of the page.
4. Django automatically sets a secret key when you create your project, however we shouldn't use this default key in our deployed version. We can use a random key generator to create a new SECRET_KEY which we can then add to our Heroku config vars.
5. The following entries must be added to the Heroku config vars:
  - EMAIL_HOST_USER and EMAIL_HOST_PASS for email notifications
  - GEMINI_API_KEY for AI functionality
  - Google Maps API key for map integration
  - IP_TOKEN for the IPInfo API to retrieve user IP addresses and login details
  - Stripe publishable and secret keys for payment processing

### Local Deployment

This repository can be cloned and run locally with the following steps:

- Login to GitHub.
- Select repository named: https://github.com/Tamas-Gavlider/MyVault
- Click code toggle button and copy the url (https://github.com/Tamas-Gavlider/MyVault.git).
- In your IDE, open the terminal and run the git clone command (git clone https://github.com/Tamas-Gavlider/MyVault.git). The repository will now be cloned in your workspace.

### Testing 

I have used Chrome Developer tool while building the web page and troubleshoot any issues immediately.<br>
The following issues were raised during my mid project meeting with my mentor:

- The private key validation was coded with JavaScript. But it is better to be done with Python.
- The project kanban board issues were not visible by other users on GitHub. The user story template was connected to other project, so I had to delete and readd the issues with the correct repo.
- Change the sender details transactions details. It should show the name of the sender instead of their sending address. 
- Notify user if changes made on the account.

#### HTML

[W3C](https://validator.w3.org/) was used to validate the HTML on all pages of the site. It was also used to validate the CSS. As the site is created with Django and utilises Django templating language within the HTML, I have checked the HTML by inspecting the page source and then running this through the validator.

|   Page   |   Result   |   Evidence   |
| ---------- | :------------:| --------:|
|   Home   |  No error  |     [home](/docs/testing/w3c/home.png)                        |
|  Login   |  No error  |     [login](/docs/testing/w3c/login.png)                      |
|  Logout  |  No error  |     [logout](/docs/testing/w3c/logout.png)                    |
|  Register|  No error  |     [signup](/docs/testing/w3c/signup.png)                    |
|   FAQ    |  No error  |     [faq](/docs/testing/w3c/faq.png)                          |
|   ASK    |  No error  |     [ask](/docs/testing/w3c/ask.png)                          |
|  Profile |  No error  |     [profile](/docs/testing/w3c/profile.png)                  |
|  Delete Profile |  No error | [delete profile](/docs/testing/w3c/delete-profile.png)  |
|  Update Profile |  No error | [update profile](/docs/testing/w3c/update-profile.png)  |
|  Location       |  No error | [location](/docs/testing/w3c/location.png)              |
|  Validate Key |  No error  |[validate key](/docs/testing/w3c/validate-key.png)        |
|  Dashboard |  No error  |   [dashboard](/docs/testing/w3c/dashboard.png)              |
|  Transactions |  No error  | [transactions](/docs/testing/w3c/transactions.png)       |
|  Transaction History |  No error  |[transaction history](/docs/testing/w3c/transaction-history.png)  |
|  Send Payment |  No error  | [send payment](/docs/testing/w3c/send-payment.png) |

#### CSS

[W3C](https://validator.w3.org/) was used to validate the CSS.
![css](/docs/testing/w3c/css-validator.png)

#### Python

[Code Institute Python Linter](https://pep8ci.herokuapp.com/) was used to validate the python files.

| File      |   Result     |              Screenshot     |
|-----------|:----------------------:|------------------------:|
| my-home-models.py     |   Pass            |        [home-models](/docs/testing/pep8/my-home-models.png)       
| my-home-views.py      |   Pass            |        [home-views](/docs/testing/pep8/my-home-views.png)  
| my-home-admin.py      |   Pass            |        [home-admin](/docs/testing/pep8/my-home-admin.png)   
| my-home-urls.py      |   Pass            |        [home-urls](/docs/testing/pep8/my-home-urls.png)   
| my-profile-models.py  |   Pass            |       [profile-models](/docs/testing/pep8/my-profile-models.png)       
| my-profile-signals.py      |   Pass            |        [profile-signals](/docs/testing/pep8/my-profile-signals.png)  
| my-profile-tests.py      |   Pass            |        [profile-tests](/docs/testing/pep8/my-profile-tests.png)   
| my-profile-urls.py     |   Pass            |        [profile-urls](/docs/testing/pep8/my-profile-urls.png)       
| my-profile-views.py    |   Pass         |        [profile-views](/docs/testing/pep8/my-profile-views.png)  
| my-profile-form.py      |   Pass            |        [profile-form](/docs/testing/pep8/my-profile-form.png)
| my-profile-admin.py      |   Pass            |        [profile-admin](/docs/testing/pep8/my-profile-admin.png)  
| my-profile-tasks.py      |   Pass            |        [profile-tasks](/docs/testing/pep8/profile-tasks.png) 
| my-profile-app.py      |   Pass            |        [profile-app](/docs/testing/pep8/profile-app.png)  
| my-transactions-admin.py      |   Pass            |        [transaction-admin](/docs/testing/pep8/transactions-admin.png) 
| my-transactions-models.py      |   Pass            |        [transaction-models](/docs/testing/pep8/transactions-models.png) 
| my-transactions-tests.py      |   Pass            |        [transaction-test](/docs/testing/pep8/transactions-test.png) 
| my-transactions-urls.py      |   Pass            |        [transaction-urls](/docs/testing/pep8/transactions-urls.png) 
| my-transactions-views.py      |   Pass            |        [transaction-views](/docs/testing/pep8/transactions-views.png) 
| dashboard-views.py      |   Pass            |        [dashboard-views](/docs/testing/pep8/dashboard-views.png) 
| dashboard-urls.py      |   Pass            |        [dashboard-urls](/docs/testing/pep8/dashboard-url.png) 



#### Lighthouse 

I have used Googles Lighthouse testing to test the performance, accessibility, best practices and SEO of the site.

| Page      |   Mobile/Desktop     |              Score     |
|-----------|:----------------------:|:------------------------:|
| Home      |   Mobile             |        ![home-mobile](/docs/testing/lighthouse/home-mobile.png)       
| Home      |   Desktop            |        ![home-mobile](/docs/testing/lighthouse/home-desktop.png)      
| Profile   |   Mobile             |        ![home-mobile](/docs/testing/lighthouse/profile-mobile.png) 
| Profile   |   Desktop            |        ![home-mobile](/docs/testing/lighthouse/profile-desktop.png)    
| Edit-Profile   |   Mobile        |        ![home-mobile](/docs/testing/lighthouse/edit-profile-mobile.png)    
| Edit-Profile   |   Desktop       |        ![home-mobile](/docs/testing/lighthouse/edit-profile-desktop.png)   
| Delete-Profile   |   Mobile      |        ![home-mobile](/docs/testing/lighthouse/delete-profile-mobile.png)    
| Delete-Profile   |   Desktop     |        ![home-mobile](/docs/testing/lighthouse/delete-profile-desktop.png)   
| Validate Pk   |   Mobile         |        ![home-mobile](/docs/testing/lighthouse/validate-pk-mobile.png)    
| Validate Pk   |   Desktop        |        ![home-mobile](/docs/testing/lighthouse/validate-pk-desktop.png)   
| Location  |   Desktop            |        ![home-mobile](/docs/testing/lighthouse/location-desktop.png)    
| FAQ   |          Desktop         |        ![home-mobile](/docs/testing/lighthouse/faq-desktop.png)   
| FAQ   |          Mobile          |        ![home-mobile](/docs/testing/lighthouse/faq-mobile.png) 
| Ask   |          Desktop         |        ![home-mobile](/docs/testing/lighthouse/ask-desktop.png)   
| Ask   |          Mobile          |        ![home-mobile](/docs/testing/lighthouse/ask-mobile.png) 
| Dashboard   |         Desktop    |        ![home-mobile](/docs/testing/lighthouse/dashboard-desktop.png)   
| Dashboard   |         Mobile     |        ![home-mobile](/docs/testing/lighthouse/dashboard-mobile.png) 
| Transaction   |       Desktop    |        ![home-mobile](/docs/testing/lighthouse/transaction-desktop.png)   
| Transaction   |       Mobile     |        ![home-mobile](/docs/testing/lighthouse/transaction-mobile.png) 
| Transaction History   |Desktop   |        ![home-mobile](/docs/testing/lighthouse/history-desktop.png)  
| Transaction History  | Mobile    |        ![home-mobile](/docs/testing/lighthouse/history-mobile.png) 


#### Wave

WAVE(Web Accessibility Evaluation Tool) allows developers to create content that is more accessible to users with disabilities. It does this by identifying accessibility and WGAC errors.

| Page    |  Result      |  Evidence |
|---------|--------------| -----------|
| Home    |  No erros    | [home](/docs/testing/wave/home-wave.png)             |
| Login   |  No errors   | [login](/docs/testing/wave/login-wave.png)           |
| Logout  |  No errors   | [logout](/docs/testing/wave/logout-wave.png)         |
| Register|  No errors   | [register](/docs/testing/wave/register-wave.png)     |
| FAQ     |  No errors   | [faq](/docs/testing/wave/faq-wave.png)               |
| Ask     |  No errors   |  [ask](/docs/testing/wave/ask-wave.png)              |
| Profile   |  No errors | [profile](/docs/testing/wave/profile-wave.png)       |
| Update profile    | No errors   | [update profile](/docs/testing/wave/update-profile-wave.png)        |
| Delete profile   |   No errors     |  [delete profile](/docs/testing/wave/delete-profile.png)       |
| Reset Password   |   No errors       |  [password reset](/docs/testing/wave/pwd-reset-wave.png)       |
| Validate Key  |   No errors       |   [validate key](/docs/testing/wave/validate-key-wave.png)     |
| Location   |   No errors       |   [location](/docs/testing/wave/location-wave.png)     |
| Dashboard   |  No errors       |   [dashboard](/docs/testing/wave/dashboard-wave.png)    |
| Transactions   |   No errors       | [transactions](/docs/testing/wave/transactions-wave.png)        |
| Send payment   |  No errors        | [send payment](/docs/testing/wave/send-payment-wave.png)        |
| Transactions History   |   No errors       | [transactions history](/docs/testing/wave/transactions-history-wave.png)        |

#### Automated testing

Automated testing for this project was carried out with [Django TestCase](https://docs.djangoproject.com/en/4.1/topics/testing/overview/).

Tranasctions:
![Transaction](/docs/testing/automated_testing/transaction-app-test.png)
Profile:
![Profile](/docs/testing/automated_testing/profile-app-test.png)

#### Manual Testing

#### Full Testing

Full testing was performed on the following devices:
- Mobile:
  - Iphone 11
  - Iphone 13
- Laptop: 
  - Macbook Pro 2019 13 inch screen
  - Mackbook Pro 2014 15 inch screen

Testing was also performed using the following browsers:
- Chrome
- FireFox
- Safari

#### Bugs

## Credits

### Media

The background image was downloaded from [Pexels](https://www.pexels.com/).
<br>
The favicon logo was created on [FreeLogoDesign](https://www.freelogodesign.org/)
<br>
All screenshots used in this README file were taken by myself.

### Content

FAQ questions were generated by [Toolsaday](https://toolsaday.com/writing/faq-generator).

For the location tracker I referred to [IPinfo](https://github.com/ipinfo/python/blob/master/README.md).

For the last login time format I reffered to [StackOverFlow](https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python).

[Stripe API](https://docs.stripe.com/checkout/quickstart) documentation to implement the test payments.

[Secrets library](https://docs.python.org/3/library/secrets.html) to implement the private key, and addresses.

[Gemini API](https://ai.google.dev/gemini-api/docs) documentation for the AI responses.

[Google Maps API](https://developers.google.com/maps/documentation) for the map on the location page.

[W3Schools](https://www.w3schools.com/) to review how certain libraries function and for Django tutorials.
