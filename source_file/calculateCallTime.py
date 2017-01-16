# For calculate call time
# 2016.12.15
# by louisa

import csv

FILE_USER_DATA = './setting/user_data.txt'

f_in = open('../motion.tsv', 'r')
f_out = open('../results/call_logs.csv', 'ab')
TITLE_FORMAT = ['ID', 'CALL_TIME', 'START_TIME', 'END_TIME', 'DATE']

csvWriter = csv.writer(f_out)

first_day_list = []
last_day_list = []
first_call_time_list = []
last_call_time_list = []
is_start_time_recorded = False
is_end_time_recorded = False
is_experiment_started = False
is_experiment_ended = False
startCallDate_list = []
endCallDate_list = []
start_time = ''
end_time = ''
call_id = 1


# Write down ID, Name, Start Date, End Date and Titles at top of f_out
# and get experiment schedule from f_userData
def init_output_file( temp_file = open(FILE_USER_DATA, 'r') ):
    # Insert a blank line on the top of data.
    # Without this blank line you will get an error:
    # "Either the file has error or it is not a SYLK file format. "
    # when you open output .csv file by Excel.
    csvWriter.writerow([])
    # Write user data read from user_data.txt
    for line in temp_file:
        item_list = line.strip('\n').split('\t')
        user_data_output = []
        for i in range(len(item_list)):
            user_data_output.append(item_list[i])
        csvWriter.writerow(user_data_output)
    # Insert a blank line under the user data
    csvWriter.writerow([])
    # Write title
    csvWriter.writerow(TITLE_FORMAT)
    temp_file.close()


def get_experiment_schedule( temp_file = open(FILE_USER_DATA, 'r') ):
    global first_day_list
    global last_day_list
    global first_call_time_list
    global last_call_time_list

    for line in temp_file:
        item_list = line.strip('\n').split('\t')
        if item_list[0] == 'Start Date:':
            first_day_list = item_list[1].split('.')
        elif item_list[0] == 'End Date:':
            last_day_list = item_list[1].split('.')
        elif item_list[0] == 'Start Time:':
            first_call_time_list = item_list[1].split(':')
        elif item_list[0] == 'End Time:':
            last_call_time_list = item_list[1].split(':')

    temp_file.close()


# def check_day_in_range(date_list):
#     is_in_range = [False] * 3
#     # year = xxx_list[0],  month = xxx_list[1],  day = xxx_list[2]
#     if first_day_list[0] == last_day_list[0]:      # Start and end in same year.
#         is_in_range[0] = True
#         if first_day_list[1] == last_day_list[1]:       # Start and end in same month.
#             is_in_range[1] = True
#             if date_list[2] in range(first_day_list[2], (last_day_list[2]+1)):
#                 is_in_range[2] = True
#     elif ( first_day_list[0] != last_day_list[0] \
#             and \
#         first_day_list[1] != last_day_list[1] \
#             and \
#         first_day_list[2] != last_day_list[2] ):
#         for i in range(3):
#             if date_list[i] in range(first_day_list[i], (last_day_list[i]+1)):
#                 is_in_range[i] = True
#
#     if is_in_range.count(True) == 3:
#         return True
#     else:
#         return False


def check_same_day(start_list, end_list):
    is_same_day = [False] * 3
    for i in range(3):
        # year = xxx_list[0],  month = xxx_list[1],  day = xxx_list[2]
        if start_list[i] == end_list[i]:
            is_same_day[i] = True
    if is_same_day.count(True) == 3:
        return True
    else:
        return False


def cut_time_data(temp_data):
    temp_list1 = temp_data.split('T')
    temp_list2 = temp_list1[1].split('+')
    time_list = temp_list2[0].split(':')
    return time_list


def cut_date_data(date_str):
    temp_list = date_str.split('T')
    date_list = temp_list[0].split('-')
    return date_list


