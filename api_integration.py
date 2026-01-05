"""
Google Sheets KPI Dashboard - API Integration
Reads data from Google Sheets and exposes via REST API for dashboard consumption
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class GoogleSheetsConnector:
    """Connects to Google Sheets API and fetches data"""
    
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        """
        Initialize connector with credentials and spreadsheet ID
        
        Args:
            credentials_path: Path to service account JSON file
            spreadsheet_id: Google Sheets ID from URL
        """
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google using service account credentials"""
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=SCOPES
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("✅ Google Sheets API authenticated successfully")
        except FileNotFoundError:
            logger.error(f"❌ Credentials file not found: {self.credentials_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Authentication failed: {str(e)}")
            raise
    
    def fetch_data(self, sheet_range: str = "Raw_Data!A:F") -> List[Dict[str, Any]]:
        """
        Fetch data from specified range in Google Sheet
        
        Args:
            sheet_range: Range in A1 notation (e.g., "Raw_Data!A:F")
        
        Returns:
            List of dictionaries with headers as keys
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_range
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("⚠️ No data found in specified range")
                return []
            
            # First row is headers
            headers = values[0]
            data = []
            
            for row in values[1:]:
                # Pad row if it's shorter than headers
                while len(row) < len(headers):
                    row.append("")
                
                # Create dictionary for this row
                row_dict = {}
                for i, header in enumerate(headers):
                    value = row[i]
                    # Try to convert to appropriate type
                    if header.lower() == 'montant':
                        try:
                            row_dict[header] = float(value)
                        except (ValueError, TypeError):
                            row_dict[header] = 0
                    else:
                        row_dict[header] = value
                
                data.append(row_dict)
            
            logger.info(f"✅ Successfully fetched {len(data)} rows")
            return data
        
        except Exception as e:
            logger.error(f"❌ Error fetching data: {str(e)}")
            raise
    
    def get_unique_values(self, data: List[Dict], column: str) -> List[str]:
        """Get unique values from a specific column"""
        return sorted(list(set([str(row.get(column, '')) for row in data if row.get(column)])))


class KPICalculator:
    """Calculates KPIs from raw data"""
    
    @staticmethod
    def calculate_total_revenue(data: List[Dict]) -> float:
        """Sum of all montant values"""
        return sum([float(row.get('Montant', 0)) for row in data])
    
    @staticmethod
    def calculate_total_deals(data: List[Dict]) -> int:
        """Count of all deals"""
        return len(data)
    
    @staticmethod
    def calculate_deals_won(data: List[Dict]) -> int:
        """Count of deals with status 'Gagné'"""
        return sum([1 for row in data if row.get('Statut', '').strip().lower() == 'gagné'])
    
    @staticmethod
    def calculate_conversion_rate(deals_won: int, total_deals: int) -> float:
        """Conversion rate as percentage"""
        if total_deals == 0:
            return 0.0
        return round((deals_won / total_deals) * 100, 1)
    
    @staticmethod
    def calculate_revenue_by_channel(data: List[Dict]) -> Dict[str, float]:
        """Revenue grouped by Canal"""
        result = {}
        for row in data:
            canal = row.get('Canal', 'Unknown')
            montant = float(row.get('Montant', 0))
            result[canal] = result.get(canal, 0) + montant
        return result
    
    @staticmethod
    def calculate_status_distribution(data: List[Dict]) -> Dict[str, int]:
        """Count of deals by status"""
        result = {}
        for row in data:
            statut = row.get('Statut', 'Unknown')
            result[statut] = result.get(statut, 0) + 1
        return result
    
    @staticmethod
    def calculate_revenue_by_rep(data: List[Dict]) -> Dict[str, float]:
        """Revenue grouped by Commercial"""
        result = {}
        for row in data:
            commercial = row.get('Commercial', 'Unknown')
            montant = float(row.get('Montant', 0))
            result[commercial] = result.get(commercial, 0) + montant
        return result
    
    @staticmethod
    def calculate_revenue_trend(data: List[Dict]) -> Dict[str, float]:
        """Daily revenue for won deals"""
        result = {}
        for row in data:
            if row.get('Statut', '').strip().lower() == 'gagné':
                date = str(row.get('Date', 'Unknown'))
                montant = float(row.get('Montant', 0))
                result[date] = result.get(date, 0) + montant
        return dict(sorted(result.items()))


def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"✅ Config loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.warning(f"⚠️ Config file not found: {config_path}")
        # Return defaults
        return {
            "sheet_id": os.getenv("GOOGLE_SHEET_ID"),
            "range": "Raw_Data!A:F",
            "credentials_path": os.getenv("GOOGLE_CREDENTIALS_PATH", "./google-credentials.json")
        }


def main():
    """Main execution"""
    # Load configuration
    config = load_config()
    
    sheet_id = config.get("sheet_id")
    sheet_range = config.get("range", "Raw_Data!A:F")
    credentials_path = config.get("credentials_path")
    
    logger.info("=" * 60)
    logger.info("🚀 KPI Dashboard - Google Sheets Sync")
    logger.info("=" * 60)
    
    # Initialize connector
    connector = GoogleSheetsConnector(credentials_path, sheet_id)
    
    # Fetch raw data
    raw_data = connector.fetch_data(sheet_range)
    
    if not raw_data:
        logger.error("❌ No data to process. Exiting.")
        return
    
    # Calculate KPIs
    calculator = KPICalculator()
    
    total_revenue = calculator.calculate_total_revenue(raw_data)
    total_deals = calculator.calculate_total_deals(raw_data)
    deals_won = calculator.calculate_deals_won(raw_data)
    conversion_rate = calculator.calculate_conversion_rate(deals_won, total_deals)
    
    revenue_by_channel = calculator.calculate_revenue_by_channel(raw_data)
    status_distribution = calculator.calculate_status_distribution(raw_data)
    revenue_by_rep = calculator.calculate_revenue_by_rep(raw_data)
    revenue_trend = calculator.calculate_revenue_trend(raw_data)
    
    # Build response
    dashboard_data = {
        "last_updated": datetime.now().isoformat(),
        "kpis": {
            "total_revenue": round(total_revenue, 2),
            "total_deals": total_deals,
            "deals_won": deals_won,
            "conversion_rate": conversion_rate,
        },
        "charts": {
            "revenue_by_channel": revenue_by_channel,
            "status_distribution": status_distribution,
            "revenue_by_rep": revenue_by_rep,
            "revenue_trend": revenue_trend,
        },
        "raw_data": raw_data[-100:],  # Last 100 rows
    }
    
    # Log summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 KPI SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total Revenue: €{total_revenue:,.2f}")
    logger.info(f"Total Deals: {total_deals}")
    logger.info(f"Deals Won: {deals_won}")
    logger.info(f"Conversion Rate: {conversion_rate}%")
    logger.info("=" * 60)
    
    # Save output as JSON
    output_file = "dashboard_data.json"
    with open(output_file, 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    logger.info(f"\n✅ Dashboard data saved to {output_file}")
    
    # Print for debugging
    logger.info(f"\n✅ Dashboard ready! Open kpi-dashboard.html in your browser")
    
    return dashboard_data


if __name__ == "__main__":
    main()
