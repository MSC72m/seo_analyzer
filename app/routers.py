import json
import logging
from typing import Dict, Any, List
import re
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError
from .config import OPENROUTER_API_KEY, YOUR_APP_NAME

router = APIRouter(tags=["SEO"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_page_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'SEOAnalyzerBot/1.0'})
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching content from {url}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching content: {str(e)}"
        )


def extract_text_content(soup: BeautifulSoup) -> str:
    text = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
    return text if text else ' '.join(soup.stripped_strings)


def count_words(text: str) -> int:
    return len(re.findall(r'\w+', text))


def extract_keywords(text: str) -> Dict[str, int]:
    words = re.findall(r'\w+', text.lower())
    word_counts = {}
    for word in words:
        if len(word) > 3:  # Ignore short words
            word_counts[word] = word_counts.get(word, 0) + 1
    return dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])


def analyze_meta_tags(soup: BeautifulSoup) -> Dict[str, Any]:
    meta_tags = {}
    title_tag = soup.find('title')
    meta_tags['title'] = title_tag.text if title_tag else None

    for tag in soup.find_all('meta'):
        if 'name' in tag.attrs and tag.attrs['name'].lower() in ['description', 'keywords']:
            meta_tags[tag.attrs['name'].lower()] = tag.attrs.get('content', '')

    return meta_tags


def check_seo_issues(soup: BeautifulSoup, text_content: str, url: str) -> List[Dict[str, Any]]:
    issues = []

    if len(text_content) < 300:
        issues.append(
            {"issue": "Content length is too short", "description": "Less than 300 characters", "severity": "High"})

    h1_tags = soup.find_all('h1')
    if not h1_tags:
        issues.append({"issue": "No H1 tag found", "description": "Missing main heading", "severity": "High"})
    elif len(h1_tags) > 1:
        issues.append(
            {"issue": "Multiple H1 tags found", "description": f"{len(h1_tags)} H1 tags present", "severity": "Medium"})

    img_tags = soup.find_all('img', alt='')
    if img_tags:
        issues.append(
            {"issue": "Images without alt text", "description": f"{len(img_tags)} images found without alt text",
             "severity": "Medium"})

    if not url.startswith('https'):
        issues.append({"issue": "Not using HTTPS", "description": "Site is not secured with SSL", "severity": "High"})

    return issues


def calculate_seo_score(issues: List[Dict[str, Any]], word_count: int, meta_tags: Dict[str, Any]) -> int:
    score = 100
    for issue in issues:
        if issue['severity'] == 'High':
            score -= 10
        elif issue['severity'] == 'Medium':
            score -= 5
        else:
            score -= 2

    if word_count < 300:
        score -= 10
    elif word_count < 600:
        score -= 5

    if not meta_tags.get('description'):
        score -= 10
    if not meta_tags.get('keywords'):
        score -= 5

    return max(0, score)


def evaluate_content_quality(content: str, url: str) -> Dict[str, Any]:
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": url,
                "X-Title": YOUR_APP_NAME,
                "Content-Type": "application/json"
            },
            json={
                "model": "nousresearch/hermes-3-llama-3.1-405b",
                "messages": [
                    {"role": "system",
                     "content": "You are an SEO expert. Evaluate the following content and provide scores and suggestions."},
                    {"role": "user",
                     "content": f"Evaluate this content:\n\n{content}\n\nProvide scores (0-10) for readability, relevance, and engagement. Also, give an overall score (0-100) and suggestions for improvement. Return the response as a JSON object."}
                ]
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        if 'choices' not in result or not result['choices']:
            raise ValueError("Unexpected response format from OpenRouter API")
        return json.loads(result['choices'][0]['message']['content'])
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to OpenRouter API: {str(e)}")
        return {"error": "Failed to evaluate content quality", "details": str(e)}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {str(e)}")
        return {"error": "Failed to parse content evaluation results", "details": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error evaluating content quality: {str(e)}")
        return {"error": "Unexpected error during content evaluation", "details": str(e)}


@router.get("/analyzer")
async def get_analyzer(url: str = Query(..., description="The URL to analyze")):
    try:
        html_content = fetch_page_content(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = extract_text_content(soup)

        with ThreadPoolExecutor(max_workers=4) as executor:
            word_count_future = executor.submit(count_words, text_content)
            keywords_future = executor.submit(extract_keywords, text_content)
            meta_tags_future = executor.submit(analyze_meta_tags, soup)
            seo_issues_future = executor.submit(check_seo_issues, soup, text_content, url)

        word_count = word_count_future.result()
        keywords = keywords_future.result()
        meta_tags = meta_tags_future.result()
        seo_issues = seo_issues_future.result()

        seo_score = calculate_seo_score(seo_issues, word_count, meta_tags)
        content_evaluation = evaluate_content_quality(text_content[:1000], url)

        response = {
            "url": url,
            "word_count": word_count,
            "keywords": keywords,
            "meta_tags": meta_tags,
            "seo_issues": seo_issues,
            "seo_score": seo_score,
            "content_evaluation": content_evaluation
        }

        return JSONResponse(response)
    except MaxRetryError:
        logger.error(f"Max retries exceeded while analyzing URL: {url}")
        raise HTTPException(
            detail="Max retries exceeded. The server might be down or not responding.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except TimeoutError:
        logger.error(f"Timed out while analyzing URL: {url}")
        raise HTTPException(detail="Timed out", status_code=status.HTTP_408_REQUEST_TIMEOUT)
    except Exception as e:
        logger.error(f"Error analyzing URL: {url}, Error: {str(e)}")
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
