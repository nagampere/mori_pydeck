# %%
import pydeck as pdk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time


# %%
UK_ACCIDENTS_DATA = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'

layer = pdk.Layer(
    'HexagonLayer',  # `type` positional argument is here
    UK_ACCIDENTS_DATA,
    get_position=['lng', 'lat'],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36)

# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.map_style = "mapbox://styles/mapbox/light-v9"

# Save the map to an HTML file
r.to_html('deck_map.html', open_browser=False)

# %%
# Chrome headlessモード設定
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1200,800")

# Chrome Driver起動
driver = webdriver.Chrome(options=options)
driver.get("file://" + os.path.abspath("deck_map.html"))

# レンダリング待ち（時間調整可能）
time.sleep(5)

# スクリーンショット保存
driver.save_screenshot("map_capture.png")
driver.quit()

print("✅ PNG画像として保存しました：map_capture.png")

# %%



