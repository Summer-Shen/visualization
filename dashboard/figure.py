import json

import pandas as pd
import plotly.graph_objects as go

data = pd.read_excel("../year_data.xlsx", index_col=0)
general_style = dict(margin=dict(l=2, r=2, t=2, b=2), autosize=True)

keys = {
    "房地产开发企业个数(个)": [
        "内资房地产开发企业个数(个)",
        "国有房地产开发企业个数(个)",
        "集体房地产开发企业个数(个)",
        "港、澳、台投资房地产开发企业个数(个)",
        "外商投资房地产开发企业个数(个)"
    ],
    "房地产开发企业平均从业人数(人)": [
        "港、澳、台投资房地产开发企业平均从业人数(人)",
        "外商投资房地产开发企业平均从业人数(人)",
        "内资房地产开发企业平均从业人数(人)",
        "国有房地产开发企业平均从业人数(人)",
        "集体房地产开发企业平均从业人数(人)"
    ],
    "房地产开发企业资产负债": [
        "房地产开发企业实收资本(亿元)",
        "房地产开发企业资产总计(亿元)",
        "房地产开发企业累计折旧(亿元)",
        "房地产开发企业本年折旧(亿元)",
        "房地产开发企业负债合计(亿元)",
        "房地产开发企业所有者权益(亿元)", ],
    "房地产开发企业资金来源": [
        "房地产开发企业本年实际到位资金(亿元)",
        "房地产开发企业国内贷款(亿元)",
        "房地产开发企业利用外资(亿元)",
        "房地产开发企业自筹资金(亿元)",
        "房地产开发企业其他资金来源(亿元)"],
    "房地产开发企业经营情况": [
        "房地产开发企业主营业务收入(亿元)",
        "房地产开发企业土地转让收入(亿元)",
        "房地产开发企业商品房销售收入(亿元)",
        "房地产开发企业房屋出租收入(亿元)",
        "房地产开发企业其他收入(亿元)",
        "房地产开发企业主营业务税金及附加(亿元)",
        "房地产开发企业营业利润(亿元)"]
}

company_type = {"内资": "Domestic Funded", "国有": "State-owned", "集体": "Collective-owned",
                "港、澳、台投资": "Funds from Hong Kong, Macao and Taiwan", "外商投资": "Foreign Funded"}

to_pinyin = {
    "青海": "QingHai",
    "江苏": "JiangSu",
    "福建": "FuJian",
    "浙江": "ZheJiang",
    "黑龙江": "HeiLongJiang",
    "河北": "HeBei",
    "天津": "TianJin",
    "山西": "Shan1Xi",
    "湖南": "HuNan",
    "宁夏": "NingXia",
    "江西": "JiangXi",
    "陕西": "Shan3Xi",
    "西藏": "XiZang",
    "新疆": "XinJiang",
    "北京": "BeiJing",
    "山东": "ShanDong",
    "海南": "HaiNan",
    "贵州": "GuiZhou",
    "吉林": "JiLin",
    "辽宁": "LiaoNing",
    "湖北": "HuBei",
    "广东": "GuangDong",
    "甘肃": "GanSu",
    "内蒙古": "NeiMengGu",
    "河南": "HeNan",
    "四川": "SiChuan",
    "安徽": "AnHui",
    "云南": "YunNan",
    "重庆": "ChongQing",
    "上海": "ShangHai",
    "广西": "GuangXi",
    "全国": "China"
}

from_pinyin = {
    "YunNan": "云南",
    "HuNan": "湖南",
    "HeNan": "河南",
    "HeBei": "河北",
    "BeiJing": "北京",
    "GuangDong": "广东",
    "LiaoNing": "辽宁",
    "JiLin": "吉林",
    "GuiZhou": "贵州",
    "ZheJiang": "浙江",
    "JiangSu": "江苏",
    "XiZang": "西藏",
    "JiangXi": "江西",
    "QingHai": "青海",
    "Shan1Xi": "山西",
    "FuJian": "福建",
    "AnHui": "安徽",
    "TianJin": "天津",
    "GuangXi": "广西",
    "SiChuan": "四川",
    "NingXia": "宁夏",
    "HaiNan": "海南",
    "ChongQing": "重庆",
    "ShanDong": "山东",
    "GanSu": "甘肃",
    "ShangHai": "上海",
    "HuBei": "湖北",
    "XinJiang": "新疆",
    "Shan3Xi": "陕西",
    "NeiMengGu": "内蒙古",
    "HeiLongJiang": "黑龙江",
    "China": "全国"
}


