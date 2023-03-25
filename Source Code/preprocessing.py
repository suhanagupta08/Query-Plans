
import psycopg2
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from selenium import webdriver
from selenium.webdriver.common.by import By
from annotation import PlanTree

class Preprocessor:
    def __init__(self):
        self.cur = None
        self.conn = None

    def establish_connection(self, database, user, password):
        # # establish the connection
        # self.conn = psycopg2.connect(database=database, user=user, password=password)
        # # create a cursor object
        # self.cur = self.conn.cursor()
        #conn = None
        try:
            self.conn = psycopg2.connect(database=database, user=user, password=password)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            verify = True
            info = {
                "username" : user,
                "password" : password,
                "database" : database
            }
            json_object = json.dumps(info, indent=4)
            with open("logininfo.json", "w") as outputfile:
                 outputfile.write(json_object)
        except (Exception, psycopg2.DatabaseError) as error:
            verify = False
        return verify


    def connect(self):
        """ Connect to the PostgreSQL database server """
        #conn = None
        f = open('logininfo.json', "r")
        data = json.load(f)
        username = data['username']
        pwd = data['password']
        database_name = data['database']
        try:
            # read connection parameters
            #username = postgres, pwd = root
            self.conn = psycopg2.connect(database=database_name, user=username, password=pwd)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # create a cursor
            self.cur = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return 

    def execute_query_qep(self, query):
        try:
            self.cur.execute("SET enable_hashjoin = on")
            self.cur.execute("SET enable_mergejoin = on")
            self.cur.execute("SET enable_nestloop = on")
            self.cur.execute("SET enable_indexscan = on")
            self.cur.execute("SET enable_seqscan = on")
            final_query = "EXPLAIN (analyze, verbose, costs, format JSON)" + query
            # execute the explain query
            query_plan = self.cur.execute(final_query)
            # print("setting on")
            # fetch all rows of the query result
            result = self.cur.fetchall()
            # queryPlan = result[0][0][0]["Plan"]
            queryPlan = (json.dumps(result, sort_keys=False, indent=4))
            # print("JSON TO CHECK: ", queryPlan)
            # return queryPlan
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Please check the query statement entered: ", query)
            return None

        # Viewing query_plan for testing
        #query_plan = (json.dumps(result, sort_keys=False, indent=4))
        # print(query_plan)
        # Return results in dict
        return result[0][0][0]['Plan']

    def execute_query_qep1(self, query):
        try:
            final_query = "EXPLAIN (analyze, verbose, costs, format JSON)" + query
            # execute the explain query
            query_plan = self.cur.execute(final_query)
            # print("setting on")
            # fetch all rows of the query result
            result = self.cur.fetchall()
            # queryPlan = result[0][0][0]["Plan"]
            queryPlan = (json.dumps(result, sort_keys=False, indent=4))
            # print("JSON TO CHECK: ", queryPlan)
            # return queryPlan
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Please check the query statement entered: ", query)
            return None

        # Viewing query_plan for testing
        #query_plan = (json.dumps(result, sort_keys=False, indent=4))
        # print(query_plan)
        # Return results in dict
        return result[0][0][0]['Plan']

    def execute_query_aqp(self, query):
        try:
            query_plan = self.execute_query_qep1(query)
            if query_plan:
                plan_tree = PlanTree(query_plan)
                node_types = plan_tree.get_all_node_types()

                if "Hash Join" in node_types:
                    self.cur.execute("SET enable_hashjoin = off")
                elif "Merge Join" in node_types:
                    self.cur.execute("SET enable_mergejoin = off")
                elif "Nested Loop" in node_types:
                    self.cur.execute("SET enable_nestloop = off")
                elif "Index Scan" in node_types:
                    self.cur.execute("SET enable_indexscan = off")
                elif "Seq Scan" in node_types:
                    self.cur.execute("SET enable_seqscan = off")
                else:
                    print("NO modification has made.")

            return self.execute_query_qep1(query)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Please check the query statement entered: ", query)
            return None
