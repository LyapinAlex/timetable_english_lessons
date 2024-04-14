#pragma once
#include <vector>
#include <iostream>
#include "params.hpp"

using namespace std;


class Group {
public:
	vector<int> list_students = { 0,0,0,0,0,0,0,0 };
	int num_group;
	int course_group;
	int first_day;
	int second_day;
	int first_time;
	int second_time;
	int id_teacher;
	int first_time_end;
	int second_time_end;
	float score;
	bool working = false;
	//
	std::pair<int, int> expand_time_first_day;
	std::pair<int, int> expand_time_second_day;


	Group(vector<int> list, int num, int course, int d_1, int d_2, int t_1, int t_2) {
		list_students = list;
		num_group = num;
		course_group = course;
		first_day = d_1;
		second_day = d_2;
		first_time = t_1;
		second_time = t_2;
		score = list.size();

	}

	void Print_info() {

		cout << "st:";
		for (int k = 0; k < list_students.size(); k++)
			cout << list_students[k] << " ";
		cout << '\n';

		cout << "n_g" << " " << num_group << " " << '\n';
		cout << "c_g" << " " << course_group << '\n';
		cout << "days_g" << " " << first_day << " " << second_day << '\n';
		cout << "times_g" << " " << first_time << " " << second_time << '\n';
		cout << "times_g" << " " << first_time_end << " " << second_time_end << '\n';


	}

	bool operator==(const Group& other) const {
		return this->list_students.size() == other.list_students.size() && std::equal(this->list_students.begin(), this->list_students.end(), other.list_students.begin(), other.list_students.end());
	}

};


class First_sol {
public:
	int students[J];
	vector<vector<Group>> groups;
	int rooms[D][T];

	First_sol() {


		for (int j = 0; j < J; j++)
			students[j] = 0;

		for (int d = 0; d < D; d++)
			for (int t = 0; t < T; t++)
				rooms[d][t] = 0;


		vector<Group> vec_gr;

		groups.reserve(L);
		for (int l = 0; l < L; l++) {
			groups.push_back(vec_gr);
			groups[l].reserve(10);
		}
	}



};

First_sol create_groups(short(&students_record)[J][D][T], short(&students_courses)[J][L]);

void pr_sol(First_sol f);