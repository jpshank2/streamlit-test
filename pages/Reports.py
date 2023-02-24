import streamlit as st
# import numpy as np
# import pandas as pd
import snowflake.connector
# import plotly.express as px
from AR import create_ar_reports

st.write("# Hello, Reports! :wave:")
st.write('[AR Reports](#AR)')
st.write('## random text to see if link actually works')
st.write("""I'm baby disrupt activated charcoal vaporware fashion axe. Pabst pinterest forage dreamcatcher, +1 same hashtag church-key. Post-ironic banh mi stumptown lumbersexual jianbing, kombucha tonx disrupt tote bag microdosing. Jianbing seitan wolf celiac, raw denim chia williamsburg. Kinfolk taxidermy sartorial prism yes plz, lomo chambray mlkshk food truck retro cold-pressed flannel microdosing marfa. Ascot vexillologist cronut authentic narwhal semiotics prism, mlkshk cred skateboard vinyl. Retro iPhone pop-up bruh snackwave YOLO palo santo plaid.

Put a bird on it biodiesel polaroid listicle paleo tofu ethical synth flexitarian hella neutra praxis. Pork belly listicle pop-up tbh viral direct trade, blue bottle venmo tofu pug before they sold out. Live-edge schlitz tousled, PBR&B fashion axe freegan flannel bespoke kale chips lo-fi shabby chic. Fit lo-fi selvage, street art ennui raclette trust fund retro drinking vinegar paleo activated charcoal. Etsy fam succulents whatever selfies. Hoodie succulents sartorial, fixie asymmetrical mlkshk fashion axe sriracha lyft.

Meh pok pok freegan letterpress. Four loko DSA gatekeep tattooed prism. Stumptown bruh single-origin coffee forage paleo JOMO hexagon typewriter woke YOLO pitchfork enamel pin. Bodega boys marfa pitchfork YOLO vaporware small batch, fam iPhone. Unicorn humblebrag distillery vexillologist banh mi typewriter bruh activated charcoal migas occupy mlkshk celiac kale chips bicycle rights tbh. Brunch JOMO lo-fi kale chips chillwave adaptogen tonx pinterest butcher.

Pok pok messenger bag next level stumptown coloring book +1 plaid, vexillologist yr praxis skateboard mustache. Hella subway tile prism salvia meggings swag lomo tonx snackwave tofu paleo chartreuse messenger bag. Craft beer helvetica synth lomo Brooklyn, meh meditation. Banjo shoreditch XOXO vice adaptogen yr bruh hoodie irony single-origin coffee meggings lyft mumblecore af. Pork belly food truck jianbing sustainable disrupt. Vaporware coloring book succulents, cardigan dreamcatcher banh mi quinoa drinking vinegar subway tile chicharrones vinyl williamsburg selfies crucifix. Coloring book vape four loko af swag direct trade mixtape live-edge neutra.

Drinking vinegar shoreditch ennui succulents kitsch live-edge, lomo semiotics literally. Craft beer try-hard VHS, portland vaporware bushwick iceland snackwave ramps forage tote bag. Fixie synth kogi banjo paleo. Pork belly cardigan kickstarter edison bulb hell of.

Dummy text? More like dummy thicc text, amirite?""")

@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

st.write('### AR Reports {#AR}')
create_ar_reports(st, conn)

# @st.cache_data(ttl=3600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         rows = cur.fetchall()
#         columns = [column[0] for column in cur.description]
#         results = list()
#         for row in rows:
#             results.append(dict(zip(columns, row)))
        
#         return pd.DataFrame(results)

# try:
#     rows = run_query("""SELECT AR.*, C.*, D.AGING_PERIOD_SORT, D.AGING_PERIOD as OG_PERIOD 
#         from TRANS_AR AR 
#             INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex 
#             INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = AR.DEBTTRANDATE 
#         WHERE DEBTTRANUNPAID <> 0;""")

#     office_office_AR = rows[['OFFICE', 'DEBTTRANUNPAID']]
#     office_office_AR = office_office_AR.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()

#     levels = [
#         st.selectbox('Office', ['All'] + [i for i in office_office_AR.OFFICE.unique()])
#     ]


#     if levels[0] == 'All':
#         office_AR_DF = office_office_AR
#         yVal = 'OFFICE'
#         title = 'AR by Office w/ drilldown'
#     else:
#         office_partner_AR = rows[rows['OFFICE'] == levels[0]]
#         office_partner_AR = office_partner_AR[['CLIENTPARTNER', 'DEBTTRANUNPAID']]
#         levels.append(st.selectbox('Client Partner', ['All'] + [i for i in office_partner_AR.CLIENTPARTNER.unique()]))

#         office_AR_DF = office_partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
#         yVal = 'CLIENTPARTNER'
#         title = levels[0] + ' AR by Client Partner w/ drilldown'

#         if levels[1] != 'All':
#             office_AR_DF = rows[(rows['OFFICE'] == levels[0]) & (rows['CLIENTPARTNER'] == levels[1])]
#             office_AR_DF = office_AR_DF[['CLIENT', 'DEBTTRANUNPAID']]
#             office_AR_DF = office_AR_DF.groupby('CLIENT', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
#             yVal = 'CLIENT'
#             title = f'{levels[1]}\'s {levels[0]} AR by Client w/ drilldown'
            
#     st.write(px.bar(office_AR_DF, x='OUTSTANDING_AR', y=yVal, orientation='h', barmode='group', title=title, text='OUTSTANDING_AR'))

#     partner_AR = rows[['CLIENTPARTNER', 'DEBTTRANUNPAID']].copy()
#     partner_AR = partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()

#     st.write(px.bar(partner_AR, y='CLIENTPARTNER', x='OUTSTANDING_AR', orientation='h', title='AR by Client Partner'))

#     aging_AR = rows[['AGING_PERIOD_SORT', 'OG_PERIOD', 'DEBTTRANUNPAID']].copy()
#     aging_AR['AGING_PERIOD'] = np.where(aging_AR['AGING_PERIOD_SORT'] < 4, aging_AR['OG_PERIOD'] + ' AR', 'Overdue 90+ AR')
#     aging_AR = aging_AR[['AGING_PERIOD', 'DEBTTRANUNPAID']]
#     aging_AR = aging_AR.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
#     st.write(px.pie(aging_AR, values='OUTSTANDING_AR', names='AGING_PERIOD', title='AR Aging Periods'))
    
# except Exception as e:
#     print(st.write(e))
