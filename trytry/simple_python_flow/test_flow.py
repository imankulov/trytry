# -*- coding: utf-8 -*-
from trytry.testflow.test_runners import StepRunner


class GenericSimplePythonRunner(StepRunner):
    on_err_hint = ("Oh my God! Something goes wrong. Try read "
                   "instruction more carefully and perform the "
                   "task more diligently. Remember, I'm watching "
                   "you.")

    def get_command(self, user_input):
        return ['python', '-c', user_input]


class Step1Runner(GenericSimplePythonRunner):
    """
    Write "hello world", son of a bitch!
    """

    expected_out = 'hello world'
    on_success_hint = ('Congratulations! You rules! '
                       'Your first Python program work! '
                       'Let\'s go to the next level of knowledge')
    on_wrong_out_hint = ("It's nice, but we asked you to write hello "
                         "world")

class Step2Runner(GenericSimplePythonRunner):
    """
    Then show me what is 1 + 1, son of a bitch!
    """

    expected_out = '2'
    on_success_hint = ("Congratulations! You rules! "
                       "You know the maths. That's all for now")
    on_wrong_out_hint = ("It's nice, but we asked you to write 1 + 1")


class SimplePythonFlow(object):

    def install(self):
        pass

    step1 = Step1Runner()
    step2 = Step2Runner()

    def destroy(self):
        pass
