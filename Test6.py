class JobDescreption:
    def __init__(self, JobRole, MustHaveSkills, SecondarySkills, Descreption):
        self.JobRole = JobRole
        self.MustHaveSkills = MustHaveSkills
        self.SecondarySkills = SecondarySkills
        self.Descreption = Descreption


def CatagorizeByJdText(text):
    # print(text)
    Jd_Json_array = []
    Job_role_index = text.index('Job role:')
    Must_have_skill_index = text.index('Must have skills:')
    if 'Secondary skills:' in text:
        Secondary_skill_index = text.index('Secondary skills:')
    Job_description_index = text.index('Job description:')

    res1 = ''
    res2 = ''
    res3 = ''
    res4 = ''
    # getting elements in between
    for idx in range(Job_role_index + len('Job role:') + 1, Must_have_skill_index):
        res1 = res1 + text[idx]

    if 'Secondary skills:' in text:
        for idx in range(Must_have_skill_index + len('Must have skills:'), Secondary_skill_index):
            res2 = res2 + text[idx]

        for idx in range(Secondary_skill_index + len('Secondary skills:'), Job_description_index):
            res3 = res3 + text[idx]

        for idx in range(Job_description_index + len('Job description:'), len(text)):
            res4 = res4 + text[idx]

    else:
        for idx in range(Must_have_skill_index + len('Must have skills:'), Job_description_index):
            res2 = res2 + text[idx]

        res3 = "---"

        for idx in range(Job_description_index + len('Job description:'), len(text)):
            res4 = res4 + text[idx]
        # print("Job description: " + res4.strip() + "\n")
    JobData = JobDescreption(res1.strip(), res2.strip(),
                             res3.strip(), res4.strip())

    Jd_Json_array.append(JobData)
    print(Jd_Json_array[0].SecondarySkills)
    return Jd_Json_array[0]


def create_word_link(file_path):
    # Extract the file name from the file path
    file_name = file_path.split("/")[-1]
    return f"[{file_name}](file://{file_path})"
