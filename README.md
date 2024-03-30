
# Example Docker OpenCV Alpine Image

The Example Docker OpenCV Alpine Image API is a simple Python project using Flask to create an API that allows users to upload images and retrieve size information about these images.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See the *Installation* section for notes on how to deploy the project on a live system.

### Prerequisites

Before you begin, ensure you have Python and pip installed on your system. This project is written with Python 3.x.

### Installing

To install and run this project locally, follow these steps:

#### Clone the repository

```bash
git clone https://github.com/tuanha1305/example-opencv-docker-alpine.git
cd example-opencv-docker-alpine
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Run the application

```bash
python app.py
```

This will start the Flask server on `localhost` on the default port `5001`. You can access the API at `http://localhost:5001`.

## Using the API

### Upload an Image

- **URL**: `/api/v1/size`
- **Method**: `POST`
- **Body**: FormData with the image file included.
- **Response**: JSON containing image dimensions and size.

### Example Response

```json
{
    "success": true,
    "data": {
        "width": 1024,
        "height": 768,
        "size_bytes": 123456
    },
    "message": "Successfully uploaded."
}
```

Example curl

```bash
curl --location 'http://127.0.0.1:5001/api/v1/size' \
--form 'file=@"/b7ecdbb8-f020-4a19-afd0-2afe589fc8ef.png"'
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please refer to the **CONTRIBUTING.md** for more information.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Flask for the amazing simplicity in building web applications.
- Pillow for handling image files.
- OpenCV for more advanced image processing capabilities.

