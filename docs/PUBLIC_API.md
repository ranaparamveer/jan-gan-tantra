# Public API for Journalists and Activists

## Overview

The Public API provides access to aggregated civic data for investigative journalism, research, and advocacy. All endpoints are rate-limited to 100 requests per hour.

## Authentication

Most endpoints are public, but data export requires authentication:

```bash
# Get API token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token in requests
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/public/export/?dataset=issues
```

## Endpoints

### 1. Issue Statistics

Get aggregated issue statistics by region, category, and time period.

**Endpoint**: `GET /api/public/statistics/issues/`

**Parameters**:
- `region` (optional): Filter by region/city
- `category` (optional): Filter by category
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)

**Example**:
```bash
curl "http://localhost:8000/api/public/statistics/issues/?region=Delhi&start_date=2024-01-01"
```

**Response**:
```json
{
  "total_issues": 1523,
  "resolution_rate": 67.5,
  "avg_resolution_days": 12.3,
  "by_status": [
    {"status": "resolved", "count": 1028},
    {"status": "reported", "count": 495}
  ],
  "by_category": [
    {"category__name": "Sanitation", "count": 654},
    {"category__name": "Infrastructure", "count": 432}
  ]
}
```

### 2. Department Performance

Get performance metrics for government departments.

**Endpoint**: `GET /api/public/statistics/departments/`

**Parameters**:
- `department_id` (optional): Filter by department ID
- `min_issues` (optional): Minimum issues to include (default: 10)

**Example**:
```bash
curl "http://localhost:8000/api/public/statistics/departments/?min_issues=50"
```

**Response**:
```json
{
  "departments": [
    {
      "department_id": 1,
      "department_name": "Municipal Corporation",
      "total_issues": 523,
      "resolved_issues": 412,
      "pending_issues": 111,
      "resolution_rate": 78.77
    }
  ],
  "count": 15
}
```

### 3. Trend Analysis

Get time-series data for visualization and analysis.

**Endpoint**: `GET /api/public/trends/`

**Parameters**:
- `metric` (required): Metric to analyze (`issues`, `solutions`)
- `period` (required): Time period (`daily`, `weekly`, `monthly`)
- `days` (optional): Number of days to look back (default: 30)

**Example**:
```bash
curl "http://localhost:8000/api/public/trends/?metric=issues&period=daily&days=30"
```

**Response**:
```json
{
  "metric": "issues",
  "period": "daily",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "data_points": [
    {"date": "2024-01-01", "count": 23},
    {"date": "2024-01-02", "count": 31}
  ]
}
```

### 4. Data Export

Export datasets in JSON/CSV format for analysis.

**Endpoint**: `GET /api/public/export/`  
**Authentication**: Required

**Parameters**:
- `dataset` (required): Dataset to export (`issues`, `departments`, `solutions`)
- `format` (optional): Export format (`json`, `csv`) - default: json
- `limit` (optional): Maximum records (default: 1000, max: 10000)

**Example**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/public/export/?dataset=issues&limit=5000&format=json"
```

**Response**:
```json
{
  "dataset": "issues",
  "format": "json",
  "count": 5000,
  "data": [
    {
      "id": 1,
      "title": "Broken street light",
      "category": "Infrastructure",
      "status": "resolved",
      "created_at": "2024-01-15T10:30:00Z",
      "upvotes": 23
    }
  ]
}
```

## Rate Limiting

- **Rate**: 100 requests per hour per user
- **Headers**: Check `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers

## Use Cases

### Investigative Journalism

```bash
# Get department performance for accountability reporting
curl "http://localhost:8000/api/public/statistics/departments/"

# Export all issues for data analysis
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/public/export/?dataset=issues&limit=10000"
```

### Research & Analysis

```bash
# Get 90-day trend data for visualization
curl "http://localhost:8000/api/public/trends/?metric=issues&period=daily&days=90"

# Compare resolution rates across regions
curl "http://localhost:8000/api/public/statistics/issues/?region=Delhi"
curl "http://localhost:8000/api/public/statistics/issues/?region=Mumbai"
```

### Advocacy & Activism

```bash
# Find departments with low resolution rates
curl "http://localhost:8000/api/public/statistics/departments/?min_issues=100"

# Track issue trends over time
curl "http://localhost:8000/api/public/trends/?metric=issues&period=monthly&days=365"
```

## Support

For API access or questions:
- Email: api@jan-gan-tantra.org
- Documentation: http://localhost:8000/swagger/
- GitHub: https://github.com/ranaparamveer/jan-gan-tantra

---

**Note**: This API is provided for public good. Please use responsibly and cite Jan-Gan-Tantra when publishing findings.
