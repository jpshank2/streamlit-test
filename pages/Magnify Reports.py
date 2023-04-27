import streamlit as st
# from utilities.queries import get_rows
from utilities.loading_screen import loading
# from reports.AR import create_ar_reports
# import reports.WIP as wip
from PIL import Image
from requests import get
from io import BytesIO

st.set_page_config(
    page_title='Magnify | Reports',
    layout='wide',
    page_icon=Image.open(BytesIO(get('https://i.imgur.com/sL3m54K.png').content))
)

MainHeaderImage = Image.open(BytesIO(get('https://i.imgur.com/khnCmv8.png').content))
one, two, three= st.columns(3)
two.image(MainHeaderImage, use_column_width = True)

if 'company' not in st.session_state:
    loading(st)

if 'company' in st.session_state:
    
    for session in list(st.session_state.key()):
        if session not in st.session_state['master_states']:
            del st.session_state[session]

# if 'conn' not in st.session_state:
#     st.session_state['conn'] = init_connection()
# if 'switches' not in st.session_state:
#     domain = 'demo' if st.experimental_user.email == None else st.experimental_user.email.split('@')[-1]
#     st.session_state['switches'] = get_rows(f"SELECT * FROM STREAMLITAPP.MANAGED_IDENTITY_TEST WHERE DOMAIN = '{domain}'")

    st.markdown("# Magnify Reports")

    if st.session_state['level'] == 4:
        st.markdown('[AR Reports](#ar-reports)')
        st.markdown('[WIP Reports](#wip-reports)')
        st.markdown('[Staff Reports](#staff-reports)')
    # else:
    #     st.markdown('[WIP Reports](#wip-reports)')

    # st.markdown('## random text to see if link actually works')
    # st.markdown("""I'm baby disrupt activated charcoal vaporware fashion axe. Pabst pinterest forage dreamcatcher, +1 same hashtag church-key. Post-ironic banh mi stumptown lumbersexual jianbing, kombucha tonx disrupt tote bag microdosing. Jianbing seitan wolf celiac, raw denim chia williamsburg. Kinfolk taxidermy sartorial prism yes plz, lomo chambray mlkshk food truck retro cold-pressed flannel microdosing marfa. Ascot vexillologist cronut authentic narwhal semiotics prism, mlkshk cred skateboard vinyl. Retro iPhone pop-up bruh snackwave YOLO palo santo plaid.""")

    # st.markdown("""Put a bird on it biodiesel polaroid listicle paleo tofu ethical synth flexitarian hella neutra praxis. Pork belly listicle pop-up tbh viral direct trade, blue bottle venmo tofu pug before they sold out. Live-edge schlitz tousled, PBR&B fashion axe freegan flannel bespoke kale chips lo-fi shabby chic. Fit lo-fi selvage, street art ennui raclette trust fund retro drinking vinegar paleo activated charcoal. Etsy fam succulents whatever selfies. Hoodie succulents sartorial, fixie asymmetrical mlkshk fashion axe sriracha lyft.""")

    # st.markdown("""Meh pok pok freegan letterpress. Four loko DSA gatekeep tattooed prism. Stumptown bruh single-origin coffee forage paleo JOMO hexagon typewriter woke YOLO pitchfork enamel pin. Bodega boys marfa pitchfork YOLO vaporware small batch, fam iPhone. Unicorn humblebrag distillery vexillologist banh mi typewriter bruh activated charcoal migas occupy mlkshk celiac kale chips bicycle rights tbh. Brunch JOMO lo-fi kale chips chillwave adaptogen tonx pinterest butcher.""")

    # st.markdown("""Pok pok messenger bag next level stumptown coloring book +1 plaid, vexillologist yr praxis skateboard mustache. Hella subway tile prism salvia meggings swag lomo tonx snackwave tofu paleo chartreuse messenger bag. Craft beer helvetica synth lomo Brooklyn, meh meditation. Banjo shoreditch XOXO vice adaptogen yr bruh hoodie irony single-origin coffee meggings lyft mumblecore af. Pork belly food truck jianbing sustainable disrupt. Vaporware coloring book succulents, cardigan dreamcatcher banh mi quinoa drinking vinegar subway tile chicharrones vinyl williamsburg selfies crucifix. Coloring book vape four loko af swag direct trade mixtape live-edge neutra.""")

    # st.markdown("""Drinking vinegar shoreditch ennui succulents kitsch live-edge, lomo semiotics literally. Craft beer try-hard VHS, portland vaporware bushwick iceland snackwave ramps forage tote bag. Fixie synth kogi banjo paleo. Pork belly cardigan kickstarter edison bulb hell of.""")

    # st.markdown("""Dummy text? More like dummy thicc text, amirite?""")
    
    try:
#         if 'ar' not in st.session_state:
#             st.session_state['ar'] = get_rows("""select ar.debttranunpaid,
#     c.client,
#     c.office,
#     c.client_partner, 
#     D.AGING_PERIOD_SORT, 
#     D.AGING_PERIOD as OG_PERIOD, 
#     D.MONTH_NAME AS MONTH
# from trans_ar ar
#     inner join dim_client_master c on c.contindex = ar.contindex
#     inner join dim_dates d on d.calendar_date = ar.debttrandate
# where DEBTTRANDATE >= date_from_parts(year(current_timestamp) - 3, 1, 1);""")
        exec(f"""from reports.AR import level_{st.session_state['level']}_ar as level_ar\nlevel_ar(st)""")

        exec(f"""from reports.WIP import level_{st.session_state['level']}_wip as level_wip\nlevel_wip(st)""")

        exec(f"""from reports.people import level_{st.session_state['level']}_people as level_people\nlevel_people(st)""")
    except Exception as e:
        st.write(e)