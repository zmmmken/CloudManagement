
# database project
# arman sabbagh 9722762053
# mahdi kenevisi 9622762317
# amirhosein ebrahimi 9612762456

import psycopg2
import datetime
import uuid
import hashlib

"""
tables:

users
admin
os
platform
cloud
ticket
    0 status: waiting
    1 status: answered
    2 status: rejected
snapshots
"""


class Database:
    connection = None

    def __init__(self):
        self.open_connection()


    def open_connection(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host="localhost",
                database="university_project",
                user="postgres",
                password="mahdi123",
                port=5432  # optional
            )
            return self.connection
        else:
            print(type(self.connection))
            return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def user_create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users('
                       'first_name character(30),'
                       'last_name character(30),'
                       'passport_id integer PRIMARY KEY,'
                       'email character(30),'
                       'password character(60) NOT NULL,'
                       'join_date character(30),'
                       'account_balance integer'
                       # 'CONSTRAINT user_id PRIMARY KEY (passport_id)'
                       ');')
        self.connection.commit()
        cursor.close()

    def user_drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table users;')
        self.connection.commit()
        cursor.close()

    def user_insert_table(self, first_name: str, last_name: str, passport_id: int, email: str, password: str, account_balance: int) -> bool:
        join_date = str(datetime.datetime.today()).split(" ")[0]
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                        insert into users
                        (first_name, last_name, passport_id, email, password, join_date, account_balance)
                        values (%s, %s, %s, %s, %s, %s, %s);
                    """, (first_name, last_name, passport_id, email, password, join_date, account_balance)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def update_user(self, first_name: str, last_name: str, passport_id: int, email: str, password: str, account_balance: int, is_admin: bool) -> bool:
        join_date = str(datetime.datetime.today()).split(" ")[0]
        cursor = self.connection.cursor()
        try:
            if not is_admin:
                cursor.execute("""
                        update users set
                        first_name=%s, last_name=%s, email=%s, password=%s,account_balance=%s
                        where  users.passport_id = %s;
                    """, (first_name, last_name, email, password, account_balance, passport_id)
                           )
            else:
                cursor.execute("""
                                                    update admin set
                                                    first_name=%s, last_name=%s, email=%s, password=%s
                                                    where  admin.passport_id = %s;
                                                """,
                               (first_name, last_name, email, password, passport_id))
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def user_delete(self, passport_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                delete from users where users.passport_id = %s RETURNING users.passport_id;
                """, (passport_id,))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True

    def check_user(self, passport_id: str) -> list:
        passport_id = int(passport_id)
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select * from users where (users.passport_id = %s);
                """, [passport_id])
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        # if len(record) == 0:
        #     return False
        return record

    def get_all_user(self):
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select * from users;
                """,)
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        return record

    # def create_platform(self):
    #     self.platform_insert_table()


    def admin_create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                        create table if not exists admin(
                        admin_id serial PRIMARY KEY,
                        first_name character(30),
                        last_name character(30),
                        passport_id integer,
                        email character(30),
                        password character(60) NOT NULL
                        );
                        """)
        self.connection.commit()
        cursor.close()

    def admin_drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table admin;')
        self.connection.commit()
        cursor.close()

    def admin_insert_table(self, first_name: str, last_name: str, passport_id: int, email: str, password: str) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                                insert into admin
                                (first_name, last_name, passport_id, email, password)
                                values (%s, %s, %s, %s, %s);
                            """, (first_name, last_name, passport_id, email, password)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def admin_get_table(self, passport_id: int,) -> list:
        passport_id = int(passport_id)
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select * from admin where (admin.passport_id = %s);
                """, [passport_id])
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        # if len(record) == 0:
        #     return False
        return record

    # alert os where os.admin = %s ;
    # delete from os where admin_id in (SELECT admin_id FROM admin);
    def admin_delete(self, admin_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                delete from admin where admin.admin_id = %s RETURNING admin.admin_id;
                """, (admin_id,))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True

    def os_create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                                create table if not exists os(
                                os_id serial PRIMARY KEY,
                                os_name character(30) unique,
                                );
                                """)
        self.connection.commit()
        cursor.close()

    def os_drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table os;')
        self.connection.commit()
        cursor.close()

    def os_insert_table(self, os_name: str) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                                insert into os (os_name)
                                values (%s);
                            """, (os_name,)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def os_delete(self, os_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                delete from os where os.os_id = %s RETURNING os.os_id;
                """, (os_id,))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True

    def create_table_dependency(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                                 create table if not exists platform_os(
                                 os_id int REFERENCES  os(os_id),
                                 platform_id int REFERENCES  platform(platform_pk)
                                 );
                                 """)
        self.connection.commit()
        cursor.close()

    def dependency_insert_table(self, os_id: int, platform_pk: int) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                                insert into platform_os (os_id,platform_id)
                                values (%s,%s);
                            """, (os_id,platform_pk)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def dependency_delete_table(self, os_id: int, platform_pk: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                delete from platform_os where os_id = %s and platform_id=%s RETURNING platform_os.os_id;
                """, (os_id, platform_pk))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True

    def get_os(self):
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select * from os;
                """, )
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        return record

    def platform_create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                            create table if not exists platform(
                            platform_pk serial PRIMARY KEY,
                            storage_size integer,
                            ram integer,
                            cpu_core integer,
                            cpu_rate integer,
                            bandwidth integer
                            );
                        """)
        self.connection.commit()
        cursor.close()

    def platform_drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table platform;')
        self.connection.commit()
        cursor.close()

    def platform_insert_table(self, storage_size: int, ram: int, cpu_core: int, cpu_rate: int, bandwidth: int) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                                insert into platform
                                (storage_size, ram, cpu_core, cpu_rate, bandwidth)
                                values (%s, %s, %s, %s, %s);
                            """, (storage_size, ram, cpu_core, cpu_rate, bandwidth)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def platform_delete(self, platform_pk: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                        delete from platform where platform.platform_pk = %s RETURNING platform.platform_pk;
                        """, (platform_pk,))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True

    def update_platform(self, ram, core, rate, storage, bandwidth, platform_pk):
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        try:
            cursor.execute("""
                        update platform set
                        ram=%s, cpu_core=%s, cpu_rate=%s, bandwidth=%s,storage_size=%s
                        where  platform.platform_pk = %s;
                    """, (ram, core, rate, bandwidth, storage, platform_pk)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def select_platform(self):
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select * from platform order by platform.platform_pk;
                """,)
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        # if len(record) == 0:
        #     return False
        return record



    def cloud_create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                    create table if not exists cloud(
                    cloud_id serial PRIMARY KEY,
                    daily_price integer,
                    storage_size integer,
                    ram integer,
                    cpu_core integer,
                    cpu_rate integer,
                    bandwidth integer,
                    create_date character(30),
                    ssh_hash character(150),
                    ssh_salt character(38),
                    os_id int references os(os_id) on delete cascade,
                    passport_id int references users(passport_id) on delete cascade,
                    platform_pk int references platform(platform_pk) on delete cascade
                    );
                """)
        self.connection.commit()
        cursor.close()

    def cloud_drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table cloud;')
        self.connection.commit()
        cursor.close()

    def cloud_insert_table(self, cloud_password: str, platform_pk: int, storage_size: int, ram: int, cpu_core: int, cpu_rate: int, bandwidth: int, os_id: int, passport_id: int) -> bool:
        cursor = self.connection.cursor()
        daily_price = (cpu_core * cpu_rate * 5000) + (ram * 4000) + (storage_size * 2000) + (bandwidth * 1000)
        ssh_salt = uuid.uuid4().hex
        ssh_hash = hashlib.sha256(ssh_salt.encode() + cloud_password.encode()).hexdigest()
        try:
            cursor.execute("""
                            do $$
                            begin
                                if not exists (select 1 from pg_type where typname = 'platform_data_type') then 
                                    create type platform_data_type as (
                                        platform_storage_size integer,
                                        platform_ram integer,
                                        platform_cpu_core integer,
                                        platform_cpu_rate integer,
                                        platform_bandwidth integer
                                    );
                                end if;
                            end; 
                            $$;

                            CREATE OR REPLACE FUNCTION get_platform_data(input_platform_pk integer)
                                RETURNS platform_data_type AS $$

                            declare result_data platform_data_type;
                            begin
                                select storage_size, ram, cpu_core, cpu_rate, bandwidth
                                into result_data.platform_storage_size,
                                    result_data.platform_ram,
                                    result_data.platform_cpu_core,
                                    result_data.platform_cpu_rate,
                                    result_data.platform_bandwidth
                                from platform
                                where platform_pk = input_platform_pk;
                                return result_data;
                            end;
                            $$ language plpgsql;

                            CREATE OR REPLACE FUNCTION check_platform_data_to_cloud(
                                platform_pk integer, 
                                storage_size integer,
                                ram integer,
                                cpu_core integer,
                                cpu_rate integer,
                                bandwidth integer
                            )
                              RETURNS bool AS $$
                            declare platform_data platform_data_type;
                            declare answer bool;
                            begin
                                platform_data = get_platform_data(platform_pk);
                                if platform_data.platform_storage_size >= storage_size
                                    and platform_data.platform_ram >= ram
                                    and platform_data.platform_cpu_core >= cpu_core
                                    and platform_data.platform_cpu_rate >= cpu_rate
                                    and platform_data.platform_bandwidth >= bandwidth
                                    then answer = TRUE;
                                else answer = FALSE;
                                end if;
                            return answer;
                            END;
                            $$ LANGUAGE PLPGSQL;

                            do $$
                            begin
                                if check_platform_data_to_cloud(%s, %s, %s, %s, %s, %s) then 
                                    insert into cloud
                                    (platform_pk, storage_size, ram, cpu_core, cpu_rate,
                                     bandwidth, os_id, passport_id, daily_price, ssh_hash, ssh_salt)
                                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                else RAISE EXCEPTION 'error'; 
                                end if;
                            end;$$;
                            """, ([platform_pk, storage_size, ram, cpu_core, cpu_rate,
                                  bandwidth, platform_pk, storage_size, ram, cpu_core, cpu_rate,
                                  bandwidth, os_id, passport_id, daily_price, ssh_hash, ssh_salt])
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def check_password(self, input_password: str, cloud_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("""
                            select ssh_hash, ssh_salt from cloud where cloud.cloud_id = %s;
                        """, (cloud_id,)
                       )
        ssh_hash, ssh_salt = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        hash_input_password = hashlib.sha256(ssh_salt.encode() + input_password.encode()).hexdigest()
        if hash_input_password == ssh_hash:
            return True
        return False

    def cloud_delete(self, cloud_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                        delete from cloud where cloud.cloud_id = %s RETURNING cloud.cloud_id;
                        """, (cloud_id,))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True

    def select_cloud(self, passport):
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select * from cloud where cloud.passport_id = %s;
                """, [passport])
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()

        return record

    def all_platform_os(self,):
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                 select os.os_id,os.os_name,platform.platform_pk,storage_size,ram,cpu_core,cpu_rate,bandwidth from os, platform, platform_os where (os.os_id=platform_os.os_id and platform.platform_pk = platform_os.platform_id);
                  
                """, )
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        return record


    # todo
    def selected_platform_os(self, platform_id) -> list:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select os_name,os.os_id from os,platform_os,platform where platform.platform_pk=%s and platform.platform_pk=platform_os.platform_id and os.os_id=platform_os.os_id
                """,[platform_id])
        self.connection.commit()
        record = list
        record = cursor.fetchall()
        cursor.close()
        return record

    def unselected_platform_os(self, platform_id) -> list:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                select os_name,os_id from os EXCEPT
                select os_name,os.os_id from os,platform_os,platform where platform.platform_pk=%s and platform.platform_pk=platform_os.platform_id and os.os_id=platform_os.os_id

        """, [platform_id])
        self.connection.commit()
        record = list
        record = cursor.fetchall()
        cursor.close()
        return record

    def ticket_create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                    create table if not exists ticket(
                    ticket_id serial PRIMARY KEY,
                    passport_id int references users(passport_id) on delete cascade,
                    create_time character(30),
                    response text,
                    question text,
                    status smallint
                    );
                """)
        self.connection.commit()
        cursor.close()

    def ticket_drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table ticket;')
        self.connection.commit()
        cursor.close()

    def ticket_insert_table(self, passport_id: int, question: str) -> bool:
        cursor = self.connection.cursor()
        create_time = str(datetime.datetime.now()).split(".")[0]
        status = 0
        try:
            cursor.execute("""
                                insert into ticket
                                (passport_id, create_time, status,question)
                                values (%s, %s, %s, %s);
                            """, (passport_id, create_time, status,question)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def ticket_get_table(self, passport_id: int, is_admin: bool) -> list:
        cursor = self.connection.cursor()
        create_time = str(datetime.datetime.now()).split(".")[0]
        record =[]
        try:
            if not is_admin:
                cursor.execute("""
                                                select * from ticket where passport_id=%s;
                                            """, [passport_id])
            else:
                cursor.execute("""
                                                select * from ticket;
                                            """,)

            self.connection.commit()
            record = cursor.fetchall()
            cursor.close()
            return record
        except:
            cursor.close()
            return record

    def ticket_delete(self, ticket_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                        delete from ticket where ticket.ticket_id = %s RETURNING ticket.ticket_id;
                        """, (ticket_id,))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True

    def update_ticket(self, ticket_id: str, passport_id: int, response: str, question: str, status: int) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                        update ticket set
                        ticket_id=%s, passport_id=%s,response=%s,question=%s,status=%s
                        where  ticket.ticket_id = %s;
                    """, (ticket_id, passport_id, response, question, status, ticket_id)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    # todo
    def snapshots_create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                    create table if not exists snapshots(
                    snapshots_id serial PRIMARY KEY,
                    cloud_id int references cloud(cloud_id) on delete cascade,
                    create_time character(30),
                    sizee int,
                    );
                """)
        self.connection.commit()
        cursor.close()

    def snapshots_drop_table(self):
        cursor = self.connection.cursor()
        cursor.execute('drop table snapshots;')
        self.connection.commit()
        cursor.close()

    # todo: size chie?
    def snapshots_insert_table(self, cloud_id: int) -> bool:
        cursor = self.connection.cursor()
        create_time = str(datetime.datetime.now()).split(".")[0]
        cursor.execute("rollback;")
        try:
            cursor.execute("""  
                                CREATE OR REPLACE FUNCTION get_size_of_cloud(input_cloud_id int)
                                RETURNS int AS $$
                            declare  resultt int;
                            begin
                                select storage_size
                                into result
                                from cloud
                                where cloud.cloud_id = input_cloud_id;
                                return result;
                            end;
                            $$ language plpgsql;
                            
                            do $$
                            begin
                                if check_platform_data_to_cloud(%s, %s, %s, %s, %s, %s) then 
                                    insert into cloud
                                    (platform_pk, storage_size, ram, cpu_core, cpu_rate,
                                     bandwidth, os_id, passport_id, daily_price, ssh_hash, ssh_salt)
                                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                else RAISE EXCEPTION 'error'; 
                                end if;
                            end;$$;
                            
                                insert into snapshots
                                (cloud_id, create_time, sizee)
                                values (%s, %s, %s);
                            """, (cloud_id, create_time)
                           )
            self.connection.commit()
            cursor.close()
            return True
        except:
            cursor.close()
            return False

    def snapshots_delete(self, snapshots_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("rollback;")
        cursor.execute("""
                        delete from snapshots where snapshots.snapshots_id = %s RETURNING snapshots.snapshots_id;
                        """, (snapshots_id,))
        self.connection.commit()
        record = cursor.fetchall()
        cursor.close()
        if len(record) == 0:
            return False
        return True




def main():
    database = Database()
    database.open_connection()

    database.user_create_table()
    database.admin_create_table()
    database.os_create_table()
    database.platform_create_table()
    database.cloud_create_table()
    database.ticket_create_table()
    database.snapshots_create_table()

    # Todo: test for insert
    arman_insert = database.user_insert_table(first_name="arman",
                                              last_name="sabbagh",
                                              passport_id=123456789,
                                              email="arman@yahoo.com",
                                              password="arm123")
    if arman_insert:
        print("user arman add successfully")
    else:
        print("user arman can not add to database")

    mahdi_insert = database.user_insert_table(first_name="mahdi",
                                              last_name="kenevisi",
                                              passport_id=987654321,
                                              email="mahdi@gmail.com",
                                              password="zmmm123")
    if mahdi_insert:
        print("user mahdi add successfully")
    else:
        print("user mahdi can not add to database")

    # Todo: test for delete user
    user_delete = database.user_delete(123456789)
    if user_delete:
        print("user delete successfully")
    else:
        print("user don't exist")

    # Todo: test for insert admin
    admin1_insert = database.admin_insert_table("admin1", "admin1_lastname", 123321, "admin1@gamil", "admin1_pass")
    if admin1_insert:
        print("admin1 add successfully")
    else:
        print("admin1 can not add to database")

    admin2_insert = database.admin_insert_table("admin2", "admin2_lastname", 123321, "admin2@gamil", "admin2_pass")
    if admin2_insert:
        print("admin2 add successfully")
    else:
        print("admin2 can not add to database")

    # Todo: test for delete admin
    admin_delete = database.admin_delete(1)
    if admin_delete:
        print("admin delete successfully")
    else:
        print("admin don't exist")

    # Todo: test for insert os
    os_insert1 = database.os_insert_table("cent2 os")
    if os_insert1:
        print("os 1 add successfully")
    else:
        print("os 1 is not unique or admin doesn't exist")

    os_insert2 = database.os_insert_table("cent os")
    if os_insert2:
        print("os 2 add successfully")
    else:
        print("os 2 is not unique or admin doesn't exist")

    # Todo: test for delete os
    os_delete = database.os_delete(1)
    if os_delete:
        print("os delete successfully")
    else:
        print("os don't exist")

    # Todo: test for insert platform
    platform1_insert = database.platform_insert_table(storage_size=1000,
                                                      ram=2000,
                                                      cpu_core=3,
                                                      cpu_rate=600,
                                                      bandwidth=5)
    if platform1_insert:
        print("platform 1 add successfully")
    else:
        print("platform 1 can not add to database")

    platform2_insert = database.platform_insert_table(storage_size=8000,
                                                      ram=500,
                                                      cpu_core=8,
                                                      cpu_rate=6000,
                                                      bandwidth=16)
    if platform2_insert:
        print("platform 2 add successfully")
    else:
        print("platform 2 can not add to database")

    # Todo: test for delete platform
    platform_delete = database.platform_delete(3)
    if platform_delete:
        print("platform delete successfully")
    else:
        print("platform don't exist")

    # Todo: test for insert cloud
    cloud1_insert = database.cloud_insert_table(cloud_password="heyyyy",
                                                platform_pk=1,
                                                storage_size=800,
                                                ram=1500,
                                                cpu_core=3,
                                                cpu_rate=400,
                                                bandwidth=4,
                                                os_id=2,
                                                passport_id=987654321)
    if cloud1_insert:
        print("cloud 1 add successfully")
    else:
        print("cloud 1 can not add to database")

    cloud2_insert = database.cloud_insert_table(cloud_password="hiii",
                                                platform_pk=1,
                                                storage_size=1200,
                                                ram=1500,
                                                cpu_core=30,
                                                cpu_rate=5000,
                                                bandwidth=40,
                                                os_id=2,
                                                passport_id=987654321)
    if cloud2_insert:
        print("cloud 2 add successfully")
    else:
        print("cloud 2 can not add to database")

    # Todo: test for delete cloud
    cloud_delete = database.cloud_delete(4)
    if cloud_delete:
        print("cloud delete successfully")
    else:
        print("cloud don't exist")

    # Todo: test for insert ticket
    ticket1_insert = database.ticket_insert_table(987654321)

    if ticket1_insert:
        print("ticket 1 add successfully")
    else:
        print("ticket 1 can not add to database")

    ticket2_insert = database.ticket_insert_table(9877777654321)

    if ticket2_insert:
        print("ticket 2 add successfully")
    else:
        print("ticket 2 can not add to database")

    # Todo: test for delete ticket
    ticket_delete = database.ticket_insert_table(1)
    if ticket_delete:
        print("ticket delete successfully")
    else:
        print("ticket don't exist")

    # Todo: test for insert snapshots
    snapshots1_insert = database.snapshots_insert_table(1)

    if snapshots1_insert:
        print("snapshots 1 add successfully")
    else:
        print("snapshots 1 can not add to database")

    snapshots2_insert = database.snapshots_insert_table(9877777654321)

    if snapshots2_insert:
        print("snapshots 2 add successfully")
    else:
        print("snapshots 2 can not add to database")

    # Todo: test for delete snapshots
    snapshots_delete = database.snapshots_delete(1)
    if snapshots_delete:
        print("snapshots delete successfully")
    else:
        print("snapshots don't exist")

    database.close_connection()


if __name__ == "__main__":
    main()

