import streamlit as st
# from datetime import datetime

default_tweets = """lydia ko off to a solid start at evian championship.
lydia kos drawing on past experience in her bid to lift her first major trophy ahead of final round of evian championship at lake geneva.
lydia ko becomes youngest ever winner of a major at the evian.
lydia ko records first ever major title overnight youngest ever major winner.
kiwi golfer lydiako fired a bogey free eight under 63 to become the youngest winner of a womens major at the evian championship in france.
teenager ko makes history with evian win.
lydia ko takes scintillating major win in her stride.
teenager lydia ko makes history at evian.
lydia ko says she was spurred on to her major triumph by a vocal young fan during the weekend.
evian les bains france with two holes left to.
18 year old lydia ko wins evian championship to become youngest lpga major champion.
amazing teen golfer lydia ko hailed over major record.
new zealand golfer lydia ko already looking ahead to rio olympics after major success.
teenager lydia ko poised for golfing riches after evian championship win.
skysportnz lydia ko not even a mention."""

def draw_sidebar():
    # Language
    lang_name_format = {'Portuguese' : 'pt', 'English' : 'en'}
    #st.sidebar.header('Language')
    # lang = st.sidebar.radio('Language', ('English', "Portuguese"))
    lang = st.sidebar.radio('Language', ('English'))
    lang = lang_name_format[lang]

    # Tools
    st.sidebar.header('Extraction tools')

    st.sidebar.subheader('Actor entity extraction')
    ACTOR_ENTITY_EXTRACTION_TOOLS = {'spacy' : False, 'nltk' : False}
    # ACTOR_ENTITY_EXTRACTION_TOOLS = {'spacy' : False}
    ACTOR_ENTITY_EXTRACTION_TOOLS['spacy']    = st.sidebar.checkbox('spaCy', key='1', value=True)
    ACTOR_ENTITY_EXTRACTION_TOOLS['nltk']     = st.sidebar.checkbox('NLTK', key='2', value=False)

    st.sidebar.subheader('Time entity extraction')
    TIME_ENTITY_EXTRACTION_TOOLS = {'py_heideltime' : False}
    TIME_ENTITY_EXTRACTION_TOOLS['py_heideltime'] = st.sidebar.checkbox('py_heideltime', key='4', value=True)

    st.sidebar.subheader('Event entity extraction')
    EVENT_ENTITY_EXTRACTION_TOOLS = {'spacy' : False}
    EVENT_ENTITY_EXTRACTION_TOOLS['spacy'] = st.sidebar.checkbox('spacy', key='5', value=True)

    st.sidebar.subheader('Objectal link extraction')
    OBJECTAL_LINK_EXTRACTION_TOOLS  = {'spacy' : False}
    OBJECTAL_LINK_EXTRACTION_TOOLS['spacy'] = st.sidebar.checkbox('spacy', key='6', value=True)

    return lang, {'actor_extraction_tools'              : [tool for tool in ACTOR_ENTITY_EXTRACTION_TOOLS if ACTOR_ENTITY_EXTRACTION_TOOLS[tool]],
                  'time_extraction_tools'               : [tool for tool in TIME_ENTITY_EXTRACTION_TOOLS if TIME_ENTITY_EXTRACTION_TOOLS[tool]],
                  'event_extraction_tools'              : [tool for tool in EVENT_ENTITY_EXTRACTION_TOOLS if EVENT_ENTITY_EXTRACTION_TOOLS[tool]],
                  'objectal_link_extraction_tools'      : [tool for tool in OBJECTAL_LINK_EXTRACTION_TOOLS if OBJECTAL_LINK_EXTRACTION_TOOLS[tool]]
                 }


def valid_input(tools, narrative_text):
    # Check if it's selected, at least, one tool per extraction
    for key in tools:
        if len(tools[key]) == 0:
            signal_error(key)
            return False

    # Check if narrative text isn't empty
    if narrative_text == '':
        signal_error('narrative_text')
        return False

    return True


def signal_error(input_error_code):
    if input_error_code == 'actor_extraction_tools':
        st.error('You need to specify at least one tool to the actor extraction!')
    elif input_error_code == 'timex_extraction_tools':
        st.error('You need to specify at least one tool to the time extraction!')
    elif input_error_code == 'event_extraction_tools':
        st.error('You need to specify at least one tool to the event extraction!')
    elif input_error_code == 'objectal_extraction_tools':
        st.error('You need to specify at least one tool to the objectal extraction!')
    elif input_error_code == 'semanticrole_extraction_tools':
        st.error('You need to specify at least one tool to the semantic role extraction!')

def app():
    """
    Returns
    -------
    [] - If no valid configuration to start extraction
    [lang : str, publication_time : str, narrative_text : str, tools : {str -> [str]}] - If valid configuration to start extraction (follow to output phase)
    """
    lang, tools = draw_sidebar()

    publication_time = str(st.date_input('Publication Date'))
    narrative_text = st.text_area(label='Narrative Text', value=default_tweets, height=300)

    pressed_extract = st.button('Extract!')

    if pressed_extract and valid_input(tools, narrative_text):
        return [lang, publication_time, narrative_text, tools]
    else:
        return []
