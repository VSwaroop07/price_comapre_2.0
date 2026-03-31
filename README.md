# Retail Purchase Intelligence System (Price Compare 2.0)

Welcome to the **Retail Purchase Intelligence System**! This web application is a smart search engine designed for shoppers. Instead of manually checking prices across different e-commerce websites, you can type your desired product once, and this app will fetch, compare, and display the top results from **Amazon, Flipkart, and Shopclues** side-by-side.

## 🚀 Features
- **Cross-Platform Search**: Instantly searches across Amazon, Flipkart, and Shopclues.
- **Bot Bypass**: Uses ScraperAPI to reliably extract data without getting blocked by anti-bot protections.
- **Smart Data Extraction**: Uses BeautifulSoup to scrape product titles, images, links, and prices.
- **Intelligent Sorting**: Cleans raw price data (removes symbols and commas) and ranks products from lowest to highest price.
- **Clean UI**: A responsive, dark-mode friendly interface built with Bootstrap to display easy-to-read product cards.

## 🛠️ Tech Stack
- **Backend**: Python, Django
- **Web Scraping**: BeautifulSoup 4, Requests, ScraperAPI
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (for storing user accounts securely)

## 🌊 How It Works & Architecture
1. **User Request**: The user enters a search term (e.g., "iPhone 15") on the frontend.
2. **Backend Processing**: Django constructs search URLs for Flipkart, Amazon, and Shopclues.
3. **Scraping**: The backend routes requests through **ScraperAPI** to bypass blocks and fetches the raw HTML.
4. **Data Parsing**: **BeautifulSoup** extracts the product image, title, price, and buy link.
5. **Sorting & Filtering**: The system cleans the prices, sorts all products from lowest to highest, and ignores invalid entries.
6. **Display**: The sorted data is sent back to the frontend and rendered as beautiful product cards.

> *For a more detailed explanation of the architecture, see the [HOW_IT_WORKS.md](HOW_IT_WORKS.md) file.*

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine:

### Prerequisites
- Python 3.8+
- Node.js & npm (for ScraperAPI SDK if used directly in any JS scripts)
- Git

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "price_comapre 2.0/price_comapre/price_comapre"
```

### 2. Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```
**On Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node Dependencies
There is a `package.json` for frontend/scraping utilities.
```bash
npm install
```

### 5. Setup Environment Variables
You may need to provide your **ScraperAPI Key** in an environment variables file (e.g. `.env`) if your Python or Node extractors are using it behind the scenes. Look for `.env.example` if available.

### 6. Run Database Migrations
Initialize the SQLite database for user accounts.
```bash
python manage.py migrate
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/` to use the application!

## 📝 License & Disclaimer
This project is intended for educational purposes on how web scraping and data aggregation work. Always observe the Terms of Service of the respective platforms you interface with.
