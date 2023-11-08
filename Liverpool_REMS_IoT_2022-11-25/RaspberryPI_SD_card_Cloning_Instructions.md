# Instructions to clone a RaspberryPI SD card in a Windows PC

## Requirements:

- Have a PC with Windows OS and a micro SD card reader
- Install Win32DiskImager
- Install Raspberry Pi imager (optional)


## 1. Create a backup image of an SD card:

  - Insert the SD card you want to backup into a windows PC
  - Open Win32DiskImager
  - Select Image File (Directory where the image will be saved)
  - Select Device (Look which Drive is the sd card, if it is [H:\], [F:\], [D:\]...etc.)
  - Click on "Read"


## 2. Clone a new SD card with the created image:

 2.1- Using Win32DiskImager:

  - Insert the new SD card you want to clone into the windows PC
  - Open Win32DiskImager
  - Select Image File (Directory where the image was saved)
  - Select Device (Type of drive of the new SD card)
  - Click on "Write"

 2.2- Using Raspberry Pi Imager (Recommended):

  - Operating system: "Select a custom .img from your computer"
  - Storage: Select the SD card
  - Click on "WRITE"


## 3. Insert the new SD card into the RaspberryPI and boot