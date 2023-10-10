
# Web Service for Audio Transcription in Docker Container
 
This project is a web service packaged in a Docker container that simplifies the transcription of WAV audio files. It offers a user-friendly API endpoint that allows users to upload one or more WAV files for transcription.

## Docker installation

To build the Docker file on macOS, ensure that you change the credsStore configuration in $HOME/.docker/config.json from "desktop" to "osxkeychain." This adjustment is necessary for building the Docker image on your macOS system.

```
$HOME/.docker/config.json

{
	"auths": {},
	"credsStore": "osxkeychain",
	"currentContext": "desktop-linux",
	"plugins": {
		"-x-cli-hints": {
			"enabled": "true"
		}
	}
}
```

Building the docker image

```sudo docker build -t whisper-api-img . ```    

Running docker

```docker run -p 8000:8000 whisper-api-im```

## Running locally

Install ffmpeg

```
./venv/bin/pip3 install "git+https://github.com/openai/whisper.git
./venv/bin/uvicorn fast_api:app --host "0.0.0.0" --port "8000"
```
