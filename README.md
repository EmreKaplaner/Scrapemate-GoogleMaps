# Scrapemate-GoogleMaps

A comprehensive data scraping tool designed to extract information from Google Maps search results. It is developed using the Go programming language and integrates several libraries and frameworks to facilitate efficient data retrieval and processing.

The core functionality of the project revolves around scraping Google Maps search results based on user-defined queries. The program accepts input queries either from a local file or from standard input (stdin), allowing for flexible usage. Users can specify various parameters, such as concurrency level, maximum scrolling depth, language code, and debug mode, to tailor the scraping process according to their requirements.

The program utilizes the Playwright library for web automation, enabling it to simulate user interactions with the Google Maps interface to retrieve search results. It employs concurrency to enhance performance, allowing multiple scraping tasks to execute concurrently for faster data extraction.

Additionally, the project supports output customization, offering options to save scraped data either as CSV or JSON files. Users can specify the output destination, choosing between standard output (stdout) or local files. Moreover, for users requiring database integration, the program supports connection to PostgreSQL databases, facilitating seamless data storage and management.

