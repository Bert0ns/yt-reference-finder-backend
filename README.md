# Youtube Reference Finder - Backend

<hr/>

This project is a Flask application that serves as the backend for "Youtube Reference Finder". 
The application extracts keywords from a provided text (via PDF/image file upload or direct text input), 
generates search queries based on these keywords using a local language model (Ollama), 
and searches for relevant educational videos on YouTube. 
The found videos are then ranked and returned to the user.

## Configuration

<hr/>

### Environment Variables
The application uses several environment variables for configuration:

- `YOUTUBE_API_KEY`: Your YouTube API key to access the YouTube Data API.
- `OLLAMA_MODEL`: The name of the Ollama model to use (e.g., gemma3:4b).
- `OLLAMA_API_URL`: The URL of the running Ollama instance (e.g., `http://ollama:11434` when using Docker, `http://localhost:11434` for local execution).
- `PRODUCTION_ENVIROMENT`: Set to `"True"` for the production environment, otherwise `"False"`. Controls Flask's debug mode and potentially other environment-specific settings.

An example `.env` file is provided for local configuration. 
When using Docker, these variables are passed through the `docker-compose.yml` file.

## Running the Application

<hr/>

### Via Docker (Recommended)
The recommended method for running the application is via Docker Compose, 
which will manage both the Flask application and the Ollama service.

1. **Build and Start Containers:**
    `docker-compose up -d --build`
    This command will build the images (if not already built) and start the containers in detached mode. 
    The Ollama service will automatically download the model specified in OLLAMA_MODEL.

The Flask application will be accessible at `http://localhost:5000` and the Ollama service at `http://localhost:11434`.

### Locally (Without Docker)


1. Ensure all dependencies are installed:
    The project dependencies are listed in the `requirements.txt` file. 
    They can be installed using pip:
    ```bash
    pip install -r requirements.txt
    ```

2. Ensure an Ollama instance is running and accessible at the URL specified in OLLAMA_API_URL 
(typically [http://localhost:11434]()). 
You will need to manually download the desired Ollama model (e.g., `ollama pull gemma3:4b`).
3. Set the necessary environment variables (e.g., by creating a `.env` file or exporting them in your shell).
4. Run the `app.py` script:
    ```bash
    python app.py
    ```
5. The application will be accessible at [http://localhost:5000]().

## API Endpoints

<hr/>

`GET /`

`GET /about`

Returns a simple JSON message describing the API.
* Example response:
    ```json
    {
        "about": "This is a simple API to extract keywords from a text and search YouTube videos based on them."
    }
    ```

`POST /process`

Processes the provided text (from a file or direct input), extracts keywords, 
generates search queries, and returns relevant YouTube videos.

* Request: The request must be of type `multipart/form-data` if uploading a file, or `application/x-www-form-urlencoded` if sending direct text.
    * `file`: (Optional) A file from which to extract text. Supported formats are `.pdf`, `.jpg`, `.jpeg`, `.png`.
    * `text`: (Optional if file is provided) A text string to process.
* Success Response (Code 200): A JSON object containing the extracted keywords, generated queries, and a list of ranked videos.

* Example response:
    ```json lines
    {
    "keywords": ["keyword 1", "keyword 2", ...],
    "queries": ["search query 1", "search query 2", ...],
    "videos": [
        {
            "title": "Video Title 1",
            "description": "Video Description 1",
            "thumbnail": "thumbnail_url_1",
            "video_id": "video_id_1",
            "url": "youtube_video_url_1",
            "channel_id": "channel_id_1",
            "channel_subscribers": 150000,
            "like_count": 12000,
            "view_count": 500000,
            "engagement_score": 0.85,
            "relevance_score": 0.0 // Note: relevance_score is initialized to 0.0 and does not seem to be actively calculated in the provided code.
        },
        ...
      ]
    }
    ```
The `videos` list is limited to the top 10 ranked results.

## Main Features

<hr/>

1. Text Extraction: From PDF files, images (JPG, PNG), or direct text input.
2. Keyword Extraction: Uses Rake-NLTK to identify the most relevant phrases and keywords from the text.
3. Query Generation: Uses a language model (via Ollama) to generate optimized YouTube search queries from keywords.
4. YouTube Video Search: Searches for videos on YouTube using the generated queries, filtering by relevance, category (Education), available captions, channel subscriber count, likes, and language.
5. Video Ranking: Videos are ranked based on an engagement score (likes/views) and normalized.
6. Logging: YouTube API responses are logged in the youtube_responses.log file.

## Useful commands

<hr/>

Installing dependencies:
`pip install -r requirements.txt`

Updating dependency list in `requirements.txt`:
`pip freeze > requirements.txt`

Build and start the docker image:
```bash
docker-compose up -d --build
```

Build the Docker image:
```bash
docker-compose build
```

Start docker container:
```bash
docker-compose up -d
```