#pragma once
#include "params.hpp"
#include "base_group.hpp"
#include <vector>



using namespace std;

class Second_sol {
public:
	vector<vector<pair<int, int>>> teachers;
	int teachers_work_days[D][I];
	int schedule_of_teachers[I][D][Real_time];
	vector<Group> sort_groups;

	Second_sol(){

		for (int i = 0; i < I; i++)
			for (int d = 0; d < D; d++) {
				teachers_work_days[d][i] = 0;
				for (int t = 0; t < Real_time; t++)
					schedule_of_teachers[i][d][t] = 0;
			}

		vector<pair<int, int>> vec_gr;

		teachers.reserve(I);
		for (int i = 0; i < I; i++) {
			teachers.push_back(vec_gr);
			teachers[i].reserve(10);
		}

	}



};

void create_schedule(short(&students_record)[J][D][T], short(&students_courses)[J][L], First_sol *f_s);

