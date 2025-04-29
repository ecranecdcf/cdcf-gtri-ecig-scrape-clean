import re
import pandas as pd

patterns = {
    "display_type": r"\b(LED|LCD|OLED|TFT)(\sdisplay|\s(screen)?)?\b",
    "color_display": r"\b(colorful|vibrant|color-changing)\s?(display|screen)?\b",
    "touch_screen": r"\b(touch\s?screen|interactive\s?touch\s?screen)\b",
    "curved_screen": r"\b(3D\s?curved|wraparound)\s?(screen|display)?\b",
    "battery_indicator": r"\b(battery\s?(level|meter|indicator)?)\b",
    "eliquid_indicator": r"\b(e-juice|e-liquid)\s?(indicator|meter)?\b",
    "smart_display": r"\b(smart|intelligent)\s?(display|screen)?\b",
    "digital_display": r"\b(digital)\s?(display|screen)?\b",
    "hd_display": r"\b(HD|high[-\s]?definition)\s?(display|screen)?\b",
    "animated": r"\b(animation|animated)\b",
    "backlit": r"\b(back-lit|glow-in-the-dark|glow in the dark)\b",

}

def apply_screen_regex(df, col):
    for key, pattern in patterns.items():
        df[key] = df[col].str.contains(pattern, case=False, regex=True)

if __name__ == "__main__":
    filename = 'vapingdotcom'
    df = pd.read_csv(f'scraped_data/{filename}_scrape.csv')
    description_columns = df.filter(regex='description').astype(str).fillna('')
    df['description_all'] = description_columns.agg(' '.join, axis=1)

    print('applying screen regex')
    apply_screen_regex(df, 'description_all')
    df_new = df[['tag', 'title', 'display_type', 'color_display',
       'touch_screen', 'curved_screen', 'battery_indicator',
       'eliquid_indicator', 'smart_display', 'digital_display', 'hd_display',
       'animated', 'backlit', 'link']]
    df_new.to_csv(f'nlp/screens_sample_data/{filename}_screens.csv', index=False)
