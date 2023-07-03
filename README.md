
# Restaurant-reservations-System

The website provides a reservation system for a restaurant, allows customers to create an account and manage or delete their account, make table reservations profile and cancel their reservations. This application is built using the Django framework, leveraging several built-in modules and some custom code.

## Site Owner
The site owner, or administrator, would typically have full control over the system, as provided by Django's built-in administration capabilities. In this context, the site owner can:

- Access, update, and delete all user (Customer) information.
- Access, update, and delete all reservations.
- Manage tables, including their number and capacity.
- Manage menu items, including adding, updating, and removing items.

## Customers
Customers are the users of the website who can register and create their own accounts. The 'User' model from Django's auth module is used to manage user authentication, and a custom 'Customer' model is linked to each User to store additional data.

Each customer has:

- An associated User from Django's auth module, which manages the customer's authentication.
- Name, phone number, and email stored in the 'Customer' model.
As an authenticated customer, a user can:

- Make a reservation: They can specify the date, time, the number of guests, their contact information, and optionally order items in advance.
- View their reservations: They can see all of their past and upcoming reservations, sorted by date and time.
- Cancel a reservation: They can cancel a specific reservation if needed.
- Update their profile: They can change their username, email, name, and phone number.
- Change their password.
- or delete their account

These actions are performed through the use of various Django views and forms, such as the ReservationCreateView, UserRegisterView, and ReservationForm. Note that to perform any actions on reservations, a customer must be logged in, as indicated by the LoginRequiredMixin on some views and the @login_required decorator on others.

![Screenshot (57)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/820593a0-abfd-4f52-882c-994df8f03749)

![Screenshot (58)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/fa204057-78f4-4c32-98f4-ec9804ab142d)

![Screenshot (60)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/cd7c6773-63ec-4da6-b7e4-7d48b96648bf)

![Screenshot (66)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/83e2e8f2-e395-42d5-858e-57fe712f034f)

![Screenshot (62)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/7884ca4d-0cfd-4e35-b894-09c304a8afb5)

## Models
There are five models used in this application: Customer, Reservation, Table, Menu, and Item.

- Customer - Represents a customer in the restaurant. Each customer has a name, phone_number, and email.

- Reservation - Represents a reservation made by a customer. It contains date, time, number of guests, name, email, phone number, ordered_items, tables, associated customer, and duration of the reservation.

- Table - Represents a table in the restaurant. Each table has a number, capacity, and a reservation status.

- Menu - Represents a menu in the restaurant. Each menu has a name.

- Item - Represents an item in the restaurant's menu. Each item has a name, price, and menu it belongs to.

## Forms
The application includes five forms: ProfileUpdateForm, UserRegisterForm, CustomerProfileUpdateForm, ReservationForm, and PasswordChangeForm.

- ProfileUpdateForm - Used to update the profile of an existing user.

- UserRegisterForm - Used to register a new user.

- CustomerProfileUpdateForm - Used to update the profile of an existing customer.

- ReservationForm - Used to make a new reservation. It includes additional validation for 'phone_number', 'name' and 'date' fields. Also includes a complex cleaning method to determine table availability and assign tables to the reservation.

- PasswordChangeForm - Used to change the user's password.

## Views
There are several views handling various user requests:

- ReservationCreateView - Handles creating a new reservation.

- CancelReservationView - Handles cancelling a reservation.

- reservation_detail - Handles the display of reservation details.

- reservation_list - Handles the display of a list of reservations.

- home - Handles requests to the homepage.

- update_profile - Handles updating a user's profile.

- change_password - Handles changing a user's password.

- DeleteAccountView - Handles deleting a user's account.

- UserRegisterView - Handles user registration.

![Screenshot (65)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/7260de17-02eb-4eec-97ff-8291c086d2ad)

![Screenshot (63)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/201ccb62-c1fd-4838-b28f-6b00420513c7)

![Screenshot (64)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/67da9a44-f361-468e-aa37-bf2d1ada6e2a)

## Error Handling
Reservation Form:

The ReservationForm includes custom error handling through the clean methods for the phone_number, name, and date fields:

- clean_phone_number checks that the entered phone number contains only digits. If not, it raises a ValidationError.
- clean_name checks that the entered name does not contain any numbers. If it does, it raises a ValidationError.
- clean_date ensures that the reservation date is not in the past. If it is, it raises a ValidationError.

When a user attempts to create a new reservation,the clean method checks the availability of tables at the requested date and time.

- It first calculates the number of tables needed based on the number of guests (tables_needed).
- Then it determines the time range for which the reservation would last. The code assumes a reservation duration of two hours, starting from the time the user entered.
- Next, it fetches all the tables that are currently not reserved for the specified date and time range (available_tables).

- If the number of available tables is less than the number of tables needed, an error is added to the form (self.add_error(None, f"There are not enough tables available at this time.")). This error will be displayed to the user, informing them that there aren't enough tables available at the chosen time, and they should try a different time or reduce the number of guests.

- If there are enough tables available, it selects the necessary number of tables (selected_tables) and assigns them to the reservation (cleaned_data['tables'] = selected_tables).

So in essence,the form prevents double booking by checking the availability of tables at the time of the reservation request, and only allowing the reservation to proceed if enough tables are available. This approach ensures that each table can only be reserved by one party at any given time.

![Screenshot (67)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/1159f9f7-e255-4897-870a-b3feef0de304)

![Screenshot (69)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/38b020fb-bef5-46c7-a56b-02952ba51dfc)

## Bugfix
Handling Overcapacity in Guest Numbers
```javascript     
guests = forms.IntegerField(min_value=1, max_value=40)
```
if a user tries to make a reservation for more than 40 guests (or less than 1), Django's form validation will automatically prevent this and raise a validation error, because the number of guests would fall outside of the defined min_value and max_value range.
Therefore, you don't need any additional code to handle this particular situation, as Django's forms take care of it for you. This is a good example of Django helping to maintain the integrity of your data by ensuring that users can't input values that don't make sense in the context of your application.
- No more bugs found.

## Future features
- Automated Reminders: These could be sent via email or SMS.
- Table Preference: Allow customers to select their preferred table location.
- Special Requests Handling: Provide a form field for customers to enter any special requests.
- Analytics Dashboard: an analytics dashboard for the restaurant owner or manager. This could show information like peak reservation times.

## Validator and testing
- PEP8 style guide and validated HTML and CSS code.
- I did Manual testing in different browsers and devices.
- and automated tests test_forms.py, test_models.py, test_views.py.

![Screenshot (70)](https://github.com/Attila-fawal/Battleships-game/assets/127791713/e61cc914-964b-4b68-8103-81ee752822c5)

## Deployment
This project was deployed Using Code-Institute-Org/gitpod-full-template.

Steps for deployment
- Fork or clone this repository.
- create new heroku account or if you already have one press to create a new app.
- Add name for your new app And choose the region Go to settings and add buildpacks python and nodeJS In that order.
- add a Config Var called PORT. Set this to 8000.
- Link the Heroku app to the repository
- Click the Deploy

## Credits
- code Institute For the deployment terminal.
- ElephantSQL for the database.
- Cloudinary for the Pictures.
- fontawesome for the icons.
