# sleep-well

## Team members

1. Nantawat Sukrisunt 6510545543
2. Naytitorn Chaovirachot 6510545560

All team members are affiliated with the Department of Engineering, Faculty of Software and
Knowledge Engineering, and are students at Kasetsart University.

## Overview

Sleep-Well is a RESTful API web service designed to offer sleep quality data to
users. The API will provide endpoints for accessing sleep information,
including sleep duration, quality scores, environmental factors (such as
weather and noise levels), and personal information about the individual's
sleep patterns. Additionally, the API will include analytics features to
analyze sleep comments and provide insights into sleep quality trends.

## Install instructions

Please configure the `sample.env` file before proceeding with the installation. Refer to the
detailed configuration guide in [configurations.md](installation%2Fconfigurations.md).

For a quick and efficient setup, it is recommended to use the provided script. Find instructions
in [script.md](installation%2Fscript.md).

If you prefer a manual setup, follow the steps outlined in [manual.md](installation%2Fmanual.md).

## How to run

1. To run the local server

   ```
   python manage.py runserver
   ```

2. To access the app at http://localhost:8000

3. To deactivate the virtual environment

   ```
   deactivate
   ```

## Project documentation

### Documents

* [Testing plan](https://github.com/Nantawat6510545543/sleep-well/wiki/Testing-plan)
* [Data Acquisition and Integration Presentation Slide]()
* [Software Testing Presentation Slide]()
* [Data Analytics Presentation Slide]()

### Application Architecture

* [Class Diagram](https://github.com/Nantawat6510545543/sleep-well/wiki/Class-Diagram)

* [Sequence Diagram](https://github.com/Nantawat6510545543/sleep-well/wiki/Sequence-Diagram)

* [Domain Model](https://github.com/Nantawat6510545543/sleep-well/wiki/Domain-Model)

* [Use Case Diagram](https://github.com/Nantawat6510545543/sleep-well/wiki/Use-Case-Diagram)

## Endpoints

1. **List Sleep Information**
    - **Endpoint:** `/info/sleep/`
    - **Method:** GET
    - **Description:** Retrieves a list of all sleep entries with associated
      weather and noise data. 
      
      The date can be specified using query parameters `day`, `month`, or `year`.

      For example, `/info/sleep?day=10&month=5?year=2024` would retrieve sleep entries for May 10, 2024.
      And `/info/sleep?month=5` would retrieve sleep entries for the month of May.

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

4. **Sleep Information by Location Within Range**
    - **Endpoint:** `Endpoint: /info/sleep/<float:lat>-<float:lon>`
    - **Endpoint:** `Endpoint: /info/sleep/<float:lat>-<float:lon>/range/<int:km>`
    - **Method:** GET
    - **Description:** Retrieves sleep entries within a specified range (in kilometers) from a given
      location identified by latitude and longitude coordinates. If no specific range is provided,
      the default range of 5 kilometers is used to filter sleep entries within this distance from
      the specified location.

5. **List Person Information**
    - **Endpoint:** `/info/person/`
    - **Method:** GET
    - **Description:** Retrieves a list of all persons with their information.

6. **Get Person Information by ID**
    - **Endpoint:** `/info/person/<int:person_id>/`
    - **Method:** GET
    - **Description:** Retrieves person information based on the provided
      person ID.

7. **Sleep Analytics for All Persons**
    - **Endpoint:** `/info/sleep-analytics/`
    - **Method:** GET
    - **Description:** Performs analytics on sleep data for all persons,
      including average sleep score, sentiment analysis of sleep comments, and
      environmental data analysis.

8. **Sleep Analytics for a Specific Person**
    - **Endpoint:** `/info/sleep-analytics/person/<int:person_id>/`
    - **Endpoint:** `/info/person/<int:person_id>/sleep-analytics/`
    - **Method:** GET
    - **Description:** Performs analytics on sleep data for a specific person,
      including average sleep score, sentiment analysis of sleep comments, and
      environmental data analysis.
