import pandas as pd

def generate_insights(df: pd.DataFrame):
    insights = []

    try:
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        if 'spend' in df.columns:
            total_spend = df['spend'].sum()
            insights.append(f"Total spend: ${total_spend:,.2f}")
        if 'impressions' in df.columns:
            avg_impressions = df['impressions'].mean()
            insights.append(f"Average impressions per campaign: {avg_impressions:,.0f}")
        if 'clicks' in df.columns and 'impressions' in df.columns:
            df['ctr'] = df['clicks'] / df['impressions'] * 100
            avg_ctr = df['ctr'].mean()
            insights.append(f"Average Click-Through Rate (CTR): {avg_ctr:.2f}%")
        if 'conversions' in df.columns and 'clicks' in df.columns:
            df['cvr'] = df['conversions'] / df['clicks'] * 100
            avg_cvr = df['cvr'].mean()
            insights.append(f"Average Conversion Rate (CVR): {avg_cvr:.2f}%")
        if 'sentiment' in df.columns:
            avg_sentiment = df['sentiment'].mean()
            insights.append(f"Average sentiment score: {avg_sentiment:.2f}")

    except Exception as e:
        insights.append(f"Error generating insights: {str(e)}")

    return insights