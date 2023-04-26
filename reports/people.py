from plotly.express import line
from utilities.queries import get_rows
from utilities.click_handlers import go_to_top

def level_4_people(st):
    st.markdown('## People Metrics')

    boost_df = get_rows("""select case when staff = 264 then 'Alan Carter' else 'Cameron Patterson' end as EMPLOYEE, 
        p.*
        from people.demo_boost p;""")

    boost_fig = line(boost_df, x='DATE', y='AGG', color='EMPLOYEE', markers=True)

    st.plotly_chart(boost_fig)
