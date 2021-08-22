# Sync Two Directories

We want to write code for synchronizing two file directories, which we'll call the source and the destination:

- If a file exists in the source but not in the destination, copy the file over
- If a file exists in the source, but it has a different name than in the destination, rename the destination file to match
- If a file exists in the destination but not in the source, remove it
