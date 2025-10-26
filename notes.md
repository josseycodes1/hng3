endpoints to test:

### **1. POST /countries/refresh**
- **URL:** `https://web-production-c36a5.up.railway.app/countries/refresh`
- **Method:** POST
- **Purpose:** Fetch and cache countries from external APIs
- **Expected Response:**
```json
{
    "message": "Refreshed",
    "total_countries": 250,
    "last_refreshed_at": "2025-10-26T15:52:05.958204Z"
}
```

### **2. GET /countries** (with filters & sorting)
- **URL:** `https://web-production-c36a5.up.railway.app/countries`
- **Method:** GET
- **Query Parameters to Test:**
  - `?region=Africa`
  - `?currency=USD` 
  - `?sort=gdp_desc`
- **Expected Response:** Array of country objects

### **3. GET /countries/:name**
- **URL:** `https://web-production-c36a5.up.railway.app/countries/Nigeria`
- **Method:** GET
- **Expected Response:** Single country object
- **Also Test 404:** `https://web-production-c36a5.up.railway.app/countries/NonExistentCountry`

### **4. DELETE /countries/:name**
- **URL:** `https://web-production-c36a5.up.railway.app/countries/Nigeria`
- **Method:** DELETE
- **Expected Response:** 204 No Content (empty response)
- **Also Test 404:** `DELETE /countries/NonExistentCountry`

### **5. GET /status**
- **URL:** `https://web-production-c36a5.up.railway.app/status`
- **Method:** GET
- **Expected Response:**
```json
{
    "total_countries": 250,
    "last_refreshed_at": "2025-10-26T15:52:05.958204Z"
}
```

### **6. GET /countries/image**
- **URL:** `https://web-production-c36a5.up.railway.app/countries/image`
- **Method:** GET
- **Expected Response:** Image file (PNG)
- **Also Test 404:** Should return error if no image exists

## Error Endpoints to Test

### **7. Test 404 Error**
- **URL:** `https://web-production-c36a5.up.railway.app/countries/NonExistentCountry`
- **Expected:**
```json
{
    "error": "Country not found"
}
```

### **8. Test 400 Validation Error**
- **URL:** `https://web-production-c36a5.up.railway.app/countries/` (POST with invalid data)
- **Method:** POST
- **Body:**
```json
{
    "name": "",
    "population": null,
    "currency_code": null
}
```
- **Expected:**
```json
{
    "error": "Validation failed",
    "details": {
        "name": "is required",
        "population": "is required",
        "currency_code": "is required"
    }
}
```

## Testing Order

**Step 1:** `GET /status` - Check initial status  
**Step 2:** `POST /countries/refresh` - Load data  
**Step 3:** `GET /status` - Verify data loaded  
**Step 4:** `GET /countries` - Test main endpoint  
**Step 5:** `GET /countries?region=Africa` - Test filter  
**Step 6:** `GET /countries?sort=gdp_desc` - Test sorting  
**Step 7:** `GET /countries/Nigeria` - Test single country  
**Step 8:** `DELETE /countries/Nigeria` - Test delete  
**Step 9:** `GET /countries/image` - Test image  
**Step 10:** Test error responses (404, 400)
