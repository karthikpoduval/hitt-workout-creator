import os
import argparse
import random
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips, AudioFileClip
import moviepy.video.fx as vfx
import moviepy.audio.fx as afx

def create_tabata(workout_dir, music_path, title_text, total_rounds, output_name):
    video_files = [f for f in os.listdir(workout_dir) if f.lower().endswith('.mov')]
    if not video_files:
        print("No .mov files found!")
        return
    
    random.shuffle(video_files)
    selected_videos = (video_files * (total_rounds // len(video_files) + 1))[:total_rounds]
    
    bg_music = AudioFileClip(music_path)
    final_clips = []

    # Helper to create safe text clips that won't truncate
    def safe_text(txt, f_size, color, box_size, bg=(0,0,0)):
        return TextClip(
            text=txt,
            font_size=f_size,
            color=color,
            bg_color=bg,
            size=box_size, # Force a fixed box size
            method='caption' # This prevents the "half-text" clipping
        )

    # --- Intro (10s) ---
    final_clips.append(safe_text(title_text, 70, (255,255,255), (1280, 720)).with_duration(10))

    for i, video_name in enumerate(selected_videos):
        workout_label = video_name.rsplit('.', 1)[0].replace('_', ' ').title()
        
        # --- Workout Intro (10s) ---
        intro_lbl = f"First Exercise:\n{workout_label}" if i==0 else f"Next Up:\n{workout_label}"
        final_clips.append(safe_text(intro_lbl, 60, (255,255,0), (1280, 720)).with_duration(10))

        # --- Workout Phase (40s) ---
        video_path = os.path.join(workout_dir, video_name)
        base_clip = VideoFileClip(video_path).without_audio().with_fps(24)
        loop_clip = vfx.Loop(duration=40).apply(base_clip)
        
        # UI: Workout Title (Top Center)
        workout_overlay = safe_text(workout_label, 40, (255,255,255), (800, 60)).with_duration(40).with_position(('center', 20))
        
        # UI: Progress Bar
        bar = ColorClip(size=(1280, 10), color=(255, 255, 255)).with_duration(40).with_position(('left', 'bottom'))
        bar = vfx.Resize(lambda t: (max(1, int(1280 * (1 - t/40))), 10)).apply(bar)

        # UI: Workout Countdown (Bottom Left - more room than bottom right)
        countdown_clips = []
        for sec in range(40, 0, -1):
            # Using a square box (100x100) ensures the number has room to breathe
            t_sec = safe_text(str(sec), 50, (255,255,255), (120, 100)).with_duration(1).with_position((20, 600))
            countdown_clips.append(t_sec)
        workout_timer = concatenate_videoclips(countdown_clips)

        final_clips.append(CompositeVideoClip([loop_clip.with_position("center"), workout_overlay, bar, workout_timer], size=(1280, 720)))

        # --- Rest Phase (20s) ---
        rest_bg = ColorClip(size=(1280, 720), color=(20, 20, 20)).with_duration(20)
        
        # Rest Part 1: (20-11s)
        rest_timer_clips = []
        for sec in range(20, 10, -1):
            r_t = safe_text(f"RESTING\n{sec}", 100, (255,255,255), (1280, 720)).with_duration(1)
            rest_timer_clips.append(r_t)
        rest_phase_1 = concatenate_videoclips(rest_timer_clips)
        
        # Rest Part 2: (10-1s)
        if i < len(selected_videos) - 1:
            next_name = selected_videos[i+1].rsplit('.', 1)[0].replace('_', ' ').title()
            ready_clips = []
            for sec in range(10, 0, -1):
                r_y = safe_text(f"GET READY\n{sec}\n\nUp Next:\n{next_name}", 60, (255,255,255), (1280, 720)).with_duration(1)
                ready_clips.append(r_y)
            rest_phase_2 = concatenate_videoclips(ready_clips).with_start(10)
        else:
            rest_phase_2 = safe_text("WORKOUT COMPLETE!", 70, (0,255,0), (1280, 720)).with_duration(10).with_start(10)
            
        final_clips.append(CompositeVideoClip([rest_bg, rest_phase_1, rest_phase_2]))

    # Assembly
    final_video = concatenate_videoclips(final_clips, method="compose")
    music_looped = afx.AudioLoop(duration=final_video.duration).apply(bg_music).with_volume_scaled(0.2)
    final_video = final_video.with_audio(music_looped)
    
    try:
        final_video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
    finally:
        final_video.close()
        bg_music.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True)
    parser.add_argument("--music", required=True)
    parser.add_argument("--title", default="Tabata Session")
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--out", default="final_workout.mp4")
    args = parser.parse_args()
    create_tabata(args.folder, args.music, args.title, args.rounds, args.out)