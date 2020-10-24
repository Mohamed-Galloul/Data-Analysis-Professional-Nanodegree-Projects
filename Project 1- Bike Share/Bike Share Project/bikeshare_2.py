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

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # create a list for the cities to check if the entered city is one of them.
    city_list=['chicago', 'new york city', 'washington']
    print("\nPlease Enter your selected city: 'chicago', 'new york city', 'washington'\n ")
    city=input("HINT: make sure you type city name in lowercase and put spaces between words\n ").lower()

    # check whether a valid city name or alert the user that he entered invalid city name
    while (city not in city_list):
        print('invalid city name\n ')
        print("make sure your selected city is typed like this (without single quotes): 'chicago', 'new york city', 'washington' \n")
        print("don\'t forget spaces in 'new york city' \n")
        city = input().lower()

    # get user input for month (all, january, february, ... , june)
    # create a dictionary for months as its key: month abbrev and its value: the corresponding month
    month_dict={'all':'all',
                 'jan':'january',
                 'feb':'february',
                 'mar':'march',
                 'apr':'april',
                 'may':'may',
                 'jun':'june'}
    print("please enter month abbrev. in lowercase, such jan for january, feb for february, mar, apr, may and, jun for june\n ")
    print("you can only choose between january and june [jan .. jun] OR type 'all' (without single quotes) for the whole six months\n")
    month = input().lower()

    # check whether a valid month abbrev. or alert the user that he entered invalid month abbrev.
    while (month not in month_dict ):
        print('invalid month abbrev.\n ')
        print("make sure that you choose month between january and june [jan .. jun] OR type 'all' (without single quotes) for the whole six months\n")
        print("type only the first 3 letters of the month OR all \n")
        month = input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # create a dictionary for days of week as its key: day of week abbrev and its value: the corresponding day
    day_of_week_dict={'all':'all',
                    'mon':'monday',
                    'tue':'tuesday',
                    'wed':'wednesday',
                    'thr':'thursday',
                    'fri':'friday',
                    'sat':'saturday',
                    'sun':'sunday'}
    print("please enter day of week abbrev. in lowercase, such mon for monday, tue for tuesday, wed, thr, fri, sat, and sun for sunday\n ")
    print("you can choose between monday and sunday [mon .. sun] OR type 'all' (without single quotes) for the whole days of the week\n")
    day = input().lower()

    # check whether a valid day of week or alert the user that he entered invalid day of week
    while (day not in day_of_week_dict ):
        print('invalid day abbrev.\n ')
        print("make sure that you choose day between monday and sunday [mon .. sun] OR type 'all' (without single quotes) or the whole days of the week\n")
        print("type only the first 3 letters of the day OR all \n")
        day = input().lower()

    print('-'*40)
    return city, month_dict[month], day_of_week_dict[day] #**


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
    # load the corresponding .csv file based on the entered city
    df=pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() #**weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month by month name rather than its number
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month= df['month'].value_counts().idxmax()
    print('\nMost common month: ', months[common_month - 1], ' ',df['month'].value_counts().max())

    # display the most common day of week
    common_day_of_week= df['day_of_week'].value_counts().idxmax()
    print('\nMost common day of week:', common_day_of_week, ' ',df['day_of_week'].value_counts().max())

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_start_hour= df['start_hour'].value_counts().idxmax()
    print('\nMost common start hour: ', common_start_hour, ' ',df['start_hour'].value_counts().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station= df['Start Station'].value_counts().idxmax()
    print('\nMost common start station: ', common_start_station, ' ',df['Start Station'].value_counts().max())

    # display most commonly used end station
    common_end_station= df['End Station'].value_counts().idxmax()
    print('\nMost common end station: ', common_end_station, ' ',df['End Station'].value_counts().max())

    # display most frequent combination of start station and end station trip
    df['trip_path'] = 'From  ' + df['Start Station'] + '  To  ' + df['End Station']
    common_trip_path= df['trip_path'].value_counts().idxmax()
    print('\nMost common trip path: ', common_trip_path, ' ',df['trip_path'].value_counts().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nTotal travel time: ", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nMean travel time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nCounts of user types: \n", user_types)

    # check whether the entered city has Genderand Birth Year data or not
    # only chicago and NYC have Gender and Birth Year data
    if city == 'chicago' or city == 'new york city':
    # Display counts of gender
        gender = df['Gender'].value_counts()
        print("\nCounts of gender: \n",gender )

    # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth =df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth =df['Birth Year'].value_counts().idxmax()
        print("\nEarliest year of birth: ", earliest_year_of_birth)
        print("\nMost recent year of birth: ", most_recent_year_of_birth)
        print("\nMost common year of birth: ", most_common_year_of_birth, " ", df['Birth Year'].value_counts().max())

    else:
        print("\nSorry! No provided data about Gender or Birth Year for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_sample_of_data(df):
    '''
    Display a sample of the filtered data if the user wants to see it.
    '''
    #ask the user if he/she would like to see a sample of the filtered data
    answer1 = input("would you like to see a sample of the data? (yes or no)\n")

    # let the user choose the start row number and end row number
    if answer1 == "yes":

        # make sure that the user didn't enter invalid input causing an error
        try:
            print("HINT: The presented data sample is arranged based on your filters not on the true indices unless you chose all months and all days ")
            indices = input("please enter your start row number 'INCLUDED' and end row number 'EXCLUDED' seperated by a comma (ex: 5,10)\n")
            start_index= int(indices.split(",")[0])
            end_index= int(indices.split(",")[1])
            interval= end_index-start_index # does not need to be 5 any interval based on the entered indices
            print("data from row number {} to row number {} are:\n".format(start_index,end_index))
            print(df.iloc[start_index:end_index])

        # if the user entered an input caused an error he/she will know it without effecting the whole program.
        except Exception as e:
            print(e)
            print("\nmake sure you enter integers only seperated by a comma, and be within the data range\n")
            show_sample_of_data(df) #calling the function again to give the user the chance to try again

        # ask the user again if he/she wants to see the next interval of rows
        else:
            answer2 = input("would you like to see the next {} rows? (yes or no)\n".format(interval))
            while answer2=='yes':
                start_index+=interval
                end_index+=interval
                print("data from row No. {} to row No. {} are:\n".format(start_index,end_index).format(interval))
                print(df.iloc[start_index:end_index])
                answer2 = input("\nwould you like to see the next {} rows? (yes or no)\n".format(interval))



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_sample_of_data(df)


        print("\nThese statistics were for:\n city: {} , month(s): {} , day(s) of week: {} \n".format(city,month,day))

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
