# Web Scraping Homework - Mission to Mars

In this assignment, I built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.
In this assignment, I built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. Used Jupyter Notebook, BeautifulSoup, Pandas, and Requests/SplinterThe to complete the assignment. Following outlines more details of the assignement:
1) From NASA's Mars News webpage (https://mars.nasa.gov/news/), used BeautifulSoup to collect the latest News Title and Paragragh Text. 
2) Used Splinter to navigate NASA's webpage of Mars images (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars). Collected the URL for the current featured Mars Image from the site.
3) Used Pandas to scrape a table from https://space-facts.com/mars/ that contains facts about the planet Mars. Once the table was collected, use Pandas to convert the data to a HTML table string.
4) Collected high resolution images for each of Mar's hemispheres from https://space-facts.com/mars/. 
5) Created a NoSQL database in MongoDB with a Flask application to create a new HTML page with the scraped data and images from above.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

Give examples

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

Give the example
And repeat

until finished
End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

Give an example

### And coding style tests

Explain what these tests test and why

Give an example

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

Dropwizard - The web framework used
Maven - Dependency Management
ROME - Used to generate RSS Feeds

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use SemVer for versioning. For the versions available, see the tags on this repository.

## Authors

Billie Thompson - Initial work - PurpleBooth
See also the list of contributors who participated in this project.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Hat tip to anyone whose code was used
Inspiration
etc