def calculate_time(start_list, end_list):
    start_list = map(int, start_list)
    end_list = map(int, end_list)
    hh = end_list[0] - start_list[0]
    mm = end_list[1] - start_list[1]
    ss = end_list[2] - start_list[2]
    if mm < 0:
        hh -= 1
        mm += 60
    if ss < 0:
        mm -= 1
        ss += 60
    hh_str = '%02d' % hh
    mm_str = '%02d' % mm
    ss_str = '%02d' % ss
    call_time = hh_str + ':' + mm_str + ':' + ss_str
    return call_time


def compare2time_values(start_list, end_list):
    start_list = map(int, start_list)
    end_list = map(int, end_list)
    hh = end_list[0] - start_list[0]
    mm = end_list[1] - start_list[1]
    ss = end_list[2] - start_list[2]
    if mm < 0:
        hh -= 1
        mm += 60
    if ss < 0:
        mm -= 1
        ss += 60
    if hh >= 0 and mm >= 0 and ss >= 0:
        return True
    else:
        return False


def cut_call_data(log_list):
    global is_start_time_recorded
    global is_end_time_recorded
    global startCallDate_list
    global endCallDate_list
    global start_time
    global end_time
    global call_id

    date_list = cut_date_data(log_list[2])
    # Check if the data is in the period of experiment schedule

    if log_list[1] == '<51,0>':
        if not is_start_time_recorded:
            startCallDate_list = date_list
            start_time = cut_time_data(log_list[2])
            is_start_time_recorded = True
        else:
            startCallDate_list = date_list
            start_time = cut_time_data(log_list[2])
        # for test
        #print log_list[1], log_list[2]

    if log_list[1] == '<50,0>':
        # for test
        #print log_list[1], log_list[2]
        endCallDate_list = date_list

        if is_start_time_recorded:
            is_same_day = check_same_day(startCallDate_list, endCallDate_list)
            if is_same_day:
                end_time = cut_time_data(log_list[2])
                is_start_time_recorded = False
                is_end_time_recorded = True


    if is_end_time_recorded:
        # Calculate how long a call lasted
        call_time = calculate_time(start_time, end_time)

        # Create output csv item list
        call_log_output = []
        call_log_output.append(call_id)
        call_log_output.append(call_time)
        call_log_output.append(start_time[0] + ':' + start_time[1] + ':' + start_time[2])
        call_log_output.append(end_time[0] + ':' + end_time[1] + ':' + end_time[2])
        call_log_output.append(date_list[0] + '.' + date_list[1] + '.' + date_list[2])
        # Write call logs: [id, call_time, start_time, end_time, date]
        csvWriter.writerow(call_log_output)
        #print 'call_log_output: ', call_log_output

        # initialize global variables
        is_end_time_recorded = False
        startCallDate_list = []
        endCallDate_list = []
        start_time = ''
        end_time = ''
        call_id += 1


# Main program
init_output_file()
get_experiment_schedule()
line_no = 0
for line in f_in:
    log_list = line.strip('\n').split('\t')
    if line_no > 0:
        date_list = cut_date_data(log_list[2])
        time_list = cut_time_data(log_list[2])
        if not is_experiment_started:
            is_first_day = [False] * 3
            for i in range(3):
                if date_list[i] == first_day_list[i]:
                    is_first_day[i] = True
            if is_first_day.count(True) == 3:
                if compare2time_values(first_call_time_list, time_list):
                    is_experiment_started = True
        else:
            if not is_experiment_ended:
                is_last_day = [False] * 3
                for i in range(3):
                    if date_list[i] == last_day_list[i]:
                        is_last_day[i] = True
                if is_last_day.count(True) == 3:
                    if compare2time_values(last_call_time_list, time_list):
                        is_experiment_ended = True
                        print "is_experiment_ended = ", is_experiment_ended
            else:
                break
        if is_experiment_started and not is_experiment_ended:
                cut_call_data(log_list)
    line_no += 1

f_in.close()
f_out.close()

print "call_logs.cvs has been writen!"
