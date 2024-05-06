<div align='center'>
  
<h3> Animations made by ManimCE as a birthday gift for my wife </h3>


![](https://img.shields.io/badge/Python-3.9.0-%233776AB?logo=python) ![](https://img.shields.io/badge/manim_community-0.18.0-orange) ![](https://img.shields.io/badge/pymunk-6.5.2-green)

</div>

---

#### Video
[![](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.bilibili.com%2Fx%2Fweb-interface%2Fview%3Fbvid%3DBV1bp421D7LW&query=data.stat.view&label=Bilibili&color=ff69b4)](https://www.bilibili.com/video/BV1bp421D7LW)

Edit with Adobe Premiere, add some interesting sound effects. 
See the full video on [Bilibili](https://www.bilibili.com/video/BV1bp421D7LW).

#### Main Contents
+ Linear and circle envelope forming a heart shape
  |![](media/line_heart.gif) | ![](media/circle_heart.gif)
    --- | ---
+ Stick Numbers
<div align="center">
  <img src="https://github.com/XuelongSun/ManimBirthday/blob/main/media/stick_numbers.gif" width=60%>
</div>

+ 2D physic simulation with [Pymunk](https://github.com/viblo/pymunk)
<div align="center">
  <img src="https://github.com/XuelongSun/ManimBirthday/blob/main/media/physics.gif" width=60% align="center">
</div>

#### Files
- models.py: some useful classes for computations
- birthday.py: the main scene of the animation

#### Run

Just use manim CIL to run the `MainScene` class in `birthday.py`, like:

```
manim -qh --fps 60 --disable_caching birthday.py MainScene -o birdthday.mp4
```
this will generate the video.

You can customize the animation by change the code in `birthday.py`. 

Have Fun!
