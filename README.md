# sleep-well

Sleep-Well is a RESTful API web service designed to offer sleep quality data to
users. The API will provide endpoints for accessing sleep information,
including sleep duration, quality scores, environmental factors (such as
weather and noise levels), and personal information about the individual's
sleep patterns. Additionally, the API will include analytics features to
analyze sleep comments and provide insights into sleep quality trends.

### Endpoints

1. **List Sleep Information**
    - **Endpoint:** `/info/sleep/`
    - **Method:** GET
    - **Description:** Retrieves a list of all sleep entries with associated
      weather and noise data.

2. **Get Sleep Information by ID**
    - **Endpoint:** `/info/sleep/<int:sleep_id>/`
    - **Method:** GET
    - **Description:** Retrieves sleep information based on the provided sleep
      ID.

3. **Filter Sleep Information by Person ID**
    - **Endpoint:** `/info/sleep/person/<int:person_id>/`
    - **Endpoint:** `/info/person/<int:person_id>/sleep/`
    - **Method:** GET
    - **Description:** Retrieves sleep entries filtered by the person's ID.

4. **List Person Information**
    - **Endpoint:** `/info/person/`
    - **Method:** GET
    - **Description:** Retrieves a list of all persons with their information.

5. **Get Person Information by ID**
    - **Endpoint:** `/info/person/<int:person_id>/`
    - **Method:** GET
    - **Description:** Retrieves person information based on the provided
      person ID.

6. **Sleep Analytics for All Persons**
    - **Endpoint:** `/sleep-analytics/`
    - **Method:** GET
    - **Description:** Performs analytics on sleep data for all persons,
      including average sleep score, sentiment analysis of sleep comments, and
      environmental data analysis.

7. **Sleep Analytics for a Specific Person**
    - **Endpoint:** `/sleep-analytics/person/<int:person_id>/`
    - **Endpoint:** `/person/<int:person_id>/sleep-analytics/`
    - **Method:** GET
    - **Description:** Performs analytics on sleep data for a specific person,
      including average sleep score, sentiment analysis of sleep comments, and
      environmental data analysis.
