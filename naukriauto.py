from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()

            if len(lines) < 2:
                raise ValueError("Credentials file must contain at least two lines (username and password).")

            # Extract username and password using string splitting
            username_line = lines[0].strip()
            password_line = lines[1].strip()

            if not username_line.startswith("username = '") or not password_line.startswith("password = '"):
                raise ValueError("Invalid format in credentials file. Lines should start with 'username = ' and 'password = '")

            username = username_line.split("'")[1]  # Extract the value between single quotes
            password = password_line.split("'")[1]

            if not username or not password:
                raise ValueError("Username or password cannot be empty.")

            return username, password

    except FileNotFoundError:
        print("Error: 'credentials.txt' file not found. Please create it with your username and password.")
        exit(1) 

    except ValueError as e:
        print(f"Error reading credentials: {e}")
        exit(1) 

def main():
    website_url = "https://www.naukri.com/nlogin/login?utm_source=google&utm_medium=cpc&utm_campaign=Brand&gad_source=1&gclid=EAIaIQobChMIpICfmar5hwMVTKRmAh2Y3wbZEAAYASAAEgKXK_D_BwE&gclsrc=aw.ds"

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # 1. Go to Google and search for "Human Resources Naukri"
        driver.get("https://www.google.com")

        # Wait for the search bar to be present and interactable
        google_search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )

        # Enter the search query and press Enter
        google_search_bar.send_keys("Human Resources Naukri all India")
        google_search_bar.send_keys(Keys.RETURN)

        # 2. Click on the first link in the search results
        first_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.tF2Cxc a h3"))
        )
        first_link.click()

        # 3. Wait for the Naukri page to load and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login_Layer"))
        )
        login_button.click()

        # 4. Get username and password from read_credentials()
        username, password = read_credentials()

        # 5. Enter username and password, then press Enter
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Enter your active Email ID / Username']"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password'][placeholder='Enter your password']"))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # 6. Locate the search bar button by its class name and click it
        search_bar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "nI-gNb-sb__icon-wrapper"))
        )
        search_bar_button.click()

        # 7. Wait for the search INPUT field to be present and interactable
        search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.nI-gNb-sb__keywords input.suggestor-input"))
        )

        # 8. Enter the search term and press Enter
        search_term = "recruitment" 
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

        # 9. Click the filter elements
        try:
            filters = [
                ("Remote", "span.styles_filterLabel__jRP04[title='Remote']"),
                ("3-6 Lakhs", "span.styles_filterLabel__jRP04[title='3-6 Lakhs']"),
                ("6-10 Lakhs", "span.styles_filterLabel__jRP04[title='6-10 Lakhs']")
            ]

            for filter_name, filter_selector in filters:
                filter_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, filter_selector))
                )
                filter_element.click()
                print(f"Clicked filter: {filter_name}")
                time.sleep(2)

        except Exception as e:
            print(f"Error clicking filter elements: {e}")

        # 10. Click on job postings and navigate through pages
        while True:
            try:
                # Wait for job postings to load (updated locator based on your provided HTML)
                job_postings = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.styles_job-listing-container__OCfZC div.cust-job-tuple a.title")) 
                )

                # Click on each job posting on the current page
                for job_posting in job_postings:
                    job_posting.click()

                    # Switch to the new tab/window where the job posting opened
                    driver.switch_to.window(driver.window_handles[-1])

                    try:
                        # Wait for the "Apply" button to be clickable and click it
                        apply_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "apply-button"))
                        )
                        apply_button.click()

                        # You might want to add a delay here or additional logic to handle the application process if needed
                        # time.sleep(2) 
                        # ... (code to fill out the application form if applicable) ...

                    except Exception as e:
                        print(f"Error clicking Apply button or handling application process: {e}")

                    finally:
                        # Close the current tab/window (the job posting page)
                        driver.close()

                        # Switch back to the original tab/window (the search results page)
                        driver.switch_to.window(driver.window_handles[0])

                # Go to the next page by clicking the "Next" button
                try:
                    next_page_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.styles_btn-secondary__2AsIP:not(.styles_previous__PobAs)"))
                    )
                    next_page_button.click()

                except TimeoutException:
                    print("Reached the last page. Exiting.")
                    break

            except Exception as e:
                print(f"Error processing page: {e}")
                break

    finally:
        time.sleep(600)  
        driver.quit()

if __name__ == "__main__":
    main()