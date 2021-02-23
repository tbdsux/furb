# furb
Simple Grabber and Downloader of Manga, Manhua, Manhwa

#### NOTE:
- **All download links generated are automatically cached or stored in a defined Database in order to avoid multiple similar files being uploaded to the file hosting site.**

## Frameworks Used
- [**FastApi**](https://github.com/tiangolo/fastapi) - Main Backend Framework
- [**TailwindCSS**](https://tailwindcss.com/) - HTML Design
- [**VueJS3**](vuejs.org/) - Front-end framework

### Used Service
- [**magna**](https://github.com/TheBoringDude/magna) - my simple scraper API

## File Hosting sites:
- **AnonFiles** => https://anonfiles.com
- **BayFiles** => https://bayfiles.com

## Development
1. **Clone the repo**
```
git clone https://github.com/TheBoringDude/furb.git
```

2. **Install Required Dependencies**
```
pip install -r requirements.txt
yarn install
```

**Set virtual environment**
- Linux / Unix
```
source venv/bin/activate
```
- Windows
```
venv\Scripts\activate
```

1. **Running locally**
- Starting the app. You can also run `npm run start` to execute the similar command.
```
uvicorn main:app --reload
```

- Running the frontend
```
yarn dev
```


### Some words:
- This will not work on a `serverless` platform.
- It is better for this service to be hosted on a **dedicated VPS** with atleast a **1GB** of ram of a possibility of `async-download` support.
- You are free to configure this for your own convenience.


### &copy; TheBoringDude

<a href="https://www.buymeacoffee.com/theboringdude" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="175" ></a>