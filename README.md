# SEO Analyzer API

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [GET /analyzer](#get-analyzer)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Error Handling](#error-handling)

## Overview

The **SEO Analyzer API** is a robust tool designed to evaluate web pages for Search Engine Optimization (SEO) effectiveness. This API offers a detailed analysis of various webpage components, providing insights into content quality, keyword usage, meta tag optimization, and other SEO-related metrics. It is an essential tool for developers, digital marketers, and SEO specialists aiming to enhance their site's visibility on search engines.

## Features

1. **Page Content Analysis**
   - Fetches and parses HTML content from specified URLs.
   - Extracts text content from various HTML elements, including `<p>`, `<h1>`, `<h2>`, `<li>`, etc.

2. **Word Count**
   - Computes the total word count of the extracted content, excluding HTML tags and scripts.

3. **Keyword Extraction**
   - Identifies and ranks the top 20 keywords used in the webpage content.
   - Uses natural language processing (NLP) to exclude common stop words and identify relevant keywords.

4. **Meta Tag Analysis**
   - Extracts and analyzes important meta tags such as `<title>`, `<description>`, and `<keywords>`.
   - Provides recommendations for optimizing meta tag content based on best SEO practices.

5. **SEO Issue Detection**
   - Detects common SEO issues such as:
     - Short or inadequate content length.
     - Missing, multiple, or improperly nested `<h1>` tags.
     - Images without `alt` attributes.
     - Non-secure (non-HTTPS) URLs.
     - Broken internal or external links.
   - Suggests corrective actions for detected issues.

6. **SEO Score Calculation**
   - Computes an overall SEO score based on factors like keyword density, meta tag quality, content length, and presence of common SEO issues.

7. **Content Quality Evaluation**
   - Integrates with AI services (via OpenRouter API) to evaluate content quality.
   - Provides scores for readability, relevance, and engagement based on advanced machine learning algorithms.

8. **Concurrent Processing**
   - Supports multithreading for faster processing of multiple URLs simultaneously.
   - Reduces latency and improves performance for bulk SEO analysis tasks.

9. **Detailed Reporting**
   - Generates a comprehensive JSON report summarizing all findings, scores, and actionable recommendations.


## Installation

1. Clone the repository:
git clone https://github.com/yourusername/seo-analyzer-api.git
Copy

2. Install the required dependencies:
pip install -r requirements.txt
Copy

3. Set up your environment variables:
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `YOUR_APP_NAME`: The name of your application

## Usage

To start the API server:
uvicorn main:app --reload
Copy

The API will be available at `http://localhost:8000`.

## API Endpoints

### GET /analyzer

Analyzes a given URL for SEO metrics.

**Parameters:**
- `url` (required): The URL to analyze

**Example Request:**
GET /analyzer?url=https://example.com
Copy

**Example Response:**
```json
{
  "url": "https://example.com",
  "word_count": 500,
  "keywords": {
    "example": 10,
    "content": 8,
    "seo": 5
  },
  "meta_tags": {
    "title": "Example Website",
    "description": "This is an example website for SEO analysis.",
    "keywords": "seo, analysis, example"
  },
  "seo_issues": [
    {
      "issue": "No H1 tag found",
      "description": "Missing main heading",
      "severity": "High"
    }
  ],
  "seo_score": 85,
  "content_evaluation": {
    "readability": 8,
    "relevance": 7,
    "engagement": 6,
    "overall_score": 70,
    "suggestions": [
      "Improve content structure",
      "Add more engaging elements"
    ]
  }
}
```
## Configuration
The application uses the following configuration variables, which can be set in a .env file or directly in your environment:
    • OPENROUTER_API_KEY: Your OpenRouter API key for content quality evaluation.
    • YOUR_APP_NAME: The name of your application (used in API requests).
Ensure these variables are set correctly before running the application.

## Dependencies
The SEO Analyzer API relies on several third-party libraries and tools:
    • FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
    • Requests: A simple, yet powerful HTTP library for Python.
    • BeautifulSoup: A Python library for parsing HTML and XML documents and extracting useful information.
    • OpenRouter API: An external service used for advanced AI-powered content quality evaluation.
For a complete list of dependencies, refer to the requirements.txt file.

## Error Handling
The API includes robust error handling mechanisms to ensure a smooth user experience:
    • Invalid URLs: The API validates URLs and returns a 400 Bad Request error if an invalid URL is provided.
    • Unreachable Websites: Returns a 404 Not Found or 500 Internal Server Error if the website is unreachable or encounters a server error.
    • Timeouts: Gracefully handles request timeouts and provides a meaningful error message.
    • Connection Issues: Detects and reports network-related issues.
    • Detailed Logging: All errors are logged with detailed information for debugging purposes.


