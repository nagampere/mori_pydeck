# %%
import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon

# %%
def get_largest_polygon_centroid(geometry):
    """
    マルチポリゴンが与えられたとき、最大のポリゴンを抽出してその中心座標を返す。
    単一ポリゴンのときはそのまま中心を返す。
    """
    if isinstance(geometry, MultiPolygon):
        largest = max(geometry.geoms, key=lambda g: g.area)
        return largest
    elif isinstance(geometry, Polygon):
        return geometry
    else:
        return None

# %%
# GeoDataFrameとして読み込み
gdf = gpd.read_file("japan_ver85/japan_ver85.shp")

# GeoDataFrameを都道府県ごとにdissolve
gdf_pref = gdf.dissolve(by="KEN", as_index=False)
gdf_pref["geometry"] = gdf_pref.geometry.buffer(0.000001)  # バッファを適用してジオメトリを修正
# JCODEの上2桁を抽出してIDを作成
gdf_pref['ID'] = gdf_pref['JCODE'].str[:2]
# マルチポリゴンから最も大きいポリゴンを選択し、そのポリゴンの中心座標を取得
gdf_pref['single_geometry'] = gdf_pref["geometry"].apply(get_largest_polygon_centroid)
gdf_pref['centroid'] = gdf_pref['single_geometry'].to_crs('EPSG:6677').centroid.to_crs('EPSG:6668')
gdf_pref['lat'] = gdf_pref['centroid'].y
gdf_pref['lon'] = gdf_pref['centroid'].x
# 緯度経度の座標を文字列として保存
# gdf_pref['coordinates'] = gdf_pref.apply(lambda row: f"[{row['lon']}, {row['lat']}]", axis=1)

# %%
prefecture_translation = {
    "北海道":"Hokkaido",
    "青森県":"Aomori",
    "岩手県":"Iwate",
    "宮城県":"Miyagi",
    "秋田県":"Akita",
    "山形県":"Yamagata",
    "福島県":"Fukushima",
    "茨城県":"Ibaraki",
    "栃木県":"Tochigi",
    "群馬県":"Gunma",
    "埼玉県":"Saitama",
    "千葉県":"Chiba",
    "東京都":"Tokyo",
    "神奈川県":"Kanagawa",
    "新潟県":"Niigata",
    "富山県":"Toyama",
    "石川県":"Ishikawa",
    "福井県":"Fukui",
    "山梨県":"Yamanashi",
    "長野県":"Nagano",
    "岐阜県":"Gifu",
    "静岡県":"Shizuoka",
    "愛知県":"Aichi",
    "三重県":"Mie",
    "滋賀県":"Shiga",
    "京都府":"Kyoto",
    "大阪府":"Osaka",
    "兵庫県":"Hyogo",
    "奈良県":"Nara",
    "和歌山県":"Wakayama",
    "鳥取県":"Tottori",
    "島根県":"Shimane",
    "岡山県":"Okayama",
    "広島県":"Hiroshima",
    "山口県":"Yamaguchi",
    "徳島県":"Tokushima",
    "香川県":"Kagawa",
    "愛媛県":"Ehime",
    "高知県":"Kochi",
    "福岡県":"Fukuoka",
    "佐賀県":"Saga",
    "長崎県":"Nagasaki",
    "熊本県":"Kumamoto",
    "大分県":"Oita",
    "宮崎県":"Miyazaki",
    "鹿児島県":"Kagoshima",
    "沖縄県":"Okinawa"
}

# %%
# 都道府県名を英語に変換
gdf_pref["KEN_EN"] = gdf_pref["KEN"].map(prefecture_translation)
# gdf_prefの列を抽出し、IDの順番に並べ替え
gdf_pref = gdf_pref[['ID', 'KEN', 'KEN_EN', 'lat', 'lon', 'geometry']].sort_values(by='ID', ascending=True, ignore_index=True)

# gdf_prefをGeoJSON形式で保存
gdf_pref.to_file("japan_prefectures.geojson", driver='GeoJSON')

# %%
# GeoDataFrameとして読み込み
gdf_city = gdf.copy()

# SIKUCHOSONが所属不明地の場合は除外
gdf_city = gdf_city[gdf_city['SIKUCHOSON'] != '所属不明地']
# SEIREIがない場合はSIKUCHOSON、ある場合はSEIREIであるNAMEを作成
gdf_city['NAME'] = gdf_city.apply(lambda row: row['SEIREI'] if row['SEIREI'] else row['SIKUCHOSON'], axis=1)
# CITY_ENGから、最初のハイフン(-)までの文字列を抽出してNAME_ENを作成
gdf_city['NAME_EN'] = gdf_city['CITY_ENG'].str.split('-').str[0]
# NAMEとNAME_ENでdissolve
gdf_city = gdf_city.dissolve(by=['NAME', 'NAME_EN'], as_index=False, aggfunc='first')
gdf_city["geometry"] = gdf_city.geometry.buffer(0.000001)  # バッファを適用してジオメトリを修正
# JCODEの順番に並べ替え
gdf_city = gdf_city.sort_values(by='JCODE', ascending=True, ignore_index=True)

# マルチポリゴンから最も大きいポリゴンを選択し、そのポリゴンの中心座標を取得
gdf_city['single_geometry'] = gdf_city['geometry'].apply(get_largest_polygon_centroid)
gdf_city['centroid'] = gdf_city['geometry'].to_crs('EPSG:6677').centroid.to_crs('EPSG:6668')
gdf_city['lat'] = gdf_city['centroid'].y
gdf_city['lon'] = gdf_city['centroid'].x
# 緯度経度の座標を文字列として保存
# gdf_city['coordinates'] = gdf_city.apply(lambda row: f"[{row['lon']}, {row['lat']}]", axis=1)

# ID, NAME, NAME_EN, lat, lon, geometryの列を抽出
gdf_city = gdf_city[['JCODE', 'NAME', 'NAME_EN', 'lat', 'lon', 'geometry']].rename(columns={'JCODE': 'ID'})

# gdf_cityをCSV, GeoJSON形式で保存
gdf_city.to_file("japan_cities.geojson", driver='GeoJSON')


# %%


# %%


# %%



