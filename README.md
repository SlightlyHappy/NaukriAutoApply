## Naukri Job Application Automation

This Python script automates the process of searching and applying for jobs on Naukri.com, specifically targeting roles with salary filters and remote work preference - you can change the filters and roles to your preference by inspecting the elements and adding them under the filters and by changing the search terms. 
I'm applying to remote HR positions so that's the current set up, but please feel free to mess around with the file.  

### Features

* Automated Search: Searches Naukri.com for "Human Resource Analyst" jobs
* Filtering: Applies filters for remote work and salary range (3-6 Lakhs & 6-10 Lakhs)
* Job Application: Automatically clicks on job postings and attempts to apply

### Prerequisites

* Python 3.x: Make sure you have Python installed on your system.
* Selenium: Install the Selenium library using `pip install selenium`
* WebDriver: Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Chrome) and place it in your system's PATH.
* credentials.txt: Create a file named `credentials.txt` in the same directory as your script with the following format:


username = 'your_naukri_username'
password = 'your_naukri_password'

### Important Notes

* WebDriver Compatibility: Ensure the WebDriver version matches your browser version.
* Website Changes: The script relies on specific HTML elements on Naukri.com. If the website structure changes, the script may need adjustments.
* Application Process: The script currently clicks the "Apply" button but may require additional logic to handle specific application forms.
* Ethical Use: Use this script responsibly and respect Naukri.com's terms of service. Avoid overloading their servers with excessive requests.

### Disclaimer

This script is provided for educational purposes only. The author is not responsible for any misuse or consequences arising from its use.

### License

This project is licensed under the MIT License.
