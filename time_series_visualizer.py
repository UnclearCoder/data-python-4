import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red')
    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    df_line = df.copy()
    df_line['month'] = df_line.index.month
    df_line['year'] = df_line.index.year
    sns.lineplot(data=df_line, legend=False)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year

    df_bar = df_bar.groupby(['year', 'month'])['value'].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax = df_bar.plot(kind='bar', legend=True, figsize=(15, 10))
    ax.set(xlabel='Years', ylabel='Average Page Views', title='Average Page Views per Year')
    ax.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                'October', 'November', 'December'], title='Months', loc='upper left')

    chart = ax.get_figure()
    fig = chart

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():

    df_box = df.copy()

    # Clean data
    df_box['month'] = df_box.index.month
    df_box['year'] = df_box.index.year

    df_box = df_box.sort_values('month')
    df_box['month'] = df_box['month'].apply(lambda x: '0' + str(x) if len(str(x)) == 1 else str(x))
    df_box['month'] = pd.to_datetime(df_box['month'], format='%m').dt.month_name().str.slice(stop=3)

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    ax[0] = sns.boxplot(x=df_box['year'], y=df_box['value'], ax=ax[0])
    ax[0].set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    ax[1] = sns.boxplot(x=df_box['month'], y=df_box['value'], ax=ax[1])
    ax[1].set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')
    ax[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    fig = ax[0].get_figure()


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
