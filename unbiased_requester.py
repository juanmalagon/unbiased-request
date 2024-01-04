from resources.examples import mergoni_2021_scopus_query, mergoni_2021_max_date
from resources.querying_tools import (
    language_bias_tool,
    publication_bias_tool,
    localization_bias_tool,
)
from resources.scopus_functions import (
    retrieve_results_from_list_of_queries,
    columns_to_hide,
)
import logging
import streamlit as st


# Set up logging
# Create logger with 'main'
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
# Create file handler which logs even debug messages
fh = logging.FileHandler('main.log')
fh.setLevel(logging.DEBUG)
# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# Create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - [%(module)s|%(funcName)s] - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Set up Streamlit

# Instructions

st.markdown(
    """
    # Unbiased Requester

    This app allows you to retrieve data from
    <a href="https://www.scopus.com/">Scopus</a> and then apply a set of
    querying tools to assess language, publication, availability and
    localization bias from your original query.

    The app is the accompanying material of the paper:

    Malagon J, Haelermans C. _Reading between the lines: biases and
    reproducibility challenges in efficiency of education reviews. 2023_


    ### How to use it

    1. Insert your original query string in the first text box (for help on how
    to create your query string see <a
    href="https://dev.elsevier.com/sc_search_tips.html"> Scopus search tips
    </a>).\n
    \t (Optional: Insert a maximum date in the second text box for extra
    filtering . This date usually corresponds to the publication date of the
    paper you are reviewing or writing).\n
    \t If you rather prefer to load an example query and maximum date for extra
    filtering, check the box below.
    2. Click on the checkbox "Retrieve data from your original query" to
    retrieve data from your original query.
    3. Click on the checkbox "Apply language-bias-tool" to retrieve data from
    your original query without language bias.
    4. Click on the checkbox "Apply publication-bias-tool" to retrieve data
    from your original query without publication bias.
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    ### Retrieve data
    """,
    unsafe_allow_html=True,
)
st.text_input("Insert your original query", key="original_query")
st.text_input("(Optional: Insert a maximum date for extra filtering)",
              key="max_date")

if st.checkbox("Load an example query and maximum date for extra filtering \
               (Mergoni and De Witte, 2022)"):
    del st.session_state.original_query
    del st.session_state.max_date
    st.session_state.original_query = mergoni_2021_scopus_query
    st.session_state.max_date = mergoni_2021_max_date

"This is your original query:"
st.session_state.original_query
"This is your maximum date for extra filtering:"
st.session_state.max_date


@st.cache_data
def load_data(query, max_date):
    data = retrieve_results_from_list_of_queries(
        list_of_queries=[query], max_date=max_date
    )
    return data


@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')


# Retrieve data from original query

if st.checkbox("Retrieve data from your original query"
               ):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_original = load_data(
        st.session_state.original_query, st.session_state.max_date
    )
    data_load_state.text(
        f"Data loaded! Retrieved {len(data_original)} results.")
    data_original_to_display = data_original.drop(columns=columns_to_hide)
    if st.checkbox("\t Show original data"):
        st.write("Original query data")
        st.write(data_original_to_display)
        st.download_button('Download CSV',
                           convert_df(data_original_to_display),
                           'original_query_data',
                           'text/csv',
                           key="download_original_query_data")

st.markdown(
    """
    ### Apply querying tools
    """,
    unsafe_allow_html=True,
)

st.session_state.lang_bias_query = language_bias_tool(
    st.session_state.original_query)
st.session_state.pub_bias_query = publication_bias_tool(
    st.session_state.original_query
)

# Language bias tool

if st.checkbox("Apply language-bias-tool"):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_lang = load_data(
        st.session_state.lang_bias_query, st.session_state.max_date)
    data_load_state.text(
        "Data loaded!\n" +
        f"Retrieved {len(data_lang)} results from language-bias-tool.\n" +
        "This means the tool retrieved " +
        f"{len(data_lang) - len(data_original)} additional records."
        )
    if st.checkbox("\t Show language-bias-tool additional records"):
        data_lang_diff = data_lang[
            ~data_lang['dc:identifier'].isin(
                data_original['dc:identifier'])].reset_index(drop=True)
        data_lang_diff_to_display = data_lang_diff.drop(
            columns=columns_to_hide)
        st.write("Language-bias-tool data")
        st.write(data_lang_diff_to_display)
        st.download_button('Download CSV',
                           convert_df(data_lang_diff_to_display),
                           'lang_bias_tool_data',
                           'text/csv',
                           key="download_lang_bias_tool_data")

