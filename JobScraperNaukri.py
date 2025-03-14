import asyncio
import csv
from crawl4ai import CrawlerHub
from playwright.async_api import async_playwright
import time

async def main():
    # Get job search query from user
    job_search = input("Enter job skills/designations/companies to search for: ")
    max_pages = int(input("Enter the maximum number of pages to scrape (default: 3): ") or "3")
    
    # Initialize crawler
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True for production
        page = await browser.new_page()
        
        # Navigate to Naukri.com
        print("Navigating to Naukri.com...")
        await page.goto("https://www.naukri.com/")
        
        # Wait for the search input field to be visible
        print("Entering search query...")
        await page.wait_for_selector('input.suggestor-input')
        
        # Clear the field and enter the search query
        search_input = await page.query_selector('input.suggestor-input')
        await search_input.click()
        await search_input.fill(job_search)
        
        # Click the search button
        print("Performing search...")
        await page.click('div.qsbSubmit')
        
        # Wait for search results page to load
        await page.wait_for_load_state('networkidle')
        
        # Click on Remote filter
        print("Applying Remote filter...")
        try:
            remote_filter = await page.wait_for_selector('span.styles_ellipsis__cvWP1.styles_filterLabel__jRP04[title="Remote"]', timeout=5000)
            await remote_filter.click()
        except Exception as e:
            print(f"Remote filter not found or not clickable: {e}")
        
        # Wait for page to update
        await page.wait_for_load_state('networkidle')
        
        # Click on Hybrid filter
        print("Applying Hybrid filter...")
        try:
            hybrid_filter = await page.wait_for_selector('span.styles_ellipsis__cvWP1.styles_filterLabel__jRP04[title="Hybrid"]', timeout=5000)
            await hybrid_filter.click()
        except Exception as e:
            print(f"Hybrid filter not found or not clickable: {e}")
        
        # Wait for page to update
        await page.wait_for_load_state('networkidle')
        
        # Click on Delhi/NCR filter
        print("Applying Delhi/NCR filter...")
        try:
            delhi_filter = await page.wait_for_selector('span.styles_ellipsis__cvWP1.styles_filterLabel__jRP04[title="Delhi / NCR"]', timeout=5000)
            await delhi_filter.click()
        except Exception as e:
            print(f"Delhi/NCR filter not found or not clickable: {e}")
        
        # Wait for page to update with all filters applied
        await page.wait_for_load_state('networkidle')
        print("Waiting for results to load...")
        time.sleep(3)  # Additional wait to ensure all results are loaded
        
        # Initialize list to store all job listings
        all_job_listings = []
        current_page = 1
        
        # Loop through pages
        while current_page <= max_pages:
            print(f"Scraping page {current_page}...")
            
            # Extract job listings from current page
            job_listings = await extract_job_listings(page)
            all_job_listings.extend(job_listings)
            print(f"Found {len(job_listings)} jobs on page {current_page}")
            
            # Check if we've reached the maximum pages
            if current_page >= max_pages:
                break
                
            # Find and click the Next button
            try:
                # Look for the Next button in the pagination section
                next_button = await page.query_selector('a.styles_btn-secondary__2AsIP:not(.styles_previous__PobAs)')
                
                if next_button:
                    print(f"Clicking Next button to navigate to page {current_page + 1}")
                    await next_button.click()
                    await page.wait_for_load_state('networkidle')
                    await page.wait_for_selector('.srp-jobtuple-wrapper', timeout=10000)
                    time.sleep(3)  # Wait for the page to fully load
                    current_page += 1
                else:
                    # Alternative: Try to find the specific page number link
                    next_page_link = await page.query_selector(f'a[href="/jobs-in-india-{current_page + 1}"]')
                    if next_page_link:
                        print(f"Clicking page {current_page + 1} link")
                        await next_page_link.click()
                        await page.wait_for_load_state('networkidle')
                        await page.wait_for_selector('.srp-jobtuple-wrapper', timeout=10000)
                        time.sleep(3)
                        current_page += 1
                    else:
                        # If both methods fail, try direct URL navigation
                        next_url = f"https://www.naukri.com/jobs-in-india-{current_page + 1}"
                        print(f"Navigating directly to {next_url}")
                        await page.goto(next_url)
                        await page.wait_for_load_state('networkidle')
                        await page.wait_for_selector('.srp-jobtuple-wrapper', timeout=10000)
                        time.sleep(3)
                        current_page += 1
            except Exception as e:
                print(f"Error navigating to next page: {e}")
                break
        
        # Save all results to CSV
        csv_filename = f"naukri_jobs_{job_search.replace(' ', '_')}.csv"
        print(f"Saving {len(all_job_listings)} job listings to {csv_filename}...")
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['job_title', 'company_name', 'job_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for job in all_job_listings:
                writer.writerow(job)
        
        print(f"Job search completed. Results saved to {csv_filename}")
        await browser.close()

async def extract_job_listings(page):
    job_listings = []
    
    # Find all job tuples
    job_tuples = await page.query_selector_all('div.srp-jobtuple-wrapper')
    
    for job_tuple in job_tuples:
        try:
            # Extract job title and link
            title_element = await job_tuple.query_selector('a.title')
            job_title = await title_element.get_attribute('title')
            job_url = await title_element.get_attribute('href')
            
            # Extract company name
            company_element = await job_tuple.query_selector('a.comp-name')
            company_name = await company_element.get_attribute('title')
            
            job_listings.append({
                'job_title': job_title,
                'company_name': company_name,
                'job_url': job_url
            })
        except Exception as e:
            print(f"Error extracting job details: {e}")
    
    return job_listings

if __name__ == "__main__":
    asyncio.run(main())
