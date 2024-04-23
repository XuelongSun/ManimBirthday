### Animations made by [Manim](https://github.com/ManimCommunity/manim) as a birthday gift for my wife

#### Video
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

You can customize the animation by change the code in the `birthday.py`. 

Have Fun!
