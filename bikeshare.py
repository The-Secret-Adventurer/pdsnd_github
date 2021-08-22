#Imports
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington).
    city = input('Please enter the city (chicago, new york city, washington): ').lower()
    while city not in CITY_DATA.keys():
        city = input('{} isn\'t on the list. Make sure you type the city exactly as shown above: '.format(city)).lower()
    print('Got it: {}'.format(city))
        
    # Get user input for month (january, february, ... , june, all)
    month = input('Now pick a month(january-june), or enter "all" to apply no day filter: ').lower()
    while month not in ['january', 'february', 'march' 'april', 'may', 'june', 'all']:
        month = input('Please try again. Please type the month carefully using only letters: ').lower()
    print('Okay, month is: {}'.format(month))
    
    # Get user input for day of week (monday, tuesday, ... sunday, all)
    day = input('Finally, pick a day (eg monday) or "all" : ').lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day = input('I\'m not sure that\'s a day. Make sure you type it in full: ').lower()
    print('Day is: {}'.format(day))
    
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = month.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]       
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    # find the most common month (starting from index 0)
    popular_month = df['month'].mode()[0]
    print('The most popular month is {}.'.format(popular_month))

    # Display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('The most popular day is {}.'.format(popular_day))
    
    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour is {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}.'.format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is {}.'.format(popular_end_station))

    # Display most common start station - station pair
    df['Station Pairs'] = df['Start Station'] + ' - ' + df['End Station']
    popular_station = df['Station Pairs'].max()
    print('The most popular start-end station pair is: {}'.format(popular_station))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {}.'.format(total_travel_time))
        
    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is {}.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of bikeshare use by user type:\n{}.'.format(user_types))
    
    # Display counts of gender  
    try:
        gender = df['Gender'].value_counts() 
        print('\nCount of bikeshare use by user-specified gender:\n{}'.format(gender))
    except KeyError:
        print('No gender data available')
    
    # Display earliest, most recent, and most common year of birth
    try:        
        earliest = df['Birth Year'].min().astype(int)
        most_recent = df['Birth Year'].max().astype(int)
        most_common = df['Birth Year'].mode().astype(int)
        print('\nThe earliest year of birth is {}. The most recent year of birth is {}. The most common year of birth is {}.'.format(earliest, most_recent, most_common))
    except KeyError:
        print('No birth year data available')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw(df):
    ''' Asks the user if they want to see raw data and allows them to see 5 rows at a time. '''
    
    raw_data_yn = input('Would you like to see the raw data? y/n ').lower()
    raw_data = 0
    
    while raw_data_yn.lower() == 'y':
        print(df.iloc[raw_data : raw_data + 5])
        raw_data += 5
        raw_data_yn = input('See 5 more rows? y/n ').lower()
    else:
        print('Okay.')
    
    print('-'*40)
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)
        
        restart = input('\nWould you like to restart? y/n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
