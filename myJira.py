import click
import keyring
import getpass
import json
from JIRA import jira


@click.command()
@click.option('--config', is_flag=True, 
            help='Start configuration, required for usage.')
@click.option('--create', is_flag=True, 
            help='Create ticket in default project.')
def cli(config, create):
    if config:
        start_config()
    elif config == False:
        try:
            with open('jira_config.json') as json_file:
                config = json.load(json_file)
                #config = read_jira_config() 
                for p in config['config']:
                    server_url = p['server_url']
                    project = p['default_project']
                    username = p['default_user']
                password = get_keyring(username)
        except FileNotFoundError:
            print("No config file found, please run myJira.py --config")
        else:
            if create:
                create_ticket(server_url, project, username, password)
        

def start_config():
    click.echo('Password credentials saved in windows credential manager.')
    username = input('user: ')
    password = getpass.getpass("password: ")
    jira_url = input('jira url: ')
    project_key = input('Project key: ')
    set_keyring(username, password)

    jira_config_write(jira_url, project_key, username)


def set_keyring(username, password):
    keyring.set_password("jira-api", username, password)


def get_keyring(username):
    password = keyring.get_password("jira-api", username)
    return password


def jira_config_write(server, project, username):
    jira_config = {}
    jira_config['config'] = []
    jira_config['config'].append({
        'server_url': server,
        'default_project': project,
        'default_user': username,
    })

    with open('jira_config.json', 'w') as outfile:
        json.dump(jira_config, outfile)

def create_ticket(server, project, username, password):
    
    title = input('Title: ')
    description = input('Description: ')
    label = input('Label: ')
    task_type = 'Task'

    jira = JIRA(server=(server), basic_auth=(username, password))
    issue_dict = {
        'project': {'key': project},
        'summary': title,
        'description': description,
        'issuetype': {'name': task_type},
    }
    issue = jira.create_issue(fields=issue_dict)
    issue.fields.labels.append(label)
    issue.update(fields={"labels": issue.fields.labels})


if __name__ == '__main__':
    cli()
