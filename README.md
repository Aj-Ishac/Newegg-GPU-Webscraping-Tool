# Newegg-GPU-Webscraping-Tool

Python based tool designed to retrieve Graphic Card product information from Newegg based on user-input.
Extracted data will be later fed to the Data-Processing-And-Lookup-Tool-v2 to analyze and streamline decision making on the user's part.

The program will be responsible for the following processes:
  1. Extract title, price, and link of all products found from the website filtered by user-input.
  2. Output all extracted data into a CSV file to be handled by the Data-Processing-And-Lookup-Tool-v2.
  3. Email notification when price is within range of the user's choice.
  4. Seamless communication between the Newegg-GPU-Webscraping-Tool and Data-Processing-And-Lookup-Tool-v2

The following is a step by step process on how to configure the tool for the user's use:

**Prerequisites:**

Run the following in Command Prompt as Admin
```
pip install beautifulsoup4
```
```
pip install requests
```
![my_image](/Newegg-GPU-Webscraping-Tool/Assets/pipinstalls.png)
