import random
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_google_drive_links(url):
    print("Starting the web scraping process...")
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    try:
        # Use WebDriverWait to wait for all <a> elements to be present
        wait = WebDriverWait(driver, 40)
        links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

        # Extract and return Google Drive links
        drive_links = [link.get_attribute('href') for link in links if link.get_attribute('href') and 'drive.google.com' in link.get_attribute('href')]
        print(f"Found {len(drive_links)} Google Drive links.")
        return drive_links

    except TimeoutException:
        print("Timeout occurred waiting for elements to load")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure WebDriver is properly closed
        driver.quit()

def send_email(receiver_emails, subject, body):
    print("Preparing to send email...")
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'oliverbsimmons01@gmail.com'
    password = 'tgzn kqun gxyh ocfb'  # Make sure to replace with your app-specific password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(receiver_emails)
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_emails, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    
    finally:
        server.quit()

def main():
    print("Starting main function...")
    url = 'https://www.reddit.com/r/Drumkits/'
    drive_links = scrape_google_drive_links(url)

    if drive_links:
        random_url = random.choice(drive_links)
        receiver_emails = ['oliverbsimmons01@gmail.com', 'neowagner303@outlook.com'] 
        subject = 'Weekly Random Google Drive Link'
        body = f"Here's your mystery kit of the week:\n\n{random_url}"

        send_email(receiver_emails, subject, body)
    else:
        print("No Google Drive links found.")

schedule.every().week.do(main)

if __name__ == "__main__":
    print("Starting the scheduling process...")
    while True:
        schedule.run_pending()
        time.sleep(1)
