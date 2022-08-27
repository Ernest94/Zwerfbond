# Zwerfbond

- APP

Application for Paastocht and Hemelse Hike hiking tours.


    - Build iOS application
    
    https://kivy.org/doc/stable/guide/packaging-ios.html
    https://github.com/kivy/kivy-ios

    toolchain build python3 openssl kivy plyer
    toolchain pip install plyer
    toolchain pip install requests
    toolchain pip install kivymd==1.0.2
    
    XCODE:
        - Sign the app: 
        - In Resources - paastocht-info.plist. Write the GPS popup teks; adjust information property list: "Privacy - Location When In Use Usage Description" : Deze app heeft GPS nodig.
    Set Debug - Excluded Architextures - Architectures -Build settings -> Any iOS Simulator SDK - arm64
    
    
    - Build Android application
    

    • use a VirtualBox running Ubuntu
    • install necessary tools:
        sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev
    • install buildozer:
        sudo -H pip3 install buildozer
    • create a virtual environment:
        virtualenv paastocht_virtualenv -p python3.9
    • Activate virtualenvironment
        ﻿source bin/activate
    • install necessary python packages:
        python3 -m pip install kivy
        python3 -m pip install cython
        pip install pillow
    • make a APK_files directory with the application files init
    • run: buildozer init
    • adjust: buildozer.spec
    • run: buildozer android clean (mmh the python-for-android map is not there in the platform directory in .buildozer --> now I have copied this folder from an old project)
    run: buildozer android debug deploy

    https://www.youtube.com/watch?v=cuyWeS4CY5o&ab_channel=CodingDebaseNormal
    https://github.com/CodingDebaseNormal/BuildAndSign_AAB_Python_Android_App_For_GooglePlay/blob/main/Build_Sign_AAB_PythonAndroidApp_for_GooglePlay.ipynb

- MISC
