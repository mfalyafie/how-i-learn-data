drop table if exists TrxAccounts;
CREATE TABLE TrxAccounts(
    id int not null ,
    name varchar(100) not null ,
    balance dec not null ,
    primary key(id)
);

insert into TrxAccounts(id, name, balance)
values(1, 'Azwar', 1000000);
insert into TrxAccounts(id, name, balance)
values(2, 'Yafie', 1000000);

select * from TrxAccounts;

create or replace procedure TrxTransfer(
    pengirim int,
    penerima int,
    jumlah dec
)
language plpgsql
as $$

-- call
begin
    --- pengurangan saldo rekening pengirim
    update TrxAccounts
    set balance = balance - jumlah
    where id= pengirim;
   
    -- penambahan saldo rekening penerima
    update TrxAccounts
    set balance = balance + jumlah
    where id= penerima;
   
    commit;
end;$$;

call trxtransfer(1, 2, 100000);

drop table if exists TrxProduct;
CREATE TABLE TrxProduct(
    id int not null ,
    company_name varchar(100) not null ,
    trx_type int not null ,
    primary key(id)
);

insert into TrxProduct(id, company_name, trx_type)
values(1, 'Nokia', 0);
insert into TrxProduct(id, company_name, trx_type)
values(2, 'Marugame', 1);

select * from TrxProduct;

create or replace function trx_rec_insert()
returns trigger as
$$
begin
    insert into TrxProductLog(id, company_name, trx_type)
    values(NEW.id, NEW.company_name, NEW.trx_type);
    
    return new;
    end;
$$
language 'plpqsql';

--------------------------------------------------

--- employee table
drop table if exists employee;
CREATE TABLE employee(
    emp_id serial not null ,
    first_name varchar(255) not null ,
    last_name varchar(255) not null ,
    gender char(1) not null ,
    hire_date timestamp not null ,
    primary key(emp_id)
);

--- inserting list of employees
insert into employee(first_name, last_name, gender, hire_date)
values
    ('Thalla', 'Hirasazari', 'M', '2021-01-01') ,
    ('Yafie', 'Fauzan', 'M', '2021-01-01') ,
    ('Valli', 'Sinatrya', 'M', '2021-01-01') ,
    ('Rizha', 'Teuku', 'M', '2021-01-01') ,
    ('Glen', 'Yusuf', 'M', '2021-02-01') ,
    ('Bharoar', 'Baran', 'M', '2021-02-01') ,
    ('Indra', 'Coco', 'M', '2021-02-01') ,
    ('Sahat', 'Doang', 'M', '2021-02-01') ,
    ('Sabila', 'Rodhia', 'F', '2021-02-01') ,
    ('Kaisar', 'Rennaisance', 'M', '2021-02-01')
;

select * from employee;

--- department table
drop table if exists department;
CREATE TABLE department(
    dept_id serial not null ,
    dept_name varchar(255) not null ,
    primary key(dept_id)
);

--- inserting list of department
insert into department(dept_name)
values
    ('C-Suite') ,
    ('Data') ,
    ('Commercial') ,
    ('Product')
;

select * from department;

--- title table
drop table if exists title;
CREATE TABLE title(
    title_id serial not null ,
    title varchar(255) not null ,
    job_level int not null ,
    dept_id int not null ,
    primary key(title_id) ,
    foreign key (dept_id)
        references department (dept_id)
);

--- inserting list of titles
insert into title(title, job_level, dept_id)
values
    ('CEO', 3, 1) ,
    ('Head of Data', 2, 2) ,
    ('Data Team', 1, 2) ,
    ('Head of Commercial', 2, 3) ,
    ('Commercial Team', 1, 3) ,
    ('Head of Product', 2, 4) ,
    ('Product Team', 1, 4)
;

select * from title;

--- salary table
drop table if exists salary;
CREATE TABLE salary(
    salary_id serial not null ,
    emp_id int not null ,
    salary dec not null ,
    from_date timestamp not null ,
    to_date timestamp not null ,
    primary key(salary_id) ,
    foreign key (emp_id)
        references employee (emp_id)
);