def allDistricts():
    districts = set(data["地区"])
    districts.remove("全国")
    return list(districts)


def convertProvince(s):
    return s[:3] if s[0] in ["内", "黑"] else s[:2]


class DevelopmentPage:
    def __init__(self):
        self.keys = {
            "房地产开发企业个数(个)": [
                "内资房地产开发企业个数(个)",
                "国有房地产开发企业个数(个)",
                "集体房地产开发企业个数(个)",
                "港、澳、台投资房地产开发企业个数(个)",
                "外商投资房地产开发企业个数(个)"
            ],
            "房地产开发企业平均从业人数(人)": [
                "港、澳、台投资房地产开发企业平均从业人数(人)",
                "外商投资房地产开发企业平均从业人数(人)",
                "内资房地产开发企业平均从业人数(人)",
                "国有房地产开发企业平均从业人数(人)",
                "集体房地产开发企业平均从业人数(人)"
            ],
            "房地产开发企业总收入(亿元)": [
                "房地产开发企业主营业务收入(亿元)",
                "房地产开发企业土地转让收入(亿元)",
                "房地产开发企业商品房销售收入(亿元)",
                "房地产开发企业房屋出租收入(亿元)",
                "房地产开发企业其他收入(亿元)"
            ]
        }

        self.colors_dict = {"": "blue", "内资": "lightblue", "国有": "red",
                            "集体": "lightgreen", "港、澳、台投资": "purple", "外商投资": "orange"}

    def getLineChart(self, district="全国", names=None):
        if not names:
            names = [""]
        t = data[data["地区"].str.contains(district)]
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=t["年份"],
                                 y=t[[name + "房地产开发企业个数(个)" for name in names]].sum(axis=1),
                                 mode="lines+markers",
                                 name="Number of Enterprises for Real Estate Development",
                                 showlegend=True,
                                 xaxis="x", yaxis="y1",
                                 hovertemplate=
                                 "<b>" + to_pinyin[district] + " %{x:.0f}</b><br><br>" +
                                 "Number of Enterprises: %{y:.0f}<br>" +
                                 "<extra></extra>",
                                 ))
        fig.add_trace(go.Scatter(x=t["年份"],
                                 y=t[[name + "房地产开发企业平均从业人数(人)" for name in names]].sum(axis=1),
                                 name="Average Number of Employed Persons in Enterprises for Real Estate Development",
                                 showlegend=True, mode="lines+markers",
                                 xaxis="x", yaxis="y2",
                                 hovertemplate=
                                 "<b>" + to_pinyin[district] + " %{x:.0f}</b><br><br>" +
                                 "Average Number of Employed Persons: %{y:.0f}<br>" +
                                 "<extra></extra>",
                                 ))
        fig.update_layout(
            xaxis=dict(title="Year"),
            yaxis=dict(title="# of Enterprises"),
            yaxis2=dict(anchor="x", overlaying="y", side="right",
                        title="Average # of Employed Persons"),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.14,
                xanchor="right",
                x=1
            ),
            height=420,
            **general_style
        )
        return fig

    def getBarChart(self, year=2020, building_types=None, name="房地产开发企业个数(个)", descending=False):
        assert name in ["房地产开发企业个数(个)", "房地产开发企业平均从业人数(人)"]
        if not building_types:
            building_types = [""]

        keys = [e + name for e in building_types]
        fig = go.Figure()
        t = data[(data["年份"] == year) & (data["地区"].isin(allDistricts()))]
        t.insert(1, "sum", t[keys].sum(axis=1), allow_duplicates=False)
        t = t.sort_values(["sum", "地区"], ascending=descending)
        for key in keys:
            fig.add_trace(go.Bar(x=t[key][len(t[key]) // 2:],
                                 y=[to_pinyin[convertProvince(e)] for e in t["地区"][len(t[key]) // 2:]],
                                 orientation="h",
                                 name=company_type[key[:key.index("房")]] if key.index("房") else "Total",
                                 marker_color=self.colors_dict[key[:-len(name)]],
                                 showlegend=True
                                 ))

        fig.update_layout(
            barmode="stack",
            xaxis=dict(range=[0, 1.1 * max(t["sum"])],
                       title="%s in %d" %
                             ("# of Enterprises" if name == "房地产开发企业个数(个)" else "Average # of Employed Persons",
                              year)),
            yaxis=dict(title="District"),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="right",
                x=1
            ),
            height=360,
            **general_style
        )

        return fig

    def getStackedChart(self, district="全国"):
        t = data[data["地区"].str.contains(district)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t["年份"], y=t["房地产开发企业负债合计(亿元)"],
                                 name="Total Liabilities (100 million yuan)", showlegend=True,
                                 mode="lines", fill="tozeroy",
                                 xaxis="x", yaxis="y1",
                                 hovertemplate=
                                 "<b>" + to_pinyin[district] + " %{x:.0f}</b><br><br>" +
                                 "Total Liabilities (100 million yuan): %{y:.2f}<br>" +
                                 "<extra></extra>", ))
        fig.add_trace(go.Scatter(x=t["年份"], y=t["房地产开发企业资产总计(亿元)"],
                                 name="Owners' Equity (100 million yuan)", showlegend=True,
                                 mode="lines", fill="tonexty",
                                 xaxis="x", yaxis="y1",
                                 hovertemplate=
                                 "<b>" + to_pinyin[district] + " %{x:.0f}</b><br><br>" +
                                 "Total Assets (100 million yuan): %{y:.2f}<br>" +
                                 "<extra></extra>", ))
        fig.add_trace(go.Scatter(x=t["年份"], y=t["房地产开发企业负债合计(亿元)"] / t["房地产开发企业资产总计(亿元)"],
                                 name="Assets Liability Ratio (%)", showlegend=True,
                                 mode="lines+markers",
                                 xaxis="x", yaxis="y2",
                                 hovertemplate=
                                 "<b>" + to_pinyin[district] + " %{x:.0f}</b><br><br>" +
                                 "Assets Liability Ratio (%): %{y:.2%}<br>" +
                                 "<extra></extra>", ))
        fig.update_layout(
            xaxis=dict(dtick=1, title="Year"),
            yaxis1=dict(range=[0, 144000 if district != "全国" else 1200000],
                        title="Total Assets (100 million yuan)"),
            yaxis2=dict(anchor="x", overlaying="y", side="right", range=[0, 1],
                        title="Assets Liability Ratio (%)"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1
            ),
            height=600,
            **general_style
        )
        return fig

    def getBubbleChart(self, districts=None):
        if not districts:
            districts = set(data["地区"])
            districts.remove("全国")
        keys = self.keys["房地产开发企业总收入(亿元)"]

        fig = go.Figure()
        for district in districts:
            t = data[data["地区"].str.contains(district)]
            income = t[keys].sum(axis=1)
            profit = t["房地产开发企业营业利润(亿元)"]
            cost = income - profit - t["房地产开发企业主营业务税金及附加(亿元)"]
            fig.add_trace(go.Scatter(x=t["年份"],
                                     y=profit / (income - profit),
                                     name=to_pinyin[convertProvince(district)],
                                     text=[to_pinyin[convertProvince(district)]] * len(profit),
                                     mode="markers",
                                     marker=dict(size=income,
                                                 sizemode='area',
                                                 sizeref=5,
                                                 sizemin=1, ),
                                     hovertemplate=
                                     "<b>%{text} %{x:.0f}</b><br><br>" +
                                     "Total Income: %{marker.size:,}<br>" +
                                     "Revenue Rate: %{y:.2%}<br>" +
                                     "<extra></extra>",
                                     ))
        fig.update_layout(
            xaxis=dict(title="Year"),
            yaxis=dict(range=[-0.06, 0.21], title="Revenue Ratio (%)"),
            height=600,
            **general_style
        )
        return fig

    def getPieChart(self, district="全国", year=2020, name="房地产开发企业个数(个)"):
        assert name in self.keys
        if not district:
            district = "全国"
        if not year:
            year = 2020
        keys = self.keys[name]
        t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]

        labels = [e[:e.index("房")] for e in keys]
        values = [v for e in keys for v in t[e]]
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=[company_type[e] for e in labels], values=values, showlegend=False,
                             hole=0.3, sort=False))
        fig.update_traces(marker=dict(colors=[self.colors_dict[e] for e in labels]),
                          hoverinfo='label+percent', textinfo="label")
        fig.update_layout(
            height=300,
            **general_style
        )
        return fig


