import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Extract Ranks
def extractBAPSRankings(university_name):
    # Standing Links
    link = "https://bapsoj.org/contests/icpc-preliminary-dhaka-site-2024/standings"

    # Initialize the WebDriver
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5)  # wait time for the dynamic content

    # Initialize list for scraped data
    data = []

    # Loop until there are no more pages
    while True:
        # Get the rendered HTML content
        rendered_html = driver.page_source
        soup = BeautifulSoup(rendered_html, 'html.parser')

        # Find the table and rows
        table = soup.find('table', {'class': 'MuiTable-root css-1owb465'})
        rows = table.find('tbody').find_all('tr')

        # Extract data from each row
        for row in rows:
            cells = row.find_all('td')
            
            # Extract original columns
            university_rank = cells[0].get_text(strip=True)
            team_name = cells[1].get_text(strip=True)
            icpc_rank, penalty = cells[2].get_text(strip=True).split('(')
            solve = cells[3].get_text(strip=True)
            
            # Filter for teams that contain the university name
            if university_name in team_name:
                # Remove university name from `team_name` and clean up data
                team_name = team_name.replace(university_name, "").strip()
                icpc_rank = icpc_rank.strip()  # ICPC Rank
                penalty = penalty.replace(")", "").strip()  # Penalty
                solve = solve.replace("✓", "").strip()  # Remove any checkmarks if present
                
                # Append cleaned data
                data.append([university_rank, icpc_rank, solve, penalty, team_name])

        # Try to find the "Next" button and click it
        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
            if next_button.is_enabled():
                next_button.click()
                time.sleep(3)  # Wait for the next page to load
            else:
                break  # Exit loop if "Next" button is disabled
        except NoSuchElementException:
            break  # Exit loop if there is no "Next" button

    # Close the browser
    driver.quit()

    # Reformat data for the final output
    formatted_data = []
    for index, row in enumerate(data, start=1):
        # Add sequential University Rank and reformat the row
        university_sequential_rank = index
        icpc_rank = row[1]
        solve = row[2] or 0  # If solve is empty, use 0
        penalty = row[3] or ""  # Use empty if penalty is missing
        team_name = row[4]
        formatted_data.append([university_sequential_rank, row[0], icpc_rank, penalty, team_name])

    # Convert data to DataFrame
    df = pd.DataFrame(formatted_data, columns=["University Rank", "ICPC Rank", "Solve", "Penalty", "Team"])

    # Save to CSV
    df.to_csv("university_team_standings.csv", index=False)
    print("Data saved to university_team_standings.csv")
    
# Example call
extractBAPSRankings(university_name="NORTH SOUTH UNIVERSITY")
