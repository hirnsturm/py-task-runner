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

    #
    # Initialization
    #
    def __init__(self):
        self.intro()
        self.load_configuration()
        self.proceed()
        self.gather_answers()
        self.run_tasks()
        self.leave_msg()

    #
    # Load configuration
    #
    def load_configuration(self):
        if os.path.isfile(self.configuration_file) is False:
            print(ColoredText.get_colored_text('Missing configuration file "' + self.configuration_file + '"!', 'red'))
            print(ColoredText.get_colored_text('Please create file from "taskrunner.yml.dist".', 'red'))
            print()
            sys.exit(1)
        self.configuration = yaml.safe_load(open(self.configuration_file))

    #
    # Print the intro
    #
    def intro(self):
        print()
        print(ColoredText.get_colored_text('--------------------------------------------------------------', 'yellow'))
        print(ColoredText.get_colored_text('  Task Runner', 'yellow'))
        print()
        print(ColoredText.get_colored_text('  Written by Steve Lenz', 'yellow'))
        print()
        print('  - Website: https://github.com/hirnsturm/py-task-runner')
        print('  - Issues: https://github.com/hirnsturm/py-task-runner/issues')
        print(ColoredText.get_colored_text('--------------------------------------------------------------', 'yellow'))
        print()

    #
    # Proceed?
    #
    def proceed(self):
        proceed = self.get_input('Do you want to proceed? (Y|n) ')
        if not (proceed is 'Y' or proceed is 'y' or proceed is ''):
            print()
            print('Bye')
            print()
            sys.exit(0)

    #
    # Gather answers for given questions
    #
    def gather_answers(self):
        print()
        print(ColoredText.get_colored_text('Gather configurations', 'yellow'))

        if self.configuration['questions'] is None:
            print('No questions found in taskrunner.yml!')
            return

        for key, question in self.configuration['questions'].items():
            self.answers[key] = ''
            while self.answers[key] is '':
                self.answers[key] = self.get_input(question)

    #
    # Run tasks
    #
    def run_tasks(self):
        print()
        print(ColoredText.get_colored_text('Run tasks', 'yellow'))

        if not ('tasks' in self.configuration) or self.configuration['tasks'] is None:
            print('No tasks found in taskrunner.yml!')
            return

        for task in self.configuration['tasks']:
            print(ColoredText.get_colored_text('--> ' + task['info'], 'blue'))

            if task['type'] == 'replace_placeholder':
                self.replace_placeholder(task['file'])
            elif task['type'] == 'command':
                print(ColoredText.get_colored_text('Command: ', 'blue') + task['cmd'])
                print('Output: ')
                if 1 == os.system(task['cmd']):
                    sys.exit(1)

    #
    # Replace placeholder
    #
    def replace_placeholder(self, file):
        try:
            with open(file) as f:
                template = Template(f.read())
            print(ColoredText.get_colored_text('File: ', 'blue') + file)
            file = open(file, 'w')
            file.write(template.render(self.answers))
            file.close()
        except FileNotFoundError:
            print(ColoredText.get_colored_text(file + ' is missing', 'red'))
        except PermissionError:
            print(ColoredText.get_colored_text('You are not allowed to read ' + file, 'red'))

    #
    # Get input
    #
    def get_input(self, question):
        return input(ColoredText.get_colored_text('- ' + question + ': ', 'blue'))

    #
    # Print the lease message
    #
    def leave_msg(self):
        print()
        print(ColoredText.get_colored_text('Done.', 'green'))
        print('Bye.')
        print()


#
# ColoredText
#
class ColoredText:
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
    # Prints 'text' in given 'color' (available colors see 'ColorText.color')
    #
    @staticmethod
    def get_colored_text(text, color):
        return ColoredText.color['text'][color] + text + ColoredText.color['remove']


#
#
#
if __name__ == "__main__":
    TaskRunner()
