#include <iostream>
#include <fstream>
#include <format>
#include <vector>
#include <string>
#include <string_view>
#include <list>
#include <time.h>

#include "params.hpp"
#include "base_group.hpp"
#include "base_schedule.hpp"

using namespace std;


void read_data(int number_example, short (&students_record)[J][D][T], short (&students_courses)[J][L])
{

	string file_name = "examples\\orders_2_" + to_string(number_example) + ".txt";

	//cout << file_name;
	ifstream file; // создаем объект класса ifstream
	file.open(file_name); // открываем файл
	
	for (int j = 0; j < J; j++)
	{
		for (int l = 0; l < L; l++)
		{
			file >> students_courses[j][l];
		}
	}


	for (int j = 0; j < J; j++)
	{
		for (int d = 0; d < D; d++)
		{
			for (int t = 0; t < T; t++)
			{
				file >> students_record[j][d][t];

			}
		}
	}

	/*
	for (int j = 0; j < J; j++)
	{
		for (int l = 0; l < L; l++)
		{
			cout << students_courses[j][l];
		}
	}
	cout << "\n";

	for (int j = 0; j < J; j++)
	{
		for (int d = 0; d < D; d++)
		{
			for (int t = 0; t < T; t++)
			{
				cout << students_record[j][d][t];

			}
		}
	}*/
	


}



vector<double> creat_timetable(int number_example)
{
	clock_t t_1 = clock();
	short students_record[J][D][T];
	short students_courses[J][L];
	read_data(number_example, students_record, students_courses);
	clock_t t_2 = clock();

	First_sol f_sol = create_groups(students_record, students_courses);
	clock_t t_3 = clock();
	create_schedule(students_record, students_courses, &f_sol);
	clock_t t_4 = clock();

	double preproc = (double)(t_2 - t_1) / CLOCKS_PER_SEC;
	double f_path = (double)(t_3 - t_2) / CLOCKS_PER_SEC;
	double s_path = (double)(t_4 - t_3) / CLOCKS_PER_SEC;

	/*
	cout << "preproc =" << preproc << endl;
	cout << "f_path =" << f_path << endl;
	cout << "s_path =" << s_path << endl;
	*/
	vector<double> v = { preproc , f_path , s_path };
	return v;
};



int main()
{


	for (int ex = 0; ex < 10; ex++) {
		cout << "Example " << ex + 1 << endl;
		double preproc = 0;
		double f_path = 0;
		double s_path = 0;

		/*
		vector<double> t = creat_timetable(ex + 1);

		preproc += t[0];
		f_path += t[1];
		s_path += t[2];
		*/

		for (int it = 0; it < 5; it++) {
			vector<double> t = creat_timetable(ex + 1);
			preproc += t[0];
			f_path += t[1];
			s_path += t[2];

		}
	
		preproc /= 5;
		f_path /= 5;
		s_path /= 5;

		cout << "preproc =" << preproc << endl;
		cout << "f_path =" << f_path << endl;
		cout << "s_path =" << s_path << endl;
		cout << "total =" << preproc + f_path + s_path << endl;
		cout << endl;

	}

	//cout << "time" << seconds;





}