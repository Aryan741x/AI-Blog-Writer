# AI-Blog Writer: Revolutionizing Content Creation

Welcome to AI-Blog Writer, your intelligent assistant for generating high-quality blog posts. This application leverages the power of MindsDB to generate content based on the topics you provide, making it easier and faster to create engaging blog posts.Also you can Download the Blog Post for FREE.

## Features

- **Intelligent Content Creation**: Uses MindsDB to generate relevant and engaging blog content based on your input.
- **Image Generation**: Leverages Replicate to create stunning images that match your content.
- **User-Friendly Interface**: Built with Flask, providing a simple and intuitive user experience.
- **Pdf Generation**:Download Blog Post in pdf format.

- **User-Friendly Interface**: Simple and intuitive web interface.

## Technology Stack

AI-Blog Writer is built using a combination of cutting-edge technologies and tools:

### Backend
- **[Flask](https://flask.palletsprojects.com/)**: A lightweight WSGI web application framework in Python used to build the web application.
- **[MindsDB](https://mindsdb.com/)**: An open-source AI layer for existing databases that allows for easy implementation of machine learning models, used here for generating blog content.
- **[Replicate](https://replicate.com/)**: A platform for running machine learning models in the cloud, used to generate images for the blog posts.

### Frontend
- **HTML/CSS**: For structuring and styling the web pages.
- **JavaScript**: For interactivity and dynamic content updates.

### Deployment
- **Docker**: Containerization technology used to package the application and its dependencies for consistent and efficient deployment.

### Other Tools
- **[dotenv](https://pypi.org/project/python-dotenv/)**: A Python library for loading environment variables from a `.env` file, used to manage API keys and other sensitive information.
- **[requests](https://docs.python-requests.org/en/latest/)**: A simple HTTP library for Python, used to make requests to external APIs.


## Getting Started

### Prerequisites

- Node.js and npm installed.
- Docker for creating containers.
- Git to pull the forked repo.
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone the Repository**

```bash
git init
git clone https://github.com/Aryan741x/AI-Blog-Writer.git
cd AI-Blog-Writer
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup .env**
- Go to .env file present inside the source directory.
- Put your MindsDB API_KEY as [API_KEY](https://mdb.ai/models) and replicate's API_KEY as [REPLICATE_API_KEY](https://replicate.com/account/api-tokens)
- Login through the links and obtain your Api key. 
```bash
API_KEY=""
REPLICATE_API_KEY=""
```
4. **Create Docker Image**
```bash
docker run --name mindsdb_container -p 47334:47334 -p 47335:47335 mindsdb/mindsdb

```
### Running the Application



5. **Run Docker**(It might take some time to setup even after started.)
```bash
docker start mindsdb_container
```

6. **Run Flask Server(port:5000)**
```bash
python main.py
```
7. **View the Project at**
```bash
https://localhost:5000
```


## Demo Video

[![Watch the video](https://img.youtube.com/vi/Ait5Sz0Zf9E/maxresdefault.jpg)](https://youtu.be/Ait5Sz0Zf9E)


## Acknowledgments

- Special Thanks to SSOC: Grateful for providing a platform to delve deeper into the fascinating world of AI and machine learning.
- Gratitude to the developers and community behind MindsDB for their invaluable resources and support. Thank you also for providing the opportunity to take part in Quine Quest 14.

---

Feel free to dive into the project, explore the code. Happy coding!
