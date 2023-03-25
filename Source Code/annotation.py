# Code for generating annotations

class PlanTree:
    def __init__(self, query_plan):
        self.query_plan = query_plan
        self.head = PlanNode(self.query_plan)

    def get_head(self):
        return self.head

    def get_all_node_types(self):
        nodes_set = set()
        queue = [self.head]
        nodes_set.add(self.head.get_node_type())

        while len(queue) != 0:
            temp = []
            while len(queue) != 0:
                cur = queue.pop(0)
                nodes_set.add(cur.get_node_type())
                for child in cur.children:
                    nodes_set.add(child.get_node_type())
                    temp.append(child)
            queue = temp
        return nodes_set

    # For testing only
    def print_tree(self):
        queue = [self.head]
        print("HEAD: ", self.head.get_node_type())
        level = 1
        print("Printing tree by level:")
        while len(queue) != 0:
            temp = []
            # print(level, ": ", end='')
            print(level)
            while len(queue) != 0:
                cur = queue.pop(0)
                print("CUR: ", cur.get_node_type())
                print(cur.get_node_type(), end=' | ')
                # Testing explain_node_type()
                print(cur.explain_node_type())
                print()
                #print(cur.get_misc())
                print("LENGTH OF CHILDREN: ", len(cur.children))
                for child in cur.children:
                    print("CHILD: ", child.get_node_type(), "of cur: ", cur.get_node_type())
                    temp.append(child)
            queue = temp
            print()
            level += 1
    
    def get_more_info(self):
        queue = [self.head]
        all_info = []
        level = 1
        while len(queue) != 0:
            temp = []
            node_info = []
            print(level)
            while len(queue) != 0:
                cur = queue.pop(0)
                explain_actual_cost = cur.explain_actual_cost()
                explain_cost_diff = cur.explain_cost_diff()
                node_info.append(explain_actual_cost+explain_cost_diff)
                for info in node_info:
                    all_info.append(info)
                for child in cur.children:
                    temp.append(child)
            queue = temp
            print()
            level += 1
            return all_info
    
    def get_cost_info(self):
        queue = [self.head]
        node_info = []
        level = 1
        while len(queue) != 0:
            temp = []
            # print(level, ": ", end='')
            while len(queue) != 0:
                cur = queue.pop(0)
                est_cost = cur.get_estimated_cost()
                final_est_cost = est_cost.get('Total Cost')
                actual_cost = cur.get_actual_cost()
                final_actual_cost = actual_cost.get('Total Time')
                node_info.append(final_est_cost)
                node_info.append(final_actual_cost)
                for child in cur.children:
                    temp.append(child)
            queue = temp
            level += 1
        return node_info

"""
    Information in each query plan:
    'Node Type', 'Strategy', 'Partial Mode', 'Parallel Aware',
    'Async Capable', 'Startup Cost', 'Total Cost', 'Plan Rows',
    'Plan Width', 'Actual Startup Time', 'Actual Total Time', 
    'Actual Rows', 'Actual Loops', 'Output', 'Plans'
    Information extracted by each node:
    Node Type, 
    Startup Cost, Total Cost, Plan Rows, Plan Width
    
"""


class PlanNode:
    def __init__(self, query_plan):
        self.query_plan = query_plan
        self.children = []
        self.node_type = None
        self.estimated_cost = {}
        self.actual_cost = {}
        self.misc = {}
        self.hasFilter = False
        self.filter = {}
        self.parse_plan()
        self.add_children()

    def add_children(self):
        if "Plans" in self.query_plan:
            for plan in self.query_plan['Plans']:
                self.children.append(PlanNode(plan))

    def parse_plan(self):
        self.node_type = self.query_plan['Node Type']

        self.parse_cost()
        self.parse_misc()
        self.parse_filter()
        return

    """
    Parses cost information of the query plan.
    """

    def parse_cost(self):
        self.estimated_cost['Startup Cost'] = self.query_plan['Startup Cost']
        self.estimated_cost['Total Cost'] = self.query_plan['Total Cost']
        self.estimated_cost['Plan Rows'] = self.query_plan['Plan Rows']
        self.estimated_cost['Plan Width'] = self.query_plan['Plan Width']
        self.actual_cost['Startup Time'] = self.query_plan['Actual Startup Time']
        self.actual_cost['Total Time'] = self.query_plan['Actual Total Time']
        self.actual_cost['Actual Rows'] = self.query_plan['Actual Rows']
        self.actual_cost['Actual Loops'] = self.query_plan['Actual Loops']

    """
            Parses miscellaneous information of the query plan.
            Includes Parent Relationship, Plan Width, Output
    """

    def parse_misc(self):
        if 'Parent Relationship' in self.query_plan:
            self.misc['Parent Relationship'] = self.query_plan['Parent Relationship']
        if 'Plan Width' in self.query_plan:
            self.misc['Plan Width'] = self.query_plan['Plan Width']
        if 'Output' in self.query_plan:
            self.misc['Output'] = self.query_plan['Output']

    """
    Parses filter information of the query plan.
    """

    def parse_filter(self):
        if 'Filter' in self.query_plan:
            self.hasFilter = True
        else:
            return
        self.filter['Filter'] = self.query_plan['Filter']
        self.filter['Rows Removed'] = self.query_plan['Rows Removed by Filter']

    def get_node_type(self):
        return self.node_type

    """
    Explains the estimated cost. Returns a string.
    # TODO: relation name
    """

    def explain_node_type(self):
        explain = ""

        # 1. Retrieval Methods
        if self.node_type == "Seq Scan":
            explain += "Relation [{}] is read using Sequential Scan.".format(self.query_plan['Relation Name'])
            if self.hasFilter:
                explain += 'It then filter by [{}].'.format(self.filter['Filter'])
            explain += " This is because no index is created in the table."

        elif self.node_type == "Index Scan":
            explain += 'Relation [{}] is read using the Index Scan '.format(self.query_plan['Relation Name'])
            if "Index Cond" in self.query_plan:
                explain += 'with condition(s): [{}]. '.format(self.query_plan['Index Cond'])
            if self.hasFilter:
                explain += 'It then filter by [{}]. '.format(self.filter['Filter'])

        elif self.node_type == 'Index Only Scan':
            explain += 'Relation [{}] is read using the Index Only Scan '.format(self.query_plan['Relation Name'])
            if "Index Cond" in self.query_plan:
                explain += 'with condition(s): [{}]. '.format(self.query_plan['Index Cond'])
            if self.hasFilter:
                explain += 'It then filter by [{}]. '.format(self.filter['Filter'])

        elif self.node_type == "Bitmap Heap Scan":
            explain += 'Relation [{}] is read using the Bitmap Heap Scan.'.format(self.query_plan['Relation Name'])

        elif self.node_type == "Bitmap Index Scan":
            explain += 'Relation [{}] is read using the Bitmap Index Scan.'.format(self.query_plan['Relation Name'])

        elif self.node_type == "CTE_Scan":
            explain += 'Relation [{}] is read using the CTE_Scan '.format(self.query_plan['Relation Name'])
            if "Index Cond" in self.query_plan:
                explain += 'with condition(s): [{}]. '.format(self.query_plan['Index Cond'])
            if self.hasFilter:
                explain += 'It then filter by [{}]. '.format(self.filter['Filter'])

        # 2. Join Methods
        elif self.node_type == "Hash Join":
            explain += "The Hash Join will joins the previous operations with a hash [{}] join " \
                       "on the condition(s): [{}].".format(self.query_plan['Join Type'], self.query_plan['Hash Cond'])

        elif self.node_type == "Merge Join":
            explain += 'The Merge Join will joins the previous operations using on the condition(s): [{}].'.format(
                [self.query_plan['Merge Cond']])
            if "Join Type" in self.query_plan:
                explain += ' However, only the rows from the left table is returned.'

        elif self.node_type == "Nested Loop":
            explain += "The Nested Loop operation is performed."

        # 3. Sort Method
        elif self.node_type == "Sort":
            explain += 'The Sort operation [{}] sorts the rows based on the key: [{}]'.\
                format(self.query_plan["Sort Method"], self.query_plan['Sort Key'])
            if "INC" in self.query_plan['Sort Key']:
                explain += ' in increasing order.'
            if "DESC" in self.query_plan['Sort Key']:
                explain += ' in decreasing order.'

        elif self.node_type == "Incremental Sort":
            explain += 'The Incremental Sort operation sorts the rows based on the key: [{}]'\
                .format(self.query_plan['Sort Key'])
            if "INC" in self.query_plan['Sort Key']:
                explain += ' in increasing order.'
            if "DESC" in self.query_plan['Sort Key']:
                explain += ' in decreasing order.'

        # 4. Hash
        elif self.node_type == "Hash":
            explain += 'The Hash function will generate a hash table from the records in the previous operation.'
            explain += "The number of Hash Buckets is {}.".format(self.query_plan["Hash Buckets"])

        # 5. Aggregation
        elif self.node_type == "Aggregate":
            strategy = self.query_plan["Strategy"]

            if strategy == "Plain":
                explain += 'The Aggregate operation will be performed.'
            if strategy == "Sorted":
                explain += 'The Aggregate operation will sort the tuples based on the keys: [{}].'.format(
                    self.query_plan["Group Key"])
                if self.hasFilter:
                    explain += ' The result is then filtered by [{}]. '.format(self.filter['Filter'])
            if strategy == "Hashed":
                explain += 'The Aggregate operation will hash the rows based on keys: [{}]. ' \
                           'The selected rows are then returned '.format(self.query_plan["Group Key"])

        elif self.node_type == "Gather":
            explain += 'The Gather Merge operation is performed.' + '\n'

        elif self.node_type == "Limit":
            explain += "The Limit operation will limit the scanning, with a limitation of [{}] rows"\
                .format(self.query_plan['Plan Rows'])
        else:
            explain += "The {} operation will be performed.".format(self.node_type)

        return explain

    """
    Returns startup time, total cost, plan rows, plan width of the query plan.
    """

    def get_estimated_cost(self):
        return self.estimated_cost

    """
    Explains the estimated cost. Returns a string.
    """

    def explain_estimated_cost(self):
        explain = ""

        explain += "The estimated time spending before any output can be produced is " \
                   + str(self.estimated_cost['Startup Cost']) + " disk page fetch(es). "
        explain += "The estimated total cost until completion is " \
                   + str(self.estimated_cost['Total Cost']) \
                   + ", including the costs of all child nodes. "
        explain += "The estimated number of output rows is " \
                   + str(self.estimated_cost['Plan Rows']) + ", and "
        explain += "the average width of each row is " \
                   + str(self.estimated_cost['Plan Width']) + " byte(s)."
        return explain

    """
    Returns startup time, total time, actual rows, actual loops of the actual execution.
    """

    def get_actual_cost(self):
        return self.actual_cost

    """
    Explains the actual execution cost. Returns a string.
    # TODO: BUGG: can only concatenate str to str
    """

    def explain_actual_cost(self):
        explain = ""
        explain += "The actual startup time is " \
                   + str(self.actual_cost['Startup Time']) + " ms. "
        explain += "The actual total time is " \
                   + str(self.actual_cost['Total Time'] * self.actual_cost['Actual Loops']) + " ms " \
                   + "after being executed for " + str(self.actual_cost['Actual Loops']) + " loop(s), " \
                   + "inclusive of the costs of all child nodes. "
        explain += "The total number of rows emitted is " \
                   + str(self.actual_cost['Actual Rows'] * self.actual_cost['Actual Loops']) + "."
        return explain

    """
    Explain the cost difference between the query execution plan and actual execution.
    Returns a string.
    """

    def explain_cost_diff(self):
        explain = ""
        # Explain difference in time
        explain += "The estimation of cost only considers what matters for the planner. " \
                   "Specifically, the estimated cost does not consider the time for transmitting " \
                   "output rows to the client, which cannot be optimized by changing the plan. " \
                   "Therefore, the actual execution time is usually higher. "
        # Explain difference in rows emitted
        est_rows = self.estimated_cost['Plan Rows']
        act_rows = self.actual_cost['Actual Rows'] * self.actual_cost['Actual Loops']
        if est_rows == act_rows:
            # If the estimation and actual execution are the same
            explain += "In this case, the planner yields an accurate estimation of the number of rows omitted."
        elif est_rows > act_rows:
            # If the estimation > actual execution
            explain += "In estimation, the node is assumed to be run until full completion. " \
                       "However, the plan node execution can be stopped early due to LIMIT or similar effect. " \
                       "Thus, the actual number of rows emitted is less than estimated."
        else:
            # If the estimation < actual execution
            explain += "Sometimes the node is backed up and rescanned, " \
                       "and the planner counts these repeated emissions as if they were real additional rows. " \
                       "Consequently, the reported actual row counts can be higher than estimated."
        return explain

    """
        Returns miscellaneous information of the node.
        Includes Parent Relationship, Plan Width, Output
    """

    def get_misc(self):
        return self.misc

    """
    Returns filter information of the query plan.
    Includes filter conditions and number of rows removed by filter.
    """

    def get_filter(self):
        if not self.hasFilter:
            return None
        return self.filter
