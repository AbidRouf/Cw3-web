# Friends and Hobbies
## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Download this repo as a zip.

3. Install Pyhton dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

4. Create a development database:

    ```console
    $ python manage.py migrate
    ```

5. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

7. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run build-windows
    ```

8. Open your browser and go to http://localhost:5173, you will be greeted with the home page.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).


List Of Members:
-Humayun Amin (ec22454)
-Irfan Idriss Budaly (ec22599)
-Abidur Rouf (ec22926)
-Mohamed Abdulrazaq Alsowmely (ec22451)

Mohamed Abdulrazaq Alsowmely - Frontend Functionality most specifically working on components,also aided with testing and deployment.
Abidur Rouf - Worked on Frontend Templates and functionalites with Frontend and Backend.
Irfan Idriss Budaly - Connected both Frontend and Backend functionalities and worked on testing and deployment and helped backend functionalities as well as components
Humayun Amin - Backend Functionality Working on models, views and urls
