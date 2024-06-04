# Student and class implementation

class Index:
    def __init__(self, index:int):
        self.index=index

    def __int__(self)->int:
        return self.index
    
    def __repr__(self)->str:
        if self.index==0:
            return "None"
        else:
            return str(self.index)

class Student:
    def __init__(self, name: str, grade: int):
        self.name=name
        self.grade=grade

class Class:
    def __init__(self, num: int):
        self.num=num
        self.students=[]
    
    def add_student(self,student: Student)->Index:
        self.students.append(student)
        return Index(len(self.students))
    
    def get_student(self,index: Index)->Student|None:
        if int(index) > len(self.students) or int(index) < 1: 
            return None
        return self.students[int(index)-1]
    
    # find student by name and return the index
    # return 0 if no student
    def find_student_by_name(self, to_search:str)->Index:
        for (index,student) in enumerate(self.students):
            if student.name == to_search :
                return Index(int(index)+1)
        return Index(0)
    
    def has_uniform_grade(self)->bool:
        if len(self.students)>0:
            for student in self.students:
                if student.grade!=self.students[0].grade:
                    return False
            return True
        else:
            return True

