"""
IronForge — Advanced Gym Tracker (Streamlit Web App)
Deploy on Render: https://render.com
"""

import streamlit as st
import json
import os
import datetime
import time
import random
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IronForge — Gym Tracker",
    page_icon="🏋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif !important;
    background-color: #0d0d0f !important;
    color: #f0f0f5 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111114 !important;
    border-right: 1px solid #2a2a32 !important;
}
section[data-testid="stSidebar"] * { color: #f0f0f5 !important; }

/* Main background */
.main .block-container {
    background: #0d0d0f !important;
    padding-top: 1.5rem !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #1e1e24 !important;
    border: 1px solid #2a2a32 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}
[data-testid="stMetricValue"] {
    color: #f97316 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] { color: #9898aa !important; }

/* Buttons */
.stButton > button {
    background: #f97316 !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 1px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: #ea580c !important;
    transform: translateY(-1px) !important;
}

/* Secondary buttons via data-secondary trick */
.btn-secondary .stButton > button {
    background: #1e1e24 !important;
    color: #9898aa !important;
    border: 1px solid #2a2a32 !important;
}
.btn-danger .stButton > button {
    background: #ef4444 !important;
    color: #fff !important;
}
.btn-green .stButton > button {
    background: #22c55e !important;
    color: #000 !important;
}
.btn-blue .stButton > button {
    background: #3b82f6 !important;
    color: #fff !important;
}

/* Selectbox / inputs */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1c1c21 !important;
    color: #f0f0f5 !important;
    border: 1px solid #2a2a32 !important;
    border-radius: 8px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #1e1e24 !important;
    border: 1px solid #2a2a32 !important;
    border-radius: 10px !important;
    color: #f0f0f5 !important;
}
.streamlit-expanderContent {
    background: #1a1a1f !important;
    border: 1px solid #2a2a32 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #111114 !important;
    border-bottom: 1px solid #2a2a32 !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b6b7e !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: #1e1e24 !important;
    color: #f97316 !important;
    border-bottom: 2px solid #f97316 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #0d0d0f !important;
    padding-top: 20px !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #f97316, #fbbf24) !important;
    border-radius: 4px !important;
}
.stProgress > div > div > div {
    background: #1c1c21 !important;
    border-radius: 4px !important;
}

/* Info / success / warning boxes */
.stAlert {
    background: #1e1e24 !important;
    border: 1px solid #2a2a32 !important;
    border-radius: 10px !important;
}

/* Divider */
hr { border-color: #2a2a32 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d0d0f; }
::-webkit-scrollbar-thumb { background: #2a2a32; border-radius: 3px; }

/* Card HTML blocks */
.if-card {
    background: #1e1e24;
    border: 1px solid #2a2a32;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.if-card-highlight {
    border-color: #f97316 !important;
    background: #f9731608 !important;
}
.if-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-right: 6px;
}
.tag-gym     { background:#3b82f610; color:#3b82f6; border:1px solid #3b82f633; }
.tag-body    { background:#22c55e10; color:#22c55e; border:1px solid #22c55e33; }
.tag-orange  { background:#f9731610; color:#f97316; border:1px solid #f9731633; }
.tag-green   { background:#22c55e10; color:#22c55e; border:1px solid #22c55e33; }
.tag-purple  { background:#a855f710; color:#a855f7; border:1px solid #a855f733; }
.if-title    { font-family:'Barlow Condensed',sans-serif; font-size:28px; font-weight:800; letter-spacing:2px; color:#f0f0f5; }
.if-muted    { color:#9898aa; font-size:13px; }
.if-orange   { color:#f97316; }
.badge-earned { background:#1e1e24; border:1px solid #f97316; border-radius:12px; padding:16px; text-align:center; }
.badge-locked { background:#151518; border:1px solid #2a2a32; border-radius:12px; padding:16px; text-align:center; opacity:0.45; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────
EXERCISES = [
    {"id":1, "name":"Bench Press",       "muscle":"Chest",    "eq":"gym",        "sets":4,"reps":"8-10", "rest":90, "xp":20, "tips":["Retract shoulder blades","Slight arch in lower back","Drive through heels","Touch bar to lower chest"]},
    {"id":2, "name":"Incline DB Press",  "muscle":"Chest",    "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":15, "tips":["Set bench at 30-45°","Elbows at 45°","Full range of motion","Squeeze at top"]},
    {"id":3, "name":"Push-Up",           "muscle":"Chest",    "eq":"bodyweight", "sets":4,"reps":"15-20","rest":60, "xp":10, "tips":["Core tight throughout","Elbows at 45°","Full range","Don't let hips sag"]},
    {"id":4, "name":"Wide Push-Up",      "muscle":"Chest",    "eq":"bodyweight", "sets":3,"reps":"12-15","rest":60, "xp":8,  "tips":["Hands wider than shoulder","Body straight","Controlled movement"]},
    {"id":5, "name":"Cable Flye",        "muscle":"Chest",    "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12, "tips":["Slight bend in elbows","Feel stretch at bottom","Squeeze at top"]},
    {"id":6, "name":"Dips",              "muscle":"Chest",    "eq":"gym",        "sets":3,"reps":"10-15","rest":75, "xp":15, "tips":["Lean forward for chest","Go deep for stretch","Control descent"]},
    {"id":7, "name":"Diamond Push-Up",   "muscle":"Chest",    "eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":10, "tips":["Diamond hand shape","Elbows close","Full extension"]},
    {"id":8, "name":"Pull-Up",           "muscle":"Back",     "eq":"bodyweight", "sets":4,"reps":"6-10", "rest":90, "xp":20, "tips":["Full dead hang","Pull elbows to hips","Avoid swinging"]},
    {"id":9, "name":"Bent-Over Row",     "muscle":"Back",     "eq":"gym",        "sets":4,"reps":"8-10", "rest":90, "xp":20, "tips":["Keep back flat","Hinge to 45°","Pull elbows behind body"]},
    {"id":10,"name":"Lat Pulldown",      "muscle":"Back",     "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":15, "tips":["Lean back 15°","Pull to upper chest","Full extension at top"]},
    {"id":11,"name":"Seated Cable Row",  "muscle":"Back",     "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":15, "tips":["Keep torso upright","Squeeze shoulder blades","Full stretch at front"]},
    {"id":12,"name":"Inverted Row",      "muscle":"Back",     "eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":12, "tips":["Keep body rigid","Pull chest to bar","Lower feet for more difficulty"]},
    {"id":13,"name":"Superman Hold",     "muscle":"Back",     "eq":"bodyweight", "sets":3,"reps":"12-15","rest":60, "xp":8,  "tips":["Hold peak 2 seconds","Don't strain neck","Breathe steadily"]},
    {"id":14,"name":"Single-Arm DB Row", "muscle":"Back",     "eq":"gym",        "sets":3,"reps":"10-12","rest":60, "xp":15, "tips":["Support with same-side hand","Pull elbow high and back","Keep back flat"]},
    {"id":15,"name":"Overhead Press",    "muscle":"Shoulders","eq":"gym",        "sets":4,"reps":"8-10", "rest":90, "xp":20, "tips":["Brace core hard","Press around face","Lock out completely"]},
    {"id":16,"name":"Lateral Raise",     "muscle":"Shoulders","eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12, "tips":["Lead with elbows","Stop at shoulder height","Control the negative"]},
    {"id":17,"name":"Arnold Press",      "muscle":"Shoulders","eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":15, "tips":["Start palms facing you","Rotate as you press","Full range"]},
    {"id":18,"name":"Pike Push-Up",      "muscle":"Shoulders","eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":10, "tips":["Hips high in air","Lower head toward floor","Works toward handstand"]},
    {"id":19,"name":"Front Raise",       "muscle":"Shoulders","eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":10, "tips":["Keep arms straight","Don't swing body","Control descent"]},
    {"id":20,"name":"Barbell Curl",      "muscle":"Biceps",   "eq":"gym",        "sets":4,"reps":"8-12", "rest":75, "xp":15, "tips":["Keep elbows fixed","Full range","Slow negative 3s"]},
    {"id":21,"name":"Hammer Curl",       "muscle":"Biceps",   "eq":"gym",        "sets":3,"reps":"10-12","rest":60, "xp":12, "tips":["Thumbs pointing up","Elbows at sides","Don't swing"]},
    {"id":22,"name":"Concentration Curl","muscle":"Biceps",   "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":10, "tips":["Full range","Squeeze peak contraction","Don't move upper arm"]},
    {"id":23,"name":"Chin-Up",           "muscle":"Biceps",   "eq":"bodyweight", "sets":3,"reps":"6-10", "rest":90, "xp":18, "tips":["Supinated grip","Full dead hang","Pull chest to bar"]},
    {"id":24,"name":"Tricep Dip",        "muscle":"Triceps",  "eq":"bodyweight", "sets":4,"reps":"12-15","rest":75, "xp":15, "tips":["Torso upright","Elbows close to body","Full extension"]},
    {"id":25,"name":"Skull Crusher",     "muscle":"Triceps",  "eq":"gym",        "sets":3,"reps":"10-12","rest":75, "xp":15, "tips":["Upper arms vertical","Only move at elbows","Lock out completely"]},
    {"id":26,"name":"Tricep Pushdown",   "muscle":"Triceps",  "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12, "tips":["Elbows fixed at sides","Full lockout at bottom","Control return"]},
    {"id":27,"name":"Close-Grip Push-Up","muscle":"Triceps",  "eq":"bodyweight", "sets":3,"reps":"12-15","rest":60, "xp":10, "tips":["Hands shoulder-width or closer","Elbows close","Full range"]},
    {"id":28,"name":"Overhead Extension","muscle":"Triceps",  "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12, "tips":["Upper arms close to head","Full stretch at bottom","Keep core tight"]},
    {"id":29,"name":"Barbell Squat",     "muscle":"Legs",     "eq":"gym",        "sets":4,"reps":"8-10", "rest":120,"xp":25, "tips":["Break at hips and knees together","Chest up","Drive through full foot"]},
    {"id":30,"name":"Romanian Deadlift", "muscle":"Legs",     "eq":"gym",        "sets":3,"reps":"10-12","rest":90, "xp":20, "tips":["Push hips back not down","Feel hamstring stretch","Bar close to legs"]},
    {"id":31,"name":"Leg Press",         "muscle":"Legs",     "eq":"gym",        "sets":4,"reps":"10-15","rest":90, "xp":18, "tips":["Feet shoulder-width","Go deep","Don't lock knees at top"]},
    {"id":32,"name":"Walking Lunge",     "muscle":"Legs",     "eq":"bodyweight", "sets":3,"reps":"12-16","rest":75, "xp":15, "tips":["Long steps","Back knee near floor","Torso upright"]},
    {"id":33,"name":"Bodyweight Squat",  "muscle":"Legs",     "eq":"bodyweight", "sets":4,"reps":"20-25","rest":45, "xp":8,  "tips":["Feet shoulder-width","Weight in heels","Go to parallel"]},
    {"id":34,"name":"Jump Squat",        "muscle":"Legs",     "eq":"bodyweight", "sets":3,"reps":"15",   "rest":60, "xp":12, "tips":["Land softly","Full squat depth","Arms assist the jump"]},
    {"id":35,"name":"Leg Extension",     "muscle":"Legs",     "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12, "tips":["Full extension with squeeze","Control the negative","Keep hips down"]},
    {"id":36,"name":"Plank",             "muscle":"Core",     "eq":"bodyweight", "sets":3,"reps":"45-60s","rest":45,"xp":8,  "tips":["Straight line head to heels","Squeeze glutes and abs","Don't hold breath"]},
    {"id":37,"name":"Hanging Leg Raise", "muscle":"Core",     "eq":"gym",        "sets":3,"reps":"10-15","rest":60, "xp":15, "tips":["Control the movement","Don't swing","Squeeze abs at top"]},
    {"id":38,"name":"Bicycle Crunch",    "muscle":"Core",     "eq":"bodyweight", "sets":3,"reps":"20-30","rest":45, "xp":8,  "tips":["Slow controlled rotation","Lower back pressed down","Hands light behind head"]},
    {"id":39,"name":"Ab Wheel Rollout",  "muscle":"Core",     "eq":"gym",        "sets":3,"reps":"10-15","rest":60, "xp":18, "tips":["Start from knees","Brace core hard","Don't let hips drop"]},
    {"id":40,"name":"Russian Twist",     "muscle":"Core",     "eq":"bodyweight", "sets":3,"reps":"20-30","rest":45, "xp":8,  "tips":["Lean back slightly","Feet can be elevated","Touch ground each side"]},
    {"id":41,"name":"Mountain Climber",  "muscle":"Core",     "eq":"bodyweight", "sets":3,"reps":"30",   "rest":45, "xp":10, "tips":["Keep hips level","Drive knees to chest","Increase speed for cardio"]},
    {"id":42,"name":"Dead Bug",          "muscle":"Core",     "eq":"bodyweight", "sets":3,"reps":"10-12","rest":45, "xp":10, "tips":["Press lower back to floor","Slow and controlled","Breathe out during extension"]},
    {"id":43,"name":"Hip Thrust",        "muscle":"Glutes",   "eq":"gym",        "sets":4,"reps":"10-15","rest":75, "xp":18, "tips":["Chin tucked","Squeeze hard at top 1s","Full hip extension"]},
    {"id":44,"name":"Glute Bridge",      "muscle":"Glutes",   "eq":"bodyweight", "sets":3,"reps":"20-25","rest":45, "xp":8,  "tips":["Drive through heels","Squeeze glutes at top","Add resistance to progress"]},
    {"id":45,"name":"Cable Kickback",    "muscle":"Glutes",   "eq":"gym",        "sets":3,"reps":"12-15","rest":60, "xp":12, "tips":["Keep torso stationary","Full extension","Control return"]},
    {"id":46,"name":"Donkey Kick",       "muscle":"Glutes",   "eq":"bodyweight", "sets":3,"reps":"15-20","rest":45, "xp":8,  "tips":["Core engaged","Kick to hip height","Don't rotate hips"]},
    {"id":47,"name":"Sumo Squat",        "muscle":"Glutes",   "eq":"bodyweight", "sets":3,"reps":"15-20","rest":60, "xp":10, "tips":["Toes out 45°","Push knees over toes","Full depth"]},
    {"id":48,"name":"Standing Calf Raise","muscle":"Calves",  "eq":"gym",        "sets":4,"reps":"15-20","rest":45, "xp":10, "tips":["Full range of motion","Pause at bottom for stretch","Vary foot positions"]},
    {"id":49,"name":"Seated Calf Raise", "muscle":"Calves",   "eq":"gym",        "sets":3,"reps":"15-20","rest":45, "xp":8,  "tips":["Full stretch at bottom","Controlled movement","Heavy weight works well"]},
    {"id":50,"name":"Bodyweight Calf Raise","muscle":"Calves","eq":"bodyweight", "sets":4,"reps":"25-30","rest":30, "xp":6,  "tips":["Use step for ROM","Slow descent","Try single leg"]},
    {"id":51,"name":"Burpee",            "muscle":"Full Body","eq":"bodyweight", "sets":3,"reps":"10-15","rest":60, "xp":15, "tips":["Explosive jump at top","Chest to floor","Consistent rhythm"]},
    {"id":52,"name":"Deadlift",          "muscle":"Full Body","eq":"gym",        "sets":4,"reps":"5-6",  "rest":120,"xp":30, "tips":["Bar over mid-foot","Hinge at hips first","Brace entire core","Lock hips at top"]},
    {"id":53,"name":"Kettlebell Swing",  "muscle":"Full Body","eq":"gym",        "sets":3,"reps":"15-20","rest":60, "xp":15, "tips":["Hinge not squat","Drive with hips","Arms are just a chain"]},
    {"id":54,"name":"Box Jump",          "muscle":"Full Body","eq":"gym",        "sets":3,"reps":"8-10", "rest":90, "xp":15, "tips":["Land softly with bent knees","Full extension at top","Step down don't jump"]},
    {"id":55,"name":"Jump Rope",         "muscle":"Full Body","eq":"bodyweight", "sets":3,"reps":"60s",  "rest":45, "xp":10, "tips":["Stay on balls of feet","Keep elbows close","Build to longer sets"]},
    {"id":56,"name":"Foam Roll Quads",   "muscle":"Recovery", "eq":"bodyweight", "sets":1,"reps":"60s",  "rest":0,  "xp":3,  "tips":["Slow rolling motions","Pause on tight spots","Breathe through discomfort"]},
    {"id":57,"name":"Hip Flexor Stretch","muscle":"Recovery", "eq":"bodyweight", "sets":2,"reps":"30s",  "rest":0,  "xp":3,  "tips":["Posterior pelvic tilt","Feel stretch in front hip","Hold 30-60s"]},
    {"id":58,"name":"Chest Opener",      "muscle":"Recovery", "eq":"bodyweight", "sets":2,"reps":"30s",  "rest":0,  "xp":3,  "tips":["Arms wide","Feel chest and bicep stretch","Don't hold breath"]},
    {"id":59,"name":"Spinal Twist",      "muscle":"Recovery", "eq":"bodyweight", "sets":2,"reps":"30s",  "rest":0,  "xp":3,  "tips":["Shoulders down","Breathe into the twist","Both sides equal"]},
    {"id":60,"name":"Child's Pose",      "muscle":"Recovery", "eq":"bodyweight", "sets":1,"reps":"60s",  "rest":0,  "xp":3,  "tips":["Arms extended overhead","Sink hips to heels","Deep belly breathing"]},
]

MUSCLES = ["All","Chest","Back","Shoulders","Biceps","Triceps","Legs","Core","Glutes","Calves","Full Body","Recovery"]

MUSCLE_ICONS = {
    "Chest":"🏋","Back":"🦅","Shoulders":"🤸","Biceps":"💪","Triceps":"⬇",
    "Legs":"🦵","Core":"🔆","Glutes":"🍑","Calves":"🦶","Full Body":"⚡","Recovery":"🧘","All":"✦",
}

LEVELS = [
    (0,     "NOVICE",       "#6b6b7e"),
    (500,   "BEGINNER",     "#3b82f6"),
    (1500,  "INTERMEDIATE", "#22c55e"),
    (3500,  "ADVANCED",     "#f97316"),
    (7000,  "EXPERT",       "#fbbf24"),
    (15000, "ELITE",        "#a855f7"),
    (30000, "LEGEND",       "#ef4444"),
]

BADGES = [
    {"id":"first",     "icon":"🎯","name":"First Blood",     "desc":"Complete 1 workout"},
    {"id":"streak3",   "icon":"🔥","name":"On Fire",          "desc":"3-day streak"},
    {"id":"streak7",   "icon":"⚡","name":"Week Warrior",     "desc":"7-day streak"},
    {"id":"streak30",  "icon":"💥","name":"Iron Routine",     "desc":"30-day streak"},
    {"id":"w5",        "icon":"💪","name":"Iron Will",        "desc":"5 workouts"},
    {"id":"w10",       "icon":"🏋","name":"Gym Rat",          "desc":"10 workouts"},
    {"id":"w50",       "icon":"👑","name":"Gym King",         "desc":"50 workouts"},
    {"id":"sets50",    "icon":"⚙","name":"Grinder",          "desc":"50 total sets"},
    {"id":"sets100",   "icon":"🏆","name":"Century Club",     "desc":"100 total sets"},
    {"id":"sets500",   "icon":"💎","name":"Diamond Sets",     "desc":"500 total sets"},
    {"id":"muscles9",  "icon":"🌟","name":"Complete Package", "desc":"Train all 9 muscles"},
    {"id":"xp500",     "icon":"📈","name":"XP Hunter",        "desc":"500 XP earned"},
    {"id":"xp5000",    "icon":"🚀","name":"XP Legend",        "desc":"5000 XP earned"},
    {"id":"level3",    "icon":"⬆","name":"Rising Star",      "desc":"Reach Intermediate"},
    {"id":"level5",    "icon":"🔱","name":"Expert Status",    "desc":"Reach Expert"},
    {"id":"variety",   "icon":"🎨","name":"Variety Pack",     "desc":"Log 20 different exercises"},
    {"id":"earlybird", "icon":"🌅","name":"Early Bird",       "desc":"Workout before 8am"},
    {"id":"nightowl",  "icon":"🦉","name":"Night Owl",        "desc":"Workout after 9pm"},
    {"id":"pr",        "icon":"🥇","name":"PR Setter",        "desc":"Save a personal record"},
    {"id":"planner",   "icon":"📋","name":"The Planner",      "desc":"Load a workout plan"},
]

WORKOUT_PLANS = {
    "💪 Push Day":       ["Bench Press","Incline DB Press","Overhead Press","Tricep Dip","Tricep Pushdown","Lateral Raise"],
    "🦅 Pull Day":       ["Pull-Up","Bent-Over Row","Lat Pulldown","Seated Cable Row","Barbell Curl","Hammer Curl"],
    "🦵 Leg Day":        ["Barbell Squat","Romanian Deadlift","Leg Press","Walking Lunge","Jump Squat","Standing Calf Raise"],
    "🔆 Core Blast":     ["Plank","Ab Wheel Rollout","Hanging Leg Raise","Bicycle Crunch","Russian Twist","Mountain Climber"],
    "⚡ Full Body":      ["Deadlift","Bench Press","Pull-Up","Barbell Squat","Overhead Press","Plank"],
    "🤸 Bodyweight Only":["Push-Up","Pull-Up","Bodyweight Squat","Tricep Dip","Diamond Push-Up","Plank","Burpee"],
    "🍑 Glute Focus":    ["Hip Thrust","Glute Bridge","Cable Kickback","Donkey Kick","Sumo Squat","Romanian Deadlift"],
    "🧘 Active Recovery":["Foam Roll Quads","Hip Flexor Stretch","Chest Opener","Spinal Twist","Child's Pose"],
}

MOTIVATIONS = [
    "Every rep counts. Every drop of sweat matters.",
    "The body achieves what the mind believes.",
    "Push yourself — no one else will do it for you.",
    "Strength comes from overcoming what you thought you couldn't.",
    "You didn't come this far to only come this far.",
    "The pain you feel today is the strength you feel tomorrow.",
    "Your only competition is who you were yesterday.",
    "Fall down seven times. Get up eight.",
    "Discipline is choosing between what you want now and what you want most.",
    "Champions keep playing until they get it right.",
]

DATA_FILE = "ironforge_data.json"

# ─────────────────────────────────────────────────────────────
# SESSION STATE + DATA PERSISTENCE
# ─────────────────────────────────────────────────────────────
def default_data():
    return {
        "username": "Athlete",
        "total_xp": 0,
        "level": 0,
        "streak": 0,
        "workouts": 0,
        "total_sets": 0,
        "muscle_sets": {},
        "badges_earned": [],
        "workout_history": [],
        "bodyweight_log": [],
        "personal_records": {},
        "last_workout_date": None,
        "unique_exercises": [],
        "bodyweight_wcount": 0,
        "gym_wcount": 0,
    }

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                d = json.load(f)
                base = default_data()
                base.update(d)
                return base
        except Exception:
            pass
    return default_data()

def save_data():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.data, f, indent=2)
    except Exception:
        pass  # Render free tier has ephemeral disk — data in session_state still works

def init_session():
    if "data" not in st.session_state:
        st.session_state.data = load_data()
    if "today_log" not in st.session_state:
        st.session_state.today_log = []
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None
    if "timer_duration" not in st.session_state:
        st.session_state.timer_duration = 60
    if "motivation" not in st.session_state:
        st.session_state.motivation = random.choice(MOTIVATIONS)

init_session()

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def get_level_info():
    xp = st.session_state.data["total_xp"]
    current = LEVELS[0]
    next_lv = LEVELS[1]
    for i, (req, name, color) in enumerate(LEVELS):
        if xp >= req:
            current = LEVELS[i]
            next_lv = LEVELS[min(i+1, len(LEVELS)-1)]
    cur_req  = current[0]
    next_req = next_lv[0]
    pct = min(1.0, (xp - cur_req) / max(next_req - cur_req, 1))
    return current[1], current[2], pct, next_req

def earn_badge(bid):
    d = st.session_state.data
    if bid not in d["badges_earned"]:
        d["badges_earned"].append(bid)
        badge = next((b for b in BADGES if b["id"] == bid), None)
        if badge:
            st.toast(f"🏅 Badge Unlocked: **{badge['name']}**!", icon="🏅")

def check_badges():
    d = st.session_state.data
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
        ("variety",  len(d["unique_exercises"]) >= 20),
    ]
    for bid, cond in checks:
        if cond:
            earn_badge(bid)

def plotly_defaults(fig):
    fig.update_layout(
        paper_bgcolor="#1e1e24",
        plot_bgcolor="#1e1e24",
        font_color="#9898aa",
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    fig.update_xaxes(gridcolor="#2a2a32", tickfont_color="#6b6b7e", linecolor="#2a2a32")
    fig.update_yaxes(gridcolor="#2a2a32", tickfont_color="#6b6b7e", linecolor="#2a2a32")
    return fig

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="if-title" style="color:#f97316;font-size:32px;letter-spacing:4px;">IRONFORGE</div>', unsafe_allow_html=True)
    st.markdown('<div class="if-muted" style="margin-bottom:16px;">Advanced Gym Tracker</div>', unsafe_allow_html=True)

    # Level & XP bar
    lv_name, lv_color, lv_pct, lv_next = get_level_info()
    st.markdown(f'<span style="color:{lv_color};font-family:\'Barlow Condensed\';font-weight:800;font-size:14px;letter-spacing:2px;">⚡ {lv_name}</span>', unsafe_allow_html=True)
    st.progress(lv_pct)
    st.markdown(f'<div class="if-muted" style="margin-top:-8px;margin-bottom:12px;">{st.session_state.data["total_xp"]} XP · next level at {lv_next}</div>', unsafe_allow_html=True)

    st.divider()

    pages = [
        "🏠 Dashboard",
        "💪 Exercise Library",
        "📋 Today's Log",
        "📊 Statistics",
        "📅 History",
        "⚖️ Body Weight",
        "🏅 Achievements",
        "⏱️ Rest Timer",
        "🔄 Workout Plans",
        "⚙️ Settings",
    ]
    selected = st.radio("", pages, label_visibility="collapsed",
                        index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
    st.session_state.page = selected

    st.divider()
    d = st.session_state.data
    st.markdown(f"""
    <div style="padding:4px 0;">
        <div style="color:#f0f0f5;font-size:16px;font-weight:700;">🔥 {d['streak']}-day streak</div>
        <div class="if-muted">{d['workouts']} workouts completed</div>
        <div class="if-muted">{len(d['badges_earned'])} / {len(BADGES)} badges</div>
    </div>
    """, unsafe_allow_html=True)

page = selected

# ─────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    d = st.session_state.data
    st.markdown(f'<div class="if-title">Welcome back, {d["username"]} 👋</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="if-muted" style="margin-bottom:24px;">{datetime.datetime.now().strftime("%A, %B %d %Y")} &nbsp;·&nbsp; {st.session_state.motivation}</div>', unsafe_allow_html=True)

    # Big stats
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("🔥 Day Streak",  d["streak"])
    with c2: st.metric("💪 Workouts",    d["workouts"])
    with c3: st.metric("⚙️ Total Sets",  d["total_sets"])
    with c4: st.metric("🏅 Badges",      len(d["badges_earned"]))
    with c5: st.metric("⚡ Total XP",    d["total_xp"])

    st.markdown("---")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("#### 🚀 Quick Actions")
        qa1, qa2 = st.columns(2)
        with qa1:
            if st.button("💪 Start Training", use_container_width=True):
                st.session_state.page = "💪 Exercise Library"
                st.rerun()
            if st.button("📊 View Stats", use_container_width=True):
                st.session_state.page = "📊 Statistics"
                st.rerun()
        with qa2:
            if st.button("📋 Today's Log", use_container_width=True):
                st.session_state.page = "📋 Today's Log"
                st.rerun()
            if st.button("⏱️ Rest Timer", use_container_width=True):
                st.session_state.page = "⏱️ Rest Timer"
                st.rerun()

        st.markdown("#### 💬 Motivation")
        st.info(f'*"{st.session_state.motivation}"*')
        if st.button("New Quote", key="new_quote"):
            st.session_state.motivation = random.choice(MOTIVATIONS)
            st.rerun()

    with col_b:
        st.markdown("#### 📅 Recent Workouts")
        history = d["workout_history"]
        if history:
            for entry in history[:5]:
                muscles_str = ", ".join(entry.get("muscles", [])[:3])
                note = f" · 📝 {entry['note']}" if entry.get("note") else ""
                st.markdown(f"""
                <div class="if-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#f97316;font-weight:700;">{entry['date']}</span>
                        <span style="color:#22c55e;font-weight:700;">+{entry['xp']} XP</span>
                    </div>
                    <div class="if-muted">{entry['sets']} sets · {muscles_str}{note}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="if-card if-muted">No workouts yet — go train! 💪</div>', unsafe_allow_html=True)

    # Today's log preview
    if st.session_state.today_log:
        st.markdown("---")
        st.markdown(f"#### 📋 Today's Log Preview — {len(st.session_state.today_log)} exercises queued")
        ex_names = " · ".join(e["name"] for e in st.session_state.today_log[:6])
        st.markdown(f'<div class="if-card">{ex_names}</div>', unsafe_allow_html=True)
        if st.button("Finish Workout →", key="dash_finish"):
            st.session_state.page = "📋 Today's Log"
            st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: EXERCISE LIBRARY
# ─────────────────────────────────────────────────────────────
elif page == "💪 Exercise Library":
    st.markdown('<div class="if-title">Exercise Library</div>', unsafe_allow_html=True)
    st.markdown('<div class="if-muted" style="margin-bottom:20px;">60 exercises across 12 categories</div>', unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3 = st.columns([2, 2, 3])
    with fc1:
        muscle_filter = st.selectbox("Muscle Group", MUSCLES, label_visibility="collapsed",
                                      placeholder="Muscle Group")
    with fc2:
        eq_filter = st.selectbox("Equipment", ["All", "gym", "bodyweight"], label_visibility="collapsed")
    with fc3:
        search = st.text_input("Search exercises…", placeholder="Search exercises…", label_visibility="collapsed")

    filtered = [e for e in EXERCISES
                if (muscle_filter == "All" or e["muscle"] == muscle_filter)
                and (eq_filter == "All" or e["eq"] == eq_filter)
                and (search.lower() in e["name"].lower() or search == "")]

    st.markdown(f'<div class="if-muted" style="margin-bottom:12px;">{len(filtered)} exercises found</div>', unsafe_allow_html=True)

    if not filtered:
        st.warning("No exercises match your filters.")
    else:
        for ex in filtered:
            eq_tag  = f'<span class="if-tag tag-gym">🔧 Gym</span>' if ex["eq"] == "gym" else f'<span class="if-tag tag-body">🤸 Bodyweight</span>'
            xp_tag  = f'<span class="if-tag tag-green">+{ex["xp"]} XP</span>'
            msc_tag = f'<span class="if-tag tag-orange">{ex["muscle"]}</span>'

            with st.expander(f"{MUSCLE_ICONS.get(ex['muscle'],'💪')}  {ex['name']}  —  {ex['sets']}×{ex['reps']}  ·  {ex['rest']}s rest"):
                dc1, dc2 = st.columns([3, 1])
                with dc1:
                    st.markdown(f"{msc_tag} {eq_tag} {xp_tag}", unsafe_allow_html=True)
                    st.markdown(f"**Sets:** {ex['sets']}  &nbsp;|&nbsp;  **Reps:** {ex['reps']}  &nbsp;|&nbsp;  **Rest:** {ex['rest']}s")
                    st.markdown("**Form Tips:**")
                    for tip in ex["tips"]:
                        st.markdown(f"→ {tip}")

                    # Personal record
                    pr = st.session_state.data["personal_records"].get(str(ex["id"]), {})
                    if pr:
                        pr_txt = []
                        if "weight" in pr: pr_txt.append(f"🥇 Best weight: **{pr['weight']} kg**")
                        if "reps"   in pr: pr_txt.append(f"🔢 Best reps: **{pr['reps']}**")
                        st.markdown("  ·  ".join(pr_txt))

                with dc2:
                    if st.button("+ Add to Log", key=f"add_{ex['id']}", use_container_width=True):
                        st.session_state.today_log.append(ex.copy())
                        st.toast(f"✓ {ex['name']} added! (+{ex['xp']} XP)", icon="💪")

                    if st.button("⏱ Set Timer", key=f"timer_{ex['id']}", use_container_width=True):
                        st.session_state.timer_end = time.time() + ex["rest"]
                        st.session_state.timer_duration = ex["rest"]
                        st.session_state.page = "⏱️ Rest Timer"
                        st.rerun()

                    st.markdown("**Update PR:**")
                    pr_w = st.number_input("Weight (kg)", min_value=0.0, step=0.5,
                                           key=f"pr_w_{ex['id']}", label_visibility="collapsed")
                    pr_r = st.number_input("Reps", min_value=0, step=1,
                                           key=f"pr_r_{ex['id']}", label_visibility="collapsed")
                    if st.button("Save PR", key=f"pr_save_{ex['id']}", use_container_width=True):
                        st.session_state.data["personal_records"][str(ex["id"])] = {
                            "weight": pr_w, "reps": pr_r
                        }
                        earn_badge("pr")
                        save_data()
                        st.success("PR saved! 🥇")

# ─────────────────────────────────────────────────────────────
# PAGE: TODAY'S LOG
# ─────────────────────────────────────────────────────────────
elif page == "📋 Today's Log":
    st.markdown('<div class="if-title">Today\'s Log</div>', unsafe_allow_html=True)
    today_log = st.session_state.today_log

    if not today_log:
        st.markdown('<div class="if-card" style="text-align:center;padding:48px;color:#6b6b7e;font-size:18px;">No exercises yet.<br>Go to Exercise Library and add some! 🏋</div>', unsafe_allow_html=True)
    else:
        sets_total = sum(e["sets"] for e in today_log)
        xp_total   = sum(e["xp"]   for e in today_log)
        st.markdown(f'<div class="if-muted" style="margin-bottom:16px;">{len(today_log)} exercises · {sets_total} sets · +{xp_total} XP today</div>', unsafe_allow_html=True)

        # Note
        note = st.text_input("📝 Workout Note (optional)", placeholder="e.g. Felt strong today, PR on bench…")

        for i, ex in enumerate(today_log):
            lc1, lc2, lc3 = st.columns([5, 2, 1])
            with lc1:
                st.markdown(f"""
                <div class="if-card">
                    <strong style="font-size:15px;">{MUSCLE_ICONS.get(ex['muscle'],'💪')} {ex['name']}</strong>
                    <span class="if-muted"> · {ex['muscle']} · {ex['sets']} sets × {ex['reps']} reps · +{ex['xp']} XP</span>
                </div>
                """, unsafe_allow_html=True)
            with lc2:
                if st.button(f"⏱ {ex['rest']}s rest", key=f"logtimer_{i}", use_container_width=True):
                    st.session_state.timer_end = time.time() + ex["rest"]
                    st.session_state.timer_duration = ex["rest"]
                    st.session_state.page = "⏱️ Rest Timer"
                    st.rerun()
            with lc3:
                if st.button("✕", key=f"del_{i}", use_container_width=True):
                    st.session_state.today_log.pop(i)
                    st.rerun()

        st.markdown("---")
        fa, fb, fc = st.columns([3, 2, 2])
        with fa:
            if st.button("✅ Finish & Save Workout", use_container_width=True):
                d = st.session_state.data
                sets_total = sum(e["sets"]   for e in today_log)
                xp_total   = sum(e["xp"]     for e in today_log)
                muscles    = list(set(e["muscle"] for e in today_log))
                bonus_xp   = 50
                total_xp   = xp_total + bonus_xp

                d["workouts"]   += 1
                d["total_sets"] += sets_total
                d["total_xp"]   += total_xp

                for m in muscles:
                    d["muscle_sets"][m] = d["muscle_sets"].get(m, 0) + sets_total
                for ex in today_log:
                    if str(ex["id"]) not in d["unique_exercises"]:
                        d["unique_exercises"].append(str(ex["id"]))

                today_str = str(datetime.date.today())
                yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                if d["last_workout_date"] == yesterday:
                    d["streak"] += 1
                elif d["last_workout_date"] != today_str:
                    d["streak"] = 1
                d["last_workout_date"] = today_str

                hour = datetime.datetime.now().hour
                if hour < 8:   earn_badge("earlybird")
                if hour >= 21: earn_badge("nightowl")

                # Update level
                for i, (req, name, _) in reversed(list(enumerate(LEVELS))):
                    if d["total_xp"] >= req:
                        d["level"] = i
                        break

                entry = {
                    "date": today_str,
                    "exercises": [e["name"] for e in today_log],
                    "sets": sets_total,
                    "xp": total_xp,
                    "muscles": muscles,
                    "note": note,
                }
                d["workout_history"].insert(0, entry)
                check_badges()
                save_data()
                st.session_state.today_log = []
                st.success(f"🏆 Workout saved! {sets_total} sets · +{total_xp} XP earned!")
                st.balloons()
                st.rerun()

        with fb:
            if st.button("🗑️ Clear Log", use_container_width=True):
                st.session_state.today_log = []
                st.rerun()
        with fc:
            if st.button("+ Add More Exercises", use_container_width=True):
                st.session_state.page = "💪 Exercise Library"
                st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: STATISTICS
# ─────────────────────────────────────────────────────────────
elif page == "📊 Statistics":
    st.markdown('<div class="if-title">Statistics</div>', unsafe_allow_html=True)
    d = st.session_state.data

    # Overview metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Total Workouts", d["workouts"])
    with m2: st.metric("Day Streak",     d["streak"])
    with m3: st.metric("Total Sets",     d["total_sets"])
    with m4: st.metric("Total XP",       d["total_xp"])

    st.markdown("---")

    # Charts row 1
    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown("#### 💪 Muscle Groups (Sets)")
        ms = d["muscle_sets"]
        if ms:
            sorted_ms = sorted(ms.items(), key=lambda x: x[1], reverse=True)
            fig = go.Figure(go.Bar(
                x=[k for k,v in sorted_ms],
                y=[v for k,v in sorted_ms],
                marker_color=["#f97316","#3b82f6","#22c55e","#a855f7",
                               "#fbbf24","#ef4444","#14b8a6","#ec4899","#8b5cf6","#f97316","#22c55e","#3b82f6"],
                text=[v for k,v in sorted_ms],
                textposition="outside",
                textfont_color="#9898aa",
            ))
            plotly_defaults(fig)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet. Complete a workout first!")

    with ch2:
        st.markdown("#### 🍩 Muscle Share")
        ms = d["muscle_sets"]
        if ms:
            colors = ["#f97316","#3b82f6","#22c55e","#a855f7","#fbbf24",
                      "#ef4444","#14b8a6","#ec4899","#8b5cf6","#f97316"]
            fig = go.Figure(go.Pie(
                labels=list(ms.keys()),
                values=list(ms.values()),
                hole=0.5,
                marker_colors=colors[:len(ms)],
                textfont_size=12,
            ))
            plotly_defaults(fig)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet.")

    # Charts row 2
    ch3, ch4 = st.columns(2)

    with ch3:
        st.markdown("#### 📅 Workout Frequency (Last 21 Days)")
        today = datetime.date.today()
        dates = [(today - datetime.timedelta(days=i)) for i in range(20, -1, -1)]
        history_dates = set(e["date"] for e in d["workout_history"])
        freq = [1 if str(dd) in history_dates else 0 for dd in dates]
        labels = [str(dd)[5:] for dd in dates]
        fig = go.Figure(go.Bar(
            x=labels, y=freq,
            marker_color=["#f97316" if v else "#2a2a32" for v in freq],
        ))
        plotly_defaults(fig)
        fig.update_layout(height=250, yaxis_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with ch4:
        st.markdown("#### ⚡ XP Per Workout (Last 15)")
        history = d["workout_history"][:15][::-1]
        if history:
            fig = go.Figure(go.Scatter(
                x=[e["date"][5:] for e in history],
                y=[e["xp"] for e in history],
                mode="lines+markers",
                line=dict(color="#f97316", width=2),
                marker=dict(color="#f97316", size=8),
                fill="tozeroy",
                fillcolor="#f9731620",
            ))
            plotly_defaults(fig)
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No workout data yet.")

    # PRs table
    st.markdown("#### 🥇 Personal Records")
    prs = d["personal_records"]
    if prs:
        pr_rows = []
        for ex_id, pr in prs.items():
            ex = next((e for e in EXERCISES if str(e["id"]) == ex_id), None)
            if ex:
                pr_rows.append({
                    "Exercise": ex["name"],
                    "Muscle": ex["muscle"],
                    "Best Weight (kg)": pr.get("weight", "—"),
                    "Best Reps": pr.get("reps", "—"),
                })
        if pr_rows:
            import pandas as pd
            st.dataframe(pd.DataFrame(pr_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No PRs saved yet. Use the Exercise Library to set personal records.")

# ─────────────────────────────────────────────────────────────
# PAGE: HISTORY
# ─────────────────────────────────────────────────────────────
elif page == "📅 History":
    st.markdown('<div class="if-title">Workout History</div>', unsafe_allow_html=True)
    history = st.session_state.data["workout_history"]
    if not history:
        st.markdown('<div class="if-card" style="text-align:center;padding:48px;color:#6b6b7e;">No workouts recorded yet.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="if-muted" style="margin-bottom:16px;">{len(history)} workouts on record</div>', unsafe_allow_html=True)
        for entry in history[:50]:
            muscles_str  = ", ".join(entry.get("muscles", []))
            exercises_str = ", ".join(entry["exercises"][:5])
            if len(entry["exercises"]) > 5:
                exercises_str += f" +{len(entry['exercises'])-5} more"
            note_html = f'<div style="color:#6b6b7e;font-size:12px;margin-top:4px;">📝 {entry["note"]}</div>' if entry.get("note") else ""
            st.markdown(f"""
            <div class="if-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:#f97316;font-family:\'Barlow Condensed\';font-weight:800;font-size:16px;">{entry['date']}</span>
                    <span style="color:#22c55e;font-weight:700;">+{entry['xp']} XP</span>
                </div>
                <div style="color:#9898aa;margin-top:4px;">{entry['sets']} sets · {muscles_str}</div>
                <div style="color:#6b6b7e;font-size:12px;margin-top:3px;">{exercises_str}</div>
                {note_html}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: BODY WEIGHT
# ─────────────────────────────────────────────────────────────
elif page == "⚖️ Body Weight":
    st.markdown('<div class="if-title">Body Weight Tracker</div>', unsafe_allow_html=True)
    d = st.session_state.data

    bw_c1, bw_c2 = st.columns([1, 3])
    with bw_c1:
        st.markdown("#### Log Today")
        weight_input = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0,
                                        step=0.1, value=70.0)
        if st.button("Log Weight", use_container_width=True):
            entry = {"date": str(datetime.date.today()), "weight": weight_input}
            d["bodyweight_log"].insert(0, entry)
            save_data()
            st.toast(f"✓ {weight_input} kg logged!", icon="⚖️")
            st.rerun()

    log = d["bodyweight_log"]
    if log:
        weights = [e["weight"] for e in log]

        with bw_c2:
            m1, m2, m3, m4 = st.columns(4)
            change = round(weights[0] - weights[-1], 1) if len(weights) > 1 else 0
            with m1: st.metric("Current",  f"{weights[0]} kg")
            with m2: st.metric("Lowest",   f"{min(weights)} kg", delta=None)
            with m3: st.metric("Highest",  f"{max(weights)} kg", delta=None)
            with m4: st.metric("Total Change", f"{'+' if change>=0 else ''}{change} kg")

        # Chart
        import pandas as pd
        df = pd.DataFrame(reversed(log[:30]))
        fig = go.Figure(go.Scatter(
            x=df["date"], y=df["weight"],
            mode="lines+markers",
            line=dict(color="#3b82f6", width=2),
            marker=dict(color="#3b82f6", size=7),
            fill="tozeroy", fillcolor="#3b82f620",
        ))
        plotly_defaults(fig)
        fig.update_layout(title="Weight Progress", height=300)
        st.plotly_chart(fig, use_container_width=True)

        # Table
        st.markdown("#### Recent Entries")
        for entry in log[:15]:
            st.markdown(f"""
            <div class="if-card" style="display:flex;justify-content:space-between;padding:10px 20px;">
                <span style="color:#9898aa;">{entry['date']}</span>
                <span style="color:#3b82f6;font-weight:700;font-size:16px;">{entry['weight']} kg</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No weight entries yet. Log your first measurement above!")

# ─────────────────────────────────────────────────────────────
# PAGE: ACHIEVEMENTS
# ─────────────────────────────────────────────────────────────
elif page == "🏅 Achievements":
    d = st.session_state.data
    earned = d["badges_earned"]
    st.markdown('<div class="if-title">Achievements</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="if-muted" style="margin-bottom:24px;">{len(earned)} / {len(BADGES)} badges earned</div>', unsafe_allow_html=True)

    # Progress bar
    st.progress(len(earned) / len(BADGES))
    st.markdown("---")

    cols_per_row = 4
    rows = [BADGES[i:i+cols_per_row] for i in range(0, len(BADGES), cols_per_row)]
    for row in rows:
        cols = st.columns(cols_per_row)
        for col, badge in zip(cols, row):
            is_earned = badge["id"] in earned
            css_class = "badge-earned" if is_earned else "badge-locked"
            col.markdown(f"""
            <div class="{css_class}">
                <div style="font-size:32px;">{badge['icon']}</div>
                <div style="font-weight:700;margin-top:8px;color:{'#f0f0f5' if is_earned else '#6b6b7e'};">{badge['name']}</div>
                <div style="font-size:12px;color:#6b6b7e;margin-top:4px;">{badge['desc']}</div>
                {"<div style='color:#22c55e;font-size:11px;margin-top:6px;'>✓ Earned</div>" if is_earned else ""}
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: REST TIMER
# ─────────────────────────────────────────────────────────────
elif page == "⏱️ Rest Timer":
    st.markdown('<div class="if-title" style="text-align:center;">⏱️ Rest Timer</div>', unsafe_allow_html=True)

    # Presets
    st.markdown("#### Quick Presets")
    pc = st.columns(6)
    for i, (label, secs) in enumerate([("30s",30),("45s",45),("60s",60),("90s",90),("2 min",120),("3 min",180)]):
        if pc[i].button(label, use_container_width=True, key=f"preset_{secs}"):
            st.session_state.timer_end = time.time() + secs
            st.session_state.timer_duration = secs
            st.rerun()

    # Custom
    st.markdown("#### Custom Duration")
    tc1, tc2 = st.columns([2, 1])
    with tc1:
        custom_secs = st.number_input("Seconds", min_value=5, max_value=600,
                                       value=st.session_state.timer_duration, step=5)
    with tc2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶ Start", use_container_width=True, key="start_custom"):
            st.session_state.timer_end = time.time() + custom_secs
            st.session_state.timer_duration = custom_secs
            st.rerun()

    st.markdown("---")

    # Display
    timer_placeholder = st.empty()
    prog_placeholder  = st.empty()
    status_placeholder = st.empty()

    end = st.session_state.timer_end
    if end:
        remaining = end - time.time()
        if remaining > 0:
            mins = int(remaining) // 60
            secs = int(remaining) % 60
            pct  = 1 - remaining / st.session_state.timer_duration
            timer_placeholder.markdown(f"""
            <div style="text-align:center;font-family:'Barlow Condensed';font-size:80px;
                        font-weight:800;color:#f97316;letter-spacing:4px;
                        padding:20px;background:#1e1e24;border-radius:16px;border:1px solid #2a2a32;">
                {mins:02d}:{secs:02d}
            </div>
            """, unsafe_allow_html=True)
            prog_placeholder.progress(min(pct, 1.0))
            status_placeholder.markdown(f'<div style="text-align:center;color:#9898aa;margin-top:8px;">{int(remaining)}s remaining</div>', unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.timer_end = None
            timer_placeholder.markdown("""
            <div style="text-align:center;font-family:'Barlow Condensed';font-size:80px;
                        font-weight:800;color:#22c55e;letter-spacing:4px;
                        padding:20px;background:#1e1e24;border-radius:16px;border:1px solid #22c55e;">
                00:00
            </div>
            """, unsafe_allow_html=True)
            status_placeholder.success("✅ Rest complete! Time to lift!")
    else:
        timer_placeholder.markdown("""
        <div style="text-align:center;font-family:'Barlow Condensed';font-size:80px;
                    font-weight:800;color:#2a2a32;letter-spacing:4px;
                    padding:20px;background:#1e1e24;border-radius:16px;border:1px solid #2a2a32;">
            00:00
        </div>
        """, unsafe_allow_html=True)
        status_placeholder.markdown('<div style="text-align:center;color:#6b6b7e;">Choose a duration above to start</div>', unsafe_allow_html=True)

    if end and st.button("⏹ Stop Timer", key="stop_timer"):
        st.session_state.timer_end = None
        st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: WORKOUT PLANS
# ─────────────────────────────────────────────────────────────
elif page == "🔄 Workout Plans":
    st.markdown('<div class="if-title">Workout Plans</div>', unsafe_allow_html=True)
    st.markdown('<div class="if-muted" style="margin-bottom:24px;">Load a pre-built plan straight into today\'s log</div>', unsafe_allow_html=True)

    plan_cols = st.columns(2)
    for i, (plan_name, exercises) in enumerate(WORKOUT_PLANS.items()):
        with plan_cols[i % 2]:
            ex_list = [e for e in EXERCISES if e["name"] in exercises]
            total_sets = sum(e["sets"] for e in ex_list)
            total_xp   = sum(e["xp"]   for e in ex_list)

            with st.container():
                st.markdown(f"""
                <div class="if-card">
                    <div style="color:#f97316;font-family:'Barlow Condensed';font-size:20px;font-weight:800;">{plan_name}</div>
                    <div style="color:#9898aa;font-size:12px;margin-top:4px;">{len(ex_list)} exercises · {total_sets} sets · +{total_xp} XP</div>
                    <div style="color:#6b6b7e;font-size:12px;margin-top:6px;">{' · '.join(exercises[:4])}{'…' if len(exercises)>4 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Load Plan", key=f"plan_{i}", use_container_width=True):
                    st.session_state.today_log = [e.copy() for e in ex_list]
                    earn_badge("planner")
                    save_data()
                    st.session_state.page = "📋 Today's Log"
                    st.toast(f"✓ {plan_name} loaded — {len(ex_list)} exercises!", icon="📋")
                    st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE: SETTINGS
# ─────────────────────────────────────────────────────────────
elif page == "⚙️ Settings":
    st.markdown('<div class="if-title">Settings</div>', unsafe_allow_html=True)
    d = st.session_state.data

    st.markdown("#### 👤 Profile")
    new_name = st.text_input("Username", value=d.get("username", "Athlete"))
    if st.button("Save Username"):
        d["username"] = new_name
        save_data()
        st.success(f"✓ Username updated to **{new_name}**")

    st.markdown("---")
    st.markdown("#### 📦 Data")
    st.markdown(f"""
    <div class="if-card">
        <div style="color:#9898aa;">Data file: <code style="color:#f97316;">{os.path.abspath(DATA_FILE)}</code></div>
        <div style="color:#6b6b7e;font-size:12px;margin-top:6px;">
            ⚠️ On Render's free tier, the filesystem is ephemeral — data may reset on re-deploy.
            Upgrade to a paid plan with a Persistent Disk, or connect a database for permanent storage.
        </div>
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("📥 Export Data (JSON)"):
            st.download_button(
                "⬇️ Download ironforge_data.json",
                data=json.dumps(d, indent=2),
                file_name="ironforge_data.json",
                mime="application/json",
            )
    with sc2:
        uploaded = st.file_uploader("📤 Import Data (JSON)", type="json", label_visibility="collapsed")
        if uploaded:
            try:
                imported = json.load(uploaded)
                st.session_state.data.update(imported)
                save_data()
                st.success("✓ Data imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Import failed: {e}")

    st.markdown("---")
    st.markdown("#### ⚠️ Danger Zone")
    if st.button("🗑️ Reset All Data", type="secondary"):
        if st.button("⚠️ Confirm Reset — This cannot be undone!", type="secondary"):
            st.session_state.data = default_data()
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.session_state.today_log = []
            st.success("Data reset.")
            st.rerun()

    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.markdown("""
    <div class="if-card">
        <div style="color:#f97316;font-family:'Barlow Condensed';font-size:18px;font-weight:800;">IRONFORGE v2.0</div>
        <div style="color:#9898aa;margin-top:6px;">Built with Python · Streamlit · Plotly</div>
        <div style="color:#6b6b7e;font-size:12px;margin-top:6px;">
            60 exercises · 9 muscle groups · 20 badges · Full XP system<br>
            Data stored locally in JSON · Deploy anywhere
        </div>
    </div>
    """, unsafe_allow_html=True)