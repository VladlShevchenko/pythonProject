from abc import ABC, abstractmethod
from finalLab.connector import DbConnector
from mysql.connector import Error

from finalLab.db_service import DbService


class ICourse(ABC):
    """Interface for course"""


@property
@abstractmethod
def name(self):
    """Abstract method for getting name of the course"""
    pass


@name.setter
@abstractmethod
def name(self, value):
    """Abstract method for setting name of the course"""
    pass


@property
@abstractmethod
def topics(self):
    """Abstract method for getting list of topics"""
    pass


@topics.setter
@abstractmethod
def topics(self, value):
    """Abstract method for setting name of the course"""
    pass


class ILocalCourse(ICourse, ABC):
    """Interface for local course"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        """toString method"""
        pass


class IOffsiteCourse(ICourse, ABC):
    """Interface for offsite course"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        """toString method"""
        pass


class ITeacher(ABC):
    """Interface for teacher"""

    @property
    @abstractmethod
    def name(self):
        """Abstract method for getting name of teacher"""
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        """Abstract method for setting name of teacher"""
        pass

    @property
    @abstractmethod
    def courses(self):
        """Abstract method for getting list of teacher's courses"""
        pass

    @courses.setter
    @abstractmethod
    def courses(self, value):
        """Abstract method for setting list of teacher's courses"""
        pass


class ICourseFactory:
    """Interface for course factory"""

    @abstractmethod
    def create_teacher(self, teacher_id, teacher_name, courses_list):
        """A function that returns new Teacher object"""
        pass

    @abstractmethod
    def create_course(self, course_name, topics_list, course_type):
        """A function that returns new Course object"""
        pass


class Course(ICourse):
    """Basic course class"""

    def __init__(self, name, topics):
        self.name = name
        # self.teacher = teacher
        self.topics = topics

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name should be string")
        if len(value) <= 1:
            raise ValueError("Name must be longer than 2 symbols")
        self.__name = value

    @property
    def topics(self):
        return self.__topics

    @topics.setter
    def topics(self, value):
        if not all([isinstance(v, str) for v in value]):
            raise TypeError("Topic must be string")
        self.__topics = value

    def __str__(self):
        return f'{self.name} {self.topics}'


class LocalCourse(Course, ILocalCourse):
    """LocalCourse class with overwrited method"""

    def __init__(self, name, topics):
        super().__init__(name, topics)

    def __str__(self):
        return f"Local course {self.name}, topics: {self.topics}"


class OffsiteCourse(Course, IOffsiteCourse):
    """OffsiteCourse class with overwrited method"""

    def __init__(self, name, topics):
        super().__init__(name, topics)

    def __str__(self):
        return f"Offsite course {self.name}, topics: {self.topics}"


class Teacher(ITeacher):
    """Class for creating teacher instance"""

    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be string")
        if len(value) <= 1:
            raise ValueError("Name must be longer than 2 symbols")
        self.__name = value

    @property
    def courses(self):
        return self.__courses

    @courses.setter
    def courses(self, value):
        if not all([isinstance(program, (LocalCourse, OffsiteCourse)) for program in value]):
            raise TypeError("Wrong type of course")
        self.__courses = value

    def __str__(self):
        return f"Teacher {self.name}, courses: {self.courses}"


class CourseFactory(ICourseFactory):
    """CourseFactory class
     Which helps to create instance and save in database new teachers and new courses"""

    def create_teacher(self, teacher_id, teacher_name, courses_list):
        """Function return new Teacher object and save it in database"""
        try:
            connection = DbConnector.getConnection()
            DbService.add_teacher(connection, teacher_id, teacher_name)
            for course in courses_list:
                DbService.add_teacher_to_course(connection, teacher_id, course.name)
            return Teacher(teacher_name, courses_list)
        except Error as e:
            print(e)

        finally:
            connection.close()

    def create_course(self, name_course, topics_list, course_type):
        """Function return new Course object and save it in database"""
        try:
            connection = DbConnector.getConnection()
            if course_type == "LocalCourse":
                course = LocalCourse(name_course, topics_list)
            elif course_type == "OffsiteCourse":
                course = OffsiteCourse(name_course, topics_list)
            else:
                raise TypeError("Wrong course type")
            DbService.add_course(connection, name_course, course_type)
            for topic in topics_list:
                DbService.add_topic_to_course(connection, topic, name_course)
            return course
        except Error as e:
            print(e)

        finally:
            connection.close()

    @staticmethod
    def get_teacher_with_courses():
        """Function return teacher and related to them courses"""
        try:
            connection = DbConnector.getConnection()
            DbService.get_courses_with_teacher(connection)
        except Error as e:
            print(e)

        finally:
            connection.close()

    @staticmethod
    def get_courses_with_topics():
        """Function return courses and related to them topics"""

        try:
            connection = DbConnector.getConnection()
            DbService.get_courses_with_topics(connection)
        except Error as e:
            print(e)

        finally:
            connection.close()


if __name__ == '__main__':
    courseFactory = CourseFactory()
    course1 = courseFactory.create_course("C++", ["OOP", "SOLID", "Threads"], "LocalCourse")
    course2 = courseFactory.create_course("Kotlin", ["Android", "Mobile"], "OffsiteCourse")
    print(course1)
    teacher1 = courseFactory.create_teacher(8, "Tom Holland", [course1])
    print(teacher1)

    courseFactory.get_teacher_with_courses()
    courseFactory.get_courses_with_topics()
