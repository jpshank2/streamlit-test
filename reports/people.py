from plotly.express import line
from utilities.queries import get_rows
from utilities.click_handlers import go_to_top

def level_1_people(st):
    st.write('people 1')

def level_2_people(st):
    st.write('people 2')

def level_3_people(st):
    st.write('people 3')

def level_4_people(st):
    st.markdown('## Staff Reports')

    boost_df = get_rows("""select case when staff = 264 then 'Alan Carter' else 'Cameron Patterson' end as EMPLOYEE, 
        p.*
        from people.demo_boost p;""")

    boost_fig = line(boost_df, x='DATE', y='AGG', color='EMPLOYEE', markers=True, hover_name='EMPLOYEE', hover_data={'EMPLOYEE': False, 'AGG': True, 'ENTHUSIASM': True, 'MEANING': True, 'PRIDE': True, 'CHALLENGE': True, 'ENERGY': True, 'STRONG': True, 'RECOVERY': True, 'ENDURANCE': True})

    boost_viz, boost_tab = st.tabs(['Visual', 'Table'])
    boost_viz.plotly_chart(boost_fig, use_container_width=True)
    boost_tab.dataframe(boost_df[['EMPLOYEE', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG']])
