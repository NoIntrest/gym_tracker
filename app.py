"""
IronForge - Advanced Gym Tracker
A full-featured fitness tracking desktop application built with Python & Tkinter.
Run: python ironforge.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import math
import time
import threading
import datetime
import random
from collections import defaultdict

# ─────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────
C = {
    "bg":       "#0d0d0f",
    "bg2":      "#151518",
    "bg3":      "#1c1c21",
    "card":     "#1e1e24",
    "border":   "#2a2a32",
    "orange":   "#f97316",
    "orange2":  "#ea580c",
    "yellow":   "#fbbf24",
    "green":    "#22c55e",
    "blue":     "#3b82f6",
    "red":      "#ef4444",
    "purple":   "#a855f7",
    "text":     "#f0f0f5",
    "muted":    "#6b6b7e",
    "muted2":   "#9898aa",
}

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_HEAD  = ("Segoe UI", 14, "bold")
FONT_MED   = ("Segoe UI", 11)
FONT_SML   = ("Segoe UI", 9)
FONT_MONO  = ("Courier New", 11)

# ─────────────────────────────────────────────
# EXERCISE DATABASE  (60 exercises, 9 muscles)
# ─────────────────────────────────────────────
EXERCISES = [
    # CHEST
    {"id":1,"name":"Bench Press","muscle":"Chest","eq":"gym","icon":"🏋","sets":4,"reps":"8-10","rest":90,"xp":20,
     "desc":"The king of chest exercises. Lie flat, lower the bar to your chest and press up explosively.",
     "tips":["Keep shoulder blades retracted","Arch lower back slightly","Drive through your heels","Touch bar to lower chest"]},
    {"id":2,"name":"Incline DB Press","muscle":"Chest","eq":"gym","icon":"📐","sets":3,"reps":"10-12","rest":75,"xp":15,
     "desc":"Targets upper chest. Set bench to 30-45° and press dumbbells from shoulder level.",
     "tips":["Keep elbows at 45°","Full range of motion","Squeeze at top","Control the descent"]},
    {"id":3,"name":"Push-Up","muscle":"Chest","eq":"bodyweight","icon":"⬆","sets":4,"reps":"15-20","rest":60,"xp":10,
     "desc":"Classic bodyweight builder. Keep body rigid, lower chest to floor and press back up.",
     "tips":["Keep core tight","Elbows at 45°","Full range of motion","Don't let hips sag"]},
    {"id":4,"name":"Wide Push-Up","muscle":"Chest","eq":"bodyweight","icon":"↔","sets":3,"reps":"12-15","rest":60,"xp":8,
     "desc":"Wider hand placement shifts focus to the outer chest.",
     "tips":["Hands wider than shoulder-width","Keep body in straight line","Controlled movement"]},
    {"id":5,"name":"Cable Flye","muscle":"Chest","eq":"gym","icon":"🔗","sets":3,"reps":"12-15","rest":60,"xp":12,
     "desc":"Isolation movement stretching and contracting the chest through full range.",
     "tips":["Keep slight bend in elbows","Feel stretch at bottom","Squeeze hard at top"]},
    {"id":6,"name":"Dips","muscle":"Chest","eq":"gym","icon":"⬇","sets":3,"reps":"10-15","rest":75,"xp":15,
     "desc":"Lean forward to hit chest. Great compound movement for lower chest.",
     "tips":["Lean torso forward","Go deep for full stretch","Control the descent"]},
    {"id":7,"name":"Diamond Push-Up","muscle":"Chest","eq":"bodyweight","icon":"◆","sets":3,"reps":"10-15","rest":60,"xp":10,
     "desc":"Form a diamond with your hands for inner chest and triceps.",
     "tips":["Hands form diamond shape","Keep elbows close","Full extension at top"]},
    # BACK
    {"id":8,"name":"Pull-Up","muscle":"Back","eq":"bodyweight","icon":"⬆","sets":4,"reps":"6-10","rest":90,"xp":20,
     "desc":"Supreme back builder. Hang from bar, pull chin above it using lats.",
     "tips":["Full dead hang at bottom","Pull elbows to hips","Avoid swinging"]},
    {"id":9,"name":"Bent-Over Row","muscle":"Back","eq":"gym","icon":"↩","sets":4,"reps":"8-10","rest":90,"xp":20,
     "desc":"Heavy compound back movement. Hinge at hips and row barbell to lower chest.",
     "tips":["Keep back flat","Hinge to 45°","Pull elbows behind body","Squeeze at top"]},
    {"id":10,"name":"Lat Pulldown","muscle":"Back","eq":"gym","icon":"⬇","sets":3,"reps":"10-12","rest":75,"xp":15,
     "desc":"Great for lat width. Pull bar to upper chest while leaning back slightly.",
     "tips":["Lean back 15-20°","Pull to upper chest","Full extension at top"]},
    {"id":11,"name":"Seated Cable Row","muscle":"Back","eq":"gym","icon":"🔗","sets":3,"reps":"10-12","rest":75,"xp":15,
     "desc":"Horizontal pulling for back thickness.",
     "tips":["Keep torso upright","Squeeze shoulder blades","Full stretch at front"]},
    {"id":12,"name":"Inverted Row","muscle":"Back","eq":"bodyweight","icon":"↩","sets":3,"reps":"10-15","rest":60,"xp":12,
     "desc":"Bodyweight row under a bar. Great horizontal pulling.",
     "tips":["Keep body rigid","Pull chest to bar","Lower feet to increase difficulty"]},
    {"id":13,"name":"Superman Hold","muscle":"Back","eq":"bodyweight","icon":"✦","sets":3,"reps":"12-15","rest":60,"xp":8,
     "desc":"Lie face down and lift arms and legs simultaneously for lower back.",
     "tips":["Hold peak 2 seconds","Don't strain neck","Breathe steadily"]},
    {"id":14,"name":"Single-Arm DB Row","muscle":"Back","eq":"gym","icon":"💪","sets":3,"reps":"10-12","rest":60,"xp":15,
     "desc":"Unilateral exercise for back thickness and fixing imbalances.",
     "tips":["Support with same-side hand","Pull elbow high and back","Keep back flat"]},
    # SHOULDERS
    {"id":15,"name":"Overhead Press","muscle":"Shoulders","eq":"gym","icon":"⬆","sets":4,"reps":"8-10","rest":90,"xp":20,
     "desc":"King of shoulder exercises. Press barbell from shoulder height to lockout.",
     "tips":["Brace core hard","Press around face","Lock out completely"]},
    {"id":16,"name":"Lateral Raise","muscle":"Shoulders","eq":"gym","icon":"↔","sets":3,"reps":"12-15","rest":60,"xp":12,
     "desc":"Isolation for medial deltoid. Raise dumbbells to shoulder height.",
     "tips":["Lead with elbows","Stop at shoulder height","Control the negative"]},
    {"id":17,"name":"Arnold Press","muscle":"Shoulders","eq":"gym","icon":"🔄","sets":3,"reps":"10-12","rest":75,"xp":15,
     "desc":"Rotating pressing motion hitting all three deltoid heads.",
     "tips":["Start with palms facing you","Rotate as you press","Full range of motion"]},
    {"id":18,"name":"Pike Push-Up","muscle":"Shoulders","eq":"bodyweight","icon":"▲","sets":3,"reps":"10-15","rest":60,"xp":10,
     "desc":"Form inverted V and do a push-up to target shoulders.",
     "tips":["Hips high in the air","Lower head toward floor","Works toward handstand push-up"]},
    {"id":19,"name":"Front Raise","muscle":"Shoulders","eq":"gym","icon":"⬆","sets":3,"reps":"12-15","rest":60,"xp":10,
     "desc":"Targets anterior deltoid. Raise dumbbells in front to shoulder height.",
     "tips":["Keep arms straight","Don't swing body","Control the descent"]},
    # BICEPS
    {"id":20,"name":"Barbell Curl","muscle":"Biceps","eq":"gym","icon":"💪","sets":4,"reps":"8-12","rest":75,"xp":15,
     "desc":"Classic bicep builder. Curl from full extension to full flexion.",
     "tips":["Keep elbows fixed","Full range of motion","Slow negative (3s)"]},
    {"id":21,"name":"Hammer Curl","muscle":"Biceps","eq":"gym","icon":"🔨","sets":3,"reps":"10-12","rest":60,"xp":12,
     "desc":"Neutral grip hits brachialis for arm thickness.",
     "tips":["Thumbs pointing up","Elbows stay at sides","Don't swing"]},
    {"id":22,"name":"Concentration Curl","muscle":"Biceps","eq":"gym","icon":"🎯","sets":3,"reps":"12-15","rest":60,"xp":10,
     "desc":"Maximum isolation. Rest elbow on inner thigh and curl.",
     "tips":["Full range of motion","Squeeze peak contraction","Don't move upper arm"]},
    {"id":23,"name":"Chin-Up","muscle":"Biceps","eq":"bodyweight","icon":"⬆","sets":3,"reps":"6-10","rest":90,"xp":18,
     "desc":"Underhand grip pull-up heavily involving biceps.",
     "tips":["Supinated grip","Full dead hang","Pull chest to bar"]},
    # TRICEPS
    {"id":24,"name":"Tricep Dip","muscle":"Triceps","eq":"bodyweight","icon":"⬇","sets":4,"reps":"12-15","rest":75,"xp":15,
     "desc":"Bodyweight compound tricep exercise with parallel bars or chair.",
     "tips":["Keep torso upright","Elbows close to body","Full extension"]},
    {"id":25,"name":"Skull Crusher","muscle":"Triceps","eq":"gym","icon":"💀","sets":3,"reps":"10-12","rest":75,"xp":15,
     "desc":"Lying tricep extension. Lower barbell toward forehead.",
     "tips":["Keep upper arms vertical","Only move at elbows","Lock out completely"]},
    {"id":26,"name":"Tricep Pushdown","muscle":"Triceps","eq":"gym","icon":"⬇","sets":3,"reps":"12-15","rest":60,"xp":12,
     "desc":"Cable isolation. Push attachment down from chest to lockout.",
     "tips":["Elbows fixed at sides","Full lockout at bottom","Control return"]},
    {"id":27,"name":"Close-Grip Push-Up","muscle":"Triceps","eq":"bodyweight","icon":"▼","sets":3,"reps":"12-15","rest":60,"xp":10,
     "desc":"Narrow hand placement shifts emphasis to triceps.",
     "tips":["Hands shoulder-width or closer","Elbows close to body","Full range"]},
    {"id":28,"name":"Overhead Extension","muscle":"Triceps","eq":"gym","icon":"⬆","sets":3,"reps":"12-15","rest":60,"xp":12,
     "desc":"Stretches long head of triceps. Hold dumbbell overhead and extend.",
     "tips":["Keep upper arms close to head","Full stretch at bottom","Keep core tight"]},
    # LEGS
    {"id":29,"name":"Barbell Squat","muscle":"Legs","eq":"gym","icon":"🏋","sets":4,"reps":"8-10","rest":120,"xp":25,
     "desc":"The king of all exercises. Bar on upper back, squat below parallel.",
     "tips":["Break at hips and knees together","Keep chest up","Drive through full foot"]},
    {"id":30,"name":"Romanian Deadlift","muscle":"Legs","eq":"gym","icon":"⚡","sets":3,"reps":"10-12","rest":90,"xp":20,
     "desc":"Hip hinge targeting hamstrings and glutes.",
     "tips":["Push hips back not down","Feel hamstring stretch","Bar stays close to legs"]},
    {"id":31,"name":"Leg Press","muscle":"Legs","eq":"gym","icon":"🔧","sets":4,"reps":"10-15","rest":90,"xp":18,
     "desc":"Machine compound leg exercise for quad and glute development.",
     "tips":["Feet shoulder-width","Go deep for full range","Don't lock knees at top"]},
    {"id":32,"name":"Walking Lunge","muscle":"Legs","eq":"bodyweight","icon":"🚶","sets":3,"reps":"12-16","rest":75,"xp":15,
     "desc":"Dynamic lunge building legs and improving balance.",
     "tips":["Take long steps","Back knee almost touches floor","Keep torso upright"]},
    {"id":33,"name":"Bodyweight Squat","muscle":"Legs","eq":"bodyweight","icon":"🦵","sets":4,"reps":"20-25","rest":45,"xp":8,
     "desc":"Foundation leg movement for high-rep conditioning.",
     "tips":["Feet shoulder-width","Keep weight in heels","Go to parallel or below"]},
    {"id":34,"name":"Jump Squat","muscle":"Legs","eq":"bodyweight","icon":"⬆","sets":3,"reps":"15","rest":60,"xp":12,
     "desc":"Explosive variation builds power and burns max calories.",
     "tips":["Land softly","Full squat depth","Arms assist the jump"]},
    {"id":35,"name":"Leg Extension","muscle":"Legs","eq":"gym","icon":"🦵","sets":3,"reps":"12-15","rest":60,"xp":12,
     "desc":"Isolation for quadriceps. Extend knee from 90° to full extension.",
     "tips":["Full extension with squeeze","Control the negative","Keep hips down"]},
    # CORE
    {"id":36,"name":"Plank","muscle":"Core","eq":"bodyweight","icon":"📏","sets":3,"reps":"45-60s","rest":45,"xp":8,
     "desc":"Isometric hold building total core strength and stability.",
     "tips":["Straight line head to heels","Squeeze glutes and abs","Don't hold breath"]},
    {"id":37,"name":"Hanging Leg Raise","muscle":"Core","eq":"gym","icon":"⬆","sets":3,"reps":"10-15","rest":60,"xp":15,
     "desc":"Hanging from bar, raise straight legs for lower abs.",
     "tips":["Control the movement","Don't swing","Squeeze abs at top"]},
    {"id":38,"name":"Bicycle Crunch","muscle":"Core","eq":"bodyweight","icon":"🚲","sets":3,"reps":"20-30","rest":45,"xp":8,
     "desc":"Rotating crunch targeting all abs including obliques.",
     "tips":["Slow controlled rotation","Lower back pressed down","Hands light behind head"]},
    {"id":39,"name":"Ab Wheel Rollout","muscle":"Core","eq":"gym","icon":"⭕","sets":3,"reps":"10-15","rest":60,"xp":18,
     "desc":"Advanced core. Roll forward extending body then pull back.",
     "tips":["Start from knees","Brace core hard","Don't let hips drop"]},
    {"id":40,"name":"Russian Twist","muscle":"Core","eq":"bodyweight","icon":"🔄","sets":3,"reps":"20-30","rest":45,"xp":8,
     "desc":"Rotational exercise for obliques.",
     "tips":["Lean back slightly","Feet can be elevated","Touch ground each side"]},
    {"id":41,"name":"Dead Bug","muscle":"Core","eq":"bodyweight","icon":"🐛","sets":3,"reps":"10-12","rest":45,"xp":10,
     "desc":"Opposite arm-leg extension for anti-rotation strength.",
     "tips":["Press lower back to floor","Slow and controlled","Breathe out during extension"]},
    {"id":42,"name":"Mountain Climber","muscle":"Core","eq":"bodyweight","icon":"⛰","sets":3,"reps":"30","rest":45,"xp":10,
     "desc":"Dynamic core combining plank stability with knee drives.",
     "tips":["Keep hips level","Drive knees to chest","Increase speed for cardio"]},
    # GLUTES
    {"id":43,"name":"Hip Thrust","muscle":"Glutes","eq":"gym","icon":"📐","sets":4,"reps":"10-15","rest":75,"xp":18,
     "desc":"Best glute exercise. Bar over hips, shoulders on bench, thrust up.",
     "tips":["Chin tucked","Squeeze hard at top 1 second","Full hip extension"]},
    {"id":44,"name":"Glute Bridge","muscle":"Glutes","eq":"bodyweight","icon":"🌉","sets":3,"reps":"20-25","rest":45,"xp":8,
     "desc":"Bodyweight hip thrust. Lie on back and thrust hips to ceiling.",
     "tips":["Drive through heels","Squeeze glutes at top","Add resistance to progress"]},
    {"id":45,"name":"Cable Kickback","muscle":"Glutes","eq":"gym","icon":"🦶","sets":3,"reps":"12-15","rest":60,"xp":12,
     "desc":"Isolation kicking leg back against cable resistance.",
     "tips":["Keep torso stationary","Full extension","Control the return"]},
    {"id":46,"name":"Sumo Squat","muscle":"Glutes","eq":"bodyweight","icon":"🦵","sets":3,"reps":"15-20","rest":60,"xp":10,
     "desc":"Wide stance squat emphasizing glutes and inner thighs.",
     "tips":["Toes out 45°","Push knees over toes","Full depth"]},
    {"id":47,"name":"Donkey Kick","muscle":"Glutes","eq":"bodyweight","icon":"🦶","sets":3,"reps":"15-20","rest":45,"xp":8,
     "desc":"On all fours, kick leg up and back targeting the glute.",
     "tips":["Keep core engaged","Kick to hip height","Don't rotate hips"]},
    # CALVES
    {"id":48,"name":"Standing Calf Raise","muscle":"Calves","eq":"gym","icon":"⬆","sets":4,"reps":"15-20","rest":45,"xp":10,
     "desc":"Most effective calf exercise. Rise up on toes with controlled descent.",
     "tips":["Full range of motion","Pause at bottom for stretch","Use variety of foot positions"]},
    {"id":49,"name":"Seated Calf Raise","muscle":"Calves","eq":"gym","icon":"💺","sets":3,"reps":"15-20","rest":45,"xp":8,
     "desc":"Seated isolates soleus beneath the gastrocnemius.",
     "tips":["Full stretch at bottom","Controlled movement","Heavy weight works well"]},
    {"id":50,"name":"Bodyweight Calf Raise","muscle":"Calves","eq":"bodyweight","icon":"🦶","sets":4,"reps":"25-30","rest":30,"xp":6,
     "desc":"Use a step for extra range of motion.",
     "tips":["Use step for greater ROM","Go slow on descent","Single leg for challenge"]},
    # CARDIO/FULL BODY
    {"id":51,"name":"Burpee","muscle":"Full Body","eq":"bodyweight","icon":"⚡","sets":3,"reps":"10-15","rest":60,"xp":15,
     "desc":"Full-body explosive movement combining squat, plank, and jump.",
     "tips":["Explosive jump at top","Chest to floor at bottom","Consistent rhythm"]},
    {"id":52,"name":"Deadlift","muscle":"Full Body","eq":"gym","icon":"🏋","sets":4,"reps":"5-6","rest":120,"xp":30,
     "desc":"The ultimate strength test. Lift barbell from floor to standing.",
     "tips":["Bar over mid-foot","Hinge at hips first","Brace entire core","Lock out hips at top"]},
    {"id":53,"name":"Kettlebell Swing","muscle":"Full Body","eq":"gym","icon":"⚙","sets":3,"reps":"15-20","rest":60,"xp":15,
     "desc":"Hip-hinge explosive movement building power and cardio.",
     "tips":["Hinge not squat","Drive with hips","Arms are just a chain","Control the backswing"]},
    {"id":54,"name":"Box Jump","muscle":"Full Body","eq":"gym","icon":"📦","sets":3,"reps":"8-10","rest":90,"xp":15,
     "desc":"Explosive plyometric building lower body power.",
     "tips":["Land softly with bent knees","Full extension at top","Step down don't jump"]},
    {"id":55,"name":"Jump Rope","muscle":"Full Body","eq":"bodyweight","icon":"➰","sets":3,"reps":"60s","rest":45,"xp":10,
     "desc":"Cardiovascular exercise engaging calves and coordination.",
     "tips":["Stay on balls of feet","Keep elbows close","Build to longer sets"]},
    # FLEXIBILITY
    {"id":56,"name":"Foam Roll Quads","muscle":"Recovery","eq":"bodyweight","icon":"🌀","sets":1,"reps":"60s","rest":0,"xp":3,
     "desc":"Roll out quad tightness post-workout.",
     "tips":["Slow rolling motions","Pause on tight spots","Breathe through discomfort"]},
    {"id":57,"name":"Hip Flexor Stretch","muscle":"Recovery","eq":"bodyweight","icon":"🧘","sets":2,"reps":"30s","rest":0,"xp":3,
     "desc":"Lunge-based stretch for tight hip flexors.",
     "tips":["Posterior pelvic tilt","Feel stretch in front hip","Hold for 30-60s"]},
    {"id":58,"name":"Chest Opener","muscle":"Recovery","eq":"bodyweight","icon":"🤸","sets":2,"reps":"30s","rest":0,"xp":3,
     "desc":"Arms wide, open chest to combat rounded posture.",
     "tips":["Thumbs up as you open","Feel chest and bicep stretch","Don't hold breath"]},
    {"id":59,"name":"Spinal Twist","muscle":"Recovery","eq":"bodyweight","icon":"🔄","sets":2,"reps":"30s","rest":0,"xp":3,
     "desc":"Seated or lying spinal rotation for back mobility.",
     "tips":["Keep shoulders down","Breathe into the twist","Both sides equal time"]},
    {"id":60,"name":"Child's Pose","muscle":"Recovery","eq":"bodyweight","icon":"🙏","sets":1,"reps":"60s","rest":0,"xp":3,
     "desc":"Full body relaxation and lower back decompression.",
     "tips":["Arms extended overhead","Sink hips to heels","Deep belly breathing"]},
]

MUSCLES = ["All","Chest","Back","Shoulders","Biceps","Triceps","Legs","Core","Glutes","Calves","Full Body","Recovery"]

LEVELS = [
    ("NOVICE",      0),
    ("BEGINNER",    500),
    ("INTERMEDIATE",1500),
    ("ADVANCED",    3500),
    ("EXPERT",      7000),
    ("ELITE",       15000),
    ("LEGEND",      30000),
]

BADGES = [
    {"id":"first","icon":"🎯","name":"First Blood","desc":"Complete 1 workout"},
    {"id":"streak3","icon":"🔥","name":"On Fire","desc":"3-day streak"},
    {"id":"streak7","icon":"⚡","name":"Week Warrior","desc":"7-day streak"},
    {"id":"streak30","icon":"💥","name":"Iron Routine","desc":"30-day streak"},
    {"id":"w5","icon":"💪","name":"Iron Will","desc":"5 workouts"},
    {"id":"w10","icon":"🏋","name":"Gym Rat","desc":"10 workouts"},
    {"id":"w50","icon":"👑","name":"Gym King","desc":"50 workouts"},
    {"id":"sets50","icon":"⚙","name":"Grinder","desc":"50 total sets"},
    {"id":"sets100","icon":"🏆","name":"Century Club","desc":"100 total sets"},
    {"id":"sets500","icon":"💎","name":"Diamond Sets","desc":"500 total sets"},
    {"id":"muscles9","icon":"🌟","name":"Complete Package","desc":"Train all 9 muscles"},
    {"id":"xp500","icon":"📈","name":"XP Hunter","desc":"Earn 500 XP"},
    {"id":"xp5000","icon":"🚀","name":"XP Legend","desc":"Earn 5000 XP"},
    {"id":"level3","icon":"⬆","name":"Rising Star","desc":"Reach Intermediate"},
    {"id":"level5","icon":"🔱","name":"Expert Status","desc":"Reach Expert"},
    {"id":"bodyweight","icon":"🤸","name":"No Excuses","desc":"10 bodyweight workouts"},
    {"id":"heavy","icon":"🏗","name":"Heavy Metal","desc":"10 gym workouts"},
    {"id":"variety","icon":"🎨","name":"Variety Pack","desc":"Log 20 different exercises"},
    {"id":"earlybird","icon":"🌅","name":"Early Bird","desc":"Workout before 8am"},
    {"id":"nightowl","icon":"🦉","name":"Night Owl","desc":"Workout after 9pm"},
]

MOTIVATIONS = [
    "Every rep counts. Every drop of sweat matters.",
    "The body achieves what the mind believes.",
    "Push yourself because no one else is going to do it for you.",
    "Strength doesn't come from what you can do. It comes from overcoming what you thought you couldn't.",
    "Wake up. Work out. Look hot. Kick ass.",
    "Don't wish for it. Work for it.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "You didn't come this far to only come this far.",
    "Sweat is just fat crying.",
    "Your only competition is who you were yesterday.",
]

# ─────────────────────────────────────────────
# DATA PERSISTENCE
# ─────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.expanduser("~"), ".ironforge_data.json")

def load_data():
    default = {
        "xp": 0, "total_xp": 0, "level": 0,
        "streak": 0, "workouts": 0, "total_sets": 0,
        "muscle_sets": {}, "badges_earned": [],
        "workout_history": [], "bodyweight_log": [],
        "personal_records": {}, "last_workout_date": None,
        "total_exercises_logged": 0, "bodyweight_workout_count": 0,
        "gym_workout_count": 0, "unique_exercises": [],
        "username": "Athlete",
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                saved = json.load(f)
                default.update(saved)
        except Exception:
            pass
    return default

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ─────────────────────────────────────────────
# HELPER WIDGETS
# ─────────────────────────────────────────────
def styled_btn(parent, text, cmd, bg=None, fg=None, font=None, pad=(14,8), **kw):
    bg = bg or C["orange"]
    fg = fg or "#000000"
    font = font or ("Segoe UI", 11, "bold")
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=font, activebackground=C["orange2"], activeforeground="#000",
                  relief="flat", cursor="hand2", padx=pad[0], pady=pad[1], bd=0, **kw)
    return b

def card_frame(parent, **kw):
    f = tk.Frame(parent, bg=C["card"], relief="flat", bd=0,
                 highlightbackground=C["border"], highlightthickness=1, **kw)
    return f

def section_label(parent, text):
    tk.Label(parent, text=text, bg=C["bg"], fg=C["muted2"],
             font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10,4))

# ─────────────────────────────────────────────
# CANVAS CHART HELPERS
# ─────────────────────────────────────────────
def draw_bar_chart(canvas, data, title="", color=C["orange"]):
    canvas.delete("all")
    w = int(canvas["width"]); h = int(canvas["height"])
    canvas.configure(bg=C["card"])
    if not data:
        canvas.create_text(w//2, h//2, text="No data yet", fill=C["muted"], font=FONT_MED)
        return
    pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
    if title:
        canvas.create_text(w//2, 14, text=title, fill=C["text"], font=("Segoe UI",10,"bold"))
    max_val = max(v for _, v in data) if data else 1
    max_val = max(max_val, 1)
    chart_w = w - pad_l - pad_r
    chart_h = h - pad_t - pad_b
    bar_w = max(8, chart_w // len(data) - 6)
    for i, (label, val) in enumerate(data):
        x0 = pad_l + i * (chart_w // len(data)) + (chart_w // len(data) - bar_w) // 2
        bar_h = int((val / max_val) * chart_h)
        y0 = pad_t + chart_h - bar_h
        y1 = pad_t + chart_h
        canvas.create_rectangle(x0, y0, x0 + bar_w, y1, fill=color, outline="", width=0)
        # value label
        canvas.create_text(x0 + bar_w//2, y0 - 6, text=str(val), fill=C["muted2"], font=("Segoe UI",8))
        # x label
        short = label[:7] if len(label) > 7 else label
        canvas.create_text(x0 + bar_w//2, y1 + 12, text=short, fill=C["muted2"],
                            font=("Segoe UI",8), angle=30)
    # axes
    canvas.create_line(pad_l, pad_t, pad_l, pad_t+chart_h, fill=C["border"], width=1)
    canvas.create_line(pad_l, pad_t+chart_h, w-pad_r, pad_t+chart_h, fill=C["border"], width=1)

def draw_line_chart(canvas, points, title="", color=C["orange"]):
    canvas.delete("all")
    w = int(canvas["width"]); h = int(canvas["height"])
    canvas.configure(bg=C["card"])
    if len(points) < 2:
        canvas.create_text(w//2, h//2, text="Need more data", fill=C["muted"], font=FONT_MED)
        return
    pad = 40
    if title:
        canvas.create_text(w//2, 14, text=title, fill=C["text"], font=("Segoe UI",10,"bold"))
    vals = [p[1] for p in points]
    min_v, max_v = min(vals), max(vals)
    if min_v == max_v: max_v = min_v + 1
    def px(i): return pad + i * (w - 2*pad) // (len(points)-1)
    def py(v): return pad + (1 - (v - min_v)/(max_v - min_v)) * (h - 2*pad)
    coords = [(px(i), py(v)) for i, (_,v) in enumerate(points)]
    # fill area
    poly_pts = [pad, h-pad] + [c for pt in coords for c in pt] + [w-pad, h-pad]
    canvas.create_polygon(poly_pts, fill=color+"22", outline="")
    # line
    for i in range(len(coords)-1):
        canvas.create_line(*coords[i], *coords[i+1], fill=color, width=2, smooth=True)
    # dots
    for i, (x,y) in enumerate(coords):
        canvas.create_oval(x-4, y-4, x+4, y+4, fill=color, outline=C["bg"])
    # axes
    canvas.create_line(pad, pad, pad, h-pad, fill=C["border"])
    canvas.create_line(pad, h-pad, w-pad, h-pad, fill=C["border"])
    # labels
    for i, (lbl, v) in enumerate(points):
        canvas.create_text(px(i), h-pad+14, text=str(lbl)[-5:], fill=C["muted2"], font=("Segoe UI",8))
    canvas.create_text(pad-16, py(max_v), text=str(round(max_v,1)), fill=C["muted2"], font=("Segoe UI",8))
    canvas.create_text(pad-16, py(min_v), text=str(round(min_v,1)), fill=C["muted2"], font=("Segoe UI",8))

def draw_donut(canvas, slices, title=""):
    """slices = [(label, value, color), ...]"""
    canvas.delete("all")
    w = int(canvas["width"]); h = int(canvas["height"])
    canvas.configure(bg=C["card"])
    if not slices:
        canvas.create_text(w//2, h//2, text="No data", fill=C["muted"], font=FONT_MED)
        return
    total = sum(v for _,v,_ in slices)
    if total == 0: return
    cx, cy, r, r2 = w//2, h//2+10, min(w,h)//2-30, min(w,h)//4-10
    if title:
        canvas.create_text(w//2, 12, text=title, fill=C["text"], font=("Segoe UI",10,"bold"))
    start = -90
    for label, val, col in slices:
        extent = 360 * val / total
        canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent,
                          fill=col, outline=C["bg"], width=2, style=tk.ARC if False else "pieslice")
        start += extent
    # center hole
    canvas.create_oval(cx-r2, cy-r2, cx+r2, cy+r2, fill=C["card"], outline="")
    canvas.create_text(cx, cy, text=str(total), fill=C["text"], font=("Segoe UI",13,"bold"))
    canvas.create_text(cx, cy+16, text="total sets", fill=C["muted2"], font=("Segoe UI",8))


# ─────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────
class IronForgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IronForge — Advanced Gym Tracker")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=C["bg"])

        # Try to set icon
        try:
            self.root.iconbitmap("")
        except Exception:
            pass

        self.data = load_data()
        self.today_log = []        # list of exercise dicts logged today
        self.rest_timer_active = False
        self.rest_seconds = 0
        self.timer_thread = None
        self.filter_muscle = tk.StringVar(value="All")
        self.filter_eq    = tk.StringVar(value="All")
        self.search_var   = tk.StringVar(value="")
        self.search_var.trace_add("write", lambda *a: self.refresh_exercise_list())
        self.selected_exercise = None
        self.bw_var = tk.StringVar()
        self.note_var = tk.StringVar()

        self._build_ui()
        self._refresh_all()

    # ── UI SKELETON ──────────────────────────
    def _build_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=C["bg2"], width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main area
        self.main = tk.Frame(self.root, bg=C["bg"])
        self.main.pack(side="left", fill="both", expand=True)

        # Header in main
        self.header = tk.Frame(self.main, bg=C["bg3"], height=60)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.lbl_title = tk.Label(self.header, text="", bg=C["bg3"], fg=C["text"],
                                  font=("Segoe UI",16,"bold"))
        self.lbl_title.pack(side="left", padx=20, pady=10)

        self.lbl_motivation = tk.Label(self.header, text=random.choice(MOTIVATIONS),
                                       bg=C["bg3"], fg=C["muted"], font=("Segoe UI",9,"italic"),
                                       wraplength=400)
        self.lbl_motivation.pack(side="right", padx=20)

        # Page container
        self.page_frame = tk.Frame(self.main, bg=C["bg"])
        self.page_frame.pack(fill="both", expand=True)

        self._build_sidebar()
        self._build_pages()

    def _build_sidebar(self):
        # Logo
        tk.Label(self.sidebar, text="IRONFORGE", bg=C["bg2"], fg=C["orange"],
                 font=("Segoe UI",18,"bold")).pack(pady=(24,4))
        tk.Label(self.sidebar, text="Advanced Gym Tracker", bg=C["bg2"], fg=C["muted"],
                 font=("Segoe UI",8)).pack(pady=(0,20))

        # XP bar section
        xp_frame = tk.Frame(self.sidebar, bg=C["bg2"])
        xp_frame.pack(fill="x", padx=14, pady=(0,16))
        xp_top = tk.Frame(xp_frame, bg=C["bg2"])
        xp_top.pack(fill="x")
        self.lbl_level = tk.Label(xp_top, text="", bg=C["bg2"], fg=C["orange"],
                                   font=("Segoe UI",10,"bold"))
        self.lbl_level.pack(side="left")
        self.lbl_xp = tk.Label(xp_top, text="", bg=C["bg2"], fg=C["muted2"],
                                font=("Segoe UI",8))
        self.lbl_xp.pack(side="right")
        self.xp_canvas = tk.Canvas(xp_frame, bg=C["bg3"], height=7, highlightthickness=0)
        self.xp_canvas.pack(fill="x", pady=(4,0))
        self.xp_canvas.bind("<Configure>", lambda e: self._draw_xp_bar())

        sep = tk.Frame(self.sidebar, bg=C["border"], height=1)
        sep.pack(fill="x", padx=14, pady=8)

        # Nav buttons
        self.pages = {}
        self.nav_btns = {}
        nav_items = [
            ("🏠  Dashboard",  "dashboard"),
            ("💪  Train",       "train"),
            ("📋  Today's Log", "log"),
            ("📊  Statistics",  "stats"),
            ("📅  History",     "history"),
            ("⚖   Body Weight", "bodyweight"),
            ("🏅  Achievements","awards"),
            ("⏱   Rest Timer",  "timer"),
            ("🔄  Workouts",    "workouts"),
            ("⚙   Settings",    "settings"),
        ]
        for label, key in nav_items:
            btn = tk.Button(self.sidebar, text=label, bg=C["bg2"], fg=C["muted2"],
                            font=("Segoe UI",11), relief="flat", anchor="w",
                            padx=18, pady=10, cursor="hand2", bd=0,
                            activebackground=C["bg3"], activeforeground=C["text"],
                            command=lambda k=key: self.show_page(k))
            btn.pack(fill="x")
            self.nav_btns[key] = btn

        # Streak & workout info
        sep2 = tk.Frame(self.sidebar, bg=C["border"], height=1)
        sep2.pack(fill="x", padx=14, pady=8)
        info_frame = tk.Frame(self.sidebar, bg=C["bg2"])
        info_frame.pack(fill="x", padx=14, pady=4)
        self.lbl_streak = tk.Label(info_frame, text="", bg=C["bg2"], fg=C["text"],
                                    font=("Segoe UI",11,"bold"))
        self.lbl_streak.pack(anchor="w")
        self.lbl_workouts_side = tk.Label(info_frame, text="", bg=C["bg2"], fg=C["muted2"],
                                           font=("Segoe UI",9))
        self.lbl_workouts_side.pack(anchor="w")

    # ── PAGES ────────────────────────────────
    def _build_pages(self):
        self._build_dashboard()
        self._build_train()
        self._build_log()
        self._build_stats()
        self._build_history()
        self._build_bodyweight()
        self._build_awards()
        self._build_timer()
        self._build_workouts()
        self._build_settings()
        self.show_page("dashboard")

    def _make_page(self, key):
        f = tk.Frame(self.page_frame, bg=C["bg"])
        self.pages[key] = f
        return f

    def _scrollable(self, parent):
        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=C["bg"])
        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        return scroll_frame

    # ── DASHBOARD ────────────────────────────
    def _build_dashboard(self):
        page = self._make_page("dashboard")
        scroll = self._scrollable(page)

        tk.Label(scroll, text=f"Welcome back, {self.data['username']} 👋",
                 bg=C["bg"], fg=C["text"], font=("Segoe UI",20,"bold")).pack(anchor="w", padx=20, pady=(20,4))
        self.lbl_date = tk.Label(scroll, text="", bg=C["bg"], fg=C["muted2"],
                                  font=("Segoe UI",11))
        self.lbl_date.pack(anchor="w", padx=20, pady=(0,16))

        # Big stats row
        stats_row = tk.Frame(scroll, bg=C["bg"])
        stats_row.pack(fill="x", padx=20, pady=(0,16))
        self.dash_stat_cards = {}
        stats = [
            ("streak",   "🔥", "Day Streak",  C["orange"]),
            ("workouts", "💪", "Workouts",    C["blue"]),
            ("sets",     "⚙", "Total Sets",  C["green"]),
            ("badges",   "🏅", "Badges",      C["purple"]),
            ("xp",       "⚡", "Total XP",    C["yellow"]),
        ]
        for col, (key, icon, label, color) in enumerate(stats):
            c = card_frame(stats_row, padx=16, pady=14)
            c.grid(row=0, column=col, padx=6, sticky="ew")
            stats_row.columnconfigure(col, weight=1)
            tk.Label(c, text=icon, bg=C["card"], font=("Segoe UI",22)).pack()
            v = tk.Label(c, text="0", bg=C["card"], fg=color,
                         font=("Segoe UI",26,"bold"))
            v.pack()
            tk.Label(c, text=label, bg=C["card"], fg=C["muted2"],
                     font=("Segoe UI",9)).pack()
            self.dash_stat_cards[key] = v

        # Motivation + quick actions
        mid = tk.Frame(scroll, bg=C["bg"])
        mid.pack(fill="x", padx=20, pady=(0,16))
        mid.columnconfigure(0, weight=1); mid.columnconfigure(1, weight=1)

        mot_card = card_frame(mid, padx=16, pady=16)
        mot_card.grid(row=0, column=0, padx=(0,8), sticky="nsew")
        tk.Label(mot_card, text="Today's Motivation", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",9,"bold")).pack(anchor="w")
        self.lbl_mot2 = tk.Label(mot_card, text=random.choice(MOTIVATIONS),
                                  bg=C["card"], fg=C["text"], font=("Segoe UI",11,"italic"),
                                  wraplength=300, justify="left")
        self.lbl_mot2.pack(anchor="w", pady=(8,0))
        styled_btn(mot_card, "New Quote", lambda: self.lbl_mot2.config(text=random.choice(MOTIVATIONS)),
                   bg=C["bg3"], fg=C["muted2"], pad=(10,5)).pack(anchor="w", pady=(10,0))

        act_card = card_frame(mid, padx=16, pady=16)
        act_card.grid(row=0, column=1, padx=(8,0), sticky="nsew")
        tk.Label(act_card, text="Quick Actions", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",9,"bold")).pack(anchor="w")
        actions = [
            ("+ Start Workout",    C["orange"],  lambda: self.show_page("train")),
            ("📋 View Today's Log", C["blue"],   lambda: self.show_page("log")),
            ("📊 Statistics",       C["green"],  lambda: self.show_page("stats")),
            ("⏱ Rest Timer",       C["purple"], lambda: self.show_page("timer")),
        ]
        for txt, col, cmd in actions:
            styled_btn(act_card, txt, cmd, bg=col, pad=(12,6)).pack(fill="x", pady=3)

        # Recent activity
        section_label(scroll, "  RECENT WORKOUTS")
        self.recent_frame = tk.Frame(scroll, bg=C["bg"])
        self.recent_frame.pack(fill="x", padx=20, pady=(0,20))

    # ── TRAIN ────────────────────────────────
    def _build_train(self):
        page = self._make_page("train")

        # Top controls
        ctrl = tk.Frame(page, bg=C["bg3"])
        ctrl.pack(fill="x", padx=0, pady=0)
        ctrl_inner = tk.Frame(ctrl, bg=C["bg3"])
        ctrl_inner.pack(fill="x", padx=16, pady=12)

        tk.Label(ctrl_inner, text="Muscle:", bg=C["bg3"], fg=C["muted2"],
                 font=FONT_MED).grid(row=0, column=0, sticky="w", padx=(0,8))
        muscle_cb = ttk.Combobox(ctrl_inner, textvariable=self.filter_muscle,
                                  values=MUSCLES, state="readonly", width=14,
                                  font=FONT_MED)
        muscle_cb.grid(row=0, column=1, padx=(0,16))
        muscle_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_exercise_list())

        tk.Label(ctrl_inner, text="Type:", bg=C["bg3"], fg=C["muted2"],
                 font=FONT_MED).grid(row=0, column=2, sticky="w", padx=(0,8))
        eq_cb = ttk.Combobox(ctrl_inner, textvariable=self.filter_eq,
                              values=["All","bodyweight","gym"], state="readonly", width=12,
                              font=FONT_MED)
        eq_cb.grid(row=0, column=3, padx=(0,16))
        eq_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_exercise_list())

        tk.Label(ctrl_inner, text="Search:", bg=C["bg3"], fg=C["muted2"],
                 font=FONT_MED).grid(row=0, column=4, sticky="w", padx=(0,8))
        tk.Entry(ctrl_inner, textvariable=self.search_var, bg=C["bg3"], fg=C["text"],
                 insertbackground=C["text"], font=FONT_MED, relief="flat",
                 highlightbackground=C["border"], highlightthickness=1,
                 width=18).grid(row=0, column=5)

        # Split: list + detail
        split = tk.PanedWindow(page, orient="horizontal", bg=C["bg"],
                               sashwidth=4, sashrelief="flat")
        split.pack(fill="both", expand=True)

        # Left: exercise list
        list_frame = tk.Frame(split, bg=C["bg2"])
        split.add(list_frame, minsize=280)

        self.ex_canvas = tk.Canvas(list_frame, bg=C["bg2"], highlightthickness=0)
        ex_sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.ex_canvas.yview)
        self.ex_list_inner = tk.Frame(self.ex_canvas, bg=C["bg2"])
        self.ex_list_inner.bind("<Configure>",
            lambda e: self.ex_canvas.configure(scrollregion=self.ex_canvas.bbox("all")))
        self.ex_canvas.create_window((0,0), window=self.ex_list_inner, anchor="nw")
        self.ex_canvas.configure(yscrollcommand=ex_sb.set)
        self.ex_canvas.pack(side="left", fill="both", expand=True)
        ex_sb.pack(side="right", fill="y")
        self.ex_canvas.bind("<MouseWheel>",
            lambda e: self.ex_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Right: detail panel
        self.detail_frame = tk.Frame(split, bg=C["bg"])
        split.add(self.detail_frame, minsize=360)
        self._build_detail_panel()

    def _build_detail_panel(self):
        for w in self.detail_frame.winfo_children():
            w.destroy()
        tk.Label(self.detail_frame, text="Select an exercise to see details",
                 bg=C["bg"], fg=C["muted"], font=FONT_MED).pack(expand=True)

    def show_exercise_detail(self, ex):
        self.selected_exercise = ex
        f = self.detail_frame
        for w in f.winfo_children():
            w.destroy()
        scroll = self._scrollable(f)

        # Header
        header = card_frame(scroll, padx=20, pady=16)
        header.pack(fill="x", padx=16, pady=(16,0))
        tk.Label(header, text=ex["icon"] + "  " + ex["name"], bg=C["card"],
                 fg=C["text"], font=("Segoe UI",18,"bold")).pack(anchor="w")
        tk.Label(header, text=ex["muscle"] + " • " + ex["eq"].title(), bg=C["card"],
                 fg=C["muted2"], font=FONT_MED).pack(anchor="w", pady=(2,8))
        # Tags
        tags = tk.Frame(header, bg=C["card"])
        tags.pack(anchor="w")
        for tag, col in [(ex["muscle"], C["orange"]), (ex["eq"].title(), C["blue"]),
                         (f"+{ex['xp']} XP", C["green"])]:
            tk.Label(tags, text=tag, bg=C["bg3"], fg=col,
                     font=("Segoe UI",9,"bold"), padx=8, pady=3).pack(side="left", padx=3)

        # Stats row
        row = card_frame(scroll, padx=10, pady=12)
        row.pack(fill="x", padx=16, pady=8)
        for col, (val, lbl) in enumerate([(ex["sets"],"Sets"),(ex["reps"],"Reps"),(f"{ex['rest']}s","Rest")]):
            tk.Label(row, text=str(val), bg=C["card"], fg=C["orange"],
                     font=("Segoe UI",22,"bold")).grid(row=0, column=col*2, padx=18)
            tk.Label(row, text=lbl, bg=C["card"], fg=C["muted2"],
                     font=("Segoe UI",9)).grid(row=1, column=col*2, padx=18)
            if col < 2:
                tk.Frame(row, bg=C["border"], width=1).grid(row=0, column=col*2+1,
                          rowspan=2, sticky="ns", pady=4)

        # Description
        desc_card = card_frame(scroll, padx=16, pady=12)
        desc_card.pack(fill="x", padx=16, pady=(0,8))
        tk.Label(desc_card, text="Description", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",9,"bold")).pack(anchor="w")
        tk.Label(desc_card, text=ex["desc"], bg=C["card"], fg=C["text"],
                 font=FONT_MED, wraplength=350, justify="left").pack(anchor="w", pady=(6,0))

        # Tips
        tips_card = card_frame(scroll, padx=16, pady=12)
        tips_card.pack(fill="x", padx=16, pady=(0,8))
        tk.Label(tips_card, text="Form Tips", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",9,"bold")).pack(anchor="w", pady=(0,6))
        for tip in ex["tips"]:
            row2 = tk.Frame(tips_card, bg=C["card"])
            row2.pack(fill="x", pady=2)
            tk.Label(row2, text="→", bg=C["card"], fg=C["orange"],
                     font=FONT_MED).pack(side="left")
            tk.Label(row2, text=tip, bg=C["card"], fg=C["muted2"],
                     font=FONT_MED, wraplength=320, justify="left").pack(side="left", padx=6)

        # PR section
        pr_card = card_frame(scroll, padx=16, pady=12)
        pr_card.pack(fill="x", padx=16, pady=(0,8))
        tk.Label(pr_card, text="Personal Record", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",9,"bold")).pack(anchor="w")
        pr = self.data["personal_records"].get(str(ex["id"]), {})
        pr_row = tk.Frame(pr_card, bg=C["card"])
        pr_row.pack(fill="x", pady=(6,0))
        tk.Label(pr_row, text=f"Best Weight: {pr.get('weight','—')} kg",
                 bg=C["card"], fg=C["text"], font=FONT_MED).pack(side="left", padx=(0,20))
        tk.Label(pr_row, text=f"Best Reps: {pr.get('reps','—')}",
                 bg=C["card"], fg=C["text"], font=FONT_MED).pack(side="left")
        # PR update
        pr_entry_row = tk.Frame(pr_card, bg=C["card"])
        pr_entry_row.pack(fill="x", pady=(8,0))
        tk.Label(pr_entry_row, text="Update PR — Weight:", bg=C["card"],
                 fg=C["muted2"], font=FONT_SML).pack(side="left")
        pr_wt = tk.Entry(pr_entry_row, bg=C["bg3"], fg=C["text"], width=6,
                         font=FONT_MED, relief="flat", insertbackground=C["text"])
        pr_wt.pack(side="left", padx=6)
        tk.Label(pr_entry_row, text="Reps:", bg=C["card"], fg=C["muted2"],
                 font=FONT_SML).pack(side="left")
        pr_rp = tk.Entry(pr_entry_row, bg=C["bg3"], fg=C["text"], width=4,
                         font=FONT_MED, relief="flat", insertbackground=C["text"])
        pr_rp.pack(side="left", padx=6)
        styled_btn(pr_entry_row, "Save PR", lambda: self._save_pr(ex["id"], pr_wt.get(), pr_rp.get()),
                   bg=C["bg3"], fg=C["text"], pad=(8,4)).pack(side="left")

        # Add to log button
        btn_frame = tk.Frame(scroll, bg=C["bg"])
        btn_frame.pack(fill="x", padx=16, pady=(4,16))
        styled_btn(btn_frame, f"+ Add to Today's Log  (+{ex['xp']} XP)",
                   lambda: self.add_to_log(ex), pad=(20,12)).pack(fill="x")
        styled_btn(btn_frame, "⏱ Set Rest Timer",
                   lambda: self.quick_timer(ex["rest"]), bg=C["bg3"], fg=C["muted2"],
                   pad=(20,10)).pack(fill="x", pady=(6,0))

    def _save_pr(self, ex_id, weight, reps):
        try:
            pr = {}
            if weight: pr["weight"] = float(weight)
            if reps:   pr["reps"]   = int(reps)
            self.data["personal_records"][str(ex_id)] = pr
            save_data(self.data)
            messagebox.showinfo("PR Saved", "Personal record updated! 💪")
            # Refresh detail
            ex = next(e for e in EXERCISES if e["id"] == ex_id)
            self.show_exercise_detail(ex)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def refresh_exercise_list(self):
        for w in self.ex_list_inner.winfo_children():
            w.destroy()
        muscle = self.filter_muscle.get()
        eq     = self.filter_eq.get()
        search = self.search_var.get().lower()
        filtered = [e for e in EXERCISES
                    if (muscle == "All" or e["muscle"] == muscle)
                    and (eq == "All" or e["eq"] == eq)
                    and (search == "" or search in e["name"].lower())]

        tk.Label(self.ex_list_inner, text=f"{len(filtered)} exercises",
                 bg=C["bg2"], fg=C["muted"], font=("Segoe UI",9)).pack(anchor="w", padx=12, pady=6)

        for ex in filtered:
            self._make_ex_row(ex)

    def _make_ex_row(self, ex):
        row = tk.Frame(self.ex_list_inner, bg=C["bg2"], cursor="hand2")
        row.pack(fill="x", padx=8, pady=2)
        inner = card_frame(row, padx=12, pady=10)
        inner.pack(fill="x")
        inner.configure(cursor="hand2")

        top = tk.Frame(inner, bg=C["card"])
        top.pack(fill="x")
        tk.Label(top, text=ex["icon"] + " " + ex["name"], bg=C["card"],
                 fg=C["text"], font=("Segoe UI",11,"bold")).pack(side="left")
        eq_col = C["blue"] if ex["eq"] == "gym" else C["green"]
        tk.Label(top, text=ex["eq"].title(), bg=C["bg3"], fg=eq_col,
                 font=("Segoe UI",8), padx=6, pady=2).pack(side="right")

        bot = tk.Frame(inner, bg=C["card"])
        bot.pack(fill="x", pady=(4,0))
        tk.Label(bot, text=f"{ex['muscle']} • {ex['sets']}×{ex['reps']} • {ex['rest']}s rest • +{ex['xp']} XP",
                 bg=C["card"], fg=C["muted2"], font=("Segoe UI",9)).pack(side="left")

        for w in [row, inner, top, bot]:
            w.bind("<Button-1>", lambda e, x=ex: self.show_exercise_detail(x))
        for child in inner.winfo_children() + top.winfo_children() + bot.winfo_children():
            child.bind("<Button-1>", lambda e, x=ex: self.show_exercise_detail(x))

    # ── LOG ──────────────────────────────────
    def _build_log(self):
        page = self._make_page("log")

        # Header
        top = tk.Frame(page, bg=C["bg3"])
        top.pack(fill="x", padx=0)
        tk.Label(top, text="Today's Workout Log", bg=C["bg3"], fg=C["text"],
                 font=FONT_TITLE).pack(side="left", padx=20, pady=14)
        self.lbl_log_summary = tk.Label(top, text="", bg=C["bg3"], fg=C["muted2"],
                                         font=FONT_MED)
        self.lbl_log_summary.pack(side="right", padx=20)

        # Note
        note_frame = tk.Frame(page, bg=C["bg3"])
        note_frame.pack(fill="x", padx=20, pady=(8,0))
        tk.Label(note_frame, text="Workout Note:", bg=C["bg3"], fg=C["muted2"],
                 font=FONT_SML).pack(side="left", padx=(0,8))
        tk.Entry(note_frame, textvariable=self.note_var, bg=C["bg"], fg=C["text"],
                 insertbackground=C["text"], font=FONT_MED, relief="flat",
                 highlightbackground=C["border"], highlightthickness=1,
                 width=50).pack(side="left")

        # Log list
        self.log_canvas = tk.Canvas(page, bg=C["bg"], highlightthickness=0)
        log_sb = ttk.Scrollbar(page, orient="vertical", command=self.log_canvas.yview)
        self.log_inner = tk.Frame(self.log_canvas, bg=C["bg"])
        self.log_inner.bind("<Configure>",
            lambda e: self.log_canvas.configure(scrollregion=self.log_canvas.bbox("all")))
        self.log_canvas.create_window((0,0), window=self.log_inner, anchor="nw")
        self.log_canvas.configure(yscrollcommand=log_sb.set)
        self.log_canvas.pack(side="left", fill="both", expand=True, padx=(20,0), pady=12)
        log_sb.pack(side="right", fill="y", pady=12)

        # Bottom action bar
        self.log_bottom = tk.Frame(page, bg=C["bg3"])
        self.log_bottom.pack(fill="x", padx=20, pady=10)

    def _refresh_log_ui(self):
        for w in self.log_inner.winfo_children():
            w.destroy()
        for w in self.log_bottom.winfo_children():
            w.destroy()

        if not self.today_log:
            tk.Label(self.log_inner, text="🏋  No exercises yet.\nGo to Train and add some!",
                     bg=C["bg"], fg=C["muted"], font=("Segoe UI",13), justify="center").pack(pady=60)
            self.lbl_log_summary.config(text="0 exercises")
            return

        sets_total = sum(e["sets"] for e in self.today_log)
        xp_total   = sum(e["xp"]   for e in self.today_log)
        self.lbl_log_summary.config(
            text=f"{len(self.today_log)} exercises · {sets_total} sets · +{xp_total} XP today")

        for i, ex in enumerate(self.today_log):
            row = card_frame(self.log_inner, padx=14, pady=10)
            row.pack(fill="x", pady=3)
            left = tk.Frame(row, bg=C["card"])
            left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=ex["icon"] + "  " + ex["name"], bg=C["card"],
                     fg=C["text"], font=("Segoe UI",12,"bold")).pack(anchor="w")
            tk.Label(left, text=f'{ex["muscle"]} • {ex["sets"]} sets × {ex["reps"]} reps • +{ex["xp"]} XP',
                     bg=C["card"], fg=C["muted2"], font=("Segoe UI",9)).pack(anchor="w")
            del_btn = tk.Button(row, text="✕", bg=C["card"], fg=C["red"],
                                font=("Segoe UI",12,"bold"), relief="flat", cursor="hand2",
                                command=lambda idx=i: self._remove_log_item(idx))
            del_btn.pack(side="right")

        # Finish button
        styled_btn(self.log_bottom, "✓  Finish & Save Workout",
                   self.finish_workout, bg=C["green"], pad=(20,12)).pack(side="left")
        styled_btn(self.log_bottom, "🗑 Clear Log",
                   self._clear_log, bg=C["red"], fg=C["text"], pad=(12,12)).pack(side="left", padx=10)

    def _remove_log_item(self, idx):
        self.today_log.pop(idx)
        self._refresh_log_ui()

    def _clear_log(self):
        if messagebox.askyesno("Clear Log", "Clear today's log?"):
            self.today_log.clear()
            self._refresh_log_ui()

    def add_to_log(self, ex):
        self.today_log.append(ex.copy())
        self._refresh_log_ui()
        self._show_toast(f"✓ {ex['name']} added  (+{ex['xp']} XP)")
        self.show_page("log")

    def finish_workout(self):
        if not self.today_log:
            messagebox.showwarning("Empty Log", "Add exercises before finishing!")
            return
        sets_total = sum(e["sets"] for e in self.today_log)
        xp_total   = sum(e["xp"]   for e in self.today_log)
        bonus_xp   = 50
        total_xp   = xp_total + bonus_xp
        muscles_used = list(set(e["muscle"] for e in self.today_log))
        eq_types     = [e["eq"] for e in self.today_log]

        # Update data
        self.data["workouts"] += 1
        self.data["total_sets"] += sets_total
        self.data["total_xp"] += total_xp
        for m in muscles_used:
            self.data["muscle_sets"][m] = self.data["muscle_sets"].get(m, 0) + sets_total
        for ex in self.today_log:
            if str(ex["id"]) not in self.data["unique_exercises"]:
                self.data["unique_exercises"].append(str(ex["id"]))
        self.data["bodyweight_workout_count"] += eq_types.count("bodyweight")
        self.data["gym_workout_count"]         += eq_types.count("gym")
        self.data["total_exercises_logged"]    += len(self.today_log)

        # Streak
        today_str = str(datetime.date.today())
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        if self.data["last_workout_date"] == yesterday:
            self.data["streak"] += 1
        elif self.data["last_workout_date"] != today_str:
            self.data["streak"] = 1
        self.data["last_workout_date"] = today_str

        # Early bird / night owl
        hour = datetime.datetime.now().hour
        if hour < 8:  self._earn_badge("earlybird")
        if hour >= 21: self._earn_badge("nightowl")

        # XP & level
        self.data["xp"] = self.data.get("xp", 0) + total_xp
        old_level = self.data["level"]
        for i, (name, req) in reversed(list(enumerate(LEVELS))):
            if self.data["total_xp"] >= req:
                self.data["level"] = i
                break

        # Save history entry
        entry = {
            "date": today_str,
            "exercises": [e["name"] for e in self.today_log],
            "sets": sets_total,
            "xp": total_xp,
            "muscles": muscles_used,
            "note": self.note_var.get(),
        }
        self.data["workout_history"].insert(0, entry)
        save_data(self.data)
        self._check_all_badges()

        level_up = self.data["level"] > old_level
        msg = f"Workout saved!\n\n{len(self.today_log)} exercises · {sets_total} sets\n+{total_xp} XP earned"
        if level_up:
            msg += f"\n\n🎉 LEVEL UP! You are now {LEVELS[self.data['level']][0]}!"
        messagebox.showinfo("Workout Complete! 🏆", msg)

        self.today_log.clear()
        self.note_var.set("")
        self._refresh_log_ui()
        self._refresh_all()

    # ── STATS ─────────────────────────────────
    def _build_stats(self):
        page = self._make_page("stats")
        scroll = self._scrollable(page)

        tk.Label(scroll, text="Statistics", bg=C["bg"], fg=C["text"],
                 font=FONT_TITLE).pack(anchor="w", padx=20, pady=(16,4))

        # Charts row
        charts_row = tk.Frame(scroll, bg=C["bg"])
        charts_row.pack(fill="x", padx=20, pady=8)
        charts_row.columnconfigure(0, weight=1)
        charts_row.columnconfigure(1, weight=1)

        left_card = card_frame(charts_row, padx=0, pady=0)
        left_card.grid(row=0, column=0, padx=(0,8), sticky="nsew", pady=4)
        tk.Label(left_card, text="Muscle Groups Trained", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", padx=14, pady=(12,4))
        self.bar_canvas = tk.Canvas(left_card, bg=C["card"], height=200,
                                     highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=6, pady=(0,10))

        right_card = card_frame(charts_row, padx=0, pady=0)
        right_card.grid(row=0, column=1, padx=(8,0), sticky="nsew", pady=4)
        tk.Label(right_card, text="Muscle Share (Donut)", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", padx=14, pady=(12,4))
        self.donut_canvas = tk.Canvas(right_card, bg=C["card"], height=200,
                                       highlightthickness=0)
        self.donut_canvas.pack(fill="x", padx=6, pady=(0,10))

        # Workouts over time
        hist_card = card_frame(scroll, padx=0, pady=0)
        hist_card.pack(fill="x", padx=20, pady=(0,12))
        tk.Label(hist_card, text="Workout Frequency (Last 14 Days)", bg=C["card"],
                 fg=C["muted2"], font=("Segoe UI",10,"bold")).pack(anchor="w", padx=14, pady=(12,4))
        self.freq_canvas = tk.Canvas(hist_card, bg=C["card"], height=170,
                                      highlightthickness=0)
        self.freq_canvas.pack(fill="x", padx=6, pady=(0,10))

        # XP over time
        xp_card = card_frame(scroll, padx=0, pady=0)
        xp_card.pack(fill="x", padx=20, pady=(0,20))
        tk.Label(xp_card, text="XP Earned (Last 10 Workouts)", bg=C["card"],
                 fg=C["muted2"], font=("Segoe UI",10,"bold")).pack(anchor="w", padx=14, pady=(12,4))
        self.xp_line_canvas = tk.Canvas(xp_card, bg=C["card"], height=160,
                                         highlightthickness=0)
        self.xp_line_canvas.pack(fill="x", padx=6, pady=(0,10))

    def _refresh_stats(self):
        ms = self.data["muscle_sets"]
        if ms:
            bar_data = sorted(ms.items(), key=lambda x: x[1], reverse=True)
            draw_bar_chart(self.bar_canvas, bar_data)
            colors = [C["orange"],C["blue"],C["green"],C["purple"],C["yellow"],
                      C["red"],C["orange2"],"#ec4899","#14b8a6","#8b5cf6"]
            slices = [(m, v, colors[i % len(colors)]) for i,(m,v) in enumerate(bar_data)]
            draw_donut(self.donut_canvas, slices)
        else:
            draw_bar_chart(self.bar_canvas, [])
            draw_donut(self.donut_canvas, [])

        # Frequency
        today = datetime.date.today()
        dates = [(today - datetime.timedelta(days=i)) for i in range(13,-1,-1)]
        history_dates = set(e["date"] for e in self.data["workout_history"])
        freq_data = [(str(d)[5:], 1 if str(d) in history_dates else 0) for d in dates]
        draw_bar_chart(self.freq_canvas, freq_data, color=C["blue"])

        # XP line
        recent = self.data["workout_history"][:10][::-1]
        if recent:
            xp_data = [(e["date"][5:], e["xp"]) for e in recent]
            draw_line_chart(self.xp_line_canvas, xp_data)
        else:
            draw_line_chart(self.xp_line_canvas, [])

    # ── HISTORY ──────────────────────────────
    def _build_history(self):
        page = self._make_page("history")
        scroll = self._scrollable(page)

        tk.Label(scroll, text="Workout History", bg=C["bg"], fg=C["text"],
                 font=FONT_TITLE).pack(anchor="w", padx=20, pady=(16,4))

        self.history_inner = tk.Frame(scroll, bg=C["bg"])
        self.history_inner.pack(fill="x", padx=20, pady=(0,20))

    def _refresh_history(self):
        for w in self.history_inner.winfo_children():
            w.destroy()
        history = self.data["workout_history"]
        if not history:
            tk.Label(self.history_inner, text="No workouts recorded yet.",
                     bg=C["bg"], fg=C["muted"], font=FONT_MED).pack(pady=40)
            return
        for entry in history[:50]:
            row = card_frame(self.history_inner, padx=14, pady=10)
            row.pack(fill="x", pady=3)
            top = tk.Frame(row, bg=C["card"])
            top.pack(fill="x")
            tk.Label(top, text=entry["date"], bg=C["card"], fg=C["orange"],
                     font=("Segoe UI",11,"bold")).pack(side="left")
            tk.Label(top, text=f'+{entry["xp"]} XP', bg=C["card"], fg=C["green"],
                     font=("Segoe UI",10,"bold")).pack(side="right")
            tk.Label(row, text=f'{entry["sets"]} sets · {", ".join(entry["muscles"][:4])}',
                     bg=C["card"], fg=C["muted2"], font=("Segoe UI",9)).pack(anchor="w", pady=(4,2))
            exs = ", ".join(entry["exercises"][:5])
            if len(entry["exercises"]) > 5:
                exs += f" +{len(entry['exercises'])-5} more"
            tk.Label(row, text=exs, bg=C["card"], fg=C["muted"],
                     font=("Segoe UI",9,"italic")).pack(anchor="w")
            if entry.get("note"):
                tk.Label(row, text=f'📝 {entry["note"]}', bg=C["card"],
                         fg=C["muted2"], font=("Segoe UI",9,"italic")).pack(anchor="w", pady=(2,0))

    # ── BODY WEIGHT ───────────────────────────
    def _build_bodyweight(self):
        page = self._make_page("bodyweight")
        scroll = self._scrollable(page)

        tk.Label(scroll, text="Body Weight Tracker", bg=C["bg"], fg=C["text"],
                 font=FONT_TITLE).pack(anchor="w", padx=20, pady=(16,4))

        # Input
        inp = card_frame(scroll, padx=16, pady=14)
        inp.pack(fill="x", padx=20, pady=(0,12))
        tk.Label(inp, text="Log Weight (kg):", bg=C["card"], fg=C["muted2"],
                 font=FONT_MED).pack(side="left", padx=(0,10))
        bw_entry = tk.Entry(inp, textvariable=self.bw_var, width=8, bg=C["bg3"],
                            fg=C["text"], font=FONT_MED, relief="flat",
                            insertbackground=C["text"],
                            highlightbackground=C["border"], highlightthickness=1)
        bw_entry.pack(side="left", padx=(0,10))
        styled_btn(inp, "Log", self._log_bodyweight, pad=(14,6)).pack(side="left")

        # Stats row
        self.bw_stats_frame = tk.Frame(scroll, bg=C["bg"])
        self.bw_stats_frame.pack(fill="x", padx=20, pady=(0,12))

        # Chart
        bw_chart_card = card_frame(scroll, padx=0, pady=0)
        bw_chart_card.pack(fill="x", padx=20, pady=(0,12))
        tk.Label(bw_chart_card, text="Weight Progress", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", padx=14, pady=(12,4))
        self.bw_canvas = tk.Canvas(bw_chart_card, bg=C["card"], height=200,
                                    highlightthickness=0)
        self.bw_canvas.pack(fill="x", padx=6, pady=(0,10))

        # Log
        tk.Label(scroll, text="Recent Entries", bg=C["bg"], fg=C["muted2"],
                 font=("Segoe UI",9,"bold")).pack(anchor="w", padx=20, pady=(0,4))
        self.bw_log_frame = tk.Frame(scroll, bg=C["bg"])
        self.bw_log_frame.pack(fill="x", padx=20, pady=(0,20))

    def _log_bodyweight(self):
        try:
            val = float(self.bw_var.get())
            entry = {"date": str(datetime.date.today()), "weight": val}
            self.data["bodyweight_log"].insert(0, entry)
            save_data(self.data)
            self.bw_var.set("")
            self._refresh_bodyweight()
            self._show_toast(f"✓ {val} kg logged!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    def _refresh_bodyweight(self):
        for w in self.bw_stats_frame.winfo_children():
            w.destroy()
        for w in self.bw_log_frame.winfo_children():
            w.destroy()

        log = self.data["bodyweight_log"]
        if log:
            weights = [e["weight"] for e in log]
            current = weights[0]
            lowest  = min(weights)
            highest = max(weights)
            change  = round(current - weights[-1], 1) if len(weights) > 1 else 0
            for col, (lbl, val, color) in enumerate([
                ("Current", f"{current} kg", C["text"]),
                ("Lowest",  f"{lowest} kg",  C["green"]),
                ("Highest", f"{highest} kg", C["red"]),
                ("Change",  f"{'+' if change>=0 else ''}{change} kg", C["orange"]),
            ]):
                c = card_frame(self.bw_stats_frame, padx=14, pady=10)
                c.grid(row=0, column=col, padx=5, sticky="ew")
                self.bw_stats_frame.columnconfigure(col, weight=1)
                tk.Label(c, text=val, bg=C["card"], fg=color,
                         font=("Segoe UI",18,"bold")).pack()
                tk.Label(c, text=lbl, bg=C["card"], fg=C["muted2"],
                         font=("Segoe UI",9)).pack()

            points = [(e["date"][5:], e["weight"]) for e in reversed(log[:20])]
            draw_line_chart(self.bw_canvas, points, color=C["blue"])

            for entry in log[:10]:
                r = card_frame(self.bw_log_frame, padx=12, pady=8)
                r.pack(fill="x", pady=2)
                tk.Label(r, text=entry["date"], bg=C["card"], fg=C["muted2"],
                         font=("Segoe UI",10)).pack(side="left")
                tk.Label(r, text=f'{entry["weight"]} kg', bg=C["card"], fg=C["text"],
                         font=("Segoe UI",11,"bold")).pack(side="right")
        else:
            draw_line_chart(self.bw_canvas, [])
            tk.Label(self.bw_log_frame, text="No entries yet. Log your weight above.",
                     bg=C["bg"], fg=C["muted"], font=FONT_MED).pack(pady=20)

    # ── AWARDS ────────────────────────────────
    def _build_awards(self):
        page = self._make_page("awards")
        scroll = self._scrollable(page)

        tk.Label(scroll, text="Achievements", bg=C["bg"], fg=C["text"],
                 font=FONT_TITLE).pack(anchor="w", padx=20, pady=(16,4))

        self.lbl_badges_count = tk.Label(scroll, text="", bg=C["bg"], fg=C["muted2"],
                                          font=FONT_MED)
        self.lbl_badges_count.pack(anchor="w", padx=20, pady=(0,12))

        self.badges_grid_frame = tk.Frame(scroll, bg=C["bg"])
        self.badges_grid_frame.pack(fill="x", padx=20, pady=(0,20))

    def _refresh_awards(self):
        for w in self.badges_grid_frame.winfo_children():
            w.destroy()
        earned = self.data["badges_earned"]
        self.lbl_badges_count.config(
            text=f"{len(earned)} / {len(BADGES)} badges earned")

        cols = 4
        for i, b in enumerate(BADGES):
            is_earned = b["id"] in earned
            row_i, col_i = divmod(i, cols)
            c = card_frame(self.badges_grid_frame, padx=10, pady=12)
            c.grid(row=row_i, column=col_i, padx=5, pady=5, sticky="nsew")
            self.badges_grid_frame.columnconfigure(col_i, weight=1)
            if is_earned:
                c.configure(highlightbackground=C["orange"])
            tk.Label(c, text=b["icon"], bg=C["card"],
                     font=("Segoe UI", 24)).pack()
            tk.Label(c, text=b["name"], bg=C["card"],
                     fg=C["text"] if is_earned else C["muted"],
                     font=("Segoe UI",10,"bold")).pack()
            tk.Label(c, text=b["desc"], bg=C["card"],
                     fg=C["muted2"] if is_earned else C["muted"],
                     font=("Segoe UI",8)).pack()
            if not is_earned:
                c.configure(bg=C["bg3"])
                for child in c.winfo_children():
                    child.configure(bg=C["bg3"])

    # ── TIMER ────────────────────────────────
    def _build_timer(self):
        page = self._make_page("timer")
        # Center content
        center = tk.Frame(page, bg=C["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="⏱ Rest Timer", bg=C["bg"], fg=C["text"],
                 font=("Segoe UI",20,"bold")).pack(pady=(0,20))

        self.timer_display = tk.Label(center, text="00:00", bg=C["bg"],
                                       fg=C["orange"], font=("Courier New",60,"bold"))
        self.timer_display.pack()

        self.timer_progress_canvas = tk.Canvas(center, bg=C["bg"], height=12,
                                                width=300, highlightthickness=0)
        self.timer_progress_canvas.pack(pady=10)

        self.lbl_timer_status = tk.Label(center, text="Set your rest duration",
                                          bg=C["bg"], fg=C["muted2"], font=FONT_MED)
        self.lbl_timer_status.pack(pady=4)

        # Presets
        preset_frame = tk.Frame(center, bg=C["bg"])
        preset_frame.pack(pady=12)
        tk.Label(preset_frame, text="Presets:", bg=C["bg"], fg=C["muted2"],
                 font=FONT_MED).pack(side="left", padx=(0,10))
        for label, secs in [("30s",30),("45s",45),("60s",60),("90s",90),("2m",120),("3m",180)]:
            styled_btn(preset_frame, label, lambda s=secs: self.quick_timer(s),
                       bg=C["bg3"], fg=C["muted2"], pad=(10,6)).pack(side="left", padx=3)

        # Custom
        custom_row = tk.Frame(center, bg=C["bg"])
        custom_row.pack(pady=8)
        tk.Label(custom_row, text="Custom (seconds):", bg=C["bg"],
                 fg=C["muted2"], font=FONT_MED).pack(side="left", padx=(0,8))
        self.custom_time_var = tk.StringVar(value="60")
        tk.Entry(custom_row, textvariable=self.custom_time_var, width=6,
                 bg=C["bg3"], fg=C["text"], font=FONT_MED, relief="flat",
                 insertbackground=C["text"],
                 highlightbackground=C["border"], highlightthickness=1).pack(side="left")
        styled_btn(custom_row, "Start", lambda: self.quick_timer(
            int(self.custom_time_var.get()) if self.custom_time_var.get().isdigit() else 60),
            pad=(14,6)).pack(side="left", padx=8)

        # Controls
        ctrl_row = tk.Frame(center, bg=C["bg"])
        ctrl_row.pack(pady=12)
        self.btn_pause = styled_btn(ctrl_row, "⏸ Pause", self._pause_timer,
                                     bg=C["bg3"], fg=C["muted2"], pad=(16,10))
        self.btn_pause.pack(side="left", padx=6)
        styled_btn(ctrl_row, "⏹ Stop", self._stop_timer,
                   bg=C["red"], fg=C["text"], pad=(16,10)).pack(side="left", padx=6)

        self._timer_paused = False
        self._timer_total  = 0
        self._timer_remain = 0

    def quick_timer(self, secs):
        self._stop_timer()
        self._timer_total  = secs
        self._timer_remain = secs
        self._timer_paused = False
        self.show_page("timer")
        self._run_timer()

    def _run_timer(self):
        if self._timer_remain <= 0:
            self.timer_display.config(text="00:00", fg=C["green"])
            self.lbl_timer_status.config(text="✓ Rest complete! Time to lift!")
            self.root.bell()
            return
        if self._timer_paused:
            return
        mins = self._timer_remain // 60
        secs = self._timer_remain % 60
        self.timer_display.config(text=f"{mins:02d}:{secs:02d}")

        # Progress bar
        self.timer_progress_canvas.delete("all")
        ratio = 1 - self._timer_remain / max(self._timer_total, 1)
        w = 300
        color = C["green"] if ratio > 0.6 else (C["yellow"] if ratio > 0.3 else C["red"])
        self.timer_progress_canvas.create_rectangle(0, 0, w, 12, fill=C["bg3"], outline="")
        self.timer_progress_canvas.create_rectangle(0, 0, int(w * ratio), 12,
                                                     fill=color, outline="")

        self.lbl_timer_status.config(
            text=f"Resting… {self._timer_remain}s remaining",
            fg=C["muted2"])
        self._timer_remain -= 1
        self.root.after(1000, self._run_timer)

    def _pause_timer(self):
        self._timer_paused = not self._timer_paused
        self.btn_pause.config(text="▶ Resume" if self._timer_paused else "⏸ Pause")
        if not self._timer_paused:
            self._run_timer()

    def _stop_timer(self):
        self._timer_remain = 0
        self._timer_paused = False
        self.timer_display.config(text="00:00", fg=C["orange"])
        self.lbl_timer_status.config(text="Timer stopped")

    # ── WORKOUTS ──────────────────────────────
    def _build_workouts(self):
        page = self._make_page("workouts")
        scroll = self._scrollable(page)

        tk.Label(scroll, text="Workout Builder", bg=C["bg"], fg=C["text"],
                 font=FONT_TITLE).pack(anchor="w", padx=20, pady=(16,4))
        tk.Label(scroll, text="Build custom workout plans from your favorite exercises.",
                 bg=C["bg"], fg=C["muted2"], font=FONT_MED).pack(anchor="w", padx=20, pady=(0,12))

        # Quick plans
        section_label(scroll, "  RECOMMENDED WORKOUT PLANS")
        plans_frame = tk.Frame(scroll, bg=C["bg"])
        plans_frame.pack(fill="x", padx=20, pady=(0,16))

        plans = [
            ("Push Day", ["Bench Press","Incline DB Press","Overhead Press",
                          "Tricep Dip","Tricep Pushdown","Lateral Raise"], C["orange"]),
            ("Pull Day", ["Pull-Up","Bent-Over Row","Lat Pulldown",
                          "Seated Cable Row","Barbell Curl","Hammer Curl"], C["blue"]),
            ("Leg Day",  ["Barbell Squat","Romanian Deadlift","Leg Press",
                          "Walking Lunge","Jump Squat","Bodyweight Calf Raise"], C["green"]),
            ("Core Blast",["Plank","Ab Wheel Rollout","Hanging Leg Raise",
                           "Bicycle Crunch","Russian Twist","Mountain Climber"], C["purple"]),
            ("Full Body", ["Deadlift","Bench Press","Pull-Up","Barbell Squat",
                           "Overhead Press","Plank"], C["yellow"]),
            ("Bodyweight Only", ["Push-Up","Pull-Up","Bodyweight Squat",
                                  "Dips","Diamond Push-Up","Plank","Burpee"], C["red"]),
        ]
        plans_frame.columnconfigure(0, weight=1)
        plans_frame.columnconfigure(1, weight=1)
        for i, (name, exercises, color) in enumerate(plans):
            row_i, col_i = divmod(i, 2)
            c = card_frame(plans_frame, padx=16, pady=14)
            c.grid(row=row_i, column=col_i, padx=5, pady=5, sticky="ew")
            tk.Label(c, text=name, bg=C["card"], fg=color,
                     font=("Segoe UI",13,"bold")).pack(anchor="w")
            tk.Label(c, text=" · ".join(exercises[:3]) + "…",
                     bg=C["card"], fg=C["muted2"], font=("Segoe UI",9),
                     wraplength=280).pack(anchor="w", pady=(4,8))
            styled_btn(c, "Load This Plan", lambda exs=exercises: self._load_plan(exs),
                       bg=color, fg="#000", pad=(12,6)).pack(anchor="w")

    def _load_plan(self, exercise_names):
        self.today_log.clear()
        for name in exercise_names:
            ex = next((e for e in EXERCISES if e["name"] == name), None)
            if ex:
                self.today_log.append(ex.copy())
        self._refresh_log_ui()
        self.show_page("log")
        self._show_toast(f"✓ Plan loaded — {len(self.today_log)} exercises!")

    # ── SETTINGS ──────────────────────────────
    def _build_settings(self):
        page = self._make_page("settings")
        scroll = self._scrollable(page)

        tk.Label(scroll, text="Settings", bg=C["bg"], fg=C["text"],
                 font=FONT_TITLE).pack(anchor="w", padx=20, pady=(16,4))

        # Profile
        prof = card_frame(scroll, padx=16, pady=14)
        prof.pack(fill="x", padx=20, pady=(0,12))
        tk.Label(prof, text="Profile", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,8))
        name_row = tk.Frame(prof, bg=C["card"])
        name_row.pack(fill="x")
        tk.Label(name_row, text="Username:", bg=C["card"], fg=C["text"],
                 font=FONT_MED).pack(side="left", padx=(0,10))
        self.username_entry = tk.Entry(name_row, bg=C["bg3"], fg=C["text"],
                                       font=FONT_MED, relief="flat", width=20,
                                       insertbackground=C["text"],
                                       highlightbackground=C["border"], highlightthickness=1)
        self.username_entry.insert(0, self.data.get("username", "Athlete"))
        self.username_entry.pack(side="left")
        styled_btn(name_row, "Save", self._save_username, pad=(12,6)).pack(side="left", padx=8)

        # Stats info
        info = card_frame(scroll, padx=16, pady=14)
        info.pack(fill="x", padx=20, pady=(0,12))
        tk.Label(info, text="Data", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,8))
        tk.Label(info, text=f"Data saved to: {DATA_FILE}",
                 bg=C["card"], fg=C["muted2"], font=("Segoe UI",9)).pack(anchor="w")
        styled_btn(info, "🗑 Reset All Data", self._reset_data,
                   bg=C["red"], fg=C["text"], pad=(12,6)).pack(anchor="w", pady=(10,0))

        # About
        about = card_frame(scroll, padx=16, pady=14)
        about.pack(fill="x", padx=20, pady=(0,20))
        tk.Label(about, text="About IronForge", bg=C["card"], fg=C["muted2"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,8))
        tk.Label(about, text="Version 2.0 — Built with Python & Tkinter\n"
                             "60 exercises · 9 muscle groups · Full XP system\n"
                             "Data stored locally on your machine.",
                 bg=C["card"], fg=C["muted2"], font=("Segoe UI",10),
                 justify="left").pack(anchor="w")

    def _save_username(self):
        name = self.username_entry.get().strip() or "Athlete"
        self.data["username"] = name
        save_data(self.data)
        self._show_toast(f"✓ Username saved: {name}")

    def _reset_data(self):
        if messagebox.askyesno("Reset Data",
                               "This will delete ALL your progress.\nAre you sure?"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            self.data = load_data()
            self._refresh_all()
            self._show_toast("✓ Data reset.")

    # ── BADGES ────────────────────────────────
    def _earn_badge(self, bid):
        if bid not in self.data["badges_earned"]:
            self.data["badges_earned"].append(bid)
            badge = next((b for b in BADGES if b["id"] == bid), None)
            if badge:
                self._show_toast(f"🏅 Badge Unlocked: {badge['name']}!")

    def _check_all_badges(self):
        d = self.data
        checks = [
            ("first",    d["workouts"] >= 1),
            ("streak3",  d["streak"] >= 3),
            ("streak7",  d["streak"] >= 7),
            ("streak30", d["streak"] >= 30),
            ("w5",       d["workouts"] >= 5),
            ("w10",      d["workouts"] >= 10),
            ("w50",      d["workouts"] >= 50),
            ("sets50",   d["total_sets"] >= 50),
            ("sets100",  d["total_sets"] >= 100),
            ("sets500",  d["total_sets"] >= 500),
            ("muscles9", len(d["muscle_sets"]) >= 9),
            ("xp500",    d["total_xp"] >= 500),
            ("xp5000",   d["total_xp"] >= 5000),
            ("level3",   d["level"] >= 2),
            ("level5",   d["level"] >= 4),
            ("bodyweight", d["bodyweight_workout_count"] >= 10),
            ("heavy",    d["gym_workout_count"] >= 10),
            ("variety",  len(d["unique_exercises"]) >= 20),
        ]
        for bid, cond in checks:
            if cond:
                self._earn_badge(bid)
        save_data(self.data)

    # ── XP BAR ───────────────────────────────
    def _draw_xp_bar(self):
        c = self.xp_canvas
        c.delete("all")
        w = c.winfo_width()
        if w <= 0: return
        lvl = self.data["level"]
        cur_req  = LEVELS[lvl][1]
        next_req = LEVELS[min(lvl+1, len(LEVELS)-1)][1]
        total = self.data["total_xp"]
        if next_req > cur_req:
            pct = min(1.0, (total - cur_req) / (next_req - cur_req))
        else:
            pct = 1.0
        c.create_rectangle(0, 0, w, 7, fill=C["bg3"], outline="")
        c.create_rectangle(0, 0, int(w * pct), 7, fill=C["orange"], outline="")

    # ── SHOW/HIDE PAGES ──────────────────────
    def show_page(self, key):
        for k, f in self.pages.items():
            f.pack_forget()
        if key in self.pages:
            self.pages[key].pack(fill="both", expand=True)
        for k, btn in self.nav_btns.items():
            btn.configure(fg=C["orange"] if k == key else C["muted2"],
                          bg=C["bg3"] if k == key else C["bg2"])
        titles = {
            "dashboard":"Dashboard","train":"Exercise Library","log":"Today's Log",
            "stats":"Statistics","history":"Workout History","bodyweight":"Body Weight",
            "awards":"Achievements","timer":"Rest Timer","workouts":"Workout Builder",
            "settings":"Settings",
        }
        self.lbl_title.config(text=titles.get(key, ""))

    # ── REFRESH ALL ──────────────────────────
    def _refresh_all(self):
        d = self.data
        # Sidebar
        lvl_name = LEVELS[d["level"]][0]
        self.lbl_level.config(text=f"⚡ {lvl_name}")
        self.lbl_xp.config(text=f"{d['total_xp']} XP")
        self.lbl_streak.config(text=f"🔥 {d['streak']}-day streak")
        self.lbl_workouts_side.config(text=f"{d['workouts']} workouts completed")
        self.root.after(50, self._draw_xp_bar)

        # Dashboard stats
        if hasattr(self, "dash_stat_cards"):
            self.dash_stat_cards["streak"].config(text=str(d["streak"]))
            self.dash_stat_cards["workouts"].config(text=str(d["workouts"]))
            self.dash_stat_cards["sets"].config(text=str(d["total_sets"]))
            self.dash_stat_cards["badges"].config(text=str(len(d["badges_earned"])))
            self.dash_stat_cards["xp"].config(text=str(d["total_xp"]))

        # Date
        if hasattr(self, "lbl_date"):
            self.lbl_date.config(
                text=datetime.datetime.now().strftime("%A, %B %d %Y"))

        # Recent workouts on dashboard
        if hasattr(self, "recent_frame"):
            for w in self.recent_frame.winfo_children():
                w.destroy()
            for entry in d["workout_history"][:5]:
                r = card_frame(self.recent_frame, padx=12, pady=8)
                r.pack(fill="x", pady=2)
                tk.Label(r, text=entry["date"], bg=C["card"], fg=C["muted2"],
                         font=("Segoe UI",10)).pack(side="left")
                tk.Label(r, text=f'{entry["sets"]} sets · +{entry["xp"]} XP',
                         bg=C["card"], fg=C["text"],
                         font=("Segoe UI",10,"bold")).pack(side="right")

        # Refresh exercise list
        if hasattr(self, "ex_list_inner"):
            self.refresh_exercise_list()

        self._refresh_log_ui()
        self._refresh_stats()
        self._refresh_history()
        self._refresh_bodyweight()
        self._refresh_awards()

    # ── TOAST ────────────────────────────────
    def _show_toast(self, msg):
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.configure(bg=C["orange"])
        lbl = tk.Label(toast, text=msg, bg=C["orange"], fg="#000",
                       font=("Segoe UI",11,"bold"), padx=20, pady=10)
        lbl.pack()
        # Position bottom-center
        self.root.update_idletasks()
        rx = self.root.winfo_x() + self.root.winfo_width()//2
        ry = self.root.winfo_y() + self.root.winfo_height() - 80
        toast.geometry(f"+{rx-150}+{ry}")
        toast.after(2200, toast.destroy)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
def main():
    root = tk.Tk()
    # Apply ttk dark style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground=C["bg3"], background=C["bg3"],
                    foreground=C["text"], selectbackground=C["bg3"],
                    selectforeground=C["text"], bordercolor=C["border"],
                    arrowcolor=C["muted2"])
    style.configure("TScrollbar",
                    background=C["bg3"], troughcolor=C["bg"],
                    bordercolor=C["bg"], arrowcolor=C["muted"])
    style.map("TCombobox", fieldbackground=[("readonly", C["bg3"])],
              foreground=[("readonly", C["text"])])

    app = IronForgeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()