# Publication bias tool

if st.checkbox("Apply publication-bias-tool"):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_pub = load_data(
        st.session_state.pub_bias_query, st.session_state.max_date)
    data_load_state.text(
        "Data loaded!\n" +
        f"Retrieved {len(data_pub)} results from publication-bias-tool.\n" +
        "This means the tool retrieved " +
        f"{len(data_pub) - len(data_original)} additional records."
        )

    if st.checkbox("\t Show publication-bias-tool data additional records"):
        data_pub_diff = data_pub[
            ~data_pub['dc:identifier'].isin(
                data_original['dc:identifier'])].reset_index(drop=True)
        data_pub_diff_to_display = data_pub_diff.drop(
            columns=columns_to_hide)
        st.write("Publication-bias-tool data")
        st.write(data_pub_diff_to_display)
        st.download_button('Download CSV',
                           convert_df(data_pub_diff_to_display),
                           'pub_bias_tool_data',
                           'text/csv',
                           key="download_pub_bias_tool_data")

# Localization bias tool

if st.checkbox("Apply localization-bias-tool"):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_localized = localization_bias_tool(
        st.session_state.original_query, st.session_state.max_date)
    data_localized__weird = data_localized[
        data_localized['localized_weird']]
    data_localized__no_weird = data_localized[
        data_localized['localized_no_weird']]
    nr_titles__weird = data_localized__weird['localization_in_title'].sum()
    nr_titles__no_weird = data_localized__no_weird[
        'localization_in_title'].sum()

    data_load_state.text(
        "Data loaded!\n" +
        f"Retrieved {len(data_localized)} localized results with the " +
        "localization-bias-tool.\n" +
        f"{len(data_localized__weird)} results come from WEIRD countries, \n" +
        f" but only {nr_titles__weird} of these have localization in title " +
        f"({round(100*nr_titles__weird/len(data_localized__weird),1)}%).\n" +
        f"{len(data_localized__no_weird)} results come from non-WEIRD " +
        "countries, \n but only " +
        f"{nr_titles__no_weird} of these have localization in title " +
        f"({round(100*nr_titles__no_weird/len(data_localized__no_weird),1)}%)."
        )
    data_localized_to_display = data_localized.drop(
        columns=columns_to_hide)

    if st.checkbox("\t Show localization-bias-tool data records"):
        st.write("Localization-bias-tool data")
        st.write(data_localized_to_display)
        st.download_button('Download CSV',
                           convert_df(data_localized_to_display),
                           'localization_bias_tool_data',
                           'text/csv',
                           key="download_localization_bias_tool_data")

# Availability bias tool

if st.checkbox("Apply availability-bias-tool"):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_available = data_original.copy()
    data_available_summary = data_available.groupby(
        'openaccess').agg({'dc:identifier': 'count'}).reset_index()
    nr_open_access_records = data_available_summary[
        data_available_summary['openaccess']].iloc[0, 1]
    availability_benchmark = nr_open_access_records/len(data_available)
    data_load_state.text(
        "Data loaded!\n" +
        f"Retrieved {len(data_available)} results with the " +
        " availability-bias-tool.\n" +
        "Out of these results " +
        f"{nr_open_access_records} are open-access records.\n" +
        f"This corresponds to {round(100*availability_benchmark,1)}% of " +
        "the total records."
        )

    if st.checkbox("\t Show availability-bias-tool data records"):
        data_available_diff = data_available[
            data_available['openaccess']].reset_index(drop=True)
        st.write("Availability-bias-tool data")
        st.write(data_available_diff)
        st.download_button('Download CSV',
                           convert_df(data_available_diff),
                           'availability_bias_tool_data',
                           'text/csv',
                           key="download_availability_bias_tool_data")
