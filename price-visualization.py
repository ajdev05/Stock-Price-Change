import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

file_path = 'SPY_2024-09-13_minute_data.csv'  
df = pd.read_csv(file_path)

df['Datetime'] = pd.to_datetime(df['Datetime'])

df.set_index('Datetime', inplace=True)

resampled_df = df.resample('5min').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum'
})

fig, ax = plt.subplots(figsize=(18, 10))

for i in range(len(resampled_df) - 1):
    chunk = resampled_df.iloc[i]
    start_time = chunk.name
    next_chunk = resampled_df.iloc[i + 1]
    
    color = 'green' if next_chunk['Close'] > chunk['Open'] else 'red'
    
    ax.plot([start_time, next_chunk.name], [chunk['Close'], next_chunk['Close']], color=color, linewidth=3)

    ax.plot(start_time, chunk['Close'], 'ko', markersize=8)  

start_time_display = pd.Timestamp('2024-09-13 09:30:00') 
time_labels = [start_time_display + timedelta(minutes=5 * i) for i in range(len(resampled_df))]

ax.set_xticks(resampled_df.index)
ax.set_xticklabels([t.strftime('%H:%M') for t in time_labels]) 

fig.autofmt_xdate(rotation=45)

ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

ax.set_title('SPY Price Movement - 5 Minute Time Frame', fontsize=16)
ax.set_xlabel('Time', fontsize=14)
ax.set_ylabel('Price', fontsize=14)
legend_lines = [plt.Line2D([0], [0], color='green', linewidth=3, label='Closing Price Increased'),
                plt.Line2D([0], [0], color='red', linewidth=3, label='Closing Price Decrease')]
ax.legend(handles=legend_lines, loc='upper left', fontsize=12)

plt.xticks(fontsize=10)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.savefig(f'img_{file_path}.png')

