import asyncio
import time

import websockets
import yaml

from pycodimd import CodiMD

basenote = 'coronaschooling'

cmd = CodiMD('https://md.noemis.me')
cmd.load_cookies()

tabelle_ueberschrift = "Fach | Aufgabe | v. Dauer | reelle Dauer | Abgabefrist | abgegeben am | Rückmeldung erhalten am"
tabelle_striche = "| - | - | - | - | - | - | - |"

schooling_notes = []
weeks = {}

for note in cmd.history():
    if len(note['tags']) and 'schooling' in note['tags']:
        print('-' * 20)
        print(note['text'])

        cmd.set_permission(note['id'])
        content = cmd.content(note['id'])
        yaml_block = content.split('---')[1].replace('\t', ' ')
        metadata = yaml.load(yaml_block, Loader=yaml.SafeLoader)
        content_title = note['text']

        for line in content.split('\n'):
            if line.startswith('# '):
                content_title = line[2:]
                print(content_title)

        if not metadata['school']['week'] in weeks:
            weeks[metadata['school']['week']] = []

        task = {
            'note': note,
            'yaml': metadata,
            'title': content_title
        }
        schooling_notes.append(task)
        weeks[metadata['school']['week']].append(task)

        print('')

main_content = cmd.content(basenote)
main_lines = main_content.split('\n')

for week, week_tasks in weeks.items():
    try:
        startline = main_lines.index('<!--. start {} -->'.format(week)) + 1
        endline = main_lines.index('<!--. end {} -->'.format(week))

        for _ in range(startline, endline):
            while not cmd.delete_line(basenote, startline):
                pass
            time.sleep(0.25)

        while not cmd.insert_line(basenote, startline, tabelle_ueberschrift):
            pass

        while not cmd.insert_line(basenote, startline + 1, tabelle_striche):
            pass

        taskline = startline + 2
        for task in week_tasks:
            time.sleep(0.25)
            while not cmd.insert_line(basenote, taskline, '| {} | {} | {} | {} | {} | {} | {} |'.format(
                task['yaml']['title'].split(' - ')[0][6:],
                "[{}]({}/{})".format(task['title'], cmd.server_url, task['note']['id']),
                task['yaml']['school'].get('duration', ''),
                task['yaml']['school'].get('realDuration', ''),
                task['yaml']['school'].get('due', ''),
                task['yaml']['school'].get('submitted', ''),
                task['yaml']['school'].get('feedback', ''),
            )):
                pass
            taskline += 1

    except IndexError:
        continue


#cmd.replace_line('test', 3, r'replaced\\\\o\/')
