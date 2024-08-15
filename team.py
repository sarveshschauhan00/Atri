from utils import gpt_bot, quick_bot, content_extractor


codetype_names = {
    'html': 'html\n',
    'css': 'css\n',
    'js': 'javascript\n',
    'py': 'python\n',
    'vue': 'vue\n',
    'csv': 'csv\n',
    'json': 'json\n',
    'txt': 'plaintext\n'
}

def product_manager(content):
    """Initiates the Project: The Product Manager starts by defining the vision and goals of the project.
    They conduct market research, gather user requirements, and prioritize features. This sets the foundation for the project."""

    system_prompt = """You are a product manager, Your job is to understand the user requirements and project he wants to create and assume all the information needed

You have to describe all functionalities, features in detail"""
    product_details = gpt_bot(system_prompt, content)
    product_details = product_details.replace("*", "")
    product_details = product_details.replace("#", "")
    return product_details

def developer():
    system_prompt = "You are a professional python developer, you are given a a project description, your job is to "
    pass

def tester():
    """Tests the Software: The QA Engineer conducts various tests (unit, integration, system, and user acceptance testing) 
    to identify bugs and ensure the software meets the required quality standards. 
    They work closely with developers to address any issues that arise."""
    pass

def judge()
    pass