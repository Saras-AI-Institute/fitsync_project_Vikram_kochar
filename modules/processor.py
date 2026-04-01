def calculate_recovery_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate and add a recovery score to the dataframe.

    :param df: Pandas DataFrame containing health data
    :return: DataFrame with an added 'recovery_score' column
    """
    def score_based_on_sleep(sleep_hours):
        if sleep_hours >= 7:
            return 30  # Significant boost for good sleep
        elif sleep_hours < 6:
            return -20  # Significant reduction for poor sleep
        elif 6 <= sleep_hours < 7:
            return 15  # Moderate boost for okay sleep

    def score_based_on_heart_rate(heart_rate):
        if heart_rate < 60:
            return 20  # Best recovery
        elif 60 <= heart_rate <= 70:
            return 15  
        elif 70 < heart_rate <= 80:
            return 5  
        else:
            return -10  # Poor recovery potential

    def score_based_on_steps(steps):
        if steps < 8000:
            return 10  # Normal activity 
        elif 8000 <= steps <= 12000:
            return 15  # Optimal activity
        elif 12000 < steps <= 16000:
            return 0  # Neutral
        else:
            return -15  # Strain due to high activity

    # Calculate recovery score for each row in the dataframe
    df['recovery_score'] = df.apply(
        lambda row: max(0, min(100,
                               50 +  # Base score
                               score_based_on_sleep(row['sleep_hours']) +
                               score_based_on_heart_rate(row['heart_rate_bpm']) +
                               score_based_on_steps(row['steps'])
                              )),
        axis=1
    )

    return df

# Add function to calculate recovery score at the end of module
