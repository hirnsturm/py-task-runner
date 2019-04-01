#
# Task Runner
#
# author: Steve Lenz
#
import os
import sys

try:
    from jinja2 import Template
except ImportError:
    print('This program requires Jinja2 (http://jinja.pocoo.org/)! Installation with pip: pip3 install Jinja2')
    sys.exit(1)
try:
    import yaml
except ImportError:
    print('This program requires PyYAML (https://pyyaml.org/)! Installation with pip: pip3 install PyYAML')
    sys.exit(1)


#
# Task runner
#
class TaskRunner:
    configuration = []
    configuration_file = './taskrunner.yml'
    answers = {}
    color = {
        'remove': '\033[0m',
        'text': {
            'blue': '\033[34m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[31m',
        }
    }

    #
    # Initialization
    #
    def __init__(self):
        self.intro()
        self.load_configuration()
        self.proceed()
        self.gather_answers()
        self.run_tasks()

    #
    # Load configuration
    #
    def load_configuration(self):
        if os.path.isfile(self.configuration_file) is False:
            print(self.color['text']['red'] + 'Missing configuration file "' + self.configuration_file + '"!')
            print('Please create file from "taskrunner.yml.dist".')
            print(self.color['remove'])
            sys.exit(1)
        self.configuration = yaml.safe_load(open(self.configuration_file))

    #
    # Intro
    #
    def intro(self):
        #
        # Intro
        #
        print(self.color['text']['yellow'])
        print('--------------------------------------')
        print('  Task Runner')
        print('')
        print('  Written by Steve Lenz')
        print('--------------------------------------')
        print(self.color['remove'])

    def proceed(self):
        proceed = self.get_input('Do you want to proceed? [y|n] ')
        if not (proceed is 'y'):
            sys.exit(0)

    #
    # Gather answers for given questions
    #
    def gather_answers(self):
        print(self.color['text']['yellow'])
        print('Gather configurations' + self.color['remove'])

        if self.configuration['questions'] is None:
            print('Es konnten keine abfragen zur Konfiguration gefunden werden.')
            return

        for key, question in self.configuration['questions'].items():
            self.answers[key] = ''
            while self.answers[key] is '':
                self.answers[key] = self.get_input(question)

    #
    # Run tasks
    #
    def run_tasks(self):
        print(self.color['text']['yellow'])
        print('Run tasks' + self.color['remove'])

        if not ('tasks' in self.configuration) or self.configuration['tasks'] is None:
            print('Es konnten keine \'tasks\' gefunden werden.')
            return

        for task in self.configuration['tasks']:
            print('- ' + task['info'])
            if task['type'] == 'replace_placeholder':
                with open(task['file']) as f:
                    template = Template(f.read())
                file = open(task['file'], 'w')
                file.write(template.render(self.answers))
                file.close()
            elif task['type'] == 'command':
                if 1 == os.system(task['cmd']):
                    sys.exit(1)

    #
    # Get input
    #
    def get_input(self, question):
        return input(self.color['text']['blue'] +
                           '- ' + question + ': ' +
                           self.color['remove'])


if __name__ == "__main__":
    TaskRunner()
