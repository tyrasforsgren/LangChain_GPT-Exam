"""
Course Generator Module

This module provides functionality to generate marketing content 
and course outlines using the LangChain and OpenAI API.

Functions/Classes:
    - generate_output: Generates output for the chat using 
    ChatOpenAI model.
    - CourseGenerator: Class providing static methods to 
    generate titles, marketing text, and course outlines.

Example
-------
from course_generator import CourseGenerator

# Set API key from environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Generate marketing content
description = "A course that teaches juniors how to code python"
marketing_aid = CourseGenerator()
print(marketing_aid.generate_titles(description))
print(marketing_aid.generate_marketing_text(description))
print(marketing_aid.generate_course_outline(description, course_difficulty='beginner'))
print(marketing_aid.generate_coding_exercises("Pandas module"))
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

# Get secret API key from hidden .env file
load_dotenv()
API_KEY = os.getenv('API_KEY') # change key in .env file


def generate_output(system_template:str, product_description:str, max_tokens=1000) -> str:
    """
    Generate output content for the chat using the ChatOpenAI model.

    Parameters
    ----------
    system_template : str
        The system template for generating content.
    product_description : str
        The product description.
    max_tokens : int, optional
        The maximum number of tokens / characters for the output.
        Default : 1000

    Returns
    -------
    str
        Generated content.

    Notes
    -----
    This function uses the ChatOpenAI model to generate content based on the provided system template
    and product description. The model aims to adhere to the max_tokens limit, but it may not always
    generate responses exactly at that length. Lower limits may result in truncated responses. Default
    is set to 1000, and maximum limits below this are not reccomended in most cases. Note that tokens
    should adhere to the complexity of the prompt. 

    The system template is augmented with detailed information about the number of tokens and the provided prompt
    to assist in generating the content effectively.
    
    This function is the basis of all methods in the CourseGeneration.CourseGenerator class.
    """
    # Augment system template with additional information (detailed for reliable output)
    augmented_system_template = f"Before generating your text, understand the following steps : \
        1. This is the maximum limit of characters for you to write with : {max_tokens} \
        2. You should generate a complete text WITHOUT overstepping this limit. \
        3. Be prepared to write short, consise texts as your max limit can be lower than default. \
        4. End the generated text with : '- Your Friendly Generator.' \
        5. To the best of your ability, take spelling errors into considerations in all prompts. \
        This is the template for you to generate a texts of of : {system_template}"

    # Initialize the model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=API_KEY,
                     temperature=1,
                     max_tokens=max_tokens)

    # Create human prompt with the proper template
    human_template = "{product_description_temp}"
    human_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Translate the prompt
    chat_prompt = ChatPromptTemplate.from_messages([
        augmented_system_template,
        human_prompt])
    final_prompt = chat_prompt.format_prompt(
        product_description_temp=product_description)

    # Generate content
    result = llm.invoke(final_prompt)
    return result.content


class CourseGenerator:
    """
    Class providing static methods to generate marketing content
    and course outlines. It's purpose is to structure the module.
    Methods are all based of of global function
    generated_output."""

    @staticmethod
    def generate_titles(description:str, max_tokens=1000) -> str:
        """
        Generate creative persuasive titles for a product.

        Parameters
        ----------
        description : str
            Description of the product.
        max_tokens : int, optional
            The maximum number of tokens for the output.

        Returns
        -------
        str
            Generated titles.
        """
        system_template = "You are a marketing expert and will generate creative persuasive \
                        titles for a product. Come up with several options."
        return generate_output(system_template, description, max_tokens)

    @staticmethod
    def generate_marketing_text(description:str, max_tokens=1000) -> str:
        """
        Generate creative persuasive marketing text about a product.

        Parameters
        ----------
        description : str
            Description of the product.
        max_tokens : int, optional
            The maximum number of tokens for the output.

        Returns
        -------
        str
            Generated marketing text.
        """
        system_template = "You are a marketing expert and will generate creative persuasive \
                        marketing about a product."
        return generate_output(system_template, description, max_tokens)

    @staticmethod
    def generate_course_outline(description:str, course_difficulty='Intermediate', max_tokens=1000) -> str:
        """
        Generate a course plan/outline for students at any level.

        Parameters
        ----------
        description : str
            Description of the course.
        course_difficulty : str, optional
            The difficulty level of the course.
        max_tokens : int, optional
            The maximum number of tokens for the output.

        Returns
        -------
        str
            Generated course outline.

        Raises
        ------
        ValueError
            If the course_difficulty is not one of the specified choices.
        """
        # Create a detailed / clear template rather than a simple one for a reliable response.
        difficulty_template = f"Follow the steps to choose a difficulty : \
                        1. Try to translate the given difficulty parameter into a course difficulty. \
                            Difficulty parameter : {course_difficulty} \
                        2. If the difficulty parameter does not make sense / is not related to difficulty, \
                            default the difficulty to 'Intermediate'. \
                        3. Mention difficulty in your response."
        system_template = f"You are a teacher in the following subjects: IT, cloud solutions, \
                        system architecture, ML and AI. You will generate a course \
                        plan/outline, taking into account the difficulty level. \
                        Difficulty information : {difficulty_template}"
        return generate_output(system_template, description, max_tokens)


    @staticmethod
    def generate_coding_exercises(subject:str, difficulty=None, max_tokens=1000) -> str:
        """
        Generate coding exercises for the given subject.

        Parameters
        ----------
        subject : str
            The subject for which coding exercises are to be generated.
        difficulty : str, optional
            The difficulty level of the coding exercises.
        max_tokens : int, optional
            The maximum number of tokens for the output.

        Returns
        -------
        str
            Generated coding exercises.
        """
        
        difficulty_template = f"Follow the steps to choose a difficulty : \
                        1. Try to translate the given difficulty parameter into an exersize difficulty. \
                            Difficulty parameter : {difficulty} \
                        2. If the difficulty parameter does not make sense / is not related to difficulty, \
                            default the difficulty to 'Intermediate'. \
                        3. Mention difficulty in your response."
        system_template = f"You are a teacher in programming in Python. Generate a coding exercise for \
                        the given subject. If a difficulty is given, match that in the complexity of \
                        the problem. \
                        Difficulty information : {difficulty_template}"
        return generate_output(system_template, subject, max_tokens)
