# GenericCRM - Backend

I've been disappointed with the current state of paid, freemium, and open-source CRMs. The goal of this project is to create a CRM backend that is both generic and powerful enough that anyone can plug their own front end onto it via REST API.

## Setup

1. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:
   ```sh
   python -m app
   ```

4. Run tests:
   ```sh
   pytest
   ```