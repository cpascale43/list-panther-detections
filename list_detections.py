# pip install gql aiohttp
import subprocess
import sys
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

PANTHER_ENDPOINT = "<YOUR-GRAPHQL-ENDPOINT"
PANTHER_API_KEY = "<YOUR-API-KEY>"

# Check if a path was provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_panther_detections>")
    sys.exit(1)

# Get the path to the directory from the command-line argument
directory = sys.argv[1]

# Run the command to get the list of RuleIDs
command = (
    "grep -rl 'Enabled: true'" + f" {directory} " + "| xargs awk '/RuleID/ {print $2}'"
)
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, error = process.communicate()

# Convert the output to a list of RuleIDs
rule_ids = output.decode("utf-8").split("\n")

# Remove any empty strings from the list, reformat to single-quote strings
rule_ids = [rule_id.replace('"', '') for rule_id in rule_ids if rule_id]

# Convert the list of RuleIDs to a string format suitable for the SQL query
rule_ids_str = ", ".join(f"'{rule_id}'" for rule_id in rule_ids)

# Define the SQL query
sql = f"SELECT p_rule_id, count(*) FROM panther_views.public.all_rule_matches WHERE p_occurs_since('30 days') AND p_rule_id IN ({rule_ids_str}) GROUP BY p_rule_id ORDER BY 2 ASC"

transport = AIOHTTPTransport(
    url=PANTHER_ENDPOINT,
    headers={"X-API-Key": PANTHER_API_KEY},
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# `IssueQuery` is a nickname for the query. You can fully omit it.
issue_query = gql(
    """
    mutation IssueQuery($sql: String!) {
        executeDataLakeQuery(input: { sql: $sql }) {
            id
        }
    }
    """
)

# `GetQueryResults` is a nickname for the query. You can fully omit it.
get_query_results = gql(
    """
    query GetQueryResults($id: ID!) {
        dataLakeQuery(id: $id) {
            message
            status
            results {
                edges {
                    node
                }
            }
        }
    }
    """
)

# Issue a Data Lake (Data Explorer) query
mutation_data = client.execute(issue_query, variable_values={"sql": sql})


# an accumulator that holds all results that we fetch from all pages
all_results = []
# a helper to know when to exit the loop.
has_more = True

# Start polling the query until it returns results
while has_more:
    query_data = client.execute(
        get_query_results,
        variable_values={
            "id": mutation_data["executeDataLakeQuery"]["id"]
        },
    )

    # if it's still running, print a message and keep polling
    if query_data["dataLakeQuery"]["status"] == "running":
        print(query_data["dataLakeQuery"]["message"])
        continue

    # if it's not running & it's not completed, then it's
    # either cancelled or it has errored out. In this case,
    # throw an exception
    if query_data["dataLakeQuery"]["status"] != "succeeded":
        raise Exception(query_data["dataLakeQuery"]["message"])

    all_results.extend(
        [edge["node"] for edge in query_data["dataLakeQuery"]["results"]["edges"]]
    )
    print(all_results)
    has_more = False

print(f"{len(all_results)} detections fired over the past 30 days!")
