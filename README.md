# AudioBookzOrganizer
AudioBookzOrganizer is a Python script that renames, organizes, and enriches your audiobook collection by fetching metadata from Audible. It sorts files by author, series, or genre, applies custom naming conventions, and can even download cover art—keeping your library neat and easy to navigate.



How It Works
File Parsing: The script scans audiobook filenames for patterns that might include the title, author, series, and year. For instance, if your files are named like Author - Series - Book Title (Year).mp3, the script will parse that information directly.

Flexible Naming Convention: Users can define their preferred naming structure, such as {Author} - {Series} - {Title} ({Year}). The script will attempt to match this pattern in each filename.

Folder Organization: The script moves files into folders by author and series, creating a neatly organized structure without relying on an internet connection or any external API.

