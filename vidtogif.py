#!/usr/bin/env python3
import sys, subprocess, shutil, argparse

def ensure_moviepy():
    try:
        import moviepy  # noqa
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "imageio-ffmpeg"])
ensure_moviepy()

from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx  # noqa

def make_looping_fade_gif(src, out, width, fps, fade, wrap, still_bg):
    clip = VideoFileClip(src)
    if width:
        clip = clip.resize(width=width)

    # keep wrap sensible
    wrap = max(0.1, min(wrap, clip.duration / 2.0))

    # seamless loop: crossfade end -> start
    wrap_layer = clip.set_start(clip.duration - wrap).crossfadein(wrap)
    seamless = CompositeVideoClip([clip, wrap_layer]).subclip(0, clip.duration)

    # background layer (still or moving)
    if still_bg:
        bg = seamless.to_ImageClip(t=0).set_duration(seamless.duration)
    else:
        bg = seamless

    # top layer fades in/out over the bg
    top = seamless.fx(vfx.fadein, fade).fx(vfx.fadeout, fade)

    final = CompositeVideoClip([bg, top])

    program = "ffmpeg" if shutil.which("ffmpeg") else "imageio"
    final.write_gif(out, fps=fps, program=program, loop=0)

    # cleanup
    final.close(); bg.close(); top.close(); seamless.close(); clip.close()

def main():
    p = argparse.ArgumentParser(description="MP4 -> looping fade-on-itself GIF (MoviePy)")
    p.add_argument("input", help="input .mp4")
    p.add_argument("output", help="output .gif")
    p.add_argument("--width", type=int, default=480, help="output width (keeps aspect)")
    p.add_argument("--fps", type=int, default=12, help="GIF fps")
    p.add_argument("--fade", type=float, default=0.8, help="seconds for fade in/out")
    p.add_argument("--wrap", type=float, default=0.8, help="seconds to crossfade end→start")
    p.add_argument("--still-bg", action="store_true", help="use first frame as still background")
    args = p.parse_args()

    make_looping_fade_gif(
        src=args.input,
        out=args.output,
        width=args.width,
        fps=args.fps,
        fade=args.fade,
        wrap=args.wrap,
        still_bg=args.still_bg,
    )

if __name__ == "__main__":
    main()
