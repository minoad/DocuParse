# DocuParse

DocuParse is a tool that:

1. Accept a directory
1. Get all files of type: png, jpeg, pdf, word, txt, and others
1. Files of type: png, word, etc, are complex text files that contain both text and potentially images.
1. The program will collect all of the text and any images for those types.  It will then ocr any of the collected images and add them to the text data from the files.
1. it will then take all of the image file types.
1. it will ocr these.
1. it will then prepare the data in such a way as to put it into a MongoDB for analysis.

## Download sample data

```powershell
$source = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
$destination = "sample.pdf"

Invoke-WebRequest -Uri $source -OutFile $destination

Write-Host "Sample PDF downloaded successfully to $destination."
# Invoke-WebRequest -Uri https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -Outfile data\test\
# Invoke-WebRequest -Uri https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf -Outfile data\test\
```
