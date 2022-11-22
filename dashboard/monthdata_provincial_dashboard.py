# -*- coding: utf-8 -*-
import copy
import re

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash

# provinces we visualize
provinces = ["guangdong", "jiangsu", "heilongjiang", "tibet"]
province_labels = ["Guangdong", "Jiangsu", "Heilongjiang", "Tibet"]
default_province = "heilongjiang"
default_years = ['2019', '2020', '2021', '2022']


def import_total_sale_data(province):
    # import monthly sales data per province
    df = pd.read_csv("../dataset/monthly/provincial/" + province + "_total_sale_monthly.csv")
    df.head(10)
    # remove lines of data with empty values
    df.dropna(axis='index', how='any', inplace=True)
    df.head()
    return df


def import_floor_space_data(province):
    # import monthly floor space data per province
    df_f = pd.read_csv("../dataset/monthly/provincial/" + province + "_floor_space_monthly.csv")
    df_f.head(10)
    # remove lines of data with empty values
    df_f.dropna(axis='index', how='any', inplace=True)
    df_f.head()
    return df_f


# 画销售额折线图
def paint_fig_ts(years=default_years, province=default_province):
    df = import_total_sale_data(province)
    
    # 分别筛选出每年的数据
    for y in years:
        df_crb = df[df['Building Type'].isin(['Commercialized Residential Buildings Sold']) & df['Date'].str.contains(
            '|'.join(years))]
    
    # 编辑hover显示的数据
    hover_text_crb = []
    for index, row in df_crb.iterrows():
        hover_text_crb.append(('<b>{BuildingType}</b><br>' +
                               '{Date}<br>' +
                               '{Total_Sale}(100 million yuan)').format(
            Date=row['Date'],
            BuildingType=row['Building Type'],
            Total_Sale=row['Total Sale (100 million yuan)']
        
        ))

    # 开始画图
    trace_ts_2 = go.Scatter(x=df_crb["Date"], y=df_crb["Total Sale (100 million yuan)"],
                            name="Commercialized Residential Buildings", mode="lines", text=hover_text_crb,
                            hoverinfo="text", marker_color='#7eb0d5')
    
    trace_ts = [trace_ts_2]
    layout = go.Layout(
        barmode='stack',
        # title_text="Total Sales of Different Buildings per Month",
        # title_font_color='#425066'
    )
    fig_ts = go.Figure(data=trace_ts, layout=layout)
    return fig_ts


