# How the Retail Purchase Intelligence System Works

Welcome to the **Retail Purchase Intelligence System**! This document explains how this web application works in simple terms, the step-by-step flow when you use it, and the technologies powering it behind the scenes.

## What is it?
This app is a smart search engine for shoppers. Instead of opening multiple tabs to check prices on Amazon, Flipkart, and Shopclues separately, you just type what you want here. The app reaches out to all three stores at once, grabs the top results, and displays them side-by-side so you can quickly find the best deal.

---

## 🌊 Flow of Work (How it works step-by-step)

Here is exactly what happens when you type a product name into the search bar and hit "Compare":

### 1. You Make a Request (The Frontend)
When you type a search term (like *"iPhone 15"*) and click the search button, your browser sends that keyword securely to our application's "brain" (the Backend server).

### 2. The Brain Takes Over (The Backend)
Our backend server receives your keyword and immediately prepares to go shopping on your behalf. It constructs specific web addresses (URLs) to search for your item on three different websites:
- **Flipkart**
- **Amazon**
- **Shopclues**

### 3. Bypassing the Guards (ScraperAPI)
Big websites like Amazon and Flipkart don't like automated robots visiting their sites, so they often block them. To get around this, we send our search requests through a service called **ScraperAPI**. Think of ScraperAPI as a master of disguise—it routes our request through millions of different regular user IP addresses so the stores just think we are a normal person browsing the web.

### 4. Reading the Code (BeautifulSoup Scraping)
Once ScraperAPI successfully loads the search results page from the stores, it hands the raw, messy Website Code (HTML) back to our app. 
- We use a tool called **BeautifulSoup** to read this messy code.
- We give it specific instructions: *"Find the product image, find the product title, find the price, and find the link to buy it."*
- We do this exact process for Amazon, Flipkart, and Shopclues.

### 5. Cleaning and Sorting the Data
Now we have raw data from all three stores. We clean it up:
- We remove the ₹ symbols and commas from the prices.
- We filter out any items that don't have a valid price or name.
- We take all the valid products we found across all three sites, combine them into one giant pool, and **sort them by price (from lowest to highest)**.

### 6. Displaying the Results (Back to the Frontend)
Finally, we send that sorted, clean list of products back to your browser. The website transforms this list into beautiful, easy-to-read "Product Cards" featuring the store's logo, the product name, and the price. You can click on the name to jump straight to the store and buy the product!

---

## 🛠️ Technologies Used

Here are the tools and languages we used to build this system:

- **Python**: The core programming language that runs the entire backend logic and data processing.
- **Django**: A powerful Python website framework. It acts as the skeleton of our app, handling URLs, databases, user logins, and rendering web pages.
- **HTML, CSS, & Bootstrap**: The building blocks of the website's look and feel. We used these to create the dark-mode layout, the search bar, and the neat product cards.
- **BeautifulSoup 4**: A Python library used for "web scraping." It's the tool that parses through the messy code of other websites to extract exactly what we need (prices and titles).
- **Requests**: A simple Python tool used to send out internet requests (like asking Amazon for a webpage).
- **SQLite**: The built-in database used by Django to securely store user accounts (usernames, emails, hashed passwords) when people sign up.
- **ScraperAPI**: A third-party proxy service that helps our web scrapers bypass anti-bot protections on major e-commerce websites.
