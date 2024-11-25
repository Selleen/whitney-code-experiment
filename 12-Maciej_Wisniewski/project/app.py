from datetime import datetime
import random

title = "The Meaning of Life as Expressed in Seven Lines of Code by Maciej Wisniewski"
now = datetime.now()
current_hour = now.hour

zones = {
    "zone_1": ["in New York City...", "in Havana...", "in Ottawa...", "in Montreal...", "in Philadelphia...", "in Asuncion...",
               "in Atlanta...", "in San Juan...", "in Santiago...", "in Santo Domingo...", "in Boston...", "in La Paz...",
               "in Caracas...", "in Toronto...", "in Detroit...", "in Washington DC...", "in Harrisburg...", "in Iqaluit...",
               "in Kingstown...", "in Nassau..."],
    "zone_2": ["in Buenos Aires...", "in Brasilia...", "in Sao Paulo...", "in Rio de Janeiro...", "in Casablanca...", "in Reykjavik...",
               "in Algiers...", "in Lagos...", "in Lisbon...", "in London...", "in Dublin...", "in Odessa...", "in Harare...",
               "in Prague...", "in Stockholm...", "in Warsaw...", "in Kuwait City...", "in Nairobi...", "in Istanbul...", "in Moscow..."],
    "zone_3": ["in Bangkok...", "in Jakarta...", "in Hanoi...", "in Bandung...", "in Astana...", "in Almaty...", "in Phnom Penh...",
               "in Saigon...", "in Semarang...", "in Surabaya...", "in Surakarta...", "in Malang...", "in Medan...", "in The Settlement...",
               "in Mexicali...", "in Tijuana...", "in Vientiane...", "in Novosibirsk...", "in Omsk...", "in Palembang..."],
    "zone_4": ["in Manila...", "in Taipei...", "in Singapore...", "in Shanghai...", "in Kuala Lumpur...", "in Beijing...", "in Perth...",
               "in Hong Kong...", "in Chongqing...", "in Mataram...", "in Tangshan...", "in Tientsin...", "in Denpasar...", "in Tsingtao...",
               "in Endeh...", "in Hangzhou...", "in Seoul...", "in Tokyo...", "in Ulaanbaatar...", "in Nagoya..."],
    "zone_5": ["in Brisbane...", "in Sydney...", "in Canberra...", "in Melbourne...", "in Vladivostok...", "in Suva...", "in Noumea...",
               "in Honiara...", "in Kolonia...", "in Wellington...", "in Kamchatka...", "in Anadyr...", "in Honolulu...", "in Kiritimati...",
               "in Anchorage...", "in Phoenix...", "in San Francisco...", "in Seattle...", "in Los Angeles...", "in Vancouver..."],
    "zone_6": ["in Aklavik...", "in San Salvador...", "in Managua...", "in Tegucigalpa...", "in Denver...", "in Edmonton...", "in Guatemala...",
               "in Houston...", "in Indianapolis...", "in Kingston...", "in Bogota...", "in St. Paul...", "in Lima...", "in Mexico City...",
               "in Chicago...", "in Minneapolis...", "in Montgomery...", "in Winnipeg...", "in New Orleans...", "in Acapulco..."]
}

dates = [datetime(random.randint(1900, 2002), random.randint(1, 12), random.randint(1, 28)).strftime('%B %d, %Y') for _ in range(24)]

# Color and phrase configuration depending on the time.
if 5 <= current_hour <= 7:
    colors = [120, 180, 240, 180, 120, 60]
    stories = ["In the early morning on ", "On the morning of ", "During the day of ",
               "In the early evening on ", "On the evening of ", "During the night of "]
elif 8 <= current_hour <= 17:
    colors = [240, 180, 120, 60, 120, 180]
    stories = ["During the day of ", "In the early evening on ", "On the evening of ",
               "During the night of ", "In the early morning on ", "On the morning of "]
else:
    colors = [60, 120, 180, 240, 180, 120]
    stories = ["During the night of ", "In the early morning on ", "On the morning of ",
               "During the day of ", "In the early evening on ", "On the evening of "]

# HTML generation.
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        table {{
            margin: auto;
            border-collapse: collapse;
        }}
        td {{
            width: 140px;
            height: 140px;
            text-align: center;
            vertical-align: middle;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <h1 style="text-align:center;">{title}</h1>
    <table>
"""

for row in range(4):
    html_content += "<tr>"
    for col in range(6):
        zone_key = f"zone_{col + 1}"
        zone = random.choice(zones[zone_key])
        color = colors[col]
        story = stories[col]
        date = random.choice(dates)
        html_content += f"""
        <td style="background-color: rgba({color}, {color}, {color}, 0.5);">
            <p>{story}</p>
            <p>{date}</p>
            <p>{zone}</p>
        </td>
        """
    html_content += "</tr>"

html_content += """
    </table>
</body>
</html>
"""

# Save to an HTML file.
with open("life_support.html", "w") as file:
    file.write(html_content)

print("HTML file successfully generated as 'life_support.html'.")
