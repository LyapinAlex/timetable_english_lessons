#include"base_group.hpp"
#include<list>
#include <algorithm>
#include "base_schedule.hpp"


void create_array_rec(int l, int(&array_recod)[T][T][num_days], short(&students_record)[J][D][T], short(&students_courses)[J][L]) {

	for (int t_1 = 0; t_1 < T; t_1++)
		for (int t_2 = 0; t_2 < T; t_2++)
			for (int i = 0; i < num_days; i++)
				array_recod[t_1][t_2][i] = 0;


	for (int j = 0; j < J; j++)
		if (students_courses[j][l] == 1)
			for (int t_1 = 0; t_1 < T; t_1++)
				for (int t_2 = 0; t_2 < T; t_2++)
					for (int i = 0; i < num_days; i++)
						if ((students_record[j][couple_of_days[i][0]][t_1] == 1) && (students_record[j][couple_of_days[i][1]][t_2] == 1))
							array_recod[t_1][t_2][i]++;


	//cout << array_recod[3][7][4] << ' ' << array_recod[1][2][9] << ' ' << array_recod[6][6][4] << ' ';
	//cout << array_recod[1][5][6] << ' ' << array_recod[3][3][9] << ' ' << array_recod[10][8][5] << ' ';
}


void refresh_array(int(&array_recod)[T][T][num_days], short(&students_record)[J][D][T], int j) {

	for (int i = 0; i < num_days; i++) {

		int d_1 = couple_of_days[i][0];
		int d_2 = couple_of_days[i][1];

		for (int t_1 = 0; t_1 < T; t_1++)
			for (int t_2 = 0; t_2 < T; t_2++)
				if ((students_record[j][d_1][t_1] == 1) && (students_record[j][d_2][t_2] == 1)) {
					array_recod[t_1][t_2][i]--;
				}
	}

}


void create_group(int(&array_recod)[T][T][num_days], int i, int t_1, int t_2, int l, int cor, short(&students_record)[J][D][T], short(&students_courses)[J][L], First_sol* sol) {
	
	int k = (*sol).groups[l].size() + 1;

	int d_1 = couple_of_days[i][0];
	int d_2 = couple_of_days[i][1];
	(*sol).rooms[d_1][t_1]++;
	(*sol).rooms[d_2][t_2]++;
	
	//cout << "l " << l << " k " << k << " d_1 " << d_1 << " d_2 " << d_2 << " t_1 " << t_1 << " t_2 " << t_2 << endl;
	 
	vector<int> vec_st;
	while (vec_st.size() < cor) {
		for (int j = 0; j < J; j++) {
			if (vec_st.size() == max_num)
				break;
			if ((*sol).students[j] != 0)
				continue;
			if (students_courses[j][l] == 1){

				if ((students_record[j][d_1][t_1] == 1) && (students_record[j][d_2][t_2] == 1)) {
					(*sol).students[j] = k;
					vec_st.push_back(j);

					

				}
					
			}
		}
	}

	Group g(vec_st, k, l, d_1, d_2, t_1, t_2);
	
	//g.Print_info();
	(*sol).groups[l].push_back(g);

	//cout << array_recod[t_1][t_2][i] << endl;
	for (int j : vec_st)
		refresh_array(array_recod, students_record, j);


}


bool comp_sec( pair <int, int>  a, pair <int, int>  b) {
	return a.second < b.second;
}


void sort_by_num_in_course(int(&B)[L], short(&students_courses)[J][L]) {

	vector<pair<int, int>> A;
	for (int l = 0; l < L; l++) {
		pair<int, int> a(l, 0);
		A.push_back(a);
	}


	for (int j = 0; j < J; j++)
		for (int l = 0; l < L; l++)
			if (students_courses[j][l] == 1)
				A[l].second++;


	sort(A.begin(), A.end(), comp_sec );

	
	for (int l = 0; l < L; l++) 
		B[l] = A[l].first;


}


void pr_sol(First_sol sol) {

	int sm_J = 0;
	for (int j = 0; j < J; j++)
		if (sol.students[j] != 0)
			sm_J++;
	
	int sm_G = 0;
	for (int l = 0; l < L; l++)
		sm_G += sol.groups[l].size();

	
	cout <<"First_path st = " << sm_J << " gr = " << sm_G << endl;
}


First_sol create_groups(short(&students_record)[J][D][T], short(&students_courses)[J][L])
{
	First_sol sol;

	int B[L];
	sort_by_num_in_course(B, students_courses);


	
	for (int l : B){
		
		int array_recod[T][T][num_days];
		create_array_rec(l, array_recod, students_record, students_courses);
		int cor = max_num;
		while (cor >= min_num) {

			bool ind = false;
			
			for (int t_1 = 0; t_1 < T; t_1++) 
				for (int t_2 = 0; t_2 < T; t_2++ )
					for (int i = 0; i < num_days; i++) {
						int d_1 = couple_of_days[i][0];
						int d_2 = couple_of_days[i][1];
						if ((sol.rooms[d_1][t_1] < R) && (sol.rooms[d_2][t_2] < R))
							if (array_recod[t_1][t_2][i] >= cor) {
								create_group(array_recod, i, t_1, t_2, l, cor, students_record, students_courses, &sol);
								ind = true;
							
							}


							
						
					}

			if(ind == false)
				cor--;
		}

	}
	
	pr_sol(sol);
	return sol;

}





int* Func(int* Array)
{
	for (int i = 0; i < 3; i++) {
		Array[i]++;
	}
	return Array;
}