--- inserting list of salaries
insert into salary(emp_id, salary, from_date, to_date)
values
    (1, 20000000, '2021-05-01', '9999-01-01') ,
    (1, 15000000, '2021-01-01', '2021-05-01') ,
    (2, 15000000, '2021-01-01', '9999-01-01') ,
    (3, 15000000, '2021-01-01', '9999-01-01') ,
    (4, 15000000, '2021-01-01', '9999-01-01') ,
    (5, 10000000, '2021-02-01', '9999-01-01') ,
    (6, 10000000, '2021-02-01', '9999-01-01') ,
    (7, 7500000, '2021-02-01', '9999-01-01') ,
    (8, 7500000, '2021-02-01', '9999-01-01') ,
    (9, 8500000, '2021-02-01', '9999-01-01') ,
    (10, 8500000, '2021-02-01', '9999-01-01')
;

select * from salary;

--- training table
drop table if exists training;
CREATE TABLE training(
    training_id serial not null ,
    training_type varchar(255) not null ,
    training_name varchar(255) not null ,
    mandatory boolean not null ,
    training_level varchar(255) not null ,
    institution varchar(255) not null ,
    primary key(training_id)
);

--- inserting list of trainings
insert into training(training_type, training_name, mandatory, training_level, institution)
values
    ('Onboarding', 'Learning Organization', true, 'Beginner', 'UMG Idea Lab') ,
    ('Management Training', 'How to be a Good Leader', true, 'Advanced', 'Venidici')
;

select * from training;

--- dept_employee table
drop table if exists dept_employee;
CREATE TABLE dept_employee(
    dept_employee_id serial not null ,
    emp_id int not null ,
    dept_id int not null ,
    from_date timestamp not null ,
    to_date timestamp not null ,
    primary key(dept_employee_id) ,
    foreign key (emp_id)
        references employee (emp_id) ,
    foreign key (dept_id)
        references department (dept_id)
);

--- inserting list of employees' department assignment
insert into dept_employee(emp_id, dept_id, from_date, to_date)
values
    (1, 1, '2021-01-01', '9999-01-01') ,
    (2, 2, '2021-01-01', '9999-01-01') ,
    (3, 3, '2021-01-01', '9999-01-01') ,
    (4, 4, '2021-01-01', '9999-01-01') ,
    (5, 2, '2021-02-01', '9999-01-01') ,
    (6, 2, '2021-02-01', '9999-01-01') ,
    (7, 3, '2021-02-01', '9999-01-01') ,
    (8, 3, '2021-02-01', '9999-01-01') ,
    (9, 4, '2021-02-01', '9999-01-01') ,
    (10, 4, '2021-02-01', '9999-01-01')
;

select 
    e.first_name ,  
    d.dept_name
from dept_employee de
inner join
    employee e
        on
    e.emp_id = de.emp_id
inner join
    department d
        on
    d.dept_id = de.dept_id
;

--- dept_head table
drop table if exists dept_head;
CREATE TABLE dept_head(
    dept_head_id serial not null ,
    emp_id int not null ,
    dept_id int not null ,
    from_date timestamp not null ,
    to_date timestamp not null ,
    primary key(dept_head_id) ,
    foreign key (emp_id)
        references employee (emp_id) ,
    foreign key (dept_id)
        references department (dept_id)
);

--- inserting list of heads for each department
insert into dept_head(emp_id, dept_id, from_date, to_date)
values
    (1, 1, '2021-01-01', '9999-01-01') ,
    (2, 2, '2021-01-01', '9999-01-01') ,
    (3, 3, '2021-01-01', '9999-01-01') ,
    (4, 4, '2021-01-01', '9999-01-01')
;

select * from dept_head;

--- emp_supervision table
drop table if exists emp_supervision;
CREATE TABLE emp_supervision(
    emp_supervision_id serial not null ,
    emp_id int not null ,
    manager_id int not null ,
    from_date timestamp not null ,
    to_date timestamp not null ,
    primary key(emp_supervision_id) ,
    foreign key (emp_id)
        references employee (emp_id) ,
    foreign key (manager_id)
        references employee (emp_id)
);

--- inserting list of direct supervision for each employee
insert into emp_supervision(emp_id, manager_id, from_date, to_date)
values
    (2, 1, '2021-01-01', '9999-01-01') ,
    (3, 1, '2021-01-01', '9999-01-01') ,
    (4, 1, '2021-01-01', '9999-01-01') ,
    (5, 2, '2021-02-01', '9999-01-01') ,
    (6, 2, '2021-02-01', '9999-01-01') ,
    (7, 3, '2021-02-01', '9999-01-01') ,
    (8, 3, '2021-02-01', '9999-01-01') ,
    (9, 4, '2021-02-01', '9999-01-01') ,
    (10, 4, '2021-02-01', '9999-01-01')
;

select * 
from emp_supervision es
inner join employee e1
on es.emp_id = e1.emp_id
inner join employee e2
on es.manager_id = e2.emp_id
;

--- emp_title table
drop table if exists emp_title;
CREATE TABLE emp_title(
    emp_title_id serial not null ,
    emp_id int not null ,
    title_id int not null ,
    from_date timestamp not null ,
    to_date timestamp not null ,
    primary key(emp_title_id) ,
    foreign key (emp_id)
        references employee (emp_id) ,
    foreign key (title_id)
        references title (title_id)
);

--- inserting list of titles for each employee
insert into emp_title(emp_id, title_id, from_date, to_date)
values
    (1, 1, '2021-01-01', '9999-01-01') ,
    (2, 2, '2021-01-01', '9999-01-01') ,
    (3, 4, '2021-01-01', '9999-01-01') ,
    (4, 6, '2021-01-01', '9999-01-01') ,
    (5, 3, '2021-02-01', '9999-01-01') ,
    (6, 3, '2021-02-01', '9999-01-01') ,
    (7, 5, '2021-02-01', '9999-01-01') ,
    (8, 5, '2021-02-01', '9999-01-01') ,
    (9, 7, '2021-02-01', '9999-01-01') ,
    (10, 7, '2021-02-01', '9999-01-01')
;

select *
from emp_title et
inner join employee e
on et.emp_id = e.emp_id
inner join title t
on et.title_id = t.title_id
;

--- emp_training table
drop table if exists emp_training;
CREATE TABLE emp_training(
    emp_training_id serial not null ,
    emp_id int not null ,
    training_id int not null ,
    effective_date timestamp not null ,
    primary key(emp_training_id) ,
    foreign key (emp_id)
        references employee (emp_id) ,
    foreign key (training_id)
        references training (training_id)
);

--- inserting list of trainings for each employee
insert into emp_training(emp_id, training_id, effective_date)
values
    (2, 1, '2021-01-01') ,
    (2, 2, '2021-02-01') ,
    (3, 1, '2021-01-01') ,
    (3, 2, '2021-02-01') ,
    (4, 1, '2021-01-01') ,
    (4, 2, '2021-02-01') ,
    (5, 1, '2021-02-01') ,
    (6, 1, '2021-02-01') ,
    (7, 1, '2021-02-01') ,
    (8, 1, '2021-02-01') ,
    (9, 1, '2021-02-01') ,
    (10, 1, '2021-02-01')
;

--- create function to find average salary per job level
create or replace function get_avg_salary_job_level (
    jl_joblevel int
)
        returns table (
            job_level int ,
            avg_salary dec ,
            st_dev dec
        )
        language plpgsql
as $$
begin
        return query
                select
                        t.job_level ,
                        avg(s2.max_salary) ,
                        stddev_pop(s2.max_salary)
                from
                        (select 
                            s.emp_id, 
                            max(salary) as max_salary
                         from
                            salary s
                         group by s.emp_id) s2
                inner join
                        employee e
                            on
                        s2.emp_id = e.emp_id
                inner join
                        emp_title et
                            on
                        et.emp_id = e.emp_id
                inner join
                        title t
                            on
                        et.title_id = t.title_id
                where
                    t.job_level = jl_joblevel
                group by
                        t.job_level;
end;$$

select * from get_avg_salary_job_level(1);