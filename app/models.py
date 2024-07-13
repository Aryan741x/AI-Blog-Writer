import mindsdb_sdk
import os

def create_models():
    server = mindsdb_sdk.connect()
    project = server.get_project("ai_blog_bot")

    try:
        server.ml_engines.create(
            name="minds_endpoint_engine",
            type="minds_endpoint",
            connection_data={"minds_endpoint_api_key": os.getenv("API_KEY")}
        )
    except Exception as e:
        print(f"ML Engine creation failed: {e}")

    try:
        project = server.create_project("ai_blog_bot")
    except Exception as e:
        project = server.get_project("ai_blog_bot")

    try:
        project.models.create(
            name="blog_generator_title",
            predict="blog_content",
            engine="minds_endpoint_engine",
            max_tokens=152,
            prompt_template="Write a Blog Post Title about {{topic}} in about 50 words."
        )
    except Exception as e:
        print(f"Model creation failed: {e}")

    try:
        project.models.create(
            name="blog_generator_intro",
            predict="blog_introduction",
            engine="minds_endpoint_engine",
            max_tokens=500,
            prompt_template="Write only the intro part for my blogpost regarding the topic {{topic}}.Do not generate the whole blog post, just the introduction part of it. The introduction should be around 50 words.Do not Write Introduction word in it."
        )
    except Exception as e:
        print(f"Model creation failed: {e}")

    try:
        project.models.create(
            name="blog_generator_body",
            predict="blog_body",
            engine="minds_endpoint_engine",
            max_tokens=2048,
            prompt_template="Write the Body of the Blog Post about {{topic}} and the body should be 300 words.Do it in a way that it should be a continuation of the introduction. Do not Write Body word in it.Also give in paragraph format.Dont include the conclusion part in it."
        )
    except Exception as e:
        print(f"Model creation failed: {e}")

    try:
        project.models.create(
            name="blog_generator_conclusion",
            predict="blog_conclusion",
            engine="minds_endpoint_engine",
            max_tokens=152,
            prompt_template="Write a Blog Post Conclusion about {{topic}}.Do not generate other parts of the blog post, just the conclusion part of it. The conclusion should be around 50 words. Do not Write Conclusion word in it."
        )
    except Exception as e:
        print(f"Model creation failed: {e}")

    return project