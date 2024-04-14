#include "base_schedule.hpp"
#include "base_group.hpp"
#include <algorithm>
#include <math.h>
#include <optional>
#include <cmath>
#include <ranges>

void reform(short(&students_record)[J][D][T], Group* g);
void new_add_group_in_timetable(Group* gr, vector<vector<int>>* appropriate_time, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol* s_sol);
void new_marker_days(int i, Group* gr, int t_1, int t_2, Second_sol* s_sol);
void new_appoint(short(&students_record)[J][D][T], short(&students_courses)[J][L], First_sol* f_sol, Second_sol* s_sol);

/*
*/
bool greatest(Group* A, Group* B) {
	

	float num_gr_a = (*A).score;
	float num_gr_b = (*B).score;

	if (num_gr_b == 0)
		return true;
	else {
		if (num_gr_a == 0)
			return false;
		else {
			if (num_gr_a > num_gr_b)
				return true;
			if (num_gr_a < num_gr_b)
				return false;
			else {
		

				int t_A = Real_time - max((*A).first_time_end + 1 - timeLesssons[(*A).course_group] + 1 - (*A).first_time, (*A).second_time_end + 1 - timeLesssons[(*A).course_group] + 1 - (*A).second_time);
				int t_B = Real_time - max((*B).first_time_end + 1 - timeLesssons[(*B).course_group] + 1 - (*B).first_time, (*B).second_time_end + 1 - timeLesssons[(*B).course_group] + 1 - (*B).second_time);

				if (t_A > t_B)
					return true;
				if (t_A < t_B)
					return false;
				else {

					int a_3 = L - (*A).course_group;
					int b_3 = L - (*B).course_group;

					if (a_3 > b_3)
						return true;
					else
						return false;


				}


			}

		}

	}





}

void sorting_new(vector<Group>* vec_gr) {

	int len_size = (*vec_gr).size();

	for (int k_1 = 0; k_1 < len_size; k_1++) {
		for (int k_2 = 0; k_2 < len_size; k_2++) {
			
			/*

			float num_gr_a = (*vec_gr)[k_1].score;
			float num_gr_b = (*vec_gr)[k_2].score;

			int num_gr_a = (*vec_gr)[k_1].list_students.size();
			int num_gr_b = (*vec_gr)[k_2].list_students.size();
			*/


			if (greatest(&(*vec_gr)[k_1], &(*vec_gr)[k_2])) {
				//if ((*vec_gr)[k_1].list_students.size() > (*vec_gr)[k_2].list_students.size()) {

				Group rez = (*vec_gr)[k_1];
				(*vec_gr)[k_1] = (*vec_gr)[k_2];
				(*vec_gr)[k_2] = rez;
			}


		}

	}

}


void sorting(vector<Group>* vec_gr) {

	for (int k_1 = 0; k_1 < 86; k_1++) {
		for (int k_2 = 0; k_2 < 86; k_2++) {
			
			
			int t_A = max((*vec_gr)[k_1].first_time_end - (*vec_gr)[k_1].first_time, (*vec_gr)[k_1].second_time_end - (*vec_gr)[k_1].second_time);
			int t_B = max((*vec_gr)[k_2].first_time_end - (*vec_gr)[k_2].first_time, (*vec_gr)[k_2].second_time_end - (*vec_gr)[k_2].second_time);
			int s_A = (*vec_gr)[k_1].list_students.size();
			int s_B = (*vec_gr)[k_2].list_students.size();

			//x: len(x[0]) * 10000 + (44 - max(x[3][2] - x[3][1], x[4][2] - x[4][1])) * 100 + (13 - x[2]))
			int A_v = s_A * 10000 + (44 - t_A) * 100 + (13 - (*vec_gr)[k_1].course_group);
			int B_v = s_B * 10000 + (44 - t_B) * 100 + (13 - (*vec_gr)[k_2].course_group);
			if (A_v > B_v){
			//if ((*vec_gr)[k_1].list_students.size() > (*vec_gr)[k_2].list_students.size()) {

				Group rez = (*vec_gr)[k_1];
				(*vec_gr)[k_1] = (*vec_gr)[k_2];
				(*vec_gr)[k_2] = rez;
			}

		}

	}

}


bool comp_heur(Group A, Group B) {

	int t_A = max(A.first_time_end - A.first_time, A.second_time_end - A.second_time);
	int t_B = max(B.first_time_end - B.first_time, B.second_time_end - B.second_time);
	int s_A = A.list_students.size();
	int s_B = B.list_students.size();
		
    //x: len(x[0]) * 10000 + (44 - max(x[3][2] - x[3][1], x[4][2] - x[4][1])) * 100 + (13 - x[2]))
	int A_v = s_A * 10000 + (44 - t_A) * 100 + (13 - A.course_group);
	int B_v = s_B * 10000 + (44 - t_B) * 100 + (13 - B.course_group);
	if (B_v < A_v)
		return true;
	else
		return false;
	
}


bool comp_size(Group A, Group B) {

	return B.list_students.size() < A.list_students.size();
}



void change_format_group(short(&students_record)[J][D][T], short(&students_courses)[J][L], First_sol* f_sol, Second_sol *s_sol)
{
	int K = 0;
	for (int l = 0; l < L; l++)
		K += f_sol->groups[l].size();
		
	



	vector<Group> vec_gr;


	vec_gr.reserve(K);

	for (int l = 0; l < L; l++) {
		for (Group& x : f_sol->groups[l]) {

			reform(students_record, &x);
			vec_gr.push_back(x);
		}
	}


	for (int l = 0; l < L; l++) 
		sorting_new(&(f_sol->groups[l]));


	sorting(&vec_gr);
	/*
	for (int k = 0; k < K; k++) {
		cout << vec_gr[k].course_group << ' ' << vec_gr[k].num_group << ' ' << vec_gr[k].list_students.size() << endl;
	}
	*/
    
	s_sol->sort_groups = vec_gr;

}

void appoint(short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol* s_sol);

void create_schedule(short(&students_record)[J][D][T], short(&students_courses)[J][L], First_sol *f_sol)
{

	Second_sol  s_sol;



	/*
	for (auto gr : f_sol->groups[7]) {
		gr.Print_info();
	}
	*/

	change_format_group(students_record, students_courses, f_sol, &s_sol);
	/*
	for (auto gr : f_sol->groups[7]) {
		gr.Print_info();
	}
	*/

	new_appoint(students_record, students_courses, f_sol,&s_sol);


}



void reform(short(&students_record)[J][D][T], Group *g) {

	vector<int> vec_st = (*g).list_students;
	int d_1 = (*g).first_day;
	int d_2 = (*g).second_day;
	vector<int> time_first_day( T, 1 );
	vector<int> time_second_day( T, 1 );

	for (int j : vec_st) 
		for (int t = 0; t < T; t++){
			time_first_day[t] *= students_record[j][d_1][t];
			time_second_day[t] *= students_record[j][d_2][t];
	}

	pair<int, int> board_exp_time_first{ -1, -1 };
	pair<int, int> board_exp_time_second{ -1, -1 };
	bool ind_1 = true;
	bool ind_2 = true;

	for (int t = 0; t < T; t++) {

		if (time_first_day[t] == 1 && ind_1) {
			ind_1 = false;
			board_exp_time_first.first = t * 4;
		}
		else {
			if (time_first_day[t] == 0 && !ind_1) {
				board_exp_time_first.second = 4 * (t - 1);
				ind_1 = true;
			}
		}


		if (time_second_day[t] == 1 && ind_2) {
			ind_2 = false;
			board_exp_time_second.first = t * 4;
		}
		else {
			if (time_second_day[t] == 0 && !ind_2) {
				board_exp_time_second.second = 4 * (t - 1);
				ind_2 = true;
			}
		}
	}


	// CHANGE: 44 ->40
	/*
	if (board_exp_time_first.second == -1)
		board_exp_time_first.second = 44;
	if (board_exp_time_second.second == -1)
		board_exp_time_second.second = 44;
	*/

	if (board_exp_time_first.second == -1)
		board_exp_time_first.second = 40;
	if (board_exp_time_second.second == -1)
		board_exp_time_second.second = 40;



	(*g).first_time = board_exp_time_first.first;
	(*g).second_time = board_exp_time_second.first;

	(*g).first_time_end = board_exp_time_first.second;
	(*g).second_time_end = board_exp_time_second.second;



}


void add_group_in_timetable(int id_gr, vector<vector<int>> *appropriate_time, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol* s_sol);


bool check_in_timetable(int t_1, int t_2, Group *gr, int  i, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol);
bool check_limit_working_days(int i, Group *gr, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol);
bool check_teachers_break(int i, Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol);
bool check_time_teachers(int i, Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol);
bool check_limit_work_time(int i, Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol);

vector<int> get_list_teacher(Second_sol *s_sol);
void marker_days(int i, int id_gr, int best_time_1, int best_time_2, Second_sol* s_sol);

std::optional<Group> get_next_group(vector<vector<Group>>* groups, vector<int> counter_group) 
{

	vector<Group> applicant_group;
	


	for (int l = 0; l < L; l++)
		if ((*groups)[l].size() != 0) {

			
			//std::cout << (*groups)[l][0].list_students.size()  << endl;
			applicant_group.push_back((*groups)[l][0]);
		}

	/*
	for (auto x : counter_group)
		std::cout << x << "  ";
	std::cout << endl;
	*/

	for (Group& group: applicant_group) {

		double penalty;

		if (counter_group[group.course_group] < K)
			penalty = F[group.course_group][counter_group[group.course_group]];
		else
			penalty = 2.5;

		double num_st = group.list_students.size();
		//std::cout << num_st <<" " << penalty << endl;
		//std::cout << num_st - penalty << endl;

		group.score = (float)(num_st - penalty);
		//std::cout << group.score << endl;

		
	//	std::cout << "num :" << group.num_group << " cource: " << group.course_group << " score: " << group.score << endl;
	}

	sorting_new(&applicant_group);

	/*
	for (auto& group : applicant_group) {
		std::cout << "num :" << group.num_group << " cource: " << group.course_group << " score: " << group.score << endl;
	}
	*/

	if ((applicant_group.size() == 0) || (applicant_group[0].score <= 0.0)) {
		//std::cout << endl << " None group " << endl;
		return std::nullopt;
	}
	else 
	{


		//(applicant_group[0]).Print_info();
		//std::cout << endl << "num :" << applicant_group[0].num_group << " cource: " << applicant_group[0].course_group << " score: " << applicant_group[0].score << endl << endl;


	
		return applicant_group[0];
	}



	
}

void new_appoint(short(&students_record)[J][D][T], short(&students_courses)[J][L],First_sol* f_sol, Second_sol* s_sol)
{	


	vector<vector<Group>> groups = f_sol->groups;
	
	vector<int> counter_group(L, 0);



	std::optional<Group> cur_group = get_next_group(&groups, counter_group);

	vector<Group> assigned_groups;

	while (cur_group) {

		//std::cout << "num :" << cur_group->num_group << " cource: " << cur_group->course_group << " score: " << cur_group->score << endl;

		groups[cur_group->course_group].erase(std::remove(groups[cur_group->course_group].begin(), groups[cur_group->course_group].end(), *cur_group),groups[cur_group->course_group].end());
		
		Group group = *cur_group;

		/*
		float penalty;
		//change K type -> const int in params.hpp
		if (counter_group[group.course_group] < K)
			penalty = (float)F[group.course_group, counter_group[group.course_group]];
		else
			penalty = 2.5;

		float cost_group = group.list_students.size() - penalty;
		*/

		if (group.score < 0){
			group.working = false;
			group.id_teacher = -1;
			assigned_groups.push_back(group);
			cur_group = get_next_group(&groups, counter_group);
			continue;
		}

		vector<vector<int>> appropriate_times;

		for (int t_1 = group.first_time; t_1 < 4 + group.first_time_end; t_1++)
			for (int t_2 = group.second_time; t_2 < 4 + group.second_time_end; t_2++)
				for (int i = 0; i < I; i++) {


					if (check_in_timetable(t_1, t_2, &group, i, students_record, students_courses, s_sol)) {
						vector<int> v = { t_1, t_2, i };
						appropriate_times.push_back(v);


					}
				}


		if (appropriate_times.size() != 0) {
			counter_group[group.course_group]+=1;
			group.working = true;
			assigned_groups.push_back(group);
			new_add_group_in_timetable(&group, &appropriate_times, students_record, students_courses, s_sol);
			cur_group = get_next_group(&groups, counter_group);
			continue;
		}
		else {
			group.working = false;
			group.id_teacher = -1;
			assigned_groups.push_back(group);
			cur_group = get_next_group(&groups, counter_group);
			continue;
		}





	}


	//assigned_groups[0].Print_info();

	int sum_st = 0;
	int sum_gr = 0;
	float obj = 0;
	


	for (auto& gr : assigned_groups) {
		if (gr.working) {
			//gr.Print_info();
			sum_st += gr.list_students.size();
			sum_gr++;
			obj += gr.score;
		}

	}

	cout << "Second_part st = " << sum_st << " gr = " << sum_gr << " objval = " << obj << endl;



}



void appoint(short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol* s_sol)
{

	for (int id = 0; id < (*s_sol).sort_groups.size(); id++){
	
		Group gr = (*s_sol).sort_groups[id];
		vector<vector<int>> appropriate_times;

		for (int t_1 = gr.first_time; t_1 < 4 + gr.first_time_end; t_1++)
			for (int t_2 = gr.second_time; t_2 < 4 + gr.second_time_end; t_2++)
				for (int i = 0; i < I; i++) {

				
					if (check_in_timetable(t_1, t_2, &gr, i, students_record, students_courses, s_sol)) {
						vector<int> v = { t_1, t_2, i };
						appropriate_times.push_back(v);


					}
				}

		//cout << appropriate_times.size() << ' ' << gr.course_group << ' ' << gr.num_group << endl;
		if (appropriate_times.size() != 0){
			//cout << "l" << gr.course_group << "k" << gr.num_group << endl;
			add_group_in_timetable(id, &appropriate_times, students_record, students_courses, s_sol);
		}

	}

	/*
	for (int i = 0; i < I; i++) {
		cout << "=================" << i << "=================" << endl;
		for (int d = 0; d < D; d++) {
			for (int t = 0; t < Real_time; t++)
				cout << (*s_sol).schedule_of_teachers[i][d][t];
			cout << endl;
		}
	}

	cout << endl;
	*/
	 
	int sum_st = 0;
	int sum_gr = 0;
	float obj = 0;
	for (Group gr : (*s_sol).sort_groups) {
		if (gr.working) {

			sum_st += gr.list_students.size();
			sum_gr++;
			obj += gr.score;
		}

	}

	



}

bool check_rooms(Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol) {


	for (int t_real = 0; t_real < timeLesssons[gr->course_group]; t_real++) {
		if ((t_1 + t_real >= Real_time) || (t_2 + t_real >= Real_time))
			return false;

		int sum_t_d_1 = 0;
		int sum_t_d_2 = 0;
		for (int i = 0; i < I; i++) {
			sum_t_d_1 += s_sol->schedule_of_teachers[i][gr->first_day][t_1 + t_real];
			sum_t_d_2 += s_sol->schedule_of_teachers[i][gr->second_day][t_2 + t_real];
		}

		if ((sum_t_d_1 >= R) || (sum_t_d_2 >= R))
			return false;

	}

	return true;
}

bool check_teacher(int i, Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol) {

	

	if (!check_limit_working_days(i, gr, students_record, students_courses, s_sol))
		return false;

	if (!check_teachers_break(i, gr, t_1, t_2, students_record, students_courses, s_sol))
		return false;

	if (!check_time_teachers(i, gr, t_1, t_2, students_record, students_courses, s_sol))
		return false;

	if (!check_limit_work_time(i, gr, t_1, t_2, students_record, students_courses, s_sol)) 
		return false;
	


	return true;

}

bool check_in_timetable(int t_1, int t_2, Group *gr, int  i, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol) {

	
		

	if (!check_rooms(gr, t_1, t_2, students_record, students_courses, s_sol)) {
		
		return false;
	}
	else {
		if (!check_teacher(i, gr, t_1, t_2, students_record, students_courses, s_sol)) {
			
			return false;
		}
		else {
			
			return true;
		}
	}



}

bool check_limit_working_days(int i, Group *gr, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol)
{
	if ((s_sol->teachers_work_days[gr->first_day][i] == 1) && (s_sol->teachers_work_days[gr->second_day][i] == 1))
		return true;

	int s = 0;
	for (int d = 0; d < D; d++)
		s += s_sol->teachers_work_days[d][i];

	if ((D - 1 == s) && ((s_sol->teachers_work_days[gr->first_day][i] == 0) || (s_sol->teachers_work_days[gr->second_day][i] == 0)))
		return false;

	if ((D - 2 == s) && ((s_sol->teachers_work_days[gr->first_day][i] == 0) && (s_sol->teachers_work_days[gr->second_day][i] == 0)))
		return false;

	return true;

}

/*

bool check_teachers_break(int i, Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol)
{

	for (int t_real = 0; t_real < timeLesssons[gr->course_group] + 1; t_real++) {

		if ((t_1 + t_real == Real_time) || (t_2 + t_real == Real_time))
			continue;

		if (t_1 + t_real == 0) {
			if (s_sol->schedule_of_teachers[i][gr->first_day][1] != 0)
				return false;
		}
		else if (t_1 + t_real == Real_time - 1) {
			if (s_sol->schedule_of_teachers[i][gr->first_day][Real_time - 2] != 0)
				return false;
		}
		else
			if ((s_sol->schedule_of_teachers[i][gr->first_day][t_1 + t_real - 1] != 0) || (s_sol->schedule_of_teachers[i][gr->first_day][t_1 + t_real + 1] != 0))
				return false;


		if (t_2 + t_real == 0) {
			if (s_sol->schedule_of_teachers[i][gr->second_day][1] != 0)
				return false;
		}
		else if (t_2 + t_real == Real_time - 1) {
			if (s_sol->schedule_of_teachers[i][gr->second_day][Real_time - 2] != 0)
				return false;
		}
		else
			if ((s_sol->schedule_of_teachers[i][gr->second_day][t_2 + t_real - 1] != 0) || (s_sol->schedule_of_teachers[i][gr->second_day][t_2 + t_real + 1] != 0))
				return false;


	}

	return true;
}

*/


bool check_teachers_break(int i, Group* gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol* s_sol)
{


	if (t_1 - 1 >= 0)
		if (s_sol->schedule_of_teachers[i][gr->first_day][t_1 - 1] == 1)
			return false;


	if (t_1 + timeLesssons[gr->course_group] < Real_time)
		if (s_sol->schedule_of_teachers[i][gr->first_day][t_1 + timeLesssons[gr->course_group]] == 1)
			return false;

	if (t_2 - 1 >= 0)
		if (s_sol->schedule_of_teachers[i][gr->second_day][t_2 - 1] == 1)
			return false;

	if (t_2 + timeLesssons[gr->course_group] < Real_time)
		if (s_sol->schedule_of_teachers[i][gr->second_day][t_2 + timeLesssons[gr->course_group]] == 1)
			return false;

	return true;
}


bool check_time_teachers(int i, Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol)
{
	for (int t_real = 0; t_real < timeLesssons[gr->course_group]; t_real++) {

		if (s_sol->schedule_of_teachers[i][gr->first_day][t_1 + t_real] != 0)
			return false;

		if (s_sol->schedule_of_teachers[i][gr->second_day][t_2 + t_real] != 0)
			return false;
	}
	return true;
}

bool check_limit_work_time(int i, Group *gr, int t_1, int t_2, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol *s_sol)
{
	//first day
	int lesson_begin_inf_first_day = t_1;
	int lesson_end_inf_first_day = t_1 + timeLesssons[gr->course_group] - 1;

	int s_1 = Real_time;
	int s_2 = 0;

	for (int t = 0; t < Real_time; t++)
		if (s_sol->schedule_of_teachers[i][gr->first_day][t] != 0) {

			s_1 = t;
			break;
		}

	for (int t = Real_time - 1; t > -1; t--)
		if (s_sol->schedule_of_teachers[i][gr->first_day][t] != 0) {

			s_2 = t;
			break;
		}

	if (s_1 > lesson_begin_inf_first_day)
		s_1 = lesson_begin_inf_first_day;
	if (s_2 < lesson_end_inf_first_day)
		s_2 = lesson_end_inf_first_day;

	int S_1 = s_2 - s_1;
	// Second day
	s_1 = Real_time;
	s_2 = 0;

	int lesson_begin_inf_second_day = t_2;
	int lesson_end_inf_second_day = t_2 + timeLesssons[gr->course_group] - 1;


	for (int t = 0; t < Real_time; t++)
		if (s_sol->schedule_of_teachers[i][gr->second_day][t] != 0) {

			s_1 = t;
			break;
		}

	for (int t = Real_time - 1; t > -1; t--)
		if (s_sol->schedule_of_teachers[i][gr->second_day][t] != 0) {

			s_2 = t;
			break;
		}

	if (s_1 > lesson_begin_inf_second_day)
		s_1 = lesson_begin_inf_second_day;
	if (s_2 < lesson_end_inf_second_day)
		s_2 = lesson_end_inf_second_day;

	int S_2 = s_2 - s_1;

	if ((S_1 >= 32) || (S_2 >= 32))
		return false;

	return true;
}


int choose_best_time_for_teachers(int course, int day, vector<int> time_first_day, int i, Second_sol *s_sol);

void new_add_group_in_timetable(Group* gr, vector<vector<int>>* appropriate_time, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol* s_sol) {

	vector<int> teacher = get_list_teacher(s_sol);


	for (int i : teacher) {

		vector<pair<int, int>> place_timetable_for_i;

		for (vector<int> t : *appropriate_time) {
			if (t[2] == i) {
				pair<int, int> a(t[0], t[1]);
				place_timetable_for_i.push_back(a);
			}
		}

		int best_time_1 = -1;
		int best_time_2 = -1;
		if (place_timetable_for_i.size() == 0)
			continue;
		else {

			int wotk_time_teacher_i = 0;
			for (int t = 0; t < Real_time; t++)
				wotk_time_teacher_i += (*s_sol).schedule_of_teachers[i][(*gr).first_day][t];

			if (wotk_time_teacher_i == 0) {

				int distance_to_mid_day = Real_time;

				for (pair<int, int> time : place_timetable_for_i) {
					if (fabs(Real_time / 2 - time.first) < distance_to_mid_day) {
						distance_to_mid_day = fabs(Real_time / 2 - time.first);
						best_time_1 = time.first;
					}
				}
			}
			else {
				vector<int> time_first_day;
				for (pair<int, int> time : place_timetable_for_i) {
					time_first_day.push_back(time.first);
				}

				best_time_1 = choose_best_time_for_teachers((*gr).course_group, (*gr).first_day, time_first_day, i, s_sol);
			}


			wotk_time_teacher_i = 0;
			for (int t = 0; t < Real_time; t++)
				wotk_time_teacher_i += (*s_sol).schedule_of_teachers[i][(*gr).second_day][t];

			if (wotk_time_teacher_i == 0) {

				int distance_to_mid_day = Real_time;

				for (pair<int, int> time : place_timetable_for_i) {
					if (fabs(Real_time / 2 - time.second) < distance_to_mid_day) {
						distance_to_mid_day = fabs(Real_time / 2 - time.second);
						best_time_2 = time.second;
					}
				}
			}
			else {
				vector<int> time_second_day;
				for (pair<int, int> time : place_timetable_for_i) {
					time_second_day.push_back(time.second);
				}

				best_time_2 = choose_best_time_for_teachers((*gr).course_group, (*gr).second_day, time_second_day, i, s_sol);
			}


		}

		new_marker_days(i, gr, best_time_1, best_time_2, s_sol);
		break;

	}
}


void add_group_in_timetable(int id_gr, vector<vector<int>> *appropriate_time, short(&students_record)[J][D][T], short(&students_courses)[J][L], Second_sol* s_sol) {

	vector<int> teacher = get_list_teacher(s_sol);

	Group gr = (*s_sol).sort_groups[id_gr];

	for (int i : teacher) {

		vector<pair<int, int>> place_timetable_for_i;

		for (vector<int> t : *appropriate_time) {
			if (t[2] == i) {
				pair<int, int> a(t[0], t[1]);
				place_timetable_for_i.push_back(a);
			}
		}

		int best_time_1 = -1;
		int best_time_2 = -1;
		if (place_timetable_for_i.size() == 0)
			continue;
		else {

			int wotk_time_teacher_i = 0;
			for (int t = 0; t < Real_time; t++)
				wotk_time_teacher_i += (*s_sol).schedule_of_teachers[i][gr.first_day][t];

			if (wotk_time_teacher_i == 0) {

				int distance_to_mid_day = Real_time;

				for (pair<int, int> time : place_timetable_for_i) {
					if (fabs(Real_time / 2 - time.first) < distance_to_mid_day) {
						distance_to_mid_day = fabs(Real_time / 2 - time.first);
						best_time_1 = time.first;
					}
				}
			}
			else {
				vector<int> time_first_day;
				for (pair<int, int> time : place_timetable_for_i) {
					time_first_day.push_back(time.first);
				}

				best_time_1 = choose_best_time_for_teachers(gr.course_group, gr.first_day, time_first_day, i, s_sol);
			}


			wotk_time_teacher_i = 0;
			for (int t = 0; t < Real_time; t++)
				wotk_time_teacher_i += (*s_sol).schedule_of_teachers[i][gr.second_day][t];

			if (wotk_time_teacher_i == 0) {

				int distance_to_mid_day = Real_time;

				for (pair<int, int> time : place_timetable_for_i) {
					if (fabs(Real_time / 2 - time.second) < distance_to_mid_day) {
						distance_to_mid_day = fabs(Real_time / 2 - time.second);
						best_time_2 = time.second;
					}
				}
			}
			else {
				vector<int> time_second_day;
				for (pair<int, int> time : place_timetable_for_i) {
					time_second_day.push_back(time.second);
				}

				best_time_2 = choose_best_time_for_teachers(gr.course_group, gr.second_day, time_second_day, i, s_sol);
			}


		}

		marker_days(i, id_gr, best_time_1, best_time_2, s_sol);
		break;

	}
}


int choose_best_time_for_teachers(int course, int day, vector<int> times_day, int i, Second_sol *s_sol) {

	int best_time = -1;
	int distance = Real_time;
	for (int t : times_day) {
		int dis_metr_up = 0;
		for (int pointer_up = t + timeLesssons[course] + 2; pointer_up < Real_time; pointer_up++) {
			if (s_sol->schedule_of_teachers[i][day][pointer_up] != 0) {
				dis_metr_up = pointer_up - (t + timeLesssons[course] + 2);
				continue;
			}
		}

		int dis_metr_down = 0;
		for (int pointer_down = t; pointer_down > 0; pointer_down--) {
			if (s_sol->schedule_of_teachers[i][day][pointer_down] != 0) {
				dis_metr_down = t - pointer_down;
				continue;
			}
		}


		if (dis_metr_up <= dis_metr_down) {

			if (dis_metr_up < distance) {
				distance = dis_metr_up;
				best_time = t;
			}
		}
		else {
			if (dis_metr_down < distance) {
				distance = dis_metr_down;
				best_time = t;
			}
		}

	}

	return best_time;
}

void new_marker_days(int i, Group* gr, int t_1, int t_2, Second_sol* s_sol)
{



	for (int t_real = 0; t_real < timeLesssons[(*gr).course_group]; t_real++) {
		(*s_sol).schedule_of_teachers[i][(*gr).first_day][t_1 + t_real] = 1;
		(*s_sol).schedule_of_teachers[i][(*gr).second_day][t_2 + t_real] = 1;
	}


	(*s_sol).teachers_work_days[(*gr).first_day][i] = 1;
	(*s_sol).teachers_work_days[(*gr).second_day][i] = 1;

	gr->working = true;
	gr->id_teacher = i;

	/*
	(*s_sol).sort_groups[id_gr].first_time = t_1;
	(*s_sol).sort_groups[id_gr].first_time_end = t_1 + timeLesssons[(*gr).course_group] - 1;
	(*s_sol).sort_groups[id_gr].second_time = t_2;
	(*s_sol).sort_groups[id_gr].second_time_end = t_2 + timeLesssons[(*gr).course_group] - 1;

	(*s_sol).sort_groups[id_gr].id_teacher = i;
	(*s_sol).sort_groups[id_gr].working = true;
	*/

}


void marker_days(int i, int id_gr, int t_1, int t_2, Second_sol* s_sol)
{
	Group gr = (*s_sol).sort_groups[id_gr];



	for (int t_real = 0; t_real < timeLesssons[gr.course_group]; t_real++) {
		(*s_sol).schedule_of_teachers[i][gr.first_day][t_1 + t_real] = 1;
		(*s_sol).schedule_of_teachers[i][gr.second_day][t_2 + t_real] = 1;
	}


	(*s_sol).teachers_work_days[gr.first_day][i] = 1;
	(*s_sol).teachers_work_days[gr.second_day][i] = 1;


	(*s_sol).sort_groups[id_gr].first_time = t_1;
	(*s_sol).sort_groups[id_gr].first_time_end = t_1 + timeLesssons[gr.course_group] - 1;
	(*s_sol).sort_groups[id_gr].second_time = t_2;
	(*s_sol).sort_groups[id_gr].second_time_end = t_2 + timeLesssons[gr.course_group] - 1;

	(*s_sol).sort_groups[id_gr].id_teacher = i;
	(*s_sol).sort_groups[id_gr].working = true;

}

bool comp_sort(pair <int, int>  a, pair <int, int>  b) {
	return a.second > b.second;
}

vector<int> get_list_teacher(Second_sol *s_sol)
{
	vector<pair<int, int>> A;
	for (int i = 0; i < I; i++) {

		int sum_work_time = 0;
		for (int d = 0; d < D; d++)
			for (int t = 0; t < Real_time; t++)
				sum_work_time += (*s_sol).schedule_of_teachers[i][d][t];


		pair<int, int> a(i, sum_work_time);
		A.push_back(a);
	}


	sort(A.begin(), A.end(), comp_sort);

	vector<int> B;
	for (int i = 0; i < I; i++)
		B.push_back(A[i].first);

	return B;
}






