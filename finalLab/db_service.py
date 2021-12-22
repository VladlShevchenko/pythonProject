class DbService:
    """Class which contains basic methods to work with database"""

    @staticmethod
    def get_teachers(db_connection):
        """Method return all teachers"""

        sql = "SELECT * FROM teacher"
        cursor = db_connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    @staticmethod
    def add_teacher(db_connection, teacher_id, name):
        """Method insert teacher in database"""

        sql = "SELECT * FROM teacher WHERE id = %s OR name = %s"
        sql_insert = "INSERT INTO teacher (id, name) VALUES (%s, %s)"
        values = (teacher_id, name)

        cursor = db_connection.cursor()
        cursor.execute(sql, values)
        data = cursor.fetchall()
        if not len(data):
            cursor.execute(sql_insert, values)
            db_connection.commit()
        else:
            raise ValueError("This name or id already exists")

    @staticmethod
    def add_course(db_connection, course_name, course_type):
        """Method insert course in database"""

        sql = "SELECT * FROM course WHERE name = %s"
        sql_insert = "INSERT INTO course (name, courseType) VALUES (%s, %s)"
        values = (course_name, course_type)

        cursor = db_connection.cursor()
        cursor.execute(sql, (course_name,))
        data = cursor.fetchall()
        if not len(data):
            print('There is no component named %s' % course_name)  # delete later
            cursor.execute(sql_insert, values)
            db_connection.commit()
        else:
            raise ValueError("This name or id already exists")

    @staticmethod
    def get_courses(db_connection):
        """Method return all courses"""

        sql = "SELECT * FROM course"

        cursor = db_connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    @staticmethod
    def add_teacher_to_course(db_connection, teacher_id, course_name):
        """Method which assign teacher to course in database"""

        sql = "SELECT * FROM teacher WHERE id = %s"
        sql_check = "SELECT * FROM course WHERE name = %s"
        sql_insert = "INSERT INTO teacher_has_course (teacher_id, course_name) VALUES (%s, %s)"
        values = (teacher_id, course_name)

        cursor = db_connection.cursor()
        cursor.execute(sql, (teacher_id,))
        data_teacher = cursor.fetchall()
        cursor.execute(sql_check, (course_name,))
        data_course = cursor.fetchall()
        if not len(data_teacher):
            raise ValueError("This teacher doesn't exist")
        elif not len(data_course):
            raise ValueError("This course doesn't exist")
        else:
            cursor.execute(sql_insert, values)
            db_connection.commit()

    @staticmethod
    def get_courses_with_teacher(db_connection):
        """Method returns teacher with assigned to him courses"""

        sql = "SELECT teacher.*, GROUP_CONCAT(teacher_has_course.course_name) AS course_name FROM teacher, " \
              "teacher_has_course where teacher.id=teacher_has_course.teacher_id GROUP BY teacher.id,teacher.name; "

        cursor = db_connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    @staticmethod
    def get_courses_with_topics(db_connection):
        """Method returns course with assigned to it courses"""

        sql = "SELECT course.*, GROUP_CONCAT(course_has_topic.topic_name) AS topic_name FROM course,  " \
              "course_has_topic where course.name=course_has_topic.course_name  GROUP BY course.name; "

        cursor = db_connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    @staticmethod
    def add_topic(db_connection, topic_name):
        """Method which insert new topic in database"""

        sql = "SELECT * FROM topic WHERE name = %s"
        sql_insert = "INSERT INTO topic (name) VALUES (%s)"

        cursor = db_connection.cursor()
        cursor.execute(sql, (topic_name,))
        data = cursor.fetchall()
        if not len(data):
            print('There is no component named %s' % topic_name)  # delete later
            cursor.execute(sql_insert, (topic_name,))
            db_connection.commit()
        else:
            raise ValueError("This name already exists")

    @staticmethod
    def add_topic_to_course(db_connection, topic_name, course_name):
        """Method which assign topic to course in database"""

        sql = "SELECT * FROM topic WHERE name = %s"
        sql_check = "SELECT * FROM course WHERE name = %s"
        sql_insert = "INSERT INTO course_has_topic (course_name, topic_name) VALUES (%s, %s)"
        values = (course_name, topic_name)

        cursor = db_connection.cursor()
        cursor.execute(sql, (topic_name,))
        data_topic = cursor.fetchall()
        cursor.execute(sql_check, (course_name,))
        data_course = cursor.fetchall()
        if not len(data_topic):
            raise ValueError("This topic doesn't exist")
        elif not len(data_course):
            raise ValueError("This course doesn't exist")
        else:
            cursor.execute(sql_insert, values)
            db_connection.commit()
