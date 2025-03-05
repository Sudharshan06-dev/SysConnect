from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password, database = 'neo4j'):
        self._driver = GraphDatabase.driver(uri=uri,auth=(user, password))
        self.database = database
    
    def close(self):
        self._driver.close()
    
    def execute_query(self, query, paramters = None):
        with self._driver.session(database=self.database) as session:
            return session.run(query=query, parameters=paramters).data()
    

#Update with your credentials
neo4j_conn = Neo4jConnection('neo4j://localhost:7687', 'admin', 'password', "course")