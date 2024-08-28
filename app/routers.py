import json
import logging


from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pyseoanalyzer import analyze


router = APIRouter(tags=["SEO"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




@router.get("/analyzer")
async def get_analyzer(url: str):

    global output
    try:
        output = analyze(url)

        if output is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis returned no results"
            )


        page = output['pages'][0]
        warning = page['warnings']
        word_count = page['word_count']
        keyword = page['keywords']
        response = {
            "warnings": warning,
            "word_count": word_count,
            "keywords": keyword
        }
        """
        1- todo: more error checking is needed when the program goes to retry mode (urllib3)
        2- todo: parse the keywords that are getting extract in the keyword dict
        3- todo: clean up the warnings
        4- todo: extract page content from the webpage using bs4 or scrapy and connecting to an AI api inorder to 
        evaluate the content quality
        5- after getting the content quality need to evaluate the scores of each section using ai perfectly in the same 
        prompt (meaning sending the content in a text format in a json file to the AI with rest of data that we have
        inorder to have proper scoring system and suggestion field in the response
        """
        return JSONResponse(response)
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from analysis output: {output}")
        raise HTTPException(
            detail="Error decoding JSON from analysis output",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except TimeoutError:
        logger.error(f"Timed out while analyzing URL: {url}")
        raise HTTPException(detail="Timed out", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error analyzing URL: {url}, Error: {str(e)}")
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)