# sleep-well

Sleep-Well is a RESTful API web service designed to offer sleep quality data to
users. The API will provide endpoints for accessing sleep information,
including sleep duration, quality scores, environmental factors (such as
weather and noise levels), and personal information about the individual's
sleep patterns. Additionally, the API will include analytics features to
analyze sleep comments and provide insights into sleep quality trends.

## Install instructions
Please configure the `sample.env` file before proceeding with the installation. Refer to the detailed configuration guide in [configurations.md](Installation%2Fconfigurations.md).

For a quick and efficient setup, it is recommended to use the provided script. Find instructions in [script.md](Installation%2Fscript.md).

If you prefer a manual setup, follow the steps outlined in [manual.md](Installation%2Fmanual.md).

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

4. **Sleep Information by Date**
    - **Endpoint:** `/info/sleep/date/`
    - **Method:** GET
    - **Description:** Retrieves sleep entries that occurred on a specific date. The date can be
      specified using query parameters `day`, `mouth`, and `year`. For
      example, `/info/sleep/date/day/10/mouth/5/year/2024` would retrieve sleep entries for May 10,
        2024.

5. **Sleep Information by Location Within Range**
    - **Endpoint:** `Endpoint: /info/sleep/<float:lat>-<float:lon>`
    - **Endpoint:** `Endpoint: /info/sleep/<float:lat>-<float:lon>/range/<int:km>`
    - **Method:** GET
    - **Description:** Retrieves sleep entries within a specified range (in kilometers) from a given
      location identified by latitude and longitude coordinates. If no specific range is provided,
      the default range of 5 kilometers is used to filter sleep entries within this distance from
      the specified location.

6. **List Person Information**
    - **Endpoint:** `/info/person/`
    - **Method:** GET
    - **Description:** Retrieves a list of all persons with their information.

7. **Get Person Information by ID**
    - **Endpoint:** `/info/person/<int:person_id>/`
    - **Method:** GET
    - **Description:** Retrieves person information based on the provided
      person ID.

8. **Sleep Analytics for All Persons**
    - **Endpoint:** `/sleep-analytics/`
    - **Method:** GET
    - **Description:** Performs analytics on sleep data for all persons,
      including average sleep score, sentiment analysis of sleep comments, and
      environmental data analysis.

9. **Sleep Analytics for a Specific Person**
    - **Endpoint:** `/sleep-analytics/person/<int:person_id>/`
    - **Endpoint:** `/person/<int:person_id>/sleep-analytics/`
    - **Method:** GET
    - **Description:** Performs analytics on sleep data for a specific person,
      including average sleep score, sentiment analysis of sleep comments, and
      environmental data analysis.
