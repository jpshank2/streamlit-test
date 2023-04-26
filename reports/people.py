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

    morale_df = get_rows("""select s.staff_name, s.level, m.*, enthusiasm + meaning + pride + challenge + energy + strong + recovery + endurance as agg, monthname(m.date) as month
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

    if level_select == 'All' and staff_select != 'All':
        morale_df = morale_df[morale_df['STAFF_NAME'] == staff_select]
    elif level_select != 'All' and staff_select == 'All':
        morale_df = morale_df[morale_df['LEVEL'] == level_select]
    elif level_select != 'All' and staff_select != 'All':
        morale_df = morale_df[(morale_df['LEVEL'] == level_select) & (morale_df['STAFF_NAME'] == staff_select)]
    else:
        morale_df = morale_df
        grouped_morale_df = morale_df[['LEVEL', 'MONTH', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG']].groupby(['LEVEL', 'MONTH']).agg(AVERAGE_ENTHUSIASM=('ENTHUSIASM', 'mean'), AVERAGE_MEANING=('MEANING', 'mean'), AVERAGE_PRIDE=('PRIDE', 'mean'), AVERAGE_CHALLENGE=('CHALLENGE', 'mean'), AVERAGE_ENERGY=('ENERGY', 'mean'), AVERAGE_STRENGTH=('STRONG', 'mean'), AVERAGE_RECOVERY=('RECOVERY', 'mean'), AVERAGE_ENDURANCE=('ENDURANCE', 'mean'), AVERAGE_AGG=('AGG', 'mean'))
        color_val = 'LEVEL'
        hover_data = {'LEVEL': False, 'AVERAGE_AGG': True, 'AVERAGE_ENTHUSIASM': True, 'AVERAGE_MEANING': True, 'AVERAGE_PRIDE': True, 'AVERAGE_CHALLENGE': True, 'AVERAGE_ENERGY': True, 'AVERAGE_STRENGTH': True, 'AVERAGE_RECOVERY': True, 'AVERAGE_ENDURANCE': True}
        title = 'Average Morale by Level and Month'

    morale_viz, morale_tab = st.tabs(['Visual', 'Table'])

    morale_viz.plotly_chart(line(grouped_morale_df, x='MONTH', y='AVERAGE_AGG', color=color_val, markers=True, hover_name=color_val, hover_data=hover_data, title=title), use_container_width=True)    
    morale_tab.dataframe(morale_df[['STAFF_NAME', 'LEVEL', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG']])
