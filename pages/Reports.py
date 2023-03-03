import streamlit as st
from snowflake.connector import connect
from reports.AR import create_ar_reports
from reports.WIP import create_wip_reports

def go_to_top():
    return st.markdown('[Top of Page](#hello-reports)')

st.markdown("# Hello, Reports! :wave:")

st.markdown('[AR Reports](#ar-reports)')
st.markdown('[WIP Reports](#wip-reports)')

st.markdown('## random text to see if link actually works')
st.write("""I'm baby disrupt activated charcoal vaporware fashion axe. Pabst pinterest forage dreamcatcher, +1 same hashtag church-key. Post-ironic banh mi stumptown lumbersexual jianbing, kombucha tonx disrupt tote bag microdosing. Jianbing seitan wolf celiac, raw denim chia williamsburg. Kinfolk taxidermy sartorial prism yes plz, lomo chambray mlkshk food truck retro cold-pressed flannel microdosing marfa. Ascot vexillologist cronut authentic narwhal semiotics prism, mlkshk cred skateboard vinyl. Retro iPhone pop-up bruh snackwave YOLO palo santo plaid.

Put a bird on it biodiesel polaroid listicle paleo tofu ethical synth flexitarian hella neutra praxis. Pork belly listicle pop-up tbh viral direct trade, blue bottle venmo tofu pug before they sold out. Live-edge schlitz tousled, PBR&B fashion axe freegan flannel bespoke kale chips lo-fi shabby chic. Fit lo-fi selvage, street art ennui raclette trust fund retro drinking vinegar paleo activated charcoal. Etsy fam succulents whatever selfies. Hoodie succulents sartorial, fixie asymmetrical mlkshk fashion axe sriracha lyft.

Meh pok pok freegan letterpress. Four loko DSA gatekeep tattooed prism. Stumptown bruh single-origin coffee forage paleo JOMO hexagon typewriter woke YOLO pitchfork enamel pin. Bodega boys marfa pitchfork YOLO vaporware small batch, fam iPhone. Unicorn humblebrag distillery vexillologist banh mi typewriter bruh activated charcoal migas occupy mlkshk celiac kale chips bicycle rights tbh. Brunch JOMO lo-fi kale chips chillwave adaptogen tonx pinterest butcher.

Pok pok messenger bag next level stumptown coloring book +1 plaid, vexillologist yr praxis skateboard mustache. Hella subway tile prism salvia meggings swag lomo tonx snackwave tofu paleo chartreuse messenger bag. Craft beer helvetica synth lomo Brooklyn, meh meditation. Banjo shoreditch XOXO vice adaptogen yr bruh hoodie irony single-origin coffee meggings lyft mumblecore af. Pork belly food truck jianbing sustainable disrupt. Vaporware coloring book succulents, cardigan dreamcatcher banh mi quinoa drinking vinegar subway tile chicharrones vinyl williamsburg selfies crucifix. Coloring book vape four loko af swag direct trade mixtape live-edge neutra.

Drinking vinegar shoreditch ennui succulents kitsch live-edge, lomo semiotics literally. Craft beer try-hard VHS, portland vaporware bushwick iceland snackwave ramps forage tote bag. Fixie synth kogi banjo paleo. Pork belly cardigan kickstarter edison bulb hell of.

Dummy text? More like dummy thicc text, amirite?""")

@st.cache_resource
def init_connection():
    return connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

try:
    st.markdown('### AR Reports')
    go_to_top()
    create_ar_reports(st, conn)

    st.markdown('### WIP Reports')
    go_to_top()
    create_wip_reports(st, conn)
except Exception as e:
    st.write(e)