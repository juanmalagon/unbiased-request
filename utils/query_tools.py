import logging
import re
import pandas as pd

from utils import country_lists as cl

# from utils import examples as ex
# from utils.functions import scopus_query_list_constructor

# Scopus
# For help on using the Scopus Search API, see:
# https://dev.elsevier.com/documentation/ScopusSearchAPI
# Scopus search tips:
# https://dev.elsevier.com/sc_search_tips.html

module_logger = logging.getLogger("main.utils.query_tools")


def language_bias_tool(query: str) -> str:
    """
    Returns a query without the language restriction.
    """
    return re.sub(r"(AND\s)*LANGUAGE\(\w+\)", "", query)


def publication_bias_tool(query: str) -> str:
    """
    Returns a query including the grey literature.
    """
    return re.sub(r"(AND\s)*SRCTYPE\(\w+\)", "", query)


def find_localization_in_text(
    text: str,
    countries: list[str] = cl.countries,
    demonyms: list[str] = cl.demonyms
) -> bool:
    """
    Returns True if any country name or demonym is found in the text.
    """
    text_words = text.lower().split()
    if any(
        location.lower() in text_words for location in countries + demonyms
    ):
        return True
    else:
        return False


def determine_localization_in_title(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add column 'localization_in_title' (boolean)
    """
    df_copy = df.copy()
    df_copy["localization_in_title"] = df["dc:title"].apply(
        find_localization_in_text
    )
    return df_copy


# Publication-bias-tool: queries including the grey literature
scopus_pub_bias_tool_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND LANGUAGE(english)"
)
