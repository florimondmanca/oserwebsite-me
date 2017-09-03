oserwebsite
===
Specifications
----

This document aims at presenting the objectives and functional requirements of the OSER website project.

## Needs

The current website that OSER owns is still under the scheme of CEC. The need to revamp the website to better fit the new OSER visual identity is urgent. Moreover, the old CEC website has a number of problems :

- The stake holders (high school students, association members, parents and teachers) mostly don't use it because it is non-ergonomical, complicated and bugsome.
- Several key functionalities are broken: ability to visualise a tutoring meetings calendar, registering new users.
- The website was developed using PHP/Symfony2, a framework which requires time to learn and is unknown of basically every member of OSER, even the geekiest.

## Objectives

The goal of this project is thus to actualize the association's website so that :
- it matches its new visual identity;
- it provides a meaningful set of functionalities;
- it is easy to use (for end users);
- it is easy to maintain (for developers).
- the association's stake holders actually use it.

## Key audiences

The stake holders and key audiences for the website are :

- The high school students who signed up to the OSER programme : once signed up, they need to be able to follow and be notified of the upcoming tutoring events (meetings, visits, projects, CS events, ...), get access to educational content, etc.
- The association members (tutors) : once signed up, they need to be able to manage existing tutoring events, post new content and schedule new events.
- The parents of the students : once signed up, they need to be able to monitor their child's engagement in the programme (presence reports, participation to visits or projects).
- The teachers of the partner high schools : once signed up, they need to be able to monitor the high school's OSER students engagement (presence reports, statistics, participation to visits or projects) and to communicate with the association key members.

## Provisional site structure

You can visualize the website site map using the `sitemap` folder, which consists of empty folders organized to resemble the website's map. Check it out with:

```sh
$ tree sitemap
```

As of September 3rd, 2017:

```
sitemap
├── logged_in
│   ├── 1-dashboard
│   ├── 2-tutoring
│   │   ├── 1-mytutoringgroup
│   │   └── 2-myhighschool
│   ├── 3-faq
│   ├── 4-database__tutors
│   │   ├── 1-highschool_list
│   │   └── 2-tutoringgroup_list
│   └── 5-profile
└── visitor
    └── 1-authenticate
```

## Technical specifications

Below are the use cases that describe the functional requirements of the website.

### Use case 1: User logs in

*Prerequisites*

- The user not logged in.

*Main flow*

1. The user accesses login page.
2. The user is prompted with login details (email and password).
3. The user enters login details and submits them.
4. The system requires the user's login details from the database.
5. The system validates that entered details match those from the database.
6. System displays the dashboard.

*Alternative flow 4a: incorrect login details*

1. System tells user login has failed.
2. Return the main flow step 2.

*Outputs*

- User has logged in.

### Use case 2: User registers

*Prerequisites*

- The user not logged in.

*Main flow*

1. User accesses to the login page.
2. User does not have an account, they click on a "register" link and are taken to the register page.
3. User enters register details (first name, last name, email, password, role), submits them.
5. Based on role, user is taken to complementary register page.
6. User enters complementary register information and submits them.
7. System creates new user account and associated profile.
8. User is notified that account has been created.
9. User is taken to login page to login with new account.

*Alternative flow 3a: email already used*

1. System tells user email already used.
2. Return to main flow step 3.

*Outputs*

- System has created user account and profile.
- User receives email with user account info (email).

### Use case 3: User looks for upcoming meetings

*Prerequisites*

- User logged in as student or tutor.

*Main flow*

1. User accesses to dashboard.
2. User sees list of nearest upcoming meetings, if any.

*Outputs*

N/A

### Use case 4: User looks for all upcoming meetings

*Prerequisites*

- User logged in as student or tutor.

*Main flow*

1. User accesses to dashboard.
2. User clicks on link to see all upcoming meetings.
3. User is taken to a page listing all upcoming meetings, if any.

### Use case 5: User looks for upcoming visits

*Prerequisites*

- User logged in as student or tutor.

*Main flow*

1. User accesses to dashboard.
2. User sees list of nearest upcoming visits, if any.

*Outputs*

N/A

### Use case 5: User looks for all upcoming visits

*Prerequisites*

- User logged in as student or tutor.

*Main flow*

1. User accesses to dashboard.
2. User clicks on link to see all upcoming visits.
3. User is taken to a page listing all upcoming visits, if any.

*Outputs*

N/A

### Use case 6: User looks for visit details

*Prerequisites*

- User logged in as student or tutor.

*Main flow*

1. User accesses to dashboard.
2. User clicks on details button for visit of interest.
3. User is taken to visit details page showing: title, place, date, meeting time, estimated end time, remaining seats, description.

*Alternative flow 2a: visit not on dashboard list*

1. User clicks on link to see all visits.
2. Return to main flow step 2.

*Outputs*

N/A

### Use case 7: User signs up for visit

*Prerequisites*

- User logged in as student.

*Main flow*

1. User accesses to details for visit of interest [UC6].
2. User clicks on subscribe/participate button.
3. System adds user to list of subscribed users for this visit.
4. User is notified they have subscribed to the visit.

*Outputs*

- User is subscribed to visit of interest.
- User receives email with visit detail info.

### Use case 8: User looks for subscribed visits

*Prerequisites*

- User logged in as student.

*Main flow*

1. User accesses to visit list [UC5].
2. User sees visual clue for visits where they have subscribed.

*Outputs*

N/A

### Use case 9: User unsubscribes from visit

*Prerequisites*

- User logged in as student.
- User is subscribed to visit of interest.

*Main flow*

1. User accesses to visit list [UC5].
2. User clicks on visit of interest unsubscribe button.
3. Pop-up asks user if they are sure to want to unsubscribe.
4. User answers they are sure.
5. System removes user from list of subscribed user for this visit.
6. User is taken to visit list page and is notified they have unsubscribed from this visit.

*Alternative flow 4a: user answers not sure*

1. Pop-up disappears.
2. Return to main flow step 1.

*Outputs*

- User is not subscribed to visit of interest anymore.
