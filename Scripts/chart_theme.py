def chart_theme():
    font = "Lato"
    return {
        "width": 700,
        "height": 300,
        "background": "white",
        "config": {
            "title": {
                "fontSize": 20,
                "anchor": "start" 
            },
            "axisY": {
                "labelFont": font,
                "labelFontSize": 13,
                "labelLimit":200,
                "ticks": False, 
                "titleFont": font,
                "titleFontSize": 13,
                "titleAlign":"right",
                "titleAngle": 0, 
                "titleY": -10, 
                "titleX": 35,
            },
            "view":{"strokeOpacity": 0,
            },
        }
    }

import altair as alt
alt.themes.register("chart_theme", chart_theme)
alt.themes.enable("chart_theme")