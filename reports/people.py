from plotly.express import line, pie
from utilities.queries import get_rows
from utilities.click_handlers import go_to_top
from datetime import datetime

def level_1_people(st):
    return True

def level_2_people(st):
    return True

def level_3_people(st):
    return True

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
        FROM PE.TRANS_WIP
        WHERE wipdate >= '2023-01-01'
        GROUP BY STAFFINDEX, month(WIPDATE)) WIP ON WIP.STAFFINDEX = P.STAFF AND WIP.WIPMONTH = MONTH(P.DATE) 
        ORDER BY STAFF, DATE;""", st.session_state['today'])

    boost_fig = line(boost_df, x='DATE', y='AGG', color='EMPLOYEE', markers=True, hover_name='EMPLOYEE', hover_data={'EMPLOYEE': False, 'AGG': True, 'ENTHUSIASM': True, 'MEANING': True, 'PRIDE': True, 'CHALLENGE': True, 'ENERGY': True, 'STRONG': True, 'RECOVERY': True, 'ENDURANCE': True}, title='Staff with Significant Morale Drops')

    boost_viz, boost_tab = st.tabs(['Visual', 'Table'])
    boost_viz.plotly_chart(boost_fig, use_container_width=True)
    boost_tab.dataframe(boost_df[['EMPLOYEE', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG', 'TOTAL_HOURS', 'UTILIZATION']])

    morale_df = get_rows("""select s.staff_name, s.level, m.*, enthusiasm + meaning + pride + challenge + energy + strong + recovery + endurance as agg, monthname(m.date) as month
        from people.morale m
            inner join PE.DIM_ANON_STAFF s on s.staffindex = m.staff
        where s.staff_status = 'Active' and
            s.level not in ('No Selection', 'Unknown');""", st.session_state['today'])

    from pandas import to_datetime
    morale_df['DATE'] = to_datetime(morale_df['DATE'])
    morale_df['DATE'] = morale_df['DATE'].dt.strftime('%m / %Y')
    
    level_drop, staff_drop = st.columns(2)
    level_select = level_drop.selectbox('Staff Level', ['All'] + [i for i in morale_df.LEVEL.sort_values().unique()])
    if level_select == 'All':
        staff_select = staff_drop.selectbox('Staff', ['All'] + [i for i in morale_df.STAFF_NAME.sort_values().unique()])
    else:
        staff_select = staff_drop.selectbox('Staff', ['All'] + [i for i in morale_df[morale_df['LEVEL'] == level_select].STAFF_NAME.sort_values().unique()])

    if staff_select != 'All':
        morale_df = morale_df[morale_df['STAFF_NAME'] == staff_select]
        grouped_morale_df = morale_df[['STAFF_NAME', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG']].groupby(['STAFF_NAME', 'DATE'], as_index=False).agg(AVERAGE_ENTHUSIASM=('ENTHUSIASM', 'mean'), AVERAGE_MEANING=('MEANING', 'mean'), AVERAGE_PRIDE=('PRIDE', 'mean'), AVERAGE_CHALLENGE=('CHALLENGE', 'mean'), AVERAGE_ENERGY=('ENERGY', 'mean'), AVERAGE_STRENGTH=('STRONG', 'mean'), AVERAGE_RECOVERY=('RECOVERY', 'mean'), AVERAGE_ENDURANCE=('ENDURANCE', 'mean'), AVERAGE_AGG=('AGG', 'mean')).reset_index()
        color_val = 'STAFF_NAME'
        hover_data = {'STAFF_NAME': False, 'AVERAGE_AGG': True, 'AVERAGE_ENTHUSIASM': True, 'AVERAGE_MEANING': True, 'AVERAGE_PRIDE': True, 'AVERAGE_CHALLENGE': True, 'AVERAGE_ENERGY': True, 'AVERAGE_STRENGTH': True, 'AVERAGE_RECOVERY': True, 'AVERAGE_ENDURANCE': True}
        title = 'Average Morale by Staff and Month'
    elif level_select != 'All' and staff_select == 'All':
        morale_df = morale_df[morale_df['LEVEL'] == level_select]
        grouped_morale_df = morale_df[['STAFF_NAME', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG']].groupby(['STAFF_NAME', 'DATE'], as_index=False).agg(AVERAGE_ENTHUSIASM=('ENTHUSIASM', 'mean'), AVERAGE_MEANING=('MEANING', 'mean'), AVERAGE_PRIDE=('PRIDE', 'mean'), AVERAGE_CHALLENGE=('CHALLENGE', 'mean'), AVERAGE_ENERGY=('ENERGY', 'mean'), AVERAGE_STRENGTH=('STRONG', 'mean'), AVERAGE_RECOVERY=('RECOVERY', 'mean'), AVERAGE_ENDURANCE=('ENDURANCE', 'mean'), AVERAGE_AGG=('AGG', 'mean')).reset_index()
        color_val = 'STAFF_NAME'
        hover_data = {'STAFF_NAME': False, 'AVERAGE_AGG': True, 'AVERAGE_ENTHUSIASM': True, 'AVERAGE_MEANING': True, 'AVERAGE_PRIDE': True, 'AVERAGE_CHALLENGE': True, 'AVERAGE_ENERGY': True, 'AVERAGE_STRENGTH': True, 'AVERAGE_RECOVERY': True, 'AVERAGE_ENDURANCE': True}
        title = 'Average Morale by Staff and Month'
    else:
        morale_df = morale_df
        grouped_morale_df = morale_df[['LEVEL', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG']].groupby(['LEVEL', 'DATE'], as_index=False).agg(AVERAGE_ENTHUSIASM=('ENTHUSIASM', 'mean'), AVERAGE_MEANING=('MEANING', 'mean'), AVERAGE_PRIDE=('PRIDE', 'mean'), AVERAGE_CHALLENGE=('CHALLENGE', 'mean'), AVERAGE_ENERGY=('ENERGY', 'mean'), AVERAGE_STRENGTH=('STRONG', 'mean'), AVERAGE_RECOVERY=('RECOVERY', 'mean'), AVERAGE_ENDURANCE=('ENDURANCE', 'mean'), AVERAGE_AGG=('AGG', 'mean')).reset_index()
        color_val = 'LEVEL'
        hover_data = {'LEVEL': False, 'AVERAGE_AGG': True, 'AVERAGE_ENTHUSIASM': True, 'AVERAGE_MEANING': True, 'AVERAGE_PRIDE': True, 'AVERAGE_CHALLENGE': True, 'AVERAGE_ENERGY': True, 'AVERAGE_STRENGTH': True, 'AVERAGE_RECOVERY': True, 'AVERAGE_ENDURANCE': True}
        title = 'Average Morale by Level and Month'

    morale_viz, morale_tab = st.tabs(['Visual', 'Table'])

    morale_viz.plotly_chart(line(grouped_morale_df, x='DATE', y='AVERAGE_AGG', color=color_val, markers=True, hover_name=color_val, hover_data=hover_data, title=title), use_container_width=True)    
    morale_tab.dataframe(morale_df[['STAFF_NAME', 'LEVEL', 'DATE', 'ENTHUSIASM', 'MEANING', 'PRIDE', 'CHALLENGE', 'ENERGY', 'STRONG', 'RECOVERY', 'ENDURANCE', 'AGG']])

    review_df = get_rows(f"""select r.Date,
        date_trunc('MONTH', r.DATE) as MONTH_YEAR,
        r.project,
        s.employee as Sender,
        rec.employee as Recipient,
        r.rating,
        r.see_more,
        r.see_less
    from people.review r
        inner join PE.DIM_ANON_STAFF s on s.staffindex = r.sender
        inner join PE.DIM_ANON_STAFF rec on rec.staffindex = r.recipient
    where r.Date BETWEEN '{datetime(st.session_state['fye'] - 2, st.session_state['company'].FISCAL_MONTH.iloc[0], 1).strftime('%Y-%m-%d')}' AND '{datetime(st.session_state['fye'] - 1, st.session_state['company'].FISCAL_MONTH.iloc[0], 1)}'
    ORDER BY R.DATE;""", st.session_state['today'])

    # review_df['MONTH_YEAR'] = to_datetime(review_df['DATE'])
    # review_df['MONTH_YEAR'] = review_df['MONTH_YEAR'].dt.strftime('%m / %Y')

    st.markdown('### Review Reports')
    
    review_pie, review_tab = st.columns(2)

    sender_select = review_pie.selectbox('Sender', ['All'] + [i for i in review_df.SENDER.sort_values().unique()])
    recipient_select = review_tab.selectbox('Recipient', ['All'] + [i for i in review_df.RECIPIENT.sort_values().unique()])

    if sender_select == 'All' and recipient_select == 'All':
        review_df = review_df

        # grouped_review_df = review_df[['PROJECT', 'MONTH_YEAR']].groupby('MONTH_YEAR', as_index=False).agg(TOTAL_REVIEWS=('PROJECT', 'count')).reset_index()
    elif sender_select == 'All' and recipient_select != 'All':
        review_df = review_df[review_df['RECIPIENT'] == recipient_select]

        # grouped_review_df = review_df[['PROJECT', 'MONTH_YEAR']].groupby('MONTH_YEAR', as_index=False).agg(TOTAL_REVIEWS=('PROJECT', 'count')).reset_index()
    elif sender_select != 'All' and recipient_select == 'All':
        review_df = review_df[review_df['SENDER'] == sender_select]

        # grouped_review_df = review_df[['PROJECT', 'MONTH_YEAR']].groupby('MONTH_YEAR', as_index=False).agg(TOTAL_REVIEWS=('PROJECT', 'count')).reset_index()
    else:
        review_df = review_df[(review_df['SENDER'] == sender_select) & (review_df['RECIPIENT'] == recipient_select)]

        
    grouped_review_df = review_df[['PROJECT', 'MONTH_YEAR']].groupby('MONTH_YEAR', as_index=False).agg(TOTAL_REVIEWS=('PROJECT', 'count')).reset_index()


    review_tab.dataframe(review_df[['DATE', 'PROJECT', 'SENDER', 'RECIPIENT', 'RATING', 'SEE_MORE', 'SEE_LESS']])
    review_pie.plotly_chart(pie(review_df.groupby('RATING', as_index=False).agg(TOTAL=('RATING', 'count')).reset_index(), values='TOTAL', names='RATING', title='Reviews Ratings').update_layout({'legend_orientation': "h"}))

    st.plotly_chart(line(grouped_review_df, x='MONTH_YEAR', y='TOTAL_REVIEWS', markers=True, title='Reviews Timeline'), use_container_width=True)

    go_to_top(st.markdown)
