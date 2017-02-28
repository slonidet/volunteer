import json

from django.core.management.base import BaseCommand, CommandError
from user_tests.models import Test, Task, Question, AnswerOptions


class Command(BaseCommand):
    help = 'Creates list of questions for given task of given test.\n'\
           'It takes six required arguments:\n'\
           '--choice_type - takes one of options to estimate questions \n' \
           '\tunique - only one correct choice\n' \
           '\tmultiple - many correct choices\n' \
           '\tby_admin - question is to be estimate by admin\n' \
           '--file - takes full name of json file with task data\n' \
           '--test - takes test name\n' \
           '--time_available - takes available time to pass a test\n' \
           '--task - takes task name\n' \
           '--expert_appraisal - takes if task should be appraise'

    def add_arguments(self, parser):

        parser.add_argument(
            '--choice_type',
            action='store',
            dest='choice_type',
            help='Stores if task contains only one choice questions'
        )

        parser.add_argument(
            '--file',
            action='store',
            dest='file',
            help='Stores JSON file of given task'
        )

        parser.add_argument(
            '--test',
            action='store',
            dest='test',
            help='Stores test name'
        )

        parser.add_argument(
            '--time_available',
            action='store',
            dest='time_available',
            help='Stores available time (number of seconds) to pass test',
            type=int
        )

        parser.add_argument(
            '--task',
            action='store',
            dest='task',
            help='Stores task name'
        )

        parser.add_argument(
            '--expert_appraisal',
            required=False,
            action='store',
            dest='expert_appraisal',
            help='Stores if task should be appraise',
            type=bool
        )

        parser.set_defaults(expert_appraisal=False)

    def handle(self, *args, **options):

        choice_type = options['choice_type']
        file = options['file']
        test = options['test']
        time_available = options['time_available']
        task = options['task']
        expert_appraisal = True

        json_data = open(file).read()
        json_data = json.loads(json_data)

        test_object, test_created = Test.objects.get_or_create(
            name=test, time_available=time_available
        )
        task_object, task_created = Task.objects.get_or_create(
            test=test_object, name=task, expert_appraisal=expert_appraisal
        )

        for item in json_data:

            title = item["title"]
            question = Question.objects.create(text=title, task=task_object)

            if choice_type == 'unique':
                true_answers = [i[0] for i in item['choices'] if i[0]]
                if len(true_answers) > 1:
                    raise CommandError(
                        "This question should contain only one correct "
                        "choice"
                    )

            for is_correct, text in item["choices"]:
                AnswerOptions.objects.create(
                    question=question, text=text, is_correct=is_correct
                )
