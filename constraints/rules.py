import pandas as pd, random

BACK  = "Backend Development"
AI    = "AI/ML Development"
BLOCK = {BACK, AI}

def apply_constraints(df: pd.DataFrame,
                      topic_writers: dict,
                      rules: dict) -> pd.DataFrame:
    df.columns = [c.strip().replace("_", " ").title().replace(" ", "_")
                  for c in df.columns]

    if rules.get("backend_ai_alternation", True):
        df = _apply_backend_ai(df)

    df = _apply_month_end_bundle(
            df, topic_writers,
            rules["month_end_bundle"]["order"],
            rules["month_end_bundle"].get("scm_rotation", 2)
         )
    return df

def _apply_backend_ai(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["Date", "Post_Number"]).copy()
    dates = sorted(df['Date'].unique())
    back_dates = set(dates[::2])
    ai_dates   = set(dates[1::2])

    df.loc[df['Date'].isin(back_dates) & (df['Post_Number']==1), 'Topic'] = BACK
    df.loc[df['Date'].isin(ai_dates)  & (df['Post_Number']==1), 'Topic'] = AI

    alt_topics = [t for t in df['Topic'].unique() if t not in BLOCK]
    df.loc[(df['Topic'].isin(BLOCK)) & (df['Post_Number']>1), 'Topic'] = \
        df.loc[(df['Topic'].isin(BLOCK)) & (df['Post_Number']>1)]\
          .apply(lambda _: random.choice(alt_topics), axis=1)

    return df

# ------------- 2) Ay sonu üçlü paket ---------------
def _apply_month_end_bundle(df: pd.DataFrame,
                            topic_writers: dict,
                            order: list[str],
                            scm_rotation: int) -> pd.DataFrame:
    """
    order -> ["Game Development", "Huawei Mobile Service", "Software Community Management"]
    scm_rotation -> kaç ayda bir SCM yazar değişsin
    """
    new = df.copy()
    allowed_scm_idx = []

    for year, month in {(d.year, d.month) for d in new['Date']}:
        month_mask = (new['Date'].dt.year==year) & (new['Date'].dt.month==month)
        sats = new[month_mask & (new['Date'].dt.weekday==5)]
        if sats.empty: continue
        target = sats['Date'].max()
        idxs   = new[new['Date']==target].sort_values('Post_Number').head(len(order)).index
        if len(idxs) < len(order): continue

        for slot, topic in enumerate(order):
            new.loc[idxs[slot], 'Topic']  = topic
            new.loc[idxs[slot], 'Writer'] = topic_writers[topic][0]  # ilk yazar

            if topic == "Software Community Management":
                cyc = ((month-1)//scm_rotation) % len(topic_writers[topic])
                new.loc[idxs[slot], 'Writer'] = topic_writers[topic][cyc]
                allowed_scm_idx.append(idxs[slot])

    # SCM başka yerde görünmesin
    scm_mask = (new['Topic']=="Software Community Management") & ~new.index.isin(allowed_scm_idx)
    if scm_mask.any():
        replaceables = [t for t in new['Topic'].unique() if t!="Software Community Management"]
        new.loc[scm_mask, 'Topic'] = new.loc[scm_mask, 'Topic'].apply(lambda _: random.choice(replaceables))

    return new
