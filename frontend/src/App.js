import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [listings, setListings] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [showInquiryModal, setShowInquiryModal] = useState(false);
  const [selectedListing, setSelectedListing] = useState(null);
  const [inquiryForm, setInquiryForm] = useState({
    name: '',
    email: '',
    phone: '',
    start_date: '',
    end_date: '',
    message: ''
  });

  useEffect(() => {
    fetchListings();
    fetchCategories();
  }, []);

  const fetchListings = async (category = '', search = '') => {
    try {
      setLoading(true);
      let url = `${API_URL}/api/listings`;
      const params = new URLSearchParams();
      
      if (category) params.append('category', category);
      if (search) {
        url = `${API_URL}/api/search`;
        params.append('q', search);
        if (category) params.append('category', category);
      }
      
      if (params.toString()) url += `?${params.toString()}`;
      
      const response = await fetch(url);
      const data = await response.json();
      setListings(data);
    } catch (error) {
      console.error('Error fetching listings:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_URL}/api/categories`);
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchListings(selectedCategory, searchQuery);
  };

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
    fetchListings(category, searchQuery);
  };

  const handleInquiry = (listing) => {
    setSelectedListing(listing);
    setShowInquiryModal(true);
  };

  const submitInquiry = async (e) => {
    e.preventDefault();
    try {
      const inquiryData = {
        ...inquiryForm,
        listing_id: selectedListing.id
      };
      
      const response = await fetch(`${API_URL}/api/inquiries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inquiryData),
      });
      
      if (response.ok) {
        alert('Inquiry submitted successfully! The owner will contact you soon.');
        setShowInquiryModal(false);
        setInquiryForm({
          name: '',
          email: '',
          phone: '',
          start_date: '',
          end_date: '',
          message: ''
        });
      }
    } catch (error) {
      console.error('Error submitting inquiry:', error);
      alert('Error submitting inquiry. Please try again.');
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900">RentEverything</h1>
              <span className="ml-2 text-lg text-gray-600">🌟</span>
            </div>
            <div className="text-sm text-gray-600">
              Rent cars, bikes, houses, boats, planes & yachts
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-5xl font-bold mb-6">Rent Anything, Anywhere</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            From everyday cars to luxury yachts and private jets. Find the perfect rental for any occasion.
          </p>
          
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex flex-col sm:flex-row gap-4">
              <input
                type="text"
                placeholder="Search for cars, boats, houses..."
                className="flex-1 px-6 py-4 rounded-lg text-gray-900 text-lg focus:outline-none focus:ring-4 focus:ring-blue-300"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button
                type="submit"
                className="px-8 py-4 bg-orange-500 hover:bg-orange-600 rounded-lg text-white font-semibold text-lg transition-colors"
              >
                Search
              </button>
            </div>
          </form>
        </div>
      </section>

      {/* Categories */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Browse by Category</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <button
              onClick={() => handleCategoryFilter('')}
              className={`p-6 rounded-xl text-center transition-all ${
                selectedCategory === '' 
                  ? 'bg-blue-600 text-white shadow-lg' 
                  : 'bg-white text-gray-700 hover:bg-gray-50 shadow-md'
              }`}
            >
              <div className="text-3xl mb-2">🌟</div>
              <div className="font-semibold">All</div>
              <div className="text-sm opacity-75">{listings.length}</div>
            </button>
            {categories.map(category => (
              <button
                key={category.id}
                onClick={() => handleCategoryFilter(category.id)}
                className={`p-6 rounded-xl text-center transition-all ${
                  selectedCategory === category.id 
                    ? 'bg-blue-600 text-white shadow-lg' 
                    : 'bg-white text-gray-700 hover:bg-gray-50 shadow-md'
                }`}
              >
                <div className="text-3xl mb-2">{category.icon}</div>
                <div className="font-semibold">{category.name}</div>
                <div className="text-sm opacity-75">{category.count}</div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Listings */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-2xl font-bold text-gray-900">
              {selectedCategory ? `${categories.find(c => c.id === selectedCategory)?.name || 'Category'} Rentals` : 'All Rentals'}
            </h3>
            <div className="text-gray-600">{listings.length} listings found</div>
          </div>
          
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-600">Loading amazing rentals...</p>
            </div>
          ) : listings.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔍</div>
              <h4 className="text-2xl font-semibold text-gray-900 mb-2">No rentals found</h4>
              <p className="text-gray-600">Try adjusting your search or browse all categories</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {listings.map(listing => (
                <div key={listing.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                  <div className="aspect-w-16 aspect-h-10 bg-gray-200">
                    {listing.images && listing.images[0] ? (
                      <img
                        src={listing.images[0]}
                        alt={listing.title}
                        className="w-full h-48 object-cover"
                      />
                    ) : (
                      <div className="w-full h-48 bg-gradient-to-br from-gray-300 to-gray-400 flex items-center justify-center">
                        <span className="text-4xl text-gray-500">📷</span>
                      </div>
                    )}
                  </div>
                  
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 capitalize">
                        {categories.find(c => c.id === listing.category)?.icon} {listing.category}
                      </span>
                      <span className="text-2xl font-bold text-green-600">
                        {formatPrice(listing.price_per_day)}/day
                      </span>
                    </div>
                    
                    <h4 className="text-xl font-semibold text-gray-900 mb-2">{listing.title}</h4>
                    <p className="text-gray-600 mb-4 line-clamp-2">{listing.description}</p>
                    
                    <div className="flex items-center text-sm text-gray-500 mb-4">
                      <span className="mr-1">📍</span>
                      {listing.location}
                    </div>
                    
                    {/* Specifications */}
                    <div className="mb-4">
                      <div className="flex flex-wrap gap-2">
                        {Object.entries(listing.specifications).slice(0, 3).map(([key, value]) => (
                          <span key={key} className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-gray-100 text-gray-700">
                            {key.replace('_', ' ')}: {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    <button
                      onClick={() => handleInquiry(listing)}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
                    >
                      Book Now
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Inquiry Modal */}
      {showInquiryModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-md w-full max-h-screen overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold">Book: {selectedListing?.title}</h3>
                <button
                  onClick={() => setShowInquiryModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              
              <form onSubmit={submitInquiry} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <input
                    type="text"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={inquiryForm.name}
                    onChange={(e) => setInquiryForm({...inquiryForm, name: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={inquiryForm.email}
                    onChange={(e) => setInquiryForm({...inquiryForm, email: e.target.value})}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                  <input
                    type="tel"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={inquiryForm.phone}
                    onChange={(e) => setInquiryForm({...inquiryForm, phone: e.target.value})}
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                    <input
                      type="date"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      value={inquiryForm.start_date}
                      onChange={(e) => setInquiryForm({...inquiryForm, start_date: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                    <input
                      type="date"
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      value={inquiryForm.end_date}
                      onChange={(e) => setInquiryForm({...inquiryForm, end_date: e.target.value})}
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Message</label>
                  <textarea
                    rows="3"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Any special requirements or questions..."
                    value={inquiryForm.message}
                    onChange={(e) => setInquiryForm({...inquiryForm, message: e.target.value})}
                  ></textarea>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">Total Price Estimate:</span>
                    <span className="text-xl font-bold text-green-600">
                      {formatPrice(selectedListing?.price_per_day || 0)}/day
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">Final price will be confirmed by the owner</p>
                </div>
                
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => setShowInquiryModal(false)}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Send Inquiry
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4">RentEverything</h3>
            <p className="text-gray-400 mb-6">Your one-stop marketplace for all rental needs</p>
            <div className="flex justify-center space-x-8 text-4xl">
              <span>🚗</span>
              <span>🏍️</span>
              <span>🏡</span>
              <span>⛵</span>
              <span>✈️</span>
              <span>🛥️</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;