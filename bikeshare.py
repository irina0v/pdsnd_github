import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_list = ['january', 'february', 'march', 'april', 'may', 'june']
days_list = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
#print(days_list)
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n Hello! Let\'s explore some US bikeshare data!')
    #getting city name to choose which file to load
    city=""    
    while city not in CITY_DATA.keys():
        city = input("\n Would you like to explore data for Chicago, New York or Washington?\n").lower().replace('new york', 'new york city')   
        if city in CITY_DATA.keys():
            break
        else:
            print("\n Sorry,there is no such option")
        continue
        
    #getting user's choice on using or not a filter by month/day of the week
    month="all"
    day="all"
    filtertype = ""
    while filtertype not in ['month','day','none']:
        filtertype = input("\n Would you like to filter the data by month, day of the week or not filter at all? \n Please type month / day / none to choose from these options \n").lower()
        if filtertype == 'month':
            while month not in months_list:
                day = "all"
                month = input(" Please enter full month name\n Data available for January - June\n").lower()
                if month in months_list:
                    break
                else:
                    print("sorry, I cannot accept this\n")   
                continue
        elif filtertype == 'day':
            month = "all"
            while day not in days_list:
                day = input("Please enter full name of the day of the week\n").lower()
                if day in days_list:
                    break
                else:
                    print("sorry, I cannot accept this\n")   
                continue
        elif filtertype == 'none':
            month = "all"
            day = "all"

    #showing user's choice on a screen
    print('-'*40)
    print("\n OK, you've chosen to look at the data on:\n city: {}\n month(s): {}\n day(s): {}\n".format(city.title(), month.title(), day.title()))
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
    # add column with trip routes
    df['Route'] = df['Start Station']+" - "+df['End Station']
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
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
    # display the most common month
    common_month = df['month'].mode()[0]
        
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    
    print(" The most common MONTH to start a trip was {}".format(common_month))
    print(" The most common DAY to start a trip was {}".format(common_day))
    print(" The most common HOUR to start a trip was {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().index 
    
    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().index    
    
    # display most frequent combination of start station and end station trip
    popular_route = df['Route'].value_counts().index
    
    print(" The most common START station was {}".format(popular_start_station[0]))
    print(" The most common END station was {}".format(popular_end_station[0]))
    print(" The most common ROUTE was {}".format(popular_route[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = pd.to_timedelta(df['Trip Duration'].sum(),'s')

    # display mean travel time
    mean_travel_time = pd.to_timedelta(df['Trip Duration'].mean(),'s')
    
    print(" Users spent on shared bikes {} in total".format(total_travel_time))
    print(" Users spent on shared bikes {} on average".format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(" There were next types of users:\n",user_types)
    
    # error handling for Washington which does NOT have data on genders and birth years
    try :
        # Display counts of gender
        gender_types = df['Gender'].value_counts()
        print("\n There were users who specified their gender as:\n",gender_types)

        # Display earliest, most recent, and most common year of birth
        print("\n People who shared bikes also shared next info about their birth years.\n They were born:")
        earliest_year = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode())
        print(" earliest in ",earliest_year)    
        print(" most recently in ",most_recent)
        print(" most commonly in ",common_year)
        
    except KeyError:
        print("\n Unfortunately, there is no gender and birth year data for this city")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
def raw_data(df):
    """Prompts user to look at raw data at 5 line increments at a time."""
    
    rows = 0
    show = input("\n Would you like to see raw data for Bikeshare? it will be shown in 5 lines at a time.\n Please type yes or no\n").lower()
    while True:
        if show == "yes":
            pd.set_option("display.max_columns",200)
            print(df.iloc[rows:rows+5])
            rows+=5
            show = input("\n Would you like to see 5 more lines of data? Please type yes or no\n").lower()
        elif show == "no":
            break
        else:
            print("\nI guess this means no so we stop here\n")
            break

            
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\n Would you like to restart? Please type yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
