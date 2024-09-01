# SEO Analyzer API

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Error Handling](#error-handling)

## Overview

The SEO Analyzer API is a powerful tool designed to analyze web pages for Search Engine Optimization (SEO) purposes. It provides comprehensive insights into various aspects of a webpage, including content quality, keyword usage, meta tags, and potential SEO issues.

## Features

1. **Page Content Analysis**
   - Fetches and parses HTML content from given URLs
   - Extracts text content from various HTML elements

2. **Word Count**
   - Calculates the total word count of the extracted content

3. **Keyword Extraction**
   - Identifies and ranks the top 20 keywords used in the content

4. **Meta Tag Analysis**
   - Extracts and analyzes important meta tags (title, description, keywords)

5. **SEO Issue Detection**
   - Checks for common SEO issues such as:
     - Short content
     - Missing or multiple H1 tags
     - Images without alt text
     - Non-HTTPS URLs

6. **SEO Score Calculation**
   - Computes an overall SEO score based on various factors

7. **Content Quality Evaluation**
   - Utilizes AI (via OpenRouter API) to evaluate content quality
   - Provides scores for readability, relevance, and engagement

8. **Concurrent Processing**
   - Implements multithreading for improved performance

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

## Configuration
The application uses the following configuration variables:
    • OPENROUTER_API_KEY: Your OpenRouter API key for content quality evaluation 
    • YOUR_APP_NAME: The name of your application (used in API requests) 
Set these variables in your environment or in a .env file.

## Dependencies
    • FastAPI: Web framework for building APIs 
    • Requests: HTTP library for making requests 
    • BeautifulSoup: HTML parsing library 
    • OpenRouter API: AI-powered content quality evaluation 
For a complete list of dependencies, refer to the requirements.txt file.
Error Handling
The API implements robust error handling:
    • Invalid URLs or unreachable websites return appropriate HTTP error codes 
    • Timeouts and connection issues are handled gracefully 
    • Detailed error messages are logged for debugging purposes 

