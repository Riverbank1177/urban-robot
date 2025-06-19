import requests
import unittest
import json
from datetime import datetime, timedelta

class RentalMarketplaceAPITest(unittest.TestCase):
    def setUp(self):
        # Use the public endpoint from the .env file
        self.base_url = "https://538ef967-326d-4347-93fa-ef1f8d2939ed.preview.emergentagent.com"
        self.headers = {"Content-Type": "application/json"}
        
        # Sample test data for inquiry form
        self.test_inquiry = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "start_date": "2025-04-01",
            "end_date": "2025-04-05",
            "message": "Interested in renting this item"
        }

    def test_01_health_check(self):
        """Test the health check endpoint"""
        print("\n🔍 Testing API health check...")
        response = requests.get(f"{self.base_url}/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        print("✅ Health check endpoint is working")

    def test_02_get_listings(self):
        """Test getting all listings"""
        print("\n🔍 Testing get all listings...")
        response = requests.get(f"{self.base_url}/api/listings")
        self.assertEqual(response.status_code, 200)
        listings = response.json()
        self.assertIsInstance(listings, list)
        self.assertGreater(len(listings), 0)
        print(f"✅ Retrieved {len(listings)} listings successfully")
        
        # Verify listing structure
        first_listing = listings[0]
        required_fields = ["id", "title", "description", "category", "price_per_day", "location", "images"]
        for field in required_fields:
            self.assertIn(field, first_listing)
        print("✅ Listing structure is valid")
        
        return listings[0]["id"]  # Return first listing ID for later tests

    def test_03_get_listing_by_id(self):
        """Test getting a specific listing by ID"""
        # First get all listings to get a valid ID
        listings_response = requests.get(f"{self.base_url}/api/listings")
        listings = listings_response.json()
        if not listings:
            self.fail("No listings available to test get_listing_by_id")
        
        listing_id = listings[0]["id"]
        
        print(f"\n🔍 Testing get listing by ID: {listing_id}...")
        response = requests.get(f"{self.base_url}/api/listings/{listing_id}")
        self.assertEqual(response.status_code, 200)
        listing = response.json()
        self.assertEqual(listing["id"], listing_id)
        print("✅ Retrieved specific listing successfully")

    def test_04_get_categories(self):
        """Test getting all categories"""
        print("\n🔍 Testing get categories...")
        response = requests.get(f"{self.base_url}/api/categories")
        self.assertEqual(response.status_code, 200)
        categories = response.json()
        self.assertIsInstance(categories, list)
        
        # Verify we have the expected categories
        expected_categories = ["cars", "bikes", "houses", "boats", "planes", "yachts"]
        category_ids = [cat["id"] for cat in categories]
        
        for expected in expected_categories:
            self.assertIn(expected, category_ids, f"Missing category: {expected}")
        
        print(f"✅ Retrieved {len(categories)} categories successfully")
        print(f"✅ Categories: {', '.join(category_ids)}")

    def test_05_search_listings(self):
        """Test search functionality"""
        print("\n🔍 Testing search functionality...")
        
        # Test search for "Ferrari"
        search_term = "Ferrari"
        response = requests.get(f"{self.base_url}/api/search?q={search_term}")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertIsInstance(results, list)
        
        if results:
            print(f"✅ Search for '{search_term}' returned {len(results)} results")
            # Verify the search term appears in the results
            found = False
            for listing in results:
                if search_term.lower() in listing["title"].lower() or search_term.lower() in listing["description"].lower():
                    found = True
                    break
            self.assertTrue(found, f"Search term '{search_term}' not found in results")
            print(f"✅ Search results contain the term '{search_term}'")
        else:
            print(f"⚠️ Search for '{search_term}' returned no results")
        
        # Test search with category filter
        category = "cars"
        response = requests.get(f"{self.base_url}/api/search?q={search_term}&category={category}")
        self.assertEqual(response.status_code, 200)
        category_results = response.json()
        
        # Verify all results are in the specified category
        if category_results:
            all_in_category = all(result["category"] == category for result in category_results)
            self.assertTrue(all_in_category, f"Not all results are in category '{category}'")
            print(f"✅ Category filter for '{category}' working correctly")
        
        # Test search with no matches
        random_term = f"NonExistentItem{datetime.now().strftime('%H%M%S')}"
        response = requests.get(f"{self.base_url}/api/search?q={random_term}")
        self.assertEqual(response.status_code, 200)
        no_results = response.json()
        self.assertEqual(len(no_results), 0)
        print(f"✅ Search for non-existent term returns empty list")

    def test_06_submit_inquiry(self):
        """Test submitting an inquiry"""
        print("\n🔍 Testing inquiry submission...")
        
        # First get a listing ID to use
        listings_response = requests.get(f"{self.base_url}/api/listings")
        listings = listings_response.json()
        if not listings:
            self.fail("No listings available to test inquiry submission")
        
        listing_id = listings[0]["id"]
        
        # Create inquiry data
        inquiry_data = {
            **self.test_inquiry,
            "listing_id": listing_id
        }
        
        # Submit inquiry
        response = requests.post(
            f"{self.base_url}/api/inquiries",
            headers=self.headers,
            json=inquiry_data
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        self.assertIn("inquiry_id", result)
        print("✅ Inquiry submitted successfully")

    def test_07_filter_by_category(self):
        """Test filtering listings by category"""
        print("\n🔍 Testing category filtering...")
        
        # Get categories first
        categories_response = requests.get(f"{self.base_url}/api/categories")
        categories = categories_response.json()
        
        if not categories:
            self.fail("No categories available to test filtering")
        
        # Test each category
        for category in categories:
            category_id = category["id"]
            response = requests.get(f"{self.base_url}/api/listings?category={category_id}")
            self.assertEqual(response.status_code, 200)
            
            filtered_listings = response.json()
            
            # Verify all listings are in the specified category
            if filtered_listings:
                all_in_category = all(listing["category"] == category_id for listing in filtered_listings)
                self.assertTrue(all_in_category, f"Not all results are in category '{category_id}'")
                print(f"✅ Category filter for '{category_id}' returned {len(filtered_listings)} listings")
            else:
                print(f"⚠️ Category '{category_id}' has no listings")

    def test_08_inquiry_validation_past_date(self):
        """Test inquiry validation with past start date"""
        print("\n🔍 Testing inquiry validation with past start date...")
        
        # Get a listing ID to use
        listings_response = requests.get(f"{self.base_url}/api/listings")
        listings = listings_response.json()
        if not listings:
            self.fail("No listings available to test inquiry validation")
        
        listing_id = listings[0]["id"]
        
        # Create inquiry data with past start date
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        
        invalid_inquiry = {
            **self.test_inquiry,
            "listing_id": listing_id,
            "start_date": yesterday,
            "end_date": future_date
        }
        
        # Submit inquiry with invalid date
        response = requests.post(
            f"{self.base_url}/api/inquiries",
            headers=self.headers,
            json=invalid_inquiry
        )
        
        # The API should accept this since validation is done on frontend
        # But we're testing to confirm the behavior
        self.assertEqual(response.status_code, 200)
        print("✅ Backend accepts inquiry with past date (validation is on frontend)")

    def test_09_inquiry_validation_end_before_start(self):
        """Test inquiry validation with end date before start date"""
        print("\n🔍 Testing inquiry validation with end date before start date...")
        
        # Get a listing ID to use
        listings_response = requests.get(f"{self.base_url}/api/listings")
        listings = listings_response.json()
        if not listings:
            self.fail("No listings available to test inquiry validation")
        
        listing_id = listings[0]["id"]
        
        # Create inquiry data with end date before start date
        future_date1 = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        future_date2 = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        invalid_inquiry = {
            **self.test_inquiry,
            "listing_id": listing_id,
            "start_date": future_date1,
            "end_date": future_date2
        }
        
        # Submit inquiry with invalid dates
        response = requests.post(
            f"{self.base_url}/api/inquiries",
            headers=self.headers,
            json=invalid_inquiry
        )
        
        # The API should accept this since validation is done on frontend
        # But we're testing to confirm the behavior
        self.assertEqual(response.status_code, 200)
        print("✅ Backend accepts inquiry with end date before start date (validation is on frontend)")

    def test_10_inquiry_with_test_data(self):
        """Test inquiry with the specified test data"""
        print("\n🔍 Testing inquiry with specified test data...")
        
        # Get a listing ID to use
        listings_response = requests.get(f"{self.base_url}/api/listings")
        listings = listings_response.json()
        if not listings:
            self.fail("No listings available to test inquiry submission")
        
        listing_id = listings[0]["id"]
        
        # Create inquiry with the specified test data
        test_inquiry_data = {
            "name": "Alice Johnson",
            "email": "alice@test.com",
            "phone": "555-123-4567",
            "start_date": "2025-04-15",
            "end_date": "2025-04-20",
            "message": "Looking forward to renting this!",
            "listing_id": listing_id
        }
        
        # Submit inquiry
        response = requests.post(
            f"{self.base_url}/api/inquiries",
            headers=self.headers,
            json=test_inquiry_data
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("message", result)
        self.assertIn("inquiry_id", result)
        print("✅ Test inquiry submitted successfully")if __name__ == "__main__":
    unittest.main(verbosity=2)