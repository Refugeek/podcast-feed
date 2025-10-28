# Podcast Feed Generator

This repository automatically generates RSS feeds for podcasts stored in subfolders.

## Structure

- `episodes-{podcast-name}/`: Subfolder for each podcast.
  - `config.json`: Podcast metadata.
  - Audio files (e.g., .mp3).
  - `feed.xml`: Auto-generated RSS feed.

## Adding a New Podcast

1. Create a new subfolder `episodes-{name}`.
2. Add `config.json` with podcast details:
   ```json
   {
     "title": "Podcast Title",
     "description": "Description",
     "link": "https://example.com",
     "language": "en-us",
     "author": "Author"
   }
   ```
3. Add episode audio files.
4. Push to main branch; GitHub Actions will generate `feed.xml`.

## Current Podcasts

- EScyber: `episodes-EScyber/`

## Testing

To test locally:
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python generate_feed.py episodes-EScyber <repo_owner> <repo_name>`