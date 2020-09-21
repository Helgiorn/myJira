from jira import JIRA
import argparse
import keyring

username = ""
password = keyring.get_password("jira-api", username)
server = ""
project = ""
label = ""
jira = JIRA(server=(server), basic_auth=(username, password))

#### ARGS
parser = argparse.ArgumentParser(description='SWSU OCELOT Ticket Creator.')
parser.add_argument("--title", type=str, help="Title for JIRA ticket.")
parser.add_argument("--description", type=str, help="Description field for JIRA Ticket, required.")
parser.add_argument("--type", default="Task", type=str, help="the type of the ticket, default is Task.")
parser.add_argument("--reporter", type=str, help="input: your user id in JIRA, will list all your open reported tickets.")
parser.add_argument("--assignee", type=str, help="input: your user id in JIRA, list open issues by reporter.")

args = parser.parse_args()

if args.title:
    issue_dict = {
        'project': {'key': project},
        'summary': args.title,
        'description': args.description,
        'issuetype': {'name': args.type},
    }
    #create ticket.
    issue = jira.create_issue(fields=issue_dict)
    #Append OCELOT label to ticket.
    issue.fields.labels.append(label)
    issue.update(fields={"labels": issue.fields.labels})
elif args.reporter:
    for issue in jira.search_issues('reporter = ' + args.reporter + ' and STATUS IN ("New", "Open", "Approved", "Planned", "In Progress") order by created desc', maxResults=50):
        print('{}: {}'.format(issue.key, issue.fields.summary))
elif args.assignee:
    for issue in jira.search_issues('assignee = ' + args.assignee + ' and STATUS IN ("New", "Open", "Approved", "Planned", "In Progress") order by created desc', maxResults=50):
        print('{}: {}'.format(issue.key, issue.fields.summary))


