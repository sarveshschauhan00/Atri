import json


d = {
    "pali_learning_website/app.py": ["pali_learning_website/config.py", "pali_learning_website/requirements.txt", "pali_learning_website/modules/__init__.py", "pali_learning_website/modules/lessons.py", "pali_learning_website/modules/exercises.py", "pali_learning_website/modules/users.py", "pali_learning_website/modules/forum.py", "pali_learning_website/modules/utils.py"],
    "pali_learning_website/config.py": [],
    "pali_learning_website/requirements.txt": [],
    "pali_learning_website/static/css/styles.css": [],
    "pali_learning_website/static/js/main.js": [],
    "pali_learning_website/templates/base.html": ["pali_learning_website/static/css/styles.css", "pali_learning_website/static/js/main.js", "pali_learning_website/static/images/logo.png"],
    "pali_learning_website/templates/home.html": ["pali_learning_website/templates/base.html"],
    "pali_learning_website/templates/lessons/lesson_list.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/lessons.py"],
    "pali_learning_website/templates/lessons/lesson_detail.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/lessons.py"],
    "pali_learning_website/templates/exercises/exercise_list.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/exercises.py"],
    "pali_learning_website/templates/exercises/exercise_detail.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/exercises.py"],
    "pali_learning_website/templates/resources.html": ["pali_learning_website/templates/base.html"],
    "pali_learning_website/templates/forum/forum_home.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/forum.py"],
    "pali_learning_website/templates/forum/thread.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/forum.py"],
    "pali_learning_website/templates/account/login.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/users.py"],
    "pali_learning_website/templates/account/register.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/users.py"],
    "pali_learning_website/templates/account/profile.html": ["pali_learning_website/templates/base.html", "pali_learning_website/modules/users.py"],
    "pali_learning_website/templates/error.html": ["pali_learning_website/templates/base.html"],
    "pali_learning_website/modules/lessons.py": ["pali_learning_website/data/lessons/lesson_1.csv", "pali_learning_website/data/lessons/lesson_2.csv"],
    "pali_learning_website/modules/exercises.py": ["pali_learning_website/data/exercises/exercise_1.csv", "pali_learning_website/data/exercises/exercise_2.csv"],
    "pali_learning_website/modules/users.py": ["pali_learning_website/data/users.csv"],
    "pali_learning_website/modules/forum.py": ["pali_learning_website/data/forum_posts.csv"],
    "pali_learning_website/modules/utils.py": []
}


print(json.dumps(d, indent=4))

