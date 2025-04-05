from neo4j import GraphDatabase

# Initialize connection
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def seed_kg_data():
    with driver.session() as session:
        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")
        
        # Create banking entities
        session.run("""
        CREATE (transfer:Service {name: 'money_transfer', type: 'core'})
        CREATE (loan:Service {name: 'personal_loan', type: 'core'})
        CREATE (psd2:Regulation {name: 'PSD2', region: 'EU'})
        CREATE (kfc:Customer {name: 'KFC', category: 'business'})
        CREATE (john:Customer {name: 'John Doe', category: 'retail'})
        
        // Create relationships
        CREATE (transfer)-[:HAS_FEE {amount: 1.5, currency: 'USD'}]->(:Fee {name: 'international_fee'})
        CREATE (transfer)-[:GOVERNED_BY {since: 2018}]->(psd2)
        CREATE (transfer)-[:USED_BY {frequency: 'weekly'}]->(kfc)
        CREATE (loan)-[:USED_BY {frequency: 'monthly'}]->(john)
        CREATE (loan)-[:HAS_REQUIREMENT]->(:Requirement {name: 'credit_check'})
        """)

# Seed the data
seed_kg_data()