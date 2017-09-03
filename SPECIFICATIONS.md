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

## Functional requirements

See use_cases.pdf for use cases that describe the functional requirements of the website. Also available online on [Overleaf](https://www.overleaf.com/10878278kxcmdgfrnrmz).
