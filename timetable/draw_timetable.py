 #!usr/bin/env python
 #coding: utf-8
import matplotlib.pyplot as plt
days = ['Mon','Tue', 'Wed', 'Thur', 'Fri', 'Sat']
rooms=['Room A','Room B', 'Room C', 'Room D']
colors=['pink', 'lightgreen', 'lightblue', 'wheat', 'salmon'] 


input_files=['data_schdeule.txt']
day_labels=['Day 1']
 
def timetable_png(name_schedule): 

    for input_file, day_label in zip(input_files, day_labels):
        fig=plt.figure(figsize=(10,5.89))

        # Set Axis
        ax=fig.add_subplot(111)
        ax.yaxis.grid()
        ax.set_xlim(0.0,len(rooms)*len(days))
        ax.set_ylim(20.1, 8.9)
        ax.set_xticks(range(2,len(rooms)*len(days)+2, len(rooms)))
        ax.set_xticklabels(days)
        ax.set_ylabel('Time')

        # Set Second Axis
        ax2=ax.twiny().twinx()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_ylim(ax.get_ylim())
        ax2.set_xticks(ax.get_xticks())
        ax2.set_xticklabels(days)
        ax2.set_ylabel('Time')

        for d in range(len(days)):
            plt.axvline(len(rooms)*d,color='black')

        # # for d in range(9,21):
        #     plt.axhline(float(d),color='black',linewidth=0.2)


        for line in open(input_file, 'r'):
            data=line.split()
            event=data[-1]
            teacher = int(data[2])
            room_1 = float(data[3])
            room_2 = float(data[7])
            day_first = (float(data[4]),float(data[5]),float(data[6]))
            day_second = (float(data[8]),float(data[9]),float(data[10]))

            # plot event
            # plt.fill_between([room, room+1.96], [start, start], [end,end], color=colors[int(data[0]-1)])
            plt.fill_between([day_first[0]*len(rooms) + room_1 - 1,day_first[0]*len(rooms) + room_1 ], [day_first[1]/4 + 9.0, day_first[1]/4 + 9.0], [day_first[2]/4 + 9.25,day_first[2]/4 + 9.25], color=colors[teacher], edgecolor='k', linewidth=0.5)
            plt.fill_between([day_second[0]*len(rooms) + room_2 - 1,day_second[0]*len(rooms) + room_2 ], [day_second[1]/4 + 9.0, day_second[1]/4 + 9.0], [day_second[2]/4 + 9.25,day_second[2]/4 + 9.25], color=colors[teacher], edgecolor='k', linewidth=0.5)
            # # plot beginning time
            # plt.text(day_first[0]*len(rooms) + room - 1+0.02,day_first[1]/4 + 9.0+0.05 ,day_first[1]/4 + 9.0, va='top', fontsize=7)
            # plt.text(day_second[0]*len(rooms) + room - 1+0.02,day_second[1]/4 + 9.0+0.05 ,day_second[1]/4 + 9.0, va='top', fontsize=7)
            # plot event name

            # plt.text(day_first[0]*len(rooms) + room - 1+0.5, (day_first[1]/4 + 9.0+day_first[1]/4 + 9.0)*0.5, f"k = {data[0]} l = {data[1]}", ha='center', va='center', fontsize=6)
            # plt.text(room+0.48, (start+end)*0.5, event, ha='center', va='center', fontsize=11)
            plt.text(day_first[0]*len(rooms) + room_1 - 1+0.02,day_first[1]/4 + 9.0+0.05 ,f"L:{data[1]}K:{data[0]}", va='top', fontsize=5)
            plt.text(day_second[0]*len(rooms) + room_2 - 1+0.02,day_second[1]/4 + 9.0+0.05 ,f"L:{data[1]}K:{data[0]}", va='top', fontsize=5)    


        plt.title(name_schedule,y=1.07)
        plt.savefig('{0}.png'.format(name_schedule), dpi=200)


