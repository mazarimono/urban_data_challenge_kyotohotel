import pandas as pd 
import numpy as np 
import dash 
import dash_core_components as dcc
import dash_html_components as html 
import plotly.graph_objs as go

import os 

df = pd.read_csv('kyoto_hotel_comp1.csv', index_col=0)
dff = pd.pivot_table(df, values='count', index = 'year', aggfunc=sum)
dff['cumsum'] = dff['count'].cumsum()

dft = pd.read_csv('tourist_data_csv.csv', index_col=0)
dft = dft.dropna()

mapbox_access_token = "pk.eyJ1IjoibWF6YXJpbW9ubyIsImEiOiJjanA5Y3NnYzYwMmJmM3BsZDRva2plYTQ0In0.vlsrPy60tmdPB0tbUmtoTQ"
app = dash.Dash(__name__)

server = app.server 

app.layout = html.Div(children=[
    html.Div([
    html.H1(children="Kyoto Hotel Map"),
    ], style = {'backgroundColor': '#da70d6'}),
    html.Div([
        html.Div([
            html.H3('アプリ概要'),
            html.P('・京都市のオープンデータポータルサイトにある、旅館業法に基づく許可施設一覧のデータセットを'),
            html.P('　利用して、京都市のホテルの場所及び、その増加具合を見れるようにした。'),
            html.P('・元の位置データには住所しかなかったため、経度緯度はヤフーのAPIを利用して取得した。'),
            html.P('・そのデータを使い、年度ごとの宿泊施設の増加具合と類型も算出し可視化した。'),
            html.P('・また宿泊者数の増減を見るためにデータを取ってみたが、宿泊施設の増加を見られなかった。')
        ], style = {'marginLeft': '2%'})
    ], style = {'marginLeft': '20%', 'marginRight': '20%' ,'backgroundColor': '#EAD9FF', 'border-radius': 20, 'border': '1px bold'}),
    html.Div([
    dcc.Graph(
        id = 'kyoto-hotels',
        figure = {
            'data':[
                go.Scattermapbox(
                lat = df[df['age']== i]['ido'],
                lon = df[df['age']== i]['keido'],
                mode = 'markers',
                marker = dict(
                    size=9
                ),
                text = df[df['age']== i]['hotel_name'],
                name = str(i),
                ) for i in df['age'].unique()
            ],
            'layout':
                go.Layout(
                    autosize=True,
                    hovermode='closest',
                    mapbox = dict(
                        accesstoken=mapbox_access_token,
                        bearing = 0,
                        center = dict(
                            lat=np.mean(df['ido']),
                            lon=np.mean(df['keido'])
                        ),
                        pitch = 90,
                        zoom=10,
                    ),
                    height=600
                )
        }
    )]),
    html.Div([
        html.Div([
            html.H3('マップの使い方'),
            html.P('・マップはマウスでコントロールでき、ズームで詳細に見ることも可能。'),
            html.P('・横の凡例をクリックすると、その年代に作られたもののポイントが消したり再表示したり出来る。'),
            html.P('・ちなみに2010年を押してみると・・・。かなり多くの点が消える・・。')
        ], style={'marginLeft': '2%', 'marginTop': '4%', 'marginBotoom': '2%'}),
    ], style = {'marginLeft': '20%', 'marginRight': '20%' ,'backgroundColor': '#EAD9FF', 'border-radius': 20, 'border': '1px bold'}),
    html.Div([
        html.Div([
            html.H3('宿泊所の増え方'),
            html.P('・上のマップを見ていると、2010年台に多くの宿泊所が出来たことがわかる。'),
            html.P('・そこで下では、年ごとの登録件数をグラフ化する。')
        ], style = {'marginLeft': '2%'})
    ], style = {'marginTop': '3%', 'marginLeft': '20%', 'marginRight': '20%' ,'backgroundColor': '#EAD9FF', 'border-radius': 20, 'border': '1px bold'}),
    html.Div([
        html.Div(
                html.Div([
        dcc.Graph(
            figure = {
                'data':[
                    go.Scatter(
                        x = dff.index,  
                        y = dff['cumsum'],   
                        name = '宿泊所累計',
                    ),
                    go.Bar(
                        x = dff.index,
                        y = dff['count'],
                        name = '年間登録件数',
                    )  
                ],
                'layout':
                    go.Layout(
                        height = 600,
                        title = '宿泊所の年間登録件数と累計'
                    )
            }
        )
    ],style = {'marginLeft': '5%', 'marginRight': '5%'}),
        )
    ]),
    html.Div([
        html.Div([
            html.H3('宿泊所登録グラフ概観'),
            html.P('・グラフを見ると2015年まで累計登録件数は955件だったが、'),
            html.P('　以降、2018年10月末時点で累計登録件数は3276件と急増した。'),

        ], style = {'marginLeft': '2%'})
    ], style = {'marginTop': '3%', 'marginLeft': '20%', 'marginRight': '20%' ,'backgroundColor': '#EAD9FF', 'border-radius': 20, 'border': '1px bold'}),
    html.Div([
        html.Div([
            html.H3('観光客数'),
            html.P('・観光客データが京都市オープンデータにある。しかし、残念ながら'),
            html.P('　平成28年までしかデータが公表されておらず、宿泊所増加と宿泊客数の関係を見ることが出来ない。')
        ], style = {'marginLeft': '2%'})
    ], style = {'marginTop': '3%', 'marginLeft': '20%', 'marginRight': '20%' ,'backgroundColor': '#EAD9FF', 'border-radius': 20, 'border': '1px bold'}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='tourist-chart',
                figure = {
                    'data': [
                        go.Scatter(
                            x = dft.index,    
                            y = dft['日帰り'],
                            name = '日帰り客数',
                            stackgroup='one'
                        ),
                        go.Scatter(
                            x = dft.index, 
                            y = dft['宿泊'],
                            name = '宿泊客数',
                            stackgroup='one'
                        )
                    ],
                    'layout':
                    go.Layout(
                        height = 500,
                        title = '京都観光客数（1997年~2016年（2011、2012はデータがないため線形補正））'
                    )
                }
            )
        ], style = {'marginLeft': '10%', 'marginRight': '10%'}),
    ]),
    html.Div([
        html.Div([
            html.H3('オープンデータから得られた見識'),
            html.P('・以上、京都の宿泊所、観光に関するデータを調査した。'),
            html.P('　宿泊所は民泊ブームなどと巷で聞くように増加していることが明確で、'),
            html.P('・施設数は2016年以降で3倍以上に増加した。'),
            html.P('　一方で、宿泊者数が増加したかというのは今の所データが2016年までしか'),
            html.P('・出されていないので分からない。'),
            html.P('    '),
            html.P('・宿泊施設の増加に関してみると、中心部から地下鉄沿線にかけてあることが見て取れる。'),
            html.P('・一方で、全く増加していない地域もあり、その辺りがどうなっているのか調査してみたい。')
        ], style = {'marginLeft': '2%'})
    ], style = {'marginTop': '3%', 'marginLeft': '20%', 'marginRight': '20%' ,'backgroundColor': '#EAD9FF', 'border-radius': 20, 'border': '1px bold'}),
    html.Div([
        html.Div([
        html.H4('アーバンデータチャレンジ応募作品　合同会社長目　小川　英幸')
        ], style={'textAlign': 'center'}),
    ], style={'height': '30', 'backgroundColor': '#FFEEFF'}),
    ],style = {'backgroundColor': '#FFEEFF'})

if __name__=='__main__':
    app.run_server(debug=True)
