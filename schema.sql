drop table if exists sensor;
create table sensor(
	test_id int primary key autoincrement,
	temperature int,
	humidity int);

