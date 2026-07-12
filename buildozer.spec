[app]
title = CLAIM Awaits
package.name = claimawaits
package.domain = org.claimawaits

source.dir = android_build
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,md,mp3,ogg,wav,ttf,otf

version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
icon.filename = app_icon.png
presplash.filename = splash_screen.png

android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a

log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
