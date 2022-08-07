# DevClub Assignment 5

Introducing a Learning Management system, a platform where both instructors and students login, and for each course, the instructor uses the platform to share resources, release grades, conduct assignments and what not!

Deployed at: https://devclublms-vatsal.herokuapp.com/

## Features
### User Authentication
![Screenshot (140)](https://user-images.githubusercontent.com/97669734/183305332-db7a3b8b-965c-4f28-a874-d4b319495669.png)
![Screenshot (141)](https://user-images.githubusercontent.com/97669734/183305348-942a72ca-9137-45ca-8d6f-bb52d2e05ce6.png)

### Dashboard and Course Pages
![Screenshot (142)](https://user-images.githubusercontent.com/97669734/183305192-9741dac4-ce3d-418f-9d8f-b2f1db546f39.png)
![Screenshot (143)](https://user-images.githubusercontent.com/97669734/183305286-a356459b-cf1d-4d45-9938-f9b3ab25adaa.png)
![Screenshot (144)](https://user-images.githubusercontent.com/97669734/183305295-cbe92b00-cabf-491e-9e6e-9f6e6be6b673.png)

### Instructors can upload material such as files and links
![Screenshot (145)](https://user-images.githubusercontent.com/97669734/183305579-0f192f84-fd13-4c36-bb84-4ff434b465dc.png)

### Assignments
#### Instructor's view
![Screenshot (147)](https://user-images.githubusercontent.com/97669734/183305625-ae14a5c3-85bf-4927-a79b-0350f2f90a7b.png)
![Screenshot (148)](https://user-images.githubusercontent.com/97669734/183305636-110fc28b-9b34-4f2a-b30d-af71652dcf20.png)
![Screenshot (153)](https://user-images.githubusercontent.com/97669734/183305969-4f7e5a07-c26c-4fd8-9503-d9dc1406062e.png)

#### Student's view
![Screenshot (149)](https://user-images.githubusercontent.com/97669734/183305718-761435df-a39e-4c9b-a7e4-8872907d362c.png)

### Grades
![Screenshot (150)](https://user-images.githubusercontent.com/97669734/183305790-95926c21-7a7a-4328-8ba8-4b3684625ea6.png)

### Profile
![Screenshot (151)](https://user-images.githubusercontent.com/97669734/183305843-f3244850-2196-49c3-803c-5fd0aadf7898.png)
![Screenshot (152)](https://user-images.githubusercontent.com/97669734/183305849-9a6bc732-15ad-4f60-8cd5-1b56c7be048e.png)



## Original DevClub Assignment Statement

You have learnt about backend engineering with Django in our session. Now use it to create a web application by yourself!
## DevClub LMS (Learning Management System)
You must have used **Moodle** in your courses, where both instructors and students login, and for each course, the instructor uses the platform to share resources, send announcements, release grades, conduct quizzes and what not!

Your task is to create your own such a learning management system using Django, where you can add functionalities as per your own creativity!

### We would recommend you to have these apps inside the project: 
- Users (to store auth logic, and models for `Instructor`, `Student`, `Course`, `Admin`)
- Grades (to store logic for sharing grades for any assessment, and models for let's say a class `Grade`)
- Documents (for Instructor to upload `Docs` like lecture notes for the course)
- Quizzes (this can have models for a `QuestionBank` containing `Question`'s which form a `Quiz`)
- Communication (to work on features like Course-wide `Announcements`, `Reply`ing in threads to announcements, sending personal `Messages`)

Try to implement as many features as you can, but make sure to plan the structure of the project and database schemas well!

### Bonus:
- Deploy on Heroku
- Create documentation for any RESTful APIs created with documenter on postman
- Markdown support for Communication
- Email: For registration, password reset, notifications, instructor custom message
- Bulk upload from CSV for grades, quizzes
- Generating PDF: Print digitally signed transcript
- Add security features for the quizzes

## Submission Instructions
- **FORK** this repository, by clicking the "Fork" button on top right
- `clone` the forked repo into your machine, and `cd` into the Repo Folder such that you are in same directory level as `manage.py`
- If on macOS, run `python3 -m venv env`, otherwise `python -m venv env`
- Now activate the virtual environment by `source env/bin/activate`
- See if the environment is correctly set by running `pip list`, it should be mostly empty
- Install dependencies with `pip install -r requirements.txt`
- We have already started a dummy project called `DevClubLMS` for you
- Now, you can use `python manage.py runserver` to start the dev server or `python manage.py startapp <appname>` to create a new app inside this project
- After completing the assignment, append instructions to run your project, along with explanation of features etc in this README
- It would be nice if you can host it on Heroku and also give a documentation of each endpoint through postman
- Finally submit with your details in the [Google Form](https://forms.gle/XSidrfbrsEZuDYfy6)
- You do NOT need to make any pull requests to this repo

# Resources
- [Slides used in the session](https://docs.google.com/presentation/d/e/2PACX-1vQbtDDGQonkIoGu68VrINL2s3sQcfiH5XVnk-iU26nk16DFBGsDabichsqhdtBvowPvpxaIbFLAV2h3/pub?slide=id.p)
- Introduction to Python and Django by [Programming With Mosh](https://youtu.be/_uQrJ0TkZlc)
- Detailed Django Tutorials by [Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
- [Mozilla's Tutorials](https://developer.mozilla.org/en-US/docs/Learn/Server-side) on Server Side Programming with Django
- [Django Official Docs](https://www.djangoproject.com/start/)
- [Talk](https://youtu.be/lx5WQjXLlq8) on how Instagram uses Django at production, and also [*the time when Justin Beiber almost crashed Instagram!*](https://youtu.be/lx5WQjXLlq8?t=715)
- Advice on Backend Engineering by [Hussein Nasser](https://www.youtube.com/c/HusseinNasser-software-engineering)
- Guide for Deploying Python apps on [Heroku](https://devcenter.heroku.com/categories/python-support)
- Guide for [Postman Documenter](https://learning.postman.com/docs/publishing-your-api/documenting-your-api/)