# 画完工面积堆叠图
def paint_fig_fs(years=default_years, province=default_province):
    df_f = import_floor_space_data(province)
    
    # 按年份&建筑类型筛选数据
    for y in years:
        df_CB_F = df_f[df_f['Building Type'].isin(['Real Estate Total']) & df_f['Date'].str.contains('|'.join(years))]
        df_CRB_F = df_f[
            df_f['Building Type'].isin(['Commercialized Residential']) & df_f['Date'].str.contains('|'.join(years))]
        df_OB_F = df_f[df_f['Building Type'].isin(['Office Buildings']) & df_f['Date'].str.contains('|'.join(years))]
        df_HBU_F = df_f[
            df_f['Building Type'].isin(['Houses for Business Use']) & df_f['Date'].str.contains('|'.join(years))]
        
    # 编辑hover数据
    hover_text_CB_F = []
    for index, row in df_CB_F.iterrows():
        hover_text_CB_F.append(('<b>{BuildingType}</b><br>' +
                                '{Date}<br>' +
                                '{Floor_space}(10000 sq.m)').format(
            Date=row['Date'],
            BuildingType=row['Building Type'],
            Floor_space=row['Floor Space Completed (10000 sq.m)']
        ))
    hover_text_CRB_F = []
    for index, row in df_CRB_F.iterrows():
        hover_text_CRB_F.append(('<b>{BuildingType}</b><br>' +
                                 '{Date}<br>' +
                                 '{Floor_space}(10000 sq.m)').format(
            Date=row['Date'],
            BuildingType=row['Building Type'],
            Floor_space=row['Floor Space Completed (10000 sq.m)']
        
        ))
    hover_text_OB_F = []
    for index, row in df_OB_F.iterrows():
        hover_text_OB_F.append(('<b>{BuildingType}</b><br>' +
                                '{Date}<br>' +
                                '{Floor_space}(10000 sq.m)').format(
            Date=row['Date'],
            BuildingType=row['Building Type'],
            Floor_space=row['Floor Space Completed (10000 sq.m)']
        
        ))
    hover_text_HBU_F = []
    for index, row in df_HBU_F.iterrows():
        hover_text_HBU_F.append(('<b>{BuildingType}</b><br>' +
                                 '{Date}<br>' +
                                 '{Floor_space}(10000 sq.m)').format(
            Date=row['Date'],
            BuildingType=row['Building Type'],
            Floor_space=row['Floor Space Completed (10000 sq.m)']
        
        ))
    
    # 开始画图
    trace_fs_2 = go.Bar(x=df_CRB_F["Date"], y=df_CRB_F["Floor Space Completed (10000 sq.m)"],
                        name="Commercialized Residential Buildings", hovertext=hover_text_CRB_F, text=[],
                        hoverinfo="text", marker_color='#7eb0d5')
    trace_fs_3 = go.Bar(x=df_OB_F["Date"], y=df_OB_F["Floor Space Completed (10000 sq.m)"], name="Office Buildings",
                        hovertext=hover_text_OB_F, text=[], hoverinfo="text", marker_color='#b2e061')
    trace_fs_4 = go.Bar(x=df_HBU_F["Date"], y=df_HBU_F["Floor Space Completed (10000 sq.m)"],
                        name="Houses for Business Use", hovertext=hover_text_HBU_F, text=[], hoverinfo="text",
                        marker_color='#bd7ebe')
    
    trace_fs = [trace_fs_2, trace_fs_3, trace_fs_4]
    layout = go.Layout(
        
        barmode='stack',
        
        # title_text="Floor Space Completed of Different Buildings per Month",
        # title_font_color="#425066"
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title_text=''
        )
    
    )
    fig_fs = go.Figure(data=trace_fs, layout=layout)
    return fig_fs


# 获取月度数据
def get_month_data(month='2022/08', province=default_province):
    df_f = import_floor_space_data(province)
    return df_f[df_f['Date'].str.contains(month)]


# 画完工面积和销售面积比值的treemap
parent = ["", "", ""]
colors = [
    '#B0C4DE',
    '#B0C4DE',
    '#B0C4DE']
layout_tree = go.Layout(
    title_text="Ratio of Floor Space Completed to Floor Space Sold of Different Buildings per Month",
    title_font_color="#425066",

)


def paint_fig_treemap(province=default_province):
    hover_text = []
    
    month_data = get_month_data(province=province)
    
    for index, row in month_data.iterrows():
        hover_text.append(('Month:{}<br>' +
                           'Proportion:<b>{:.2%}</b>').format(
            row['Date'],
            row['Proportion']
        ))
    trace_init = go.Treemap(
        labels=month_data['Building Type'],
        parents=parent,
        values=month_data['Proportion'],
        marker_colors=colors,
        text=hover_text,
        hoverinfo="text"
    )
    
    figtreemap = go.Figure(data=trace_init, layout=layout_tree)
    
    return figtreemap


# dashboard
year_list = ['2019', '2020', '2021', '2022']

app = JupyterDash(external_stylesheets=[dbc.themes.SPACELAB])

