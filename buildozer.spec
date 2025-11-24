[app]
title = DailyPlanner
package.name = dailyplanner
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1   版本= 0.1

# ⚠️ 绝对不要加 pillow，绝对不要加 extra 库
requirements = python3,kivy==2.2.1,kivymd==1.1.1

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = Trueandroid。accept_sdk_license = True
android.archs = arm64-v8a

# 使用 master 分支以获取最新的构建工具修复
p4a.branch = master   p4a。分支=主

[buildozer]
log_level = 2
warn_on_root = 1
