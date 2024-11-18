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

User Stories were tracked throughout the project as [GitHub issues](https://github.com/users/Tamas-Gavlider/projects/5/views/1).

### User Stories

## Design

### Structure

The ERD represents the database structure for the application.
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

### Typography

The Nanum Myeongjo font, available via Google Fonts, is a sophisticated serif typeface inspired by traditional Korean calligraphy. The font’s graceful curves and sharp serifs make it stand out, giving your design a distinctive and memorable quality.

### Features

All pages feature a fully responsive navbar that transforms into a hamburger menu on smaller screens and a [favicon](/static/images/android-chrome-192x192.png) in the browser tab.<br>
Navbar if user logged in
![Logged in](/docs/screenshots/home-logged-in.png)

Navbar is user logged out/not registered
![Logged out](/docs/screenshots/home-logged-out.png)

#### Home

![Backgorund](/docs/screenshots/home-page-bg.png)

#### FAQ

#### Ask

![Ask page](/docs/screenshots/ask-page.png)

#### Profile

![Profile](/docs/screenshots/profile.png)
Account suspended
![Suspended](/docs/screenshots/suspended-account.png)

#### Update Profile
Update profile
![Update profile](/docs/screenshots/update-profile.png)

#### Validate private key/Unlock accounr
Validate secret private key
![Validate PK](/docs/screenshots/validate-private-key.png)

#### Dashboard

Pie chart
![Pie](/docs/screenshots/dashboard-chart-one.png)
Bar chart
![Bar](/docs/screenshots/dashboard-chart-2.png)

#### Transactions

![Transactions](/docs/screenshots/transactions.png)

#### Top up

#### Send payment

#### Transactions history

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

#### W3C Validator

#### JavaScript Validator

#### Lighthouse

#### Wave

#### Full Testing

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
