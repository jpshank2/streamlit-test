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
        p.*,
        WIP.TOTAL_HOURS
        ,WIP.UTILIZATION
        from people.demo_boost p
            INNER JOIN (SELECT STAFFINDEX
            ,MONTH(WIPDATE) AS WIPMONTH
            ,SUM(WIPHOURS) AS TOTAL_HOURS
            ,ROUND(SUM(CASE WHEN BILLABLE = 'True' THEN WIPHOURS ELSE 0 END) / SUM(WIPHOURS) * 100, 2) AS UTILIZATION
        FROM trans_wip
        WHERE wipdate >= '2023-01-01'
        GROUP BY STAFFINDEX, month(WIPDATE)) WIP ON WIP.STAFFINDEX = P.STAFF AND WIP.WIPMONTH = MONTH(P.DATE) 
        ORDER BY STAFF, DATE;""")

    boost_fig = line(boost_df, x='DATE', y='AGG', color='EMPLOYEE', markers=True, hover_name='EMPLOYEE', hover_data={'EMPLOYEE': False, 'AGG': True, 'ENTHUSIASM': True, 'MEANING': True, 'PRIDE': True, 'CHALLENGE': True, 'ENERGY': True, 'STRONG': True, 'RECOVERY': True, 'ENDURANCE': True}, title='Staff with Significant Morale Drops')

    boost_viz, boost_tab = st.tabs(['Visual', 'Table'])
    boost_viz.plotly_chart(boost_fig, use_container_width=True)
    boost_tab.dataframe(boost_df[['EMPLOYEE', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG', 'TOTAL_HOURS', 'UTILIZATION']])

    morale_df = get_rows("""select s.staff_name, s.level, m.*, enthusiasm + meaning + pride + challenge + energy + strong + recovery + endurance as agg, month(m.date) as month
        from people.morale m
            inner join dim_staff_master s on s.staffindex = m.staff
        where s.staff_status = 'Active' and
            s.level not in ('No Selection', 'Unknown');""")
    
    level_drop, staff_drop = st.columns(2)
    level_select = level_drop.selectbox('Staff Level', ['All'] + [i for i in morale_df.LEVEL.sort_values().unique()])
    if level_select == 'All':
        staff_select = staff_drop.selectbox('Staff', ['All'] + [i for i in morale_df.STAFF_NAME.sort_values().unique()])
    else:
        staff_select = staff_drop.selectbox('Staff', ['All'] + [i for i in morale_df[morale_df['LEVEL'] == level_select].STAFF_NAME.sort_values().unique()])
    
    st.dataframe(morale_df)
