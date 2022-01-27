# Newegg-GPU-Webscraping-Tool

Python based tool designed to retrieve Graphic Card product information from Newegg based on user-input.
Extracted data will be later fed to the Data-Processing-And-Lookup-Tool-v2 to analyze and streamline decision making on the user's part.

The program will be responsible for the following processes:
  1. Extract title, price, and link of all products found from the website filtered by user-input.
  2. Output all extracted data into a CSV file to be handled by the Data-Processing-And-Lookup-Tool-v2.
  3. Email notification when price is within range of the user's choice.
  4. Seamless communication between the Newegg-GPU-Webscraping-Tool and Data-Processing-And-Lookup-Tool-v2

## The following is a step by step process on how to configure the tool for the user's use:

**Install current version of Python**
```
https://www.youtube.com/watch?v=xXEt9dyvq3U
```
**Run the following in Command Prompt as Admin**
```
python --version
```
![my_image](Assets/pythonconfirmation.png)

```
pip install beautifulsoup4
```
```
pip install requests
```
![my_image](Assets/pipinstalls.png)

**File dependencies are:**  
- Newegg-GPU-Webscraping-Tool/scrappy.py  
- Newegg-GPU-Webscraping-Tool/config.py  

Scrappy.py is the main file, config.py stores user-preferences.  
On file compile, user will be prompted to input key-term to search for the Graphic Card with.  
Tool may only search for one input at a time, however multiple instances of the tool can be open at the same time.  
`examples of user input: 1080, 2080, 3070, 3080, 3090, etc`  
