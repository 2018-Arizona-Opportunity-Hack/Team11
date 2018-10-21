import imageio
import matplotlib.pyplot as plt
import numpy as np
import pdf2image
import json


class QuestionnaireReader:

    def __init__(self,
                 survey_path,
                 p1_questions='page_1_questions.json',
                 p2_questions='page_2_questions.json'
                 ):

        self.pages = pdf2image.convert_from_path(survey_path)
        with open(p1_questions) as p:
            self.page_1_questions = json.loads(p.read())

        with open(p2_questions) as p:
            self.page_2_questions = json.loads(p.read())

        self.update_originals(self.get_array(self.pages[114]), self.page_1_questions)
        self.update_originals(self.get_array(self.pages[115]), self.page_2_questions)
        print(self.get_answers(self.get_array(self.pages[116]), self.page_1_questions))
        print(self.get_answers(self.get_array(self.pages[117]), self.page_2_questions))

    @staticmethod
    def get_array(ppmImage):
        ppmImage.save('out.jpg', 'JPEG')
        return imageio.imread('out.jpg')

    @staticmethod
    def sum_darkness(array, position):
        return np.sum(array[position[0]: position[1], position[2]: position[3]])

    @staticmethod
    def return_image(array, spots):
        plt.figure()
        plt.imshow(array[spots[0]: spots[1], spots[2]: spots[3]])

    def compare_images(self, im_list, im1, im2, location):
        im = self.get_array(im_list[im1])
        self.return_image(im, location)
        im = self.get_array(im_list[im2])
        self.return_image(im, location)

    def update_originals(self, img_array, questions_dict):

        for question, answers in questions_dict.items():
            for answer, spot in answers.items():
                if answer == 'type':
                    continue
                questions_dict[question][answer].append(
                    self.sum_darkness(
                        img_array,
                        spot)
                )

    def get_answers(self, im_array, questions_dict):
        question_answers = {}
        flag = 'green'
        for question, answers in questions_dict.items():
            answer_choice = []
            answer_count = 0
            question_type = ''
            for answer, spot in answers.items():
                if answer == 'type':
                    question_type = spot
                    continue
                if question_type == 'single':
                    if self.sum_darkness(im_array, spot) < spot[4] * .98:
                        answer_count += 1
                    if question == 'quesion_11':
                        print(answer, self.sum_darkness(im_array, spot) < spot[4] * .98)
                    if len(answer_choice) > 0:
                        continue
                    if self.sum_darkness(im_array, spot) < spot[4] * .97:
                        answer_choice.append(answer)
                        continue
                    elif self.sum_darkness(im_array, spot) < spot[4] * .98:
                        answer_choice.append(answer)
                        continue
                    elif self.sum_darkness(im_array, spot) < spot[4] * .99:
                        answer_choice.append(answer)
                        continue
                    elif self.sum_darkness(im_array, spot) < spot[4] * .999:
                        answer_choice.append(answer)
                        continue
                if question_type == 'multi':
                    if self.sum_darkness(im_array, spot) < spot[4] * .98:
                        answer_choice.append(answer)
            if answer_count > 1:
                flag = 'red'
            question_answers[question] = (answer_choice, flag)
        return question_answers