class SalePage:
    def __init__(self):
        self.keys = {
            "商品房": {
                "商品房": "Commercialized Buildings",
                "住宅商品房": "Commercialized Residential Buildings",
                "别墅、高档公寓": "Villas, High-grade Apartments",
                "办公楼": "Office Buildings",
                "商业营业用房": "Houses for Business Use",
                "其他商品房": "Other"
            },
            "指标": {
                "销售面积(万平方米)": "Floor Space of Building Sold (10000 sq.m)",
                "销售额(亿元)": "Total Sale (100 million yuan)",
                "平均销售价格(元/平方米)": "Average Selling Price (yuan/sq.m)"
            },
            "竣工与销售": {
                "住宅": "Residential Buildings",
                "别墅、高档公寓": "Villas, High-grade Apartments"
            }
        }
        self.color_dict = dict(zip(self.keys["商品房"],
                                   ["blue", "lightblue", "lightgrey",
                                    "lightgreen", "lightyellow", "lightsalmon"]))
        with open(r'./china_geojson/china.json', encoding='utf8') as js:
            self.geoInfo = json.load(js)
            for e in self.geoInfo["features"]:
                name = convertProvince(e["properties"]["name"])
                if name in to_pinyin:
                    e["properties"]["name"] = to_pinyin[name]

    def getGeoMap(self, building_types=None, name="销售面积(万平方米)", year=2020):
        assert name in self.keys["指标"]
        if not building_types:
            building_types = ["商品房"]
        keys = [e + name for e in building_types]

        t = data[data["地区"].isin(allDistricts())]
        t.insert(1, "sum", t[keys].sum(axis=1), allow_duplicates=False)
        zmax, zmin = max(t["sum"]), min(t["sum"])
        t = t[t["年份"] == year]

        fig = go.Figure()
        fig.add_trace(go.Choroplethmapbox(geojson=self.geoInfo,
                                          featureidkey="properties.name",
                                          locations=[to_pinyin[convertProvince(e)] for e in t["地区"]],
                                          z=t["sum"],
                                          colorscale="OrRd",
                                          zmax=zmax, zmin=zmin
                                          )
                      )
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=2.6,
            mapbox_center={"lat": 35.9, "lon": 104.2},
            **general_style
        )
        return fig

    def getStackedChart(self, name="销售面积(万平方米)", building_types=None, district=None):
        assert name in self.keys["指标"]
        if not district:
            district = "China"
        district = from_pinyin[district]
        if not building_types:
            building_types = ["商品房"]

        t = data[data["地区"].str.contains(district)]
        accumulate = t[building_types[0] + name]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t["年份"], y=accumulate,
                                 name=self.keys["商品房"][building_types[0]], showlegend=True,
                                 mode="none", fill="tozeroy",
                                 fillcolor=self.color_dict[building_types[0]]))

        for building_type in building_types[1:]:
            accumulate += t[building_type + name]
            fig.add_trace(go.Scatter(x=t["年份"], y=accumulate,
                                     name=self.keys["商品房"][building_type], showlegend=True,
                                     mode="none", fill="tonexty",
                                     fillcolor=self.color_dict[building_type]))

        t = data[data["地区"].str.contains("全国")] if district == "全国" else data[data["地区"].isin(allDistricts())]
        accumulate = t[[e + name for e in building_types]].sum(axis=1)
        ymax = max(accumulate)

        name = self.keys["指标"][name]
        fig.update_layout(
            xaxis=dict(dtick=1, title="Year"),
            yaxis=dict(range=[0, 1.1 * ymax],
                       title=name[:name.index("(")] + "in %s " % to_pinyin[district] + name[name.index("("):]),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
            ),
            **general_style
        )
        return fig

    def getAveragePriceBar(self, districts=None, building_type=None):
        districts = ["全国"] + districts if districts else ["全国"]
        if not building_type:
            building_type = "商品房"
        assert building_type == "商品房" or building_type in self.keys["商品房"]

        tmax = max(data[data["地区"].isin(districts)][building_type + "平均销售价格(元/平方米)"])
        fig = go.Figure()
        for district in districts:
            t = data[data["地区"].str.contains(district)]
            fig.add_trace(go.Bar(x=t["年份"], y=t[building_type + "平均销售价格(元/平方米)"],
                                 name=to_pinyin[convertProvince(district)], showlegend=True))
        fig.update_layout(
            xaxis=dict(dtick=1, title="Year"),
            yaxis=dict(title="Average Selling Price (yuan/sq.m)", range=[0, 1.1 * tmax]),
            barmode="group",
            height=480,
            **general_style
        )
        return fig

    def getScatterChart(self):
        districts = allDistricts()
        shapes = ["circle", "square", "diamond", "cross", "x", "triangle-up",
                  "pentagon", "hexagram", "star", "diamond", "hourglass"]

        fig = go.Figure()

        for district in districts:
            t = data[data["地区"].str.contains(district)]
            fig.add_trace(go.Scatter(
                x=t["房地产开发企业住宅销售套数(套)"],
                y=t["房地产开发企业住宅竣工套数(套)"],
                text=t["年份"],
                name=to_pinyin[convertProvince(district)],
                meta=to_pinyin[convertProvince(district)],
                marker=dict(symbol=shapes[:len(t["年份"])]),
                showlegend=False,
                mode="markers",
                hovertemplate="(%{x:.0f}, %{y:.0f})" +
                              "<extra>%{meta} %{text}</extra>",
            ))

        fig.add_trace(go.Scatter(
            x=[0, 820000], y=[0, 820000], mode="lines",
            line=dict(color='royalblue', width=2, dash='dash'),
            showlegend=False
        ))

        fig.update_layout(
            xaxis=dict(dtick=200000, title="# of Sold Flats of Residential Buildings (unit)"),
            yaxis=dict(title="# of Completed Flats of Residential Buildings (unit)"),
            **general_style,
        )
        return fig


def getBarChartWithLine(x, y1, y2, ly, y1_name, y2_name, line_name):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y1,
        name=y1_name,
        xaxis="x", yaxis="y1"
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=y2,
        name=y2_name,
        xaxis="x", yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=ly,
        mode="lines+markers",
        xaxis="x", yaxis="y2",
        name=line_name
    ))

    fig.update_layout(
        barmode="group",
        xaxis=dict(dtick=1, title="Year"),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            # bgcolor="rgba(0,0,0,0)"
        ),

        **general_style
    )

    return fig


class InvestmentPage:
    def __init__(self):
        self.keys = {
            "分类": {
                "资金来源": "Funds Received",
                "资金用途": "Usage of Funds",
                "建筑类型": "Type of Buildings",
                "项目规模": "Size of Projects"
            },
            "资金来源": {
                "房地产开发企业国内贷款(亿元)": "Domestic Loans (100 million yuan)",
                "房地产开发企业自筹资金(亿元)": "Self-raising Funds (100 million yuan)",
                "房地产开发企业利用外资(亿元)": "Foreign Investment (100 million yuan)",
                "房地产开发企业其他资金来源(亿元)": "Other Funds (100 million yuan)",
            },
            "资金用途": {
                "房地产开发企业建筑安装工程本年完成投资额(亿元)": "Construction and Installation",
                "房地产开发企业设备工器具购置本年完成投资额(亿元)": "Purchase of Equipment and Instruments",
                "房地产开发企业其他费用本年完成投资额(亿元)": "Others",
            },
            "建筑类型": {
                "房地产开发住宅投资额(亿元)": "Residential Buildings",
                "房地产开发别墅、高档公寓投资额(亿元)": "Villas, High-grade Apartments",
                "房地产开发办公楼投资额(亿元)": "Office Buildings",
                "房地产开发商业营业用房投资额(亿元)": "Houses for Business Use",
                "房地产开发其他投资额(亿元)": "Others",
            },
            "项目规模": {
                "500万元以下房地产开发投资额(亿元)": "Less Than 5 Million Yuan",
                "500-1000万元房地产开发投资额(亿元)": "5-10 Million Yuan",
                "1000-3000万元房地产开发投资额(亿元)": "10-30 Million Yuan",
                "3000-5000万元房地产开发投资额(亿元)": "30-50 Million Yuan",
                "5000万-1亿元房地产开发投资额(亿元)": "50-100 Million Yuan",
                "1-5亿元房地产开发投资额(亿元)": "100-500 Million Yuan",
                "5-10亿元房地产开发投资额(亿元)": "500-1000 Million Yuan",
                "10亿元以上房地产开发投资额(亿元)": "1 Billion Yuan and More"
            },
        }

    def getInvestmentPlanChart(self, district=None):
        if not district:
            district = "全国"
        t = data[data["地区"].str.contains(district)]

        x, y1, y2 = t["年份"], t["房地产开发企业计划总投资(亿元)"], t["房地产开发企业自开始建设至本年底累计完成投资(亿元)"]
        fig = getBarChartWithLine(
            x, y1, y2, y2 / y1,
            "Total Investment Planed (100 million yuan)",
            "Accumulated Investment Completed (100 million yuan)",
            "Rate of the Investment Completed (%)",
        )
        fig.update_layout(
            yaxis1=dict(title="Investment Amount (100 million yuan)", range=[0, 1.1 * max(y1)]),
            yaxis2=dict(anchor="x", overlaying="y", side="right", range=[0, 1.09],
                        dtick=0.1, title="Rate of the Investment Completed(%)"),
            height=360)
        return fig

    def getInvestmentSunburst(self, district=None, year=2015):
        if not district:
            district = "全国"
        t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]
        categories = ["资金来源", "资金用途", "建筑类型", "项目规模"]
        labels = ["Investment", "Completed Investment", "Funds Received"] + \
                 [self.keys["分类"][e] for e in categories[1:]]
        parents = ["", "Investment", "Investment",
                   "Completed Investment", "Completed Investment", "Completed Investment", ]
        values = [0] * len(labels)
        for i, e in enumerate(categories):
            temp = self.keys[e]
            labels += [temp[e] for e in temp]
            parents += [self.keys["分类"][e]] * len(self.keys[e])
            values += [(1 if i else 3) * v for l in temp for v in t[l]]

        fig = go.Figure(
            go.Sunburst(
                labels=labels, parents=parents, values=values,
                maxdepth=2,
                insidetextorientation='auto'
            )
        )
        fig.update_traces(hoverinfo="label")
        fig.update_layout(
            height=320,
            **general_style
        )
        return fig

    def getInvestmentTable(self, year=2020, district=None, name="项目规模"):
        if not district:
            district = "全国"
        assert name in self.keys

        if name == "资金来源":
            label = "Source of Funds Received"
        else:
            label = "Completed Investment (Divided by %s)" % self.keys["分类"][name]

        t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]

        temp = sorted(list(zip([v for key in self.keys[name] for v in t[key]],
                               self.keys[name])), reverse=True)
        keys = [e[1] for e in temp]
        values = [e[0] for e in temp]

        percentages = []
        for e in values:
            e = e * 100 / sum(values)
            percentages.append(round(e, 2))
            if e:
                i = 3
                while not percentages[-1]:
                    percentages[-1] += round(e, i)
                    i += 1

        fig = go.Figure(go.Table(
            header=dict(
                values=[label, "Amount (100 million yuan)", "Ratio (%)"],
                font=dict(size=15),
                height=28
            ),
            cells=dict(
                values=[[self.keys[name][key] for key in keys], values, percentages],
                font=dict(size=12),
                height=24
            )
        ))
        fig.update_layout(**general_style, height=230)
        return fig


class ConstructionPage:
    def __init__(self):
        self.keys = {
            "房地产开发企业新开工房屋面积(万平方米)": {
                "房地产开发企业住宅新开工房屋面积(万平方米)": "Residential Buildings",
                "房地产开发企业办公楼新开工房屋面积(万平方米)": "Office Buildings",
                "房地产开发企业商业营业用房新开工房屋面积(万平方米)": "Houses for Business Use",
                "房地产开发企业其他用途新开工房屋面积(万平方米)": "Others"
            }
        }
        self.translate = {
            "": "",
            "房地产开发企业施工房屋面积(万平方米)": "Floor Space of Buildings under Construction (10000 sq.m)",
            "房地产开发企业竣工房屋面积(万平方米)": "Buildings Completed",
            "房地产开发企业新开工房屋面积(万平方米)": "Buildings Started This Year",
            "房地产开发企业住宅新开工房屋面积(万平方米)": "Residential Buildings",
            "房地产开发企业办公楼新开工房屋面积(万平方米)": "Office Buildings",
            "房地产开发企业商业营业用房新开工房屋面积(万平方米)": "Houses for Business Use",
            "房地产开发企业其他用途新开工房屋面积(万平方米)": "Others",
        }

    def getConstructingAreaChart(self, district=None):
        if not district:
            district = "全国"
        t = data[data["地区"].str.contains(district)]

        x, y1, y2 = t["年份"], t["房地产开发企业施工房屋面积(万平方米)"], t["房地产开发企业竣工房屋面积(万平方米)"]
        fig = getBarChartWithLine(
            x, y1, y2, y2 / y1,
            "Buildings under Construction",
            "Buildings Completed",
            "Rate of Floor Space of Buildings Completed (%)",
        )
        fig.update_layout(
            height=320,
            yaxis1=dict(title=dict(text="Floor Space (10000 sq.m)",
                                   font=dict(size=14))),
            yaxis2=dict(anchor="x", overlaying="y", side="right", range=[0, 1.09],
                        dtick=0.1, title="Completed Rate (%)"),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="left",
                x=0
            )
        )
        return fig

    def getConstructingValueChart(self, district=None):
        if not district:
            district = "全国"
        t = data[data["地区"].str.contains(district)]

        x, y1 = t["年份"], t["房地产开发企业竣工房屋价值(亿元)"]
        y2 = t["房地产开发企业竣工房屋造价(元/平方米)"] * t["房地产开发企业竣工房屋面积(万平方米)"] / 10000
        fig = getBarChartWithLine(
            x, y1, y2, (y1 - y2) / y2,
            "Value of Buildings Completed",
            "Cost of Buildings Completed",
            "Value Increasing Rate (%)",
        )
        fig.update_layout(
            yaxis1=dict(title=dict(text="Value/Cost of Building Completed (100 million yuan)",
                                   font=dict(size=10))),
            yaxis2=dict(anchor="x", overlaying="y", side="right",
                        title="Value Increasing Rate (%)"),
            height=320,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="left",
                x=0
            )
        )
        return fig

    def getConstructionTreemap(self, year=2020, district=None):
        if not district:
            district = "全国"
        t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]

        labels = ["房地产开发企业施工房屋面积(万平方米)", "房地产开发企业竣工房屋面积(万平方米)", "房地产开发企业新开工房屋面积(万平方米)"]
        parents = ["", "房地产开发企业施工房屋面积(万平方米)", "房地产开发企业施工房屋面积(万平方米)"]
        values = [v for e in labels for v in t[e]]

        keys = self.keys["房地产开发企业新开工房屋面积(万平方米)"]
        labels += keys
        parents += ["房地产开发企业新开工房屋面积(万平方米)"] * len(keys)
        values += [v for e in keys for v in t[e]]

        # values[0] -= values[1] + values[2]
        # values[2] = 0

        fig = go.Figure(go.Treemap(labels=[self.translate[e] for e in labels],
                                   parents=[self.translate[e] for e in parents],
                                   values=values,
                                   branchvalues="total",
                                   # marker_colors=["lightyellow", "lightblue", "red"] + ["lightred"] * 4,
                                   root_color="lightyellow"
                                   )
                        )
        fig.update_layout(
            # uniformtext=dict(minsize=10, mode='hide'),
            height=600,
            **general_style
        )
        return fig


if __name__ == '__main__':
    print("\"", "\",\n\"".join(e for e in data.keys() if "新开工" in e), "\"", sep="")

    # for district in allDistricts():
    #     district = convertProvince(district)
    #     py = "".join([e[0][0].capitalize() + e[0][1:] for e in pinyin(district, style=pypinyin.NORMAL)])
    #     print("\"%s\": \"%s\"," % (py, convertProvince(district)))

    page = DevelopmentPage()
    page.getBubbleChart().show()
