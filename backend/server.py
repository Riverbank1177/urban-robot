from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from pymongo import MongoClient
from datetime import datetime
import uuid

# Database Setup
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
db = client.rental_marketplace

# Collections
listings = db.listings
inquiries = db.inquiries

app = FastAPI(title="Rental Marketplace API", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Listing(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str  # cars, bikes, houses, boats, planes, yachts
    price_per_day: float
    location: str
    images: List[str] = []
    specifications: Dict[str, Any] = {}
    available: bool = True
    owner_name: str
    owner_contact: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Inquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    listing_id: str
    name: str
    email: str
    phone: str
    start_date: str
    end_date: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Sample data initialization
def init_sample_data():
    if listings.count_documents({}) == 0:
        sample_listings = [
            {
                "id": str(uuid.uuid4()),
                "title": "Luxury Ferrari 488 Spider",
                "description": "Experience the thrill of driving a luxury Ferrari 488 Spider. Perfect for special occasions and weekend getaways.",
                "category": "cars",
                "price_per_day": 899.00,
                "location": "Los Angeles, CA",
                "images": ["https://images.pexels.com/photos/1545743/pexels-photo-1545743.jpeg"],
                "specifications": {
                    "year": 2022,
                    "seats": 2,
                    "transmission": "Automatic",
                    "fuel_type": "Gasoline"
                },
                "available": True,
                "owner_name": "Elite Car Rentals",
                "owner_contact": "contact@eliterentals.com",
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Luxury Yacht Charter - 60ft",
                "description": "Stunning 60ft luxury yacht perfect for parties, events, and ocean adventures. Includes crew and amenities.",
                "category": "yachts",
                "price_per_day": 2499.00,
                "location": "Miami, FL",
                "images": ["https://images.pexels.com/photos/32619596/pexels-photo-32619596.jpeg"],
                "specifications": {
                    "length": "60 feet",
                    "guests": 12,
                    "crew_included": True,
                    "amenities": ["Kitchen", "Bedrooms", "Entertainment System"]
                },
                "available": True,
                "owner_name": "Ocean Dreams Charters",
                "owner_contact": "info@oceandreams.com",
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Beachfront Villa Rental",
                "description": "Stunning beachfront villa with panoramic ocean views. Perfect for vacation rentals and special events.",
                "category": "houses",
                "price_per_day": 799.00,
                "location": "Malibu, CA",
                "images": ["https://images.pexels.com/photos/59924/pexels-photo-59924.jpeg"],
                "specifications": {
                    "bedrooms": 4,
                    "bathrooms": 3,
                    "sleeps": 8,
                    "amenities": ["Pool", "Beach Access", "Kitchen", "WiFi"]
                },
                "available": True,
                "owner_name": "Coastal Properties",
                "owner_contact": "rentals@coastalprops.com",
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Harley Davidson Street Glide",
                "description": "Cruise in style with this iconic Harley Davidson Street Glide. Perfect for road trips and adventures.",
                "category": "bikes",
                "price_per_day": 199.00,
                "location": "Austin, TX",
                "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64"],
                "specifications": {
                    "year": 2023,
                    "engine": "Milwaukee-Eight 114",
                    "type": "Touring"
                },
                "available": True,
                "owner_name": "Lone Star Bike Rentals",
                "owner_contact": "info@lonestarbikerentals.com",
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Private Jet Charter - Cessna Citation",
                "description": "Luxury private jet charter for business or leisure travel. Includes pilot and premium service.",
                "category": "planes",
                "price_per_day": 4999.00,
                "location": "New York, NY",
                "images": ["https://images.unsplash.com/photo-1544636235-1-photo-1545670723-673ed2f20e04"],
                "specifications": {
                    "model": "Cessna Citation CJ3+",
                    "passengers": 7,
                    "range": "2,040 miles",
                    "pilot_included": True
                },
                "available": True,
                "owner_name": "Elite Aviation",
                "owner_contact": "charter@eliteaviation.com",
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Speed Boat - 32ft Sport Cruiser",
                "description": "High-performance sport boat perfect for water sports, fishing, and coastal cruising.",
                "category": "boats",
                "price_per_day": 599.00,
                "location": "San Diego, CA",
                "images": ["https://images.unsplash.com/photo-1560216874-c209251cba8e"],
                "specifications": {
                    "length": "32 feet",
                    "passengers": 8,
                    "engine": "Twin 350HP",
                    "features": ["GPS", "Sound System", "Safety Equipment"]
                },
                "available": True,
                "owner_name": "Pacific Boat Rentals",
                "owner_contact": "rentals@pacificboats.com",
                "created_at": datetime.utcnow()
            }
        ]
        
        for listing in sample_listings:
            listings.insert_one(listing)

# API Routes
@app.on_event("startup")
async def startup_event():
    init_sample_data()

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Rental Marketplace API is running"}

@app.get("/api/listings", response_model=List[Dict])
async def get_listings(category: Optional[str] = None, location: Optional[str] = None):
    """Get all listings with optional filtering"""
    query = {"available": True}
    
    if category:
        query["category"] = category.lower()
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    
    results = list(listings.find(query, {"_id": 0}).sort("created_at", -1))
    return results

@app.get("/api/listings/{listing_id}")
async def get_listing(listing_id: str):
    """Get a specific listing by ID"""
    listing = listings.find_one({"id": listing_id}, {"_id": 0})
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@app.get("/api/categories")
async def get_categories():
    """Get all available categories with counts"""
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    
    results = list(listings.aggregate(pipeline))
    categories = []
    
    category_info = {
        "cars": {"name": "Cars", "icon": "🚗"},
        "bikes": {"name": "Bikes", "icon": "🏍️"}, 
        "houses": {"name": "Houses", "icon": "🏡"},
        "boats": {"name": "Boats", "icon": "⛵"},
        "planes": {"name": "Planes", "icon": "✈️"},
        "yachts": {"name": "Yachts", "icon": "🛥️"}
    }
    
    for result in results:
        category = result["_id"]
        if category in category_info:
            categories.append({
                "id": category,
                "name": category_info[category]["name"],
                "icon": category_info[category]["icon"],
                "count": result["count"]
            })
    
    return categories

@app.post("/api/inquiries")
async def create_inquiry(inquiry: Inquiry):
    """Create a new rental inquiry"""
    # Verify listing exists
    listing = listings.find_one({"id": inquiry.listing_id}, {"_id": 0})
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    inquiry_dict = inquiry.dict()
    inquiries.insert_one(inquiry_dict)
    
    return {"message": "Inquiry submitted successfully", "inquiry_id": inquiry.id}

@app.get("/api/search")
async def search_listings(q: str, category: Optional[str] = None):
    """Search listings by keyword"""
    query = {
        "available": True,
        "$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"location": {"$regex": q, "$options": "i"}}
        ]
    }
    
    if category:
        query["category"] = category.lower()
    
    results = list(listings.find(query, {"_id": 0}).sort("created_at", -1))
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)