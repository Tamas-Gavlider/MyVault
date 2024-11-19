# MyVault

MyVault is a secure and feature-rich application designed to help users manage their finances with ease and confidence. 
It offers features like sending and receiving money with unique addresses, deposits and withdrawals through Stripe, private key authentication, and detailed transaction history. Additional functionalities include email notifications, login location tracking with Google Maps, and complete account deletion. MyVault prioritizes privacy and user responsibility<br>
<strong>"Your vault, your responsibility."</strong>

The live deployed site can be found [here](https://my-vault-cb8eb703ab63.herokuapp.com/)

## Agile Development

User stories were prioritized using MoSCoW.
The Agile process emphasizes incremental development and user-focused delivery. The following flowchart outlines how key application features and workflows, such as user validation, transaction handling, and account management, were prioritized and developed across sprints:<br>
![flowchart](/docs/screenshots/project-4.png)<br>
This workflow guided the sprint planning and ensured seamless integration of essential features.

## User Experience(UX)

### Project Goals

### User Stories

User Stories were tracked throughout the project as [GitHub issues](https://github.com/users/Tamas-Gavlider/projects/5/views/1).

## Design

### Structure

The ERD represents the database structure for the application. Due to the data being used for the project I have opted to use a relational database as this will best suit my requirements.
 - Profile - Stores user-specific details such as balance, notification preferences, and unique sending/receiving addresses. Each profile is linked to a user account via a Foreign Key.
 - Transactions - Tracks all financial activities, including deposits, withdrawals, and transfers between users, with fields for transaction type, status, and amounts.
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


Every time a user logs in, private key validation is required to ensure secure access to transaction-related features. Without validation, transactions will remain inaccessible.
![Profile](/docs/screenshots/profile.png)
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

#### Validate private key/Unlock account
The Validate Key and Unlock Account functionalities in MyVault use the same underlying logic for security and access control:

- Validate Key: When the user clicks the Validate Key button, it ensures that the private key is correctly validated. Once validated, the user gains access to sensitive sections, such as the Transactions and Dashboard pages, which require this validation for security.

- Unlock Account: The Unlock Account functionality works in a similar way. It removes the suspension from the account by validating the user's private key, restoring access to all features and functionalities that were previously disabled due to the suspension.


In both cases, the user must provide the private key to proceed. This ensures that only the rightful account holder can access and manage their sensitive information.
![Validate PK](/docs/screenshots/validate-private-key.png)

#### Dashboard
The Dashboard provides users with a comprehensive overview of their financial activity, featuring three insightful charts.
The first pie chart visualizes the distribution of the user’s transactions, breaking them down by type—Withdrawals, Deposits, Sent, and Received. It helps users understand their transaction habits at a glance.
![Pie](/docs/screenshots/dashboard-chart-one.png)
The bar chart displays the total number of transactions for the current month. This gives users a clear view of their activity over time, helping them track trends and patterns in their transactions.
![Bar](/docs/screenshots/dashboard-chart-2.png)
The third chart shows the total sum of inflows (deposits and money received) versus outflows (withdrawals and money sent) for the current month. It provides a quick overview of the user's financial balance for the month, highlighting any surplus or deficit.
![pie chart](/docs/screenshots/dashboard-chart-3.png)
#### Transactions
The Transactions page is designed to ensure that sensitive financial data is protected.
Private Key Validation: After login, if the user's private key is not validated, the transaction page will remain empty, preventing access to any sensitive information.
![Transaction no validation](/docs/screenshots/transaction-no-validation.png)
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

#### Top up

For the Top Up process, users can follow these steps:

- Enter Amount: The user needs to enter the desired top-up amount on the Transactions page.
- Click on Top Up Button: After entering the amount, the user clicks the Top Up button to proceed.
- Redirect to Checkout Page: Upon clicking the top-up button, the user is redirected to the Checkout page.
- Enter Card and User Details: On the Checkout page, the user will need to enter their card details and user information to complete the transaction.
- Stripe Testnet: The payment system is powered by Stripe, but only the testnet environment is used, meaning no real payments will be processed. This allows users to simulate transactions for testing purposes without any actual financial transfer.


This process ensures that users can top up their accounts securely while using Stripe's test environment for validation and testing purposes.
If the payment is successful, a confirmation message will be displayed to the user.<br>
![topup](/docs/screenshots/checkout.gif)
#### Send payment

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

## Technologies, Languages, and Programs used

- HTML - Markup language for creating web pages.
- CSS - Stylesheet language for styling the appearance of web pages.
- Bootstrap - A framework for building responsive, mobile-first sites.
- Python - The programming language used for the project.
- Django - A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- Djano Allauth - Used for authentication, registration & account management.
- gunicorn - a Python WSGI HTTP Server
- dj_databsae_url - allows us to utilise the DATABASE_URL variable
- psycopg2 - a postgres database adapter which allow us to connect with a postgres database
- PostgreSQL - The database used to store transactions data, user information, and other relevant data for the application.
- Google Dev Tools - To troubleshoot, test features and solve issues with responsiveness and styling.
- JavaScript - for Stripe and Google Maps.
- GitHub - Web-based platform for version control and collaboration on software projects.
- Google Fonts - Library of free and open-source web fonts.
- Heroku - Used to deploy the project for hosting and managing the live application.
- Favicon.io - To create Favicon.
- [SmartDraw](https://www.smartdraw.com/entity-relationship-diagram/er-diagram-tool.htm) - To create ER Diagram
- Stripe - for payment system

### Stripe

Stripe for the website is currently in developer mode, which allows us to be able to process test payments to check the function of the site.

| Type               | Card No                | Expiry               | CVC         | ZIP        |
|--------------------|------------------------|----------------------|-------------|------------|
| Success            | Visa 4242 4242 4242 4242 | A date in the future  | Any 3 digits | Any 5 digits |
| Require authorisation | 4000 0027 6000 3184  | A date in the future  | Any 3 digits | Any 5 digits |
| Declined           | 4000 0000 0000 0002    | A date in the future  | Any 3 digits | Any 5 digits |

## Deployment & Local Development

The project is deployed using Heroku. To deploy the project:

### Local Deployment

This repository can be cloned and run locally with the following steps:

- Login to GitHub.
- Select repository named: https://github.com/Tamas-Gavlider/MyVault
- Click code toggle button and copy the url (https://github.com/Tamas-Gavlider/MyVault.git).
- In your IDE, open the terminal and run the git clone command (git clone https://github.com/Tamas-Gavlider/MyVault.git). The repository will now be cloned in your workspace.

### Testing 

I have used Chrome Developer tool while building the web page and troubleshoot any issues immediately.<br>
The following issues were raised during my mid project meeting with my mentor:

- The private key validation was coded with JavaScript. But it is betterto be done with Python.
- The project kanban board issues were not visible by other users on GitHub. The user story template was connected to other project, so I had to delete and readd the issues with the correct repo.
- Change the sender details transactions details. It should show the name of the sender instead of their sending address. 
- Notify user if changes made on the account.

#### HTML

[W3C](https://validator.w3.org/) was used to validate the HTML on all pages of the site. It was also used to validate the CSS. As the site is created with Django and utilises Django templating language within the HTML, I have checked the HTML by inspecting the page source and then running this through the validator.

#### CSS

[W3C](https://validator.w3.org/) was used to validate the CSS.

#### JavaScript

[JS Hint](https://jshint.com/) was used to validate the JavaScript.

#### Python

[Code Institute Python Linter](https://pep8ci.herokuapp.com/) was used to validate the python.

#### Lighthouse 

I have used Googles Lighthouse testing to test the performance, accessibility, best practices and SEO of the site.

#### Wave

WAVE(Web Accessibility Evaluation Tool) allows developers to create content that is more accessible to users with disabilities. It does this by identifying accessibility and WGAC errors.

#### Automated testing

Automated testing for this project was carried out with [Django TestCase](https://docs.djangoproject.com/en/4.1/topics/testing/overview/). I would write a test, run the test and fix any issues raised before running the test again to confirm it passed. When a test passed I committed it to GitHub.

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
All screenshots used in this README file were taken by myself.

### Content

FAQ questions were generated by [Toolsaday](https://toolsaday.com/writing/faq-generator).

For the location tracker I referred to [IPinfo](https://github.com/ipinfo/python/blob/master/README.md).

For the last login time format I reffered to [StackOverFlow](https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python).

[Stripe API](https://docs.stripe.com/checkout/quickstart) documentation to implement the test payments.

[Secrets library](https://docs.python.org/3/library/secrets.html) to implement the private key, and addresses.

[Gemini API](https://ai.google.dev/gemini-api/docs) documentation for the AI responses.

[Google Maps API](https://developers.google.com/maps/documentation) for the map on the location page.
