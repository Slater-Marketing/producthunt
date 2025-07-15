# ProductHunt Daily Scraper

A Selenium-based web scraper that automatically extracts all products added to ProductHunt.com each day. The scraper runs daily at 11:00 PM PST and saves the data in both JSON and CSV formats.

## Features

- **Automated Daily Scraping**: Runs automatically at 11:00 PM PST every day
- **Complete Product Data**: Extracts product names, taglines, URLs, images, upvotes, categories, and maker information
- **Multiple Output Formats**: Saves data in both JSON and CSV formats
- **Robust Error Handling**: Comprehensive logging and error recovery
- **Headless Operation**: Runs in the background without opening browser windows
- **Infinite Scroll Support**: Handles ProductHunt's infinite scroll to capture all products

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- Windows 10/11 (for the provided scripts)

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd producthunt
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import selenium, schedule, pytz, webdriver_manager; print('All dependencies installed successfully!')"
   ```

## Usage

### Run Once (Manual Execution)

**Using Python directly:**
```bash
python producthunt_scraper.py
```

**Using PowerShell script:**
```powershell
.\run_scraper.ps1
```

**Using batch file:**
```cmd
run_scraper.bat
```

### Run with Scheduler (Continuous Operation)

**Using Python scheduler:**
```bash
python scheduler.py
```

**Using PowerShell with scheduler:**
```powershell
.\run_scraper.ps1 -Schedule
```

### Run Once with Scheduler Script
```bash
python scheduler.py --run-once
```

## Scheduling Options

### Option 1: Windows Task Scheduler (Recommended)

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, and press Enter

2. **Create Basic Task**
   - Click "Create Basic Task" in the right panel
   - Name: "ProductHunt Scraper"
   - Description: "Daily ProductHunt product scraper"

3. **Set Trigger**
   - Trigger: Daily
   - Start: Set to 11:00 PM
   - Time zone: Pacific Standard Time

4. **Set Action**
   - Action: Start a program
   - Program/script: `python`
   - Add arguments: `producthunt_scraper.py`
   - Start in: `C:\path\to\your\producthunt\folder`

5. **Finish**
   - Review settings and click Finish

### Option 2: Python Scheduler (Continuous Process)

Run the scheduler script which keeps running and executes the scraper daily:
```bash
python scheduler.py
```

### Option 3: PowerShell Script with Windows Task Scheduler

Use the PowerShell script in Task Scheduler for better error handling:
- Program/script: `powershell.exe`
- Add arguments: `-ExecutionPolicy Bypass -File "C:\path\to\run_scraper.ps1"`

## Output Files

The scraper generates the following files:

- **JSON File**: `producthunt_products_YYYYMMDD.json`
- **CSV File**: `producthunt_products_YYYYMMDD.csv`
- **Log File**: `producthunt_scraper.log`

### Data Structure

Each product entry contains:
```json
{
  "name": "Product Name",
  "tagline": "Product description/tagline",
  "url": "https://www.producthunt.com/posts/product-name",
  "image_url": "https://...",
  "upvotes": "123",
  "category": "Productivity",
  "maker": "Maker Name",
  "scraped_at": "2024-01-15T23:00:00.000000",
  "date": "2024-01-15"
}
```

## Configuration

### Chrome Options

The scraper runs Chrome in headless mode by default. To run with a visible browser window, modify the `ProductHuntScraper` initialization:

```python
scraper = ProductHuntScraper(headless=False)
```

### Custom Time Zone

To change the time zone for scheduling, modify the `scheduler.py` file:

```python
# Change from PST to your timezone
schedule.every().day.at("23:00").do(run_scraper)  # 11:00 PM
```

## Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - The scraper uses `webdriver-manager` to automatically download and manage Chrome drivers
   - Ensure Google Chrome is installed and up to date

2. **Permission Errors**
   - Run PowerShell as Administrator if you encounter permission issues
   - Ensure the script directory is writable

3. **Python Path Issues**
   - Ensure Python is in your system PATH
   - Use full path to Python executable in Task Scheduler if needed

4. **Network Issues**
   - Check your internet connection
   - ProductHunt may block requests if too frequent - the scraper includes delays to avoid this

### Logs

Check the log files for detailed information:
- `producthunt_scraper.log` - Main scraper logs
- `scheduler.log` - Scheduler-specific logs

## Data Analysis

The scraped data can be used for:
- Market research and trend analysis
- Competitor monitoring
- Product discovery
- Investment research
- Content creation

## Legal and Ethical Considerations

- This scraper is for educational and research purposes
- Respect ProductHunt's robots.txt and terms of service
- Do not overload their servers with excessive requests
- Consider the rate limiting and delays built into the scraper

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the scraper.

## License

This project is for educational purposes. Please ensure compliance with ProductHunt's terms of service when using this scraper. 