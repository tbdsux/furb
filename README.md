# furb
Simple Grabber and Downloader of Manga, Manhua, Manhwa

#### NOTE:
- **All download links generated are automatically cached or stored in a defined Database in order to avoid multiple similar files being uploaded to the file hosting site.**

## Frameworks Used
- [**FastApi**](https://github.com/tiangolo/fastapi) - Main Backend Framework
- [**TailwindCSS**](https://tailwindcss.com/) - HTML Design

### Used Service
- [**magna**](https://github.com/TheBoringDude/magna) - my simple scraper API

## Development
1. **Clone the repo**
```
git clone https://github.com/TheBoringDude/furb.git
```

2. **Install Required Dependencies**
```
pip install -r requirements.txt
npm install
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

3. **Running locally**

- Building development TailwindCSS
```
npm run devel
```

- Starting the app. You can also run `npm run start` to execute the similar command.
```
uvicorn main:app --reload
```

- Running with Live-Reload (Commonly used during design development.)
```
npm run dev
```


### Some words:
- I haven't tried hosting / uploading this on a serverless. This uses `Pillow` and `img2pdf` for downloading and compiling the images to pdf and they consume too much ram so, I don't think it would work.
- You can setup this on your own Heroku account. There might be issues and problems, my dyno might be overloaded, if I will share mine :).


#### Credits:
:heart: TheBoringDude

<a href="https://www.buymeacoffee.com/theboringdude" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="175" ></a>