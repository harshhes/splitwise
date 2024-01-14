# Splitwise

Splitwise is a Django-based web application designed to simplify the process of managing shared expenses within a group. It allows users to add, edit, and track expenses, as well as settle debts among group members. The application provides features like equal splitting of expenses, real-time updates, and user authentication.

## Table of Contents

- [Splitwise](#splitwise)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Configuration](#configuration)
  - [Usage](#usage)
  - [Database Design](#database-design)
    - [User Model](#user-model)
    - [ExpenseGroup Model](#expensegroup-model)
    - [ExpenseParticipant Model](#expenseparticipant-model)
  - [Postman API data dump:](#postman-api-data-dump)

## Features

- **Expense Management:** Easily manage shared expenses within a group.
- **Equal Split:** Automatically calculate and split expenses equally among participants.
- **User Authentication:** Secure user authentication and account management.
- **Real-time Updates:** Keep track of expenses and balances in real-time.
- **Email Notifications:** Receive email notifications for added expenses and settlements.

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/splitwise.git
   cd splitwise
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

5. Visit [http://localhost:8000/](http://localhost:8000/) in your web browser.

### Configuration

- Update configuration settings in `settings.py` as needed.
- Set environment variables for sensitive information.

## Usage

- Create user accounts and start managing expenses within your groups.
- Add expenses, specify the type, and let Splitwise handle the calculations.
- Receive real-time updates and settle debts efficiently.

## Database Design

### User Model

The `User` model is a custom user model extending `AbstractUser` with email authentication.

### ExpenseGroup Model

- `name`: Name of the expense group.
- `payer`: ForeignKey to the user who paid for the expense.
- `expense_type`: Type of expense (choices: Equal, Proportional, etc.).
- `amount`: Total expense amount.
- `image`: Image attachment for the expense (optional).
- `notes`: Additional notes for the expense (optional).
- `users`: ManyToManyField to the `User` model representing participants.
- `created_at` and `updated_at`: Timestamps for creation and updates.

### ExpenseParticipant Model

- `user`: ForeignKey to the user who participated in the expense.
- `expense`: ForeignKey to the corresponding `ExpenseGroup`.
- `owe_amount`: Amount owed by the user.
- `percentage`: Percentage of the total expense covered by the user (optional).
- `final_amount`: Final amount after settlement.
- `created_at` and `updated_at`: Timestamps for creation and updates.

## Postman API data dump:
