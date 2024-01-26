import io
import os
import random
import logging

logger = logging.getLogger()


def read_students():
    with io.open("../students.txt", encoding='utf-8') as file:
        result = file.readlines()
    return result


def generate_variant(counts):
    return tuple(random.randint(1, count) for count in counts)


def read_file(name):
    with io.open(name, encoding='utf-8') as file:
        text = file.read()
    return text


def make_tex_file(file_name, content):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with io.open(file_name, "w", encoding='utf-8') as out:
        out.write(content)


def read_tasks():
    result = []
    total_tasks = len(os.listdir('../hw/tasks'))
    logger.info(total_tasks + 1)
    for i in range(1, total_tasks):
        result.append([])
        total_variants = len(os.listdir('../hw/tasks/%d' % i))
        for k in range(1, total_variants):
            result[i - 1].append(read_file('../hw/tasks/%d/%d.tex' % (i, k)))
    return result


class VariantGenerator:
    def __init__(self):
        self.random_seed = 1183
        random.seed(self.random_seed)
        self.head = read_file('../templates/head.tex')
        self.q_start = read_file('../templates/qStart.tex')
        self.q_start2 = read_file('../templates/qStart2.tex')
        self.q_finish = read_file('../templates/qFinish.tex')
        self.tail = read_file('../templates/tail.tex')

        self.tasks = read_tasks()
        self.students = read_students()

    def generate_variants(self, total):
        counts = [len(i) for i in self.tasks]
        result = set()
        while len(result) < total:
            result.add(generate_variant(counts))
        return list(result)

    def make_main_tex_file(self):
        logger.info("Making main.tex file...")
        variants = self.generate_variants(len(self.students))
        random.shuffle(variants)

        main_content = self.head
        for i in range(len(variants)):
            main_content += self.q_start + str(self.students[i]) + self.q_start2
            for task_number, task in enumerate(self.tasks):
                main_content += task[variants[i][task_number] - 1]
            main_content += self.q_finish
        main_content += self.tail

        make_tex_file("../hw/latex/main.tex", main_content)

    def make_dump_tex_file(self):
        logger.info("Making dump.tex file...")

        dump_content = self.head
        for i in range(len(self.tasks)):
            dump_content += self.q_start + str(i + 1) + self.q_start2
            for k in range(len(self.tasks[i])):
                dump_content += self.tasks[i][k]
            dump_content += self.q_finish

        dump_content += self.tail
        make_tex_file("../hw/latex/dump.tex", dump_content)

    def run(self):
        self.make_main_tex_file()
        self.make_dump_tex_file()
        logger.info("Done!")


if __name__ == "__main__":
    latex_generator = VariantGenerator()
    latex_generator.run()
