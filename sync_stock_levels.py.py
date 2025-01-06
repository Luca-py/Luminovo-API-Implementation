import pandas as pd
import requests
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(
    filename="sync_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# API Configuration
API_URL = "https://api.luminovo.com/offers/import"  # Replace with actual endpoint
API_KEY = "your_api_key_here"  # Replace with your API key

# File Configuration
INPUT_FILE = "/Your/Path/Name"  # Path to the input Excel file

def transform_data(file_path):
    """Transform Excel data into API JSON format"""
    try:
        # Read the sheets
        sheet1 = pd.read_excel(file_path, sheet_name="Sheet1")  # Available Stock, Total Stock, etc.
        sheet2 = pd.read_excel(file_path, sheet_name="Sheet2")  # Additional information

        # Rename column in Sheet2 for consistent merging
        sheet2.rename(columns={"Internal part number (IPN) from BOM": "Internal Part Number"}, inplace=True)
        
        # Merge sheets based on the common field 'Internal Part Number' (no overlay?)
        merged_df = sheet1.merge(sheet2, on="Internal Part Number", how="left")

        # Transform merged data into the required JSON format
        inventory_data = []
        for _, row in merged_df.iterrows():
            # Safe get function to handle missing values or NaN
            def safe_get(col, default=None):
                return row[col] if col in row.index and pd.notna(row[col]) else default

            inventory_data.append({
                "availability": {
                    "available_stock": safe_get("Available Stock", 0),
                    "total_stock": safe_get("Total Stock", 0),
                    "on_order": [],
                    "lead_time": safe_get("Lead time (days)")
                },
                "notes": f"Synced on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",  # For documentation purposes
                "packaging": safe_get("Packaging", "Bag"),
                "price_type": safe_get("Price type", "Standard"),
                "part": {
                    "internal_part_number": safe_get("Internal Part Number")
                },
                "prices": [
                    {
                        "moq": safe_get("MOQ", 1),  # Default to 1 if missing
                        "mpq": safe_get("MPQ", 1),  # Default to 1 if missing
                        "unit_price": safe_get("Unit Price", 1)  # Default to 1 if missing
                    }
                ],
                "supplier": {
                    "supplier": safe_get("Supplier", "Unknown Supplier"),  # Default supplier name
                    "supplier_number": safe_get("Supplier number", "0000"),  # Default supplier number
                    "supplier_part_number": safe_get("Supplier part number", "Unknown Part"),
                    "type": "External"
                },
                "unit_of_measurement": {
                    "quantity": 1,  # Replace column if different
                    "unit": "Piece"  # Default to "Piece" if missing
                }
            })

        return {"inventory": inventory_data}
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        raise

def send_data_to_api(payload):
    """Send transformed data to Luminovo API"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            logging.info("Data successfully synced to Luminovo")
        else:
            logging.error(f"API Error: {response.status_code} - {response.text}")
            response.raise_for_status()
    except Exception as e:
        logging.error(f"Error sending data to API: {e}")
        raise

def main():
    """Main function to handle data sync"""
    try:
        logging.info("Starting stock sync process")
        
        # Transform the data
        payload = transform_data(INPUT_FILE)

        # Send to API
        send_data_to_api(payload)

        logging.info("Stock sync process completed successfully")
    except Exception as e:
        logging.error(f"Stock sync failed: {e}")

if __name__ == "__main__":
    main()