app.layout = html.Div([
    dbc.Card([dbc.CardHeader("Monthly Data by Province"),
              dbc.CardBody(
                  dbc.Row([
                      dcc.Dropdown(id="province",
                                   options=[
                                       {"label": province_labels[i], "value": provinces[i]}
                                       for i in range(len(provinces))],
                                   value=default_province, clearable=False)
        
                  ]))]),
    
    dbc.Card([dbc.CardHeader("Total Sales of Different Buildings per Month"),
              dbc.CardBody(
        
                  dbc.Row([
            
                      dbc.Col([dbc.Row([dbc.Col(
                          dcc.RangeSlider(2019, 2022, step=None, marks={
                              2019: '2019',
                              2020: '2020',
                              2021: '2021',
                              2022: '2022',
                    
                          }, value=[2019, 2022], id='year-range-slider')
                          # dbc.Checklist(
                          # id="YearChecklist",
                          # options=[{"label": e, "value": e} for e in year_list],
                          ##inline=True
                          # ),
                      )]),
                
                          dcc.Graph(
                              id='fig_ts',
                              figure=paint_fig_ts())
            
                      ], width=12)
        
                  ]))]),
    dbc.Card([dbc.CardHeader("Floor Space Completed of Different Buildings per Month"),
              dbc.CardBody(
        
                  dbc.Row(children=[
            
                      dbc.Col(children=[
                          dbc.Row([dbc.Col(
                              dcc.RangeSlider(2019, 2022, step=None, marks={
                                  2019: '2019',
                                  2020: '2020',
                                  2021: '2021',
                                  2022: '2022',
                        
                              }, value=[2019, 2022], id='year-range-slider-fs')), dbc.Col()]
                          ),
                
                          dcc.Graph(
                              id='fig_fs',
                              figure=paint_fig_fs())], width=9
                      ),
                      dbc.Col(dcc.Graph(
                          id='figtreemap',
                          figure=paint_fig_treemap()), width=3)]
                  ))]),

])


@app.callback(
    Output("fig_ts", "figure"),
    Input("year-range-slider", "value"),
    Input("province", "value"),
)
def update_line_graph(years, province):
    years_new = []
    if not years:
        return paint_fig_ts(province=province)
    else:
        for y in range(years[0], years[1] + 1):
            years_new.append(str(y))
        
        return paint_fig_ts(years_new, province)


@app.callback(
    Output("fig_fs", "figure"),
    Input("year-range-slider-fs", "value"),
    Input("province", "value")
)
def update_bar_chart(years, province):
    years_new = []
    if not years:
        return paint_fig_fs(province=province)
    else:
        for y in range(years[0], years[1] + 1):
            years_new.append(str(y))
        
        return paint_fig_fs(years_new, province=province)


@app.callback(
    Output('figtreemap', 'figure'),
    Input('fig_fs', 'hoverData'),
    Input("province", "value")
)
def link_treemap_bar_chart(hoverData, province):
    # make a copy of the bar chart and color
    update_tree = copy.deepcopy(paint_fig_treemap())
    update_color = copy.deepcopy(colors)
    if hoverData is None:
        return update_tree
    else:
        hover_label = hoverData['points'][0]['label']
        data = get_month_data(hover_label, province)
        hover_info = hoverData['points'][0]['hovertext']
        building_type = re.search('<b>(.+?)</b>', hover_info).group(1)
        hover_text = []
        for index, row in data.iterrows():
            hover_text.append(('Month:{}<br>' +
                               'Proportion:<b>{:.2%}</b>').format(
                row['Date'],
                row['Proportion']
            ))
        if building_type == 'Commercialized Residential':
            update_color[0] = '#4682B4'
        elif building_type == 'Houses for Business Use':
            update_color[1] = '#4682B4'
        else:
            update_color[2] = '#4682B4'
        
        trace = go.Treemap(
            labels=data['Building Type'],
            parents=parent,
            values=data['Proportion'],
            marker_colors=update_color,
            
            text=hover_text,
            hoverinfo="text"
        )
        layout = go.Layout(margin=dict(t=50, l=25, r=25, b=25))
        return go.Figure(data=trace, layout=layout_tree)


# Run app and display result inline in the notebook
app.run_server(mode='external')
