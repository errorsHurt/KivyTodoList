[app]

title = TodoApp
package.name = TodoApp
package.domain = gsog.de

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
icon.filename = ./resources/app_icon.png
presplash.filename = ./resources/app_icon.png
version = 0.1
requirements = python3,kivy==2.2.0,requests,kivymd,plyer,chardet,charset_normalizer,urllib3,idna,paho-mqtt

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
p4a.branch = release-2022.12.20

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

[buildozer]
log_level = 1
warn_on_root = 1
