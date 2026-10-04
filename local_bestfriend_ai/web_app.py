"""
Local Best Friend AI: Cozy Artisanal Café AI Companion (Café Dora)
Claymorphic & Glassmorphic Interactive UI/UX with 3D Three.js Barista Avatar,
English Cognitive Brain reasoning, real-time multilingual dialect mirroring,
ambient café soundscapes, voice acoustics, and offline SQLite Life Diary.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import json
import time
import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from core.cognitive_brain import CognitiveBrain
from core.memory_manager import MemoryManager
from core.rag_engine import LocalRAGEngine
from core.superpowers import SuperpowersHub
from chat import BestFriendChat

app = FastAPI(title="Café Dora: Local Best Friend AI Companion")

# Initialize central conversational chat engine
chat_engine = BestFriendChat()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>☕ Café Dora: Cozy Artisanal Best Friend AI</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>
  
  <!-- Marked.js for rich technical Markdown formatting -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <!-- Three.js (r160 with full CapsuleGeometry support) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"></script>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "primary": "#99415a",
            "primary-container": "#f78da7",
            "on-primary": "#ffffff",
            "on-primary-container": "#73243c",
            "primary-fixed": "#ffd9e0",
            "secondary": "#805345",
            "secondary-container": "#fdc1af",
            "on-secondary-container": "#794d3f",
            "tertiary": "#4e6446",
            "tertiary-container": "#9cb491",
            "on-tertiary-container": "#32462b",
            "tertiary-fixed": "#d1eac4",
            "on-tertiary-fixed": "#0d2008",
            "background": "#fff8f7",
            "on-background": "#2d1513",
            "surface": "#fff8f7",
            "on-surface": "#2d1513",
            "on-surface-variant": "#544245",
            "surface-container-lowest": "#ffffff",
            "surface-container-low": "#fff0ee",
            "surface-container": "#ffe9e6",
            "surface-container-high": "#ffe2de",
            "surface-container-highest": "#ffdad6",
            "outline": "#877275",
            "outline-variant": "#d9c0c4"
          },
          borderRadius: {
            DEFAULT: "1rem",
            lg: "2rem",
            xl: "3rem",
            full: "9999px"
          },
          spacing: {
            gutter: "1.25rem",
            "space-xs": "0.375rem",
            "space-sm": "0.75rem",
            "space-md": "1.25rem",
            "space-lg": "1.75rem",
            "space-xl": "2.5rem"
          },
          fontFamily: {
            sans: ["Plus Jakarta Sans", "sans-serif"],
            mono: ["JetBrains Mono", "monospace"]
          }
        }
      }
    };
  </script>
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      overscroll-behavior: none;
      transition: background-color 0.5s ease;
    }
    ::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(128, 83, 69, 0.2);
      border-radius: 10px;
    }
    .clay-surface {
      box-shadow: inset 2px 2px 4px rgba(255, 255, 255, 0.9), 0 8px 20px -4px rgba(74, 46, 43, 0.08);
    }
    .clay-button {
      box-shadow: inset 1px 1px 2px rgba(255, 255, 255, 0.8), 0 4px 10px -2px rgba(153, 65, 90, 0.25);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .clay-button:active {
      transform: scale(0.96);
      box-shadow: inset 2px 2px 4px rgba(74, 46, 43, 0.15);
    }
    .clay-input {
      box-shadow: inset 2px 2px 5px rgba(74, 46, 43, 0.08);
    }
    /* Thought Accordion inside chat bubbles */
    .thought-pill {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      background: rgba(153, 65, 90, 0.08);
      border: 1px dashed rgba(153, 65, 90, 0.3);
      border-radius: 10px;
      padding: 6px 10px;
      color: #99415a;
      cursor: pointer;
      margin-bottom: 6px;
      transition: all 0.2s;
    }
    .thought-pill:hover {
      background: rgba(153, 65, 90, 0.14);
      border-color: #99415a;
    }
    .thought-details {
      display: none;
      margin-top: 6px;
      padding-top: 6px;
      border-top: 1px dashed rgba(153, 65, 90, 0.2);
      white-space: pre-wrap;
      line-height: 1.4;
      color: #544245;
    }
    /* Markdown code blocks */
    .chat-bubble-markdown pre {
      background: #2d1513;
      color: #fff0ee;
      padding: 10px 12px;
      border-radius: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      overflow-x: auto;
      margin: 8px 0;
      position: relative;
    }
    .chat-bubble-markdown code {
      font-family: 'JetBrains Mono', monospace;
      background: rgba(153, 65, 90, 0.1);
      color: #99415a;
      padding: 1px 5px;
      border-radius: 4px;
      font-size: 0.85em;
    }
    .chat-bubble-markdown pre code {
      background: transparent;
      color: #ffe9e6;
      padding: 0;
    }
    .chat-bubble-markdown p {
      margin-bottom: 6px;
    }
    .chat-bubble-markdown p:last-child {
      margin-bottom: 0;
    }
    .chat-bubble-markdown strong {
      color: #2d1513;
      font-weight: 700;
    }
    .chat-bubble-markdown a {
      color: #99415a;
      text-decoration: underline;
      font-weight: 600;
    }
  </style>
</head>
<body class="bg-background font-sans text-on-surface antialiased selection:bg-primary-container selection:text-on-primary-container">

  <!-- Top Fixed Header -->
  <header class="fixed top-0 inset-x-0 z-50 bg-surface/85 backdrop-blur-xl shadow-[0_4px_20px_-2px_rgba(74,46,43,0.06)] border-b border-surface-container">
    <div class="h-20 max-w-[880px] mx-auto px-gutter flex items-center justify-between gap-space-sm">
      <div class="flex items-center gap-space-sm">
        <div class="flex items-center gap-2 px-space-sm py-1.5 rounded-full bg-surface-container-low shadow-[inset_2px_2px_4px_rgba(255,255,255,0.9),0_4px_12px_-2px_rgba(74,46,43,0.08)]">
          <span class="text-xl leading-none">☕</span>
          <span class="font-bold text-lg text-primary tracking-tight" id="companion-header-name">Café Dora</span>
        </div>
        <div class="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container text-on-surface-variant shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
          <span class="w-2.5 h-2.5 rounded-full bg-tertiary-container animate-pulse" id="header-pulse-dot"></span>
          <span class="text-xs uppercase tracking-wide font-semibold" id="barista-status-label">Phi-3 3.8B • GPU Active</span>
        </div>
      </div>

      <!-- Navigation & Mode Tabs -->
      <nav class="flex items-center gap-1 bg-surface-container-low/90 p-1 rounded-full shadow-[inset_2px_2px_4px_rgba(74,46,43,0.06)]">
        <button class="px-space-sm py-1 rounded-full text-xs font-bold transition-all bg-primary-container text-on-primary-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]" onclick="scrollToChat()">Dialogue</button>
        <button class="px-space-sm py-1 rounded-full text-xs text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-all font-semibold" onclick="openChaiChillModal()">Chai & Chill</button>
        <button class="px-space-sm py-1 rounded-full text-xs text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-all font-semibold" onclick="openStatsModal()">Life Diary</button>
      </nav>

      <!-- Right Header Actions: Theme dots, Lo-Fi toggle, Clock -->
      <div class="flex items-center gap-space-xs">
        <div class="hidden md:flex items-center gap-1.5 p-1 bg-surface-container rounded-full">
          <button aria-label="Strawberry Pink" class="w-5 h-5 rounded-full bg-[#f78da7] shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9)] hover:scale-110 active:scale-95 transition-transform" onclick="switchCafeTheme('strawberry')" title="Strawberry Latte"></button>
          <button aria-label="Warm Mocha" class="w-5 h-5 rounded-full bg-[#805345] shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9)] hover:scale-110 active:scale-95 transition-transform" onclick="switchCafeTheme('mocha')" title="Roasted Mocha"></button>
          <button aria-label="Vanilla Cloud" class="w-5 h-5 rounded-full bg-[#fdecd2] shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9)] hover:scale-110 active:scale-95 transition-transform" onclick="switchCafeTheme('vanilla')" title="Vanilla Cream"></button>
          <button aria-label="Matcha Cream" class="w-5 h-5 rounded-full bg-[#9cb491] shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9)] hover:scale-110 active:scale-95 transition-transform" onclick="switchCafeTheme('matcha')" title="Matcha Breeze"></button>
        </div>

        <button aria-label="Toggle Ambient Lo-Fi" class="flex items-center gap-1 px-3 py-1.5 rounded-full bg-surface-container text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors clay-button" id="header-lofi-btn" onclick="toggleSoundscapePlay()">
          <span class="material-symbols-outlined text-[17px]" id="header-lofi-icon">graphic_eq</span>
          <span class="hidden lg:inline text-xs font-semibold" id="header-lofi-text">Lo-Fi Play</span>
        </button>

        <div class="flex items-center px-2.5 py-1 rounded-full bg-surface-container-high text-on-surface-variant text-xs font-semibold">
          <span class="material-symbols-outlined text-[15px] mr-1 text-primary">schedule</span>
          <span id="live-cafe-clock">--:--</span>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content Layout -->
  <main class="w-full max-w-[880px] mx-auto px-gutter pt-24 pb-36 min-h-screen bg-background">
    <div class="flex flex-col w-full gap-space-lg pb-12 transition-colors duration-500" id="cafe-workspace">

      <!-- Workspace Sub-Banner & Live Persona Bar -->
      <div class="flex flex-wrap items-center justify-between gap-space-sm bg-surface-container-low/80 backdrop-blur-xl p-space-sm rounded-2xl shadow-[inset_2px_2px_4px_rgba(255,255,255,0.9),0_8px_20px_-4px_rgba(74,46,43,0.06)] border border-white/40">
        <div class="flex items-center gap-space-sm">
          <div class="relative flex items-center justify-center w-11 h-11 rounded-full bg-primary-container text-on-primary-container shadow-[inset_1px_1px_3px_rgba(255,255,255,0.8)] text-2xl">
            🤝
            <span class="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full bg-tertiary-container shadow-[0_0_8px_rgba(156,180,145,0.8)] flex items-center justify-center">
              <span class="w-1.5 h-1.5 rounded-full bg-on-tertiary-container animate-ping"></span>
            </span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-base font-bold text-on-surface cursor-pointer hover:underline" id="companion-name-badge" onclick="promptRenameCompanion()" title="Click to rename">Doraemon Barista AI</span>
              <span class="px-2 py-0.5 rounded-full bg-surface-container text-on-surface-variant text-[11px] font-bold tracking-wide">English Brain • Multilingual Heart</span>
            </div>
            <p class="text-xs text-on-surface-variant">Steaming freshly grounded thoughts & brotherly advice in Harajuku Lo-Fi Sanctuary</p>
          </div>
        </div>

        <div class="flex items-center gap-space-xs">
          <!-- Tip Heart Counter Pill -->
          <button class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-primary-container text-on-primary-container text-xs font-bold clay-button" onclick="sendHeartWarmth()" title="Send gratitude to Dora">
            <span class="material-symbols-outlined text-[16px] text-primary" style="font-variation-settings: 'FILL' 1;">favorite</span>
            <span id="tip-counter">142</span>
            <span class="opacity-80 font-normal">Tips</span>
          </button>
          <!-- Snapshot Screen Peek -->
          <button class="flex items-center gap-1 px-3 py-1.5 rounded-full bg-surface-container text-on-surface-variant hover:text-primary transition-colors text-xs font-semibold clay-button" onclick="triggerVisionSnapshot()" title="Capture screen commentary">
            <span class="material-symbols-outlined text-[16px]">photo_camera</span>
            <span class="hidden sm:inline">Screen Peek</span>
          </button>
        </div>
      </div>

      <!-- Bento Grid Primary Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-start">

        <!-- LEFT COLUMN: Brew Inspiration, Soundscape & Starters (4 Cols) -->
        <div class="lg:col-span-4 flex flex-col gap-space-md order-2 lg:order-1">

          <!-- Daily Brew Inspiration Card -->
          <div class="relative bg-surface-container-lowest p-space-md rounded-2xl clay-surface flex flex-col gap-space-sm border border-white/60">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-8 h-8 rounded-full bg-primary-fixed flex items-center justify-center text-primary text-base">🍵</span>
                <div>
                  <span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-bold">Today's Special</span>
                  <h2 class="text-sm font-bold text-on-surface leading-tight">Barista Suggestion</h2>
                </div>
              </div>
              <button aria-label="Randomize drink inspiration" class="w-8 h-8 rounded-full bg-surface-container text-on-surface-variant hover:text-primary hover:bg-surface-container-high transition-colors flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]" onclick="shuffleDrink()">
                <span class="material-symbols-outlined text-[18px]">autorenew</span>
              </button>
            </div>

            <div class="bg-surface-container-low p-space-sm rounded-xl shadow-[inset_1px_1px_3px_rgba(74,46,43,0.04)] flex flex-col gap-1 transition-all duration-300" id="drink-card-content">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-primary" id="drink-title">Iced Strawberry Matcha Latte</span>
                <span class="px-2 py-0.5 rounded-full bg-tertiary-container text-on-tertiary-container text-[10px] font-bold" id="drink-tag">Uplifting</span>
              </div>
              <p class="text-xs text-on-surface-variant" id="drink-desc">Cold whipped ceremonial grade matcha floated over housemade organic strawberry compote and silky oat milk.</p>
              <div class="flex items-center gap-2 pt-2">
                <button class="px-3 py-1 rounded-full bg-primary text-on-primary text-xs font-bold clay-button flex items-center gap-1" onclick="promptDoraRecipe()">
                  <span class="material-symbols-outlined text-[14px]">menu_book</span>
                  <span>Ask Dora for Recipe</span>
                </button>
                <span class="text-[10px] text-outline">Temp: 4°C • Decaf</span>
              </div>
            </div>

            <!-- Recipe Accordion Drawer -->
            <div class="bg-surface-container-low/70 p-2.5 rounded-xl">
              <button class="w-full flex items-center justify-between text-left text-xs font-semibold text-on-surface hover:text-primary transition-colors" onclick="toggleRecipeAccordion()">
                <span class="flex items-center gap-1.5">
                  <span class="material-symbols-outlined text-[16px] text-secondary">psychology_alt</span>
                  Barista Tasting Notes & Affinity
                </span>
                <span class="material-symbols-outlined text-[16px] transition-transform duration-200" id="accordion-icon">expand_more</span>
              </button>
              <div class="hidden pt-2 text-on-surface-variant text-xs space-y-1.5" id="recipe-accordion-panel">
                <p><strong>Aroma:</strong> Sweet wild berries, roasted nutty undertones, toasted brioche.</p>
                <p><strong>Best Pairings:</strong> Deep coding sessions, late night tapri chai debriefs, and unwinding.</p>
              </div>
            </div>
          </div>

          <!-- Café Soundscape & Ambient Lo-Fi Generator -->
          <div class="bg-surface-container-lowest p-space-md rounded-2xl clay-surface flex flex-col gap-space-sm border border-white/60">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-8 h-8 rounded-full bg-secondary-container flex items-center justify-center text-on-secondary-container text-base">🎧</span>
                <div>
                  <span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-bold">Background Atmosphere</span>
                  <h2 class="text-sm font-bold text-on-surface leading-tight">Café Soundscape</h2>
                </div>
              </div>
              <button class="w-8 h-8 rounded-full bg-tertiary-container text-on-tertiary-container hover:scale-105 active:scale-95 transition-all flex items-center justify-center shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]" id="soundscape-toggle" onclick="toggleSoundscapePlay()">
                <span class="material-symbols-outlined text-[18px]" id="soundscape-play-icon">play_arrow</span>
              </button>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <button class="soundscape-btn active px-3 py-2 rounded-xl bg-primary-container text-on-primary-container text-xs font-semibold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.7)] text-left flex items-center gap-2 transition-all" onclick="setSoundscape('Rain on Awning', this)">
                <span class="material-symbols-outlined text-[16px]">rainy</span>
                <span class="truncate">Rain Awning</span>
              </button>
              <button class="soundscape-btn px-3 py-2 rounded-xl bg-surface-container-low text-on-surface-variant text-xs font-semibold hover:bg-surface-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)] text-left flex items-center gap-2 transition-all" onclick="setSoundscape('Espresso Bar', this)">
                <span class="material-symbols-outlined text-[16px]">coffee_maker</span>
                <span class="truncate">Espresso Bar</span>
              </button>
              <button class="soundscape-btn px-3 py-2 rounded-xl bg-surface-container-low text-on-surface-variant text-xs font-semibold hover:bg-surface-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)] text-left flex items-center gap-2 transition-all" onclick="setSoundscape('Cozy Vinyl Lo-Fi', this)">
                <span class="material-symbols-outlined text-[16px]">album</span>
                <span class="truncate">Vinyl Lo-Fi</span>
              </button>
              <button class="soundscape-btn px-3 py-2 rounded-xl bg-surface-container-low text-on-surface-variant text-xs font-semibold hover:bg-surface-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)] text-left flex items-center gap-2 transition-all" onclick="setSoundscape('Gentle Whispers', this)">
                <span class="material-symbols-outlined text-[16px]">forum</span>
                <span class="truncate">Gentle Murmur</span>
              </button>
            </div>

            <!-- Volume Slider -->
            <div class="flex items-center gap-3 bg-surface-container-low px-3 py-1.5 rounded-full shadow-[inset_1px_1px_3px_rgba(74,46,43,0.06)]">
              <span class="material-symbols-outlined text-outline text-[16px]">volume_down</span>
              <input class="w-full h-1.5 bg-surface-container-highest rounded-lg appearance-none cursor-pointer accent-primary" max="100" min="0" oninput="updateSoundVol(this.value)" type="range" value="65"/>
              <span class="text-xs text-on-surface-variant w-8 text-right font-mono" id="sound-vol-label">65%</span>
            </div>
          </div>

          <!-- Quick Whisper Prompts -->
          <div class="bg-surface-container-low/90 p-space-sm rounded-2xl flex flex-col gap-2 border border-white/40">
            <span class="text-[10px] text-on-surface-variant uppercase tracking-wider flex items-center gap-1 font-bold">
              <span class="material-symbols-outlined text-[14px] text-primary">tips_and_updates</span>
              Whisper Starters
            </span>
            <div class="flex flex-col gap-1.5">
              <button class="p-2 rounded-xl bg-surface-container-lowest text-left text-on-surface-variant text-xs hover:bg-primary-container hover:text-on-primary-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),0_2px_4px_rgba(74,46,43,0.04)] transition-all flex items-center justify-between" onclick="injectUserPrompt('bhai react me component infinite loop me fas gaya kaise bachaye')">
                <span>💻 React Infinite Loop Help (Hinglish)</span>
                <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
              </button>
              <button class="p-2 rounded-xl bg-surface-container-lowest text-left text-on-surface-variant text-xs hover:bg-primary-container hover:text-on-primary-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),0_2px_4px_rgba(74,46,43,0.04)] transition-all flex items-center justify-between" onclick="injectUserPrompt('bhava nodejs server unhandled rejection mule crash hotay kay karu')">
                <span>💻 Node Crash Fix (Marathish)</span>
                <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
              </button>
              <button class="p-2 rounded-xl bg-surface-container-lowest text-left text-on-surface-variant text-xs hover:bg-primary-container hover:text-on-primary-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),0_2px_4px_rgba(74,46,43,0.04)] transition-all flex items-center justify-between" onclick="injectUserPrompt('/vibe chill')">
                <span>🎵 Vibe DJ: Evening Hindi Lo-Fi</span>
                <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
              </button>
              <button class="p-2 rounded-xl bg-surface-container-lowest text-left text-on-surface-variant text-xs hover:bg-primary-container hover:text-on-primary-container shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),0_2px_4px_rgba(74,46,43,0.04)] transition-all flex items-center justify-between" onclick="injectUserPrompt('/wingman Can we push back tomorrow\\'s sync call by 30 mins?')">
                <span>🎭 Wingman Text Doctor</span>
                <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
              </button>
            </div>
          </div>
        </div>

        <!-- CENTER COLUMN: Interactive 3D Avatar, Emotion Dock & Live Speech Zone (5 Cols) -->
        <div class="lg:col-span-5 flex flex-col gap-space-md order-1 lg:order-2">

          <!-- Dora Avatar Clay Pod -->
          <div class="relative bg-surface-container-lowest p-space-md rounded-3xl clay-surface flex flex-col items-center overflow-hidden border border-white/60">
            <div class="absolute -top-16 inset-x-0 h-44 bg-gradient-to-b from-primary-fixed/60 via-primary-container/20 to-transparent blur-2xl pointer-events-none"></div>

            <!-- Top Pod Ribbon -->
            <div class="w-full flex items-center justify-between z-20 mb-2">
              <div class="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]">
                <span class="w-2.5 h-2.5 rounded-full bg-tertiary-container animate-pulse" id="avatar-pulse"></span>
                <span class="text-xs text-on-surface-variant font-medium" id="avatar-status-text">Dora is listening • Ambient Mode</span>
              </div>
              <div class="flex items-center gap-1">
                <span class="px-2.5 py-0.5 rounded-full bg-surface-container-highest text-on-surface-variant text-[11px] font-bold">Focus 99%</span>
              </div>
            </div>

            <!-- Central 3D Canvas Asset Holder -->
            <div class="w-full relative flex items-center justify-center rounded-2xl bg-surface-container-low/60 shadow-[inset_2px_2px_6px_rgba(74,46,43,0.06)] overflow-hidden">
              <div class="w-full h-72 sm:h-80 rounded-2xl relative z-10" style="display:block;">
                <div id="threejs-container-ANIMATION_1" style="width:100%;height:100%"></div>
              </div>

              <!-- Fresh Roast Badge Overlay -->
              <div class="absolute top-4 left-6 pointer-events-none z-20 flex flex-col items-center opacity-75">
                <span class="material-symbols-outlined text-[20px] text-secondary animate-bounce">local_cafe</span>
                <span class="text-[10px] text-secondary-container bg-secondary/80 px-2 py-0.5 rounded-full mt-1 font-semibold">Fresh Roast</span>
              </div>

              <!-- Real-Time Dynamic Emotion Badge Pill on Canvas -->
              <div class="absolute bottom-3 left-3 z-20 flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface/90 backdrop-blur-md shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),0_4px_12px_rgba(0,0,0,0.08)]">
                <span class="text-sm" id="current-mood-emoji">😊</span>
                <span class="text-xs text-on-surface font-semibold" id="current-mood-label">Cheerful & Attentive</span>
              </div>
            </div>

            <!-- Interactive Eye & Expression Trigger Tray -->
            <div class="w-full mt-space-sm flex flex-col gap-2 z-20">
              <div class="flex items-center justify-between">
                <span class="text-[10px] text-on-surface-variant uppercase tracking-wider font-bold">Trigger Dora's Emotion</span>
                <span class="text-[10px] text-primary font-bold">Interactive Eyes</span>
              </div>
              <div class="grid grid-cols-4 gap-1.5">
                <button class="mood-action-btn px-2 py-2 rounded-xl bg-surface-container-low hover:bg-primary-container hover:text-on-primary-container text-xs text-on-surface shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8),0_2px_4px_rgba(74,46,43,0.04)] active:scale-95 transition-all text-center" onclick="setDoraMood('Wink 😉', 'Playful wink! Main locked in hu bhai, bol kya scene hai?', 'wink')">
                  <span class="text-base block mb-0.5">😉</span>
                  <span class="truncate">Wink</span>
                </button>
                <button class="mood-action-btn px-2 py-2 rounded-xl bg-surface-container-low hover:bg-primary-container hover:text-on-primary-container text-xs text-on-surface shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8),0_2px_4px_rgba(74,46,43,0.04)] active:scale-95 transition-all text-center" onclick="setDoraMood('Surprised 😮', 'Arre bhai! Kya wild twist hai!', 'surprised')">
                  <span class="text-base block mb-0.5">😮</span>
                  <span class="truncate">Surprise</span>
                </button>
                <button class="mood-action-btn px-2 py-2 rounded-xl bg-primary-container text-on-primary-container text-xs font-semibold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8),0_2px_4px_rgba(74,46,43,0.04)] active:scale-95 transition-all text-center" onclick="setDoraMood('Happy Squint 😊', 'Strawberry latte is ready and code is compiling cleanly!', 'happy')">
                  <span class="text-base block mb-0.5">😊</span>
                  <span class="truncate">Squint</span>
                </button>
                <button class="mood-action-btn px-2 py-2 rounded-xl bg-surface-container-low hover:bg-primary-container hover:text-on-primary-container text-xs text-on-surface shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8),0_2px_4px_rgba(74,46,43,0.04)] active:scale-95 transition-all text-center" onclick="setDoraMood('Focus Mode 🧐', 'Analyzing stack trace, RAG embeddings, and logic flow.', 'focus')">
                  <span class="text-base block mb-0.5">🧐</span>
                  <span class="truncate">Focus</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Live Speaking Speech Bubble & Foam Waveform Display -->
          <div class="relative bg-surface-container-lowest p-space-md rounded-2xl clay-surface flex flex-col gap-space-sm border border-white/60">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-full bg-primary-fixed flex items-center justify-center text-primary font-bold text-xs">AI</span>
                <span class="text-sm font-bold text-on-surface" id="bubble-barista-name">Dora</span>
                <span class="text-[11px] text-outline">• Live Voice synthesis</span>
              </div>
              <button class="flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-container-low text-on-surface-variant hover:text-primary transition-colors text-xs font-semibold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]" onclick="replayCurrentSpeech()" title="Replay voice audio">
                <span class="material-symbols-outlined text-[15px]">volume_up</span>
                <span>Speak</span>
              </button>
            </div>

            <!-- Glowing Speech Text Bubble -->
            <div class="relative bg-surface-container-low/70 p-space-sm rounded-xl shadow-[inset_1px_1px_3px_rgba(74,46,43,0.05)] min-h-[72px] flex items-center">
              <p class="text-sm text-on-surface leading-relaxed" id="live-speech-text">
                "Welcome to Café Dora! I've preheated the mugs and locked in the local model. Chahe code debug karna ho ya chai pe chill karna ho, bol kya scene hai! 👊"
              </p>
            </div>

            <!-- Animated Foam Waveform Equalizer -->
            <div class="flex items-center justify-between bg-surface-container-lowest px-3 py-2 rounded-xl shadow-[inset_1px_1px_3px_rgba(74,46,43,0.04)]">
              <div class="flex items-center gap-1.5 text-primary">
                <span class="material-symbols-outlined text-[16px] animate-pulse">graphic_eq</span>
                <span class="text-[11px] font-semibold">Local Stream: GPU Q4_K_M</span>
              </div>
              <div class="flex items-end gap-1 h-5" id="audio-waveform-bars">
                <span class="w-1 bg-primary rounded-full animate-bounce h-3"></span>
                <span class="w-1 bg-primary-container rounded-full animate-bounce h-5 delay-75"></span>
                <span class="w-1 bg-primary rounded-full animate-bounce h-2 delay-150"></span>
                <span class="w-1 bg-primary-container rounded-full animate-bounce h-4"></span>
                <span class="w-1 bg-secondary rounded-full animate-bounce h-5 delay-100"></span>
                <span class="w-1 bg-primary rounded-full animate-bounce h-2 delay-200"></span>
                <span class="w-1 bg-primary-container rounded-full animate-bounce h-4 delay-75"></span>
                <span class="w-1 bg-secondary-container rounded-full animate-bounce h-3"></span>
              </div>
            </div>

            <!-- Claymorphic Interactive Input Dock -->
            <form class="flex flex-col gap-2 mt-1" id="chat-input-form" onsubmit="handleUserSubmit(event)">
              <div class="flex items-center gap-2">
                <div class="flex-1 flex items-center bg-surface-container-lowest rounded-full px-4 py-2.5 clay-input border border-surface-container">
                  <span class="material-symbols-outlined text-outline text-[18px] mr-2">edit_note</span>
                  <input class="w-full bg-transparent text-sm text-on-surface placeholder:text-outline focus:outline-none" id="user-input-field" placeholder="Chat in Hinglish, Marathish, Devanagari, English..." type="text" autocomplete="off"/>
                </div>
                <!-- Voice Record / Push to speak button -->
                <button class="w-10 h-10 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center clay-button" id="mic-toggle-btn" onclick="toggleMicrophone()" title="Push to Speak / Voice Input" type="button">
                  <span class="material-symbols-outlined text-[20px]" id="mic-icon">mic</span>
                </button>
                <!-- Send button -->
                <button aria-label="Send message" class="w-10 h-10 rounded-full bg-primary text-on-primary flex items-center justify-center clay-button" id="send-button-main" type="submit">
                  <span class="material-symbols-outlined text-[18px]">send</span>
                </button>
              </div>

              <!-- Dock Sub-Controls: Speed Selector & Speech Tone chips -->
              <div class="flex items-center justify-between text-on-surface-variant px-2">
                <div class="flex items-center gap-1.5">
                  <span class="text-[11px] text-outline">Voice Speed:</span>
                  <div class="flex items-center bg-surface-container-low rounded-full p-0.5 shadow-[inset_1px_1px_2px_rgba(74,46,43,0.06)]">
                    <button class="speed-chip px-2 py-0.5 rounded-full text-[10px] text-on-surface-variant hover:text-on-surface" onclick="setPlaybackSpeed(0.85, this)" type="button">0.8x</button>
                    <button class="speed-chip active px-2 py-0.5 rounded-full text-[10px] bg-primary-container text-on-primary-container font-bold shadow-[inset_1px_1px_2px_rgba(255,255,255,0.8)]" onclick="setPlaybackSpeed(1.0, this)" type="button">1.0x</button>
                    <button class="speed-chip px-2 py-0.5 rounded-full text-[10px] text-on-surface-variant hover:text-on-surface" onclick="setPlaybackSpeed(1.15, this)" type="button">1.2x</button>
                  </div>
                </div>
                <span class="text-[11px] text-outline" id="latency-label">Inference: ~76 tok/s</span>
              </div>
            </form>
          </div>
        </div>

        <!-- RIGHT COLUMN: Frosted Glass Dialogue Stream & Barista Voice Tuner (3 Cols) -->
        <div class="lg:col-span-3 flex flex-col gap-space-md order-3">

          <!-- Live Chat Stream Panel -->
          <div class="bg-surface-container-lowest/90 backdrop-blur-xl p-space-md rounded-2xl clay-surface flex flex-col gap-space-sm h-[500px] border border-white/60">
            <div class="flex items-center justify-between pb-1 border-b border-surface-container">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-primary text-[18px]">receipt_long</span>
                <h2 class="text-sm font-bold text-on-surface">Order Dialogue</h2>
              </div>
              <button class="text-outline hover:text-on-surface transition-colors p-1" onclick="clearChatLog()" title="Clear stream log">
                <span class="material-symbols-outlined text-[16px]">delete_sweep</span>
              </button>
            </div>

            <!-- Scrollable Conversation Stream -->
            <div class="flex-1 overflow-y-auto space-y-3 pr-1 text-left" id="chat-messages-container">
              <!-- Initial Welcome Message from Dora -->
              <div class="flex flex-col gap-1 items-start">
                <div class="flex items-center gap-1.5 text-[10px] text-outline font-semibold">
                  <span class="w-2 h-2 rounded-full bg-primary-container"></span>
                  <span>Dora • Just now</span>
                  <span class="px-1.5 py-0.2 bg-primary/10 text-primary rounded text-[9px]">Ride-or-Die</span>
                </div>
                <div class="bg-surface-container-low p-3 rounded-2xl rounded-tl-sm text-xs text-on-surface shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),0_2px_6px_rgba(74,46,43,0.04)] max-w-[95%] leading-relaxed chat-bubble-markdown">
                  Ayy brother! Kya haal chaal? Main locked in hu—chahe code debug karna ho, client ko roast karna ho, ya late night chai pe chill karna ho, bol kya scene hai! 👊
                </div>
              </div>
            </div>

            <div class="pt-2 flex items-center justify-between text-[11px] text-outline border-t border-surface-container">
              <span>Encrypted Local Session</span>
              <span class="flex items-center gap-1 text-primary font-semibold">
                <span class="material-symbols-outlined text-[13px]">psychology</span>
                Cognitive Brain
              </span>
            </div>
          </div>

          <!-- Live Voice Synthesizer Tuner Panel -->
          <div class="bg-surface-container-lowest p-space-md rounded-2xl clay-surface flex flex-col gap-space-sm border border-white/60">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="material-symbols-outlined text-secondary text-[18px]">tune</span>
                <h2 class="text-sm font-bold text-on-surface">Voice Acoustics</h2>
              </div>
              <span class="text-[11px] text-primary font-bold">Warm Vibe</span>
            </div>

            <!-- Tone Persona Selector -->
            <div class="flex flex-col gap-1">
              <label class="text-[11px] text-on-surface-variant font-medium">Persona Timbre</label>
              <select class="w-full bg-surface-container-low px-3 py-1.5 rounded-xl text-xs text-on-surface shadow-[inset_1px_1px_2px_rgba(74,46,43,0.06)] focus:outline-none" id="voice-tone-select" onchange="updateVoiceTone(this.value)">
                <option value="warm">Warm & Velvety (Default)</option>
                <option value="bubbly">Playful & Bubbly</option>
                <option value="calm">Calm Zen Barista</option>
              </select>
            </div>

            <!-- Pitch Modulation Slider -->
            <div class="flex flex-col gap-1">
              <div class="flex items-center justify-between text-[11px]">
                <span class="text-on-surface-variant">Pitch Balance</span>
                <span class="text-outline font-mono" id="pitch-val">+1.0 Hz</span>
              </div>
              <input class="w-full h-1.5 bg-surface-container-highest rounded-lg appearance-none cursor-pointer accent-primary" max="2" min="0.5" oninput="document.getElementById('pitch-val').innerText = this.value + 'x'; currentVoicePitch = parseFloat(this.value);" step="0.1" type="range" value="1.0"/>
            </div>

            <!-- Expressiveness Gauge -->
            <div class="flex items-center justify-between bg-surface-container-low p-2 rounded-xl">
              <div class="flex flex-col">
                <span class="text-xs text-on-surface font-semibold">Expressiveness Gauge</span>
                <span class="text-[10px] text-outline">Dynamic cadence</span>
              </div>
              <div class="relative w-9 h-9 flex items-center justify-center">
                <svg class="w-9 h-9 transform -rotate-90" viewbox="0 0 36 36">
                  <path class="text-surface-container-highest" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-width="3.5"></path>
                  <path class="text-primary transition-all duration-500" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-dasharray="92, 100" stroke-linecap="round" stroke-width="3.5"></path>
                </svg>
                <span class="absolute text-[10px] text-primary font-bold">92%</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Interactive Floating Heart Feedback Toast -->
      <div class="fixed bottom-24 right-8 pointer-events-none opacity-0 transform translate-y-4 transition-all duration-300 z-50 flex items-center gap-2 px-4 py-2 rounded-full bg-primary-container text-on-primary-container text-xs font-bold shadow-[0_12px_24px_-4px_rgba(247,141,167,0.6)]" id="heart-toast">
        <span class="text-lg">💖</span>
        <span id="toast-message">Dora is smiling! Tip added to the jar.</span>
      </div>

    </div>
  </main>

  <!-- Sticky Bottom Footer with Superpower Quick Pills and Active Chat Input -->
  <footer class="fixed bottom-0 inset-x-0 z-40 bg-surface/95 backdrop-blur-2xl shadow-[0_-8px_24px_-4px_rgba(74,46,43,0.08)] border-t border-surface-container">
    <div class="max-w-[880px] mx-auto px-gutter py-2 flex flex-col items-center gap-1.5">
      <!-- Superpower Shortcut Chips -->
      <div class="w-full flex items-center justify-start sm:justify-center gap-1.5 overflow-x-auto py-0.5 no-scrollbar">
        <button class="px-2.5 py-1 rounded-full bg-surface-container-low text-xs text-on-surface-variant font-medium clay-button whitespace-nowrap hover:bg-primary-container hover:text-on-primary-container" onclick="injectUserPrompt('/chill')">☕ Chai & Chill</button>
        <button class="px-2.5 py-1 rounded-full bg-surface-container-low text-xs text-on-surface-variant font-medium clay-button whitespace-nowrap hover:bg-primary-container hover:text-on-primary-container" onclick="injectUserPrompt('/vibe focus')">🎵 Vibe DJ</button>
        <button class="px-2.5 py-1 rounded-full bg-surface-container-low text-xs text-on-surface-variant font-medium clay-button whitespace-nowrap hover:bg-primary-container hover:text-on-primary-container" onclick="injectUserPrompt('/hype gym PR 100kg')">🔥 Instant Hype</button>
        <button class="px-2.5 py-1 rounded-full bg-surface-container-low text-xs text-on-surface-variant font-medium clay-button whitespace-nowrap hover:bg-primary-container hover:text-on-primary-container" onclick="injectUserPrompt('/roast Finish documentation by tonight')">🎯 Target</button>
        <button class="px-2.5 py-1 rounded-full bg-surface-container-low text-xs text-on-surface-variant font-medium clay-button whitespace-nowrap hover:bg-primary-container hover:text-on-primary-container" onclick="openStatsModal()">📊 Life Diary</button>
        <button class="px-2.5 py-1 rounded-full bg-surface-container-low text-xs text-on-surface-variant font-medium clay-button whitespace-nowrap hover:bg-primary-container hover:text-on-primary-container" onclick="injectUserPrompt('/help')">❓ Help</button>
      </div>

      <!-- Footer Chat Input Bar -->
      <form class="w-full flex items-center justify-between gap-2" onsubmit="handleFooterSubmit(event)">
        <div class="flex-1 flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container-lowest clay-input border border-surface-container">
          <span class="material-symbols-outlined text-outline text-[18px]">edit_note</span>
          <input class="w-full bg-transparent text-xs text-on-surface placeholder:text-outline focus:outline-none" id="footer-input-field" placeholder="Chat in Hinglish, Marathish, Hindi, Marathi, English..." type="text" autocomplete="off"/>
        </div>
        <button aria-label="Send message" class="w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center clay-button" type="submit">
          <span class="material-symbols-outlined text-[15px]">send</span>
        </button>
        <button aria-label="Voice input button" class="w-8 h-8 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center clay-button" onclick="toggleMicrophone()" type="button" title="Push to Speak">
          <span class="material-symbols-outlined text-[16px]">mic</span>
        </button>
      </form>
    </div>
  </footer>

  <!-- Modals -->
  <!-- 1. Stats / Life Diary Modal -->
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden items-center justify-center p-4" id="statsModal" onclick="closeModalOnBackdrop(event, 'statsModal')">
    <div class="w-full max-w-lg bg-surface-container-lowest p-6 rounded-3xl clay-surface flex flex-col gap-4 border border-white/70">
      <div class="flex items-center justify-between pb-2 border-b border-surface-container">
        <h3 class="text-base font-bold text-on-surface flex items-center gap-2">
          <span>📊</span> Private Offline Life Diary & Memory
        </h3>
        <button class="text-outline hover:text-on-surface text-xl font-bold" onclick="closeModal('statsModal')">&times;</button>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div class="bg-surface-container-low p-3 rounded-2xl text-center">
          <div class="text-2xl font-extrabold text-primary" id="statChats">0</div>
          <div class="text-[11px] text-on-surface-variant mt-1">Total Conversations</div>
        </div>
        <div class="bg-surface-container-low p-3 rounded-2xl text-center">
          <div class="text-2xl font-extrabold text-tertiary" id="statDebriefs">0</div>
          <div class="text-[11px] text-on-surface-variant mt-1">Evening Debriefs</div>
        </div>
        <div class="bg-surface-container-low p-3 rounded-2xl text-center">
          <div class="text-2xl font-extrabold text-secondary" id="statGoals">0</div>
          <div class="text-[11px] text-on-surface-variant mt-1">Active Goal Pacts</div>
        </div>
        <div class="bg-surface-container-low p-3 rounded-2xl text-center">
          <div class="text-2xl font-extrabold text-primary" id="statFactsCount">48</div>
          <div class="text-[11px] text-on-surface-variant mt-1">Learned Memory Facts</div>
        </div>
      </div>

      <div>
        <div class="text-xs font-bold text-on-surface uppercase tracking-wide mb-1.5">Top Emotional States</div>
        <div class="space-y-1 text-xs" id="statMoodsList">Loading moods...</div>
      </div>

      <div>
        <div class="text-xs font-bold text-on-surface uppercase tracking-wide mb-1.5">Languages & Dialects</div>
        <div class="space-y-1 text-xs" id="statLangsList">Loading dialects...</div>
      </div>
    </div>
  </div>

  <!-- 2. Chai & Chill Evening Debrief Modal -->
  <div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden items-center justify-center p-4" id="chillModal" onclick="closeModalOnBackdrop(event, 'chillModal')">
    <div class="w-full max-w-lg bg-surface-container-lowest p-6 rounded-3xl clay-surface flex flex-col gap-4 border border-white/70">
      <div class="flex items-center justify-between pb-2 border-b border-surface-container">
        <h3 class="text-base font-bold text-on-surface flex items-center gap-2">
          <span>☕</span> Chai & Chill: Evening Wind-Down
        </h3>
        <button class="text-outline hover:text-on-surface text-xl font-bold" onclick="closeModal('chillModal')">&times;</button>
      </div>

      <p class="text-xs text-on-surface-variant leading-relaxed">
        Take 2 minutes to recap your day with your best friend. Your reflections will be saved privately in your local SQLite Life Diary!
      </p>

      <div class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-on-surface mb-1">1. What was your biggest win today (big or small)?</label>
          <input class="w-full bg-surface-container-low p-2.5 rounded-xl text-xs text-on-surface clay-input focus:outline-none" id="chillWins" placeholder="e.g. Fixed nasty CORS bug, hit bench press PR..."/>
        </div>
        <div>
          <label class="block text-xs font-semibold text-on-surface mb-1">2. What was the biggest headache or friction point?</label>
          <input class="w-full bg-surface-container-low p-2.5 rounded-xl text-xs text-on-surface clay-input focus:outline-none" id="chillFrustrations" placeholder="e.g. Merge conflict, slow review, feeling tired..."/>
        </div>
        <div>
          <label class="block text-xs font-semibold text-on-surface mb-1">3. How are you feeling right now (1-10 or one word)?</label>
          <input class="w-full bg-surface-container-low p-2.5 rounded-xl text-xs text-on-surface clay-input focus:outline-none" id="chillMood" placeholder="e.g. 8/10, relaxed, ready to sleep..."/>
        </div>
      </div>

      <button class="w-full py-2.5 rounded-xl bg-primary text-on-primary text-xs font-bold clay-button mt-2" onclick="submitChaiChill()">
        Submit Debrief & Get Wrap-Up ➔
      </button>
    </div>
  </div>

  <!-- Client-side Logic -->
  <script>
    // Live Clock
    function updateClock() {
      const now = new Date();
      const el = document.getElementById('live-cafe-clock');
      if (el) el.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Theme Switching
    function switchCafeTheme(themeName) {
      if (themeName === 'strawberry') {
        document.body.style.backgroundColor = '#fff8f7';
        showToast("Theme: Cozy Strawberry Pink 🍓");
      } else if (themeName === 'mocha') {
        document.body.style.backgroundColor = '#fdfaf8';
        showToast("Theme: Warm Roasted Mocha ☕");
      } else if (themeName === 'vanilla') {
        document.body.style.backgroundColor = '#fbf9f4';
        showToast("Theme: Soft Vanilla Cream 🍦");
      } else if (themeName === 'matcha') {
        document.body.style.backgroundColor = '#f2f6f1';
        showToast("Theme: Serene Matcha Breeze 🍵");
      }
    }

    // Drink Catalog
    const drinksList = [
      {
        title: "Iced Strawberry Matcha Latte",
        tag: "Uplifting",
        desc: "Cold whipped ceremonial grade matcha floated over housemade organic strawberry compote and silky oat milk."
      },
      {
        title: "Chestnut Mocha Viennese",
        tag: "Warming",
        desc: "Velvety roasted chestnut puree folded into dark espresso, topped with whipped sweet cream and cocoa dusting."
      },
      {
        title: "Lavender Honey Cappuccino",
        tag: "Floral Calm",
        desc: "Micro-foamed whole milk infused with organic French culinary lavender and a golden swirl of wildflower honey."
      },
      {
        title: "Spiced Cardamom Vanilla Flat White",
        tag: "Aromatic",
        desc: "Freshly ground green cardamom steamed into double-ristretto with Madagascar bourbon vanilla bean infusion."
      }
    ];
    let currentDrinkIdx = 0;

    function shuffleDrink() {
      currentDrinkIdx = (currentDrinkIdx + 1) % drinksList.length;
      const item = drinksList[currentDrinkIdx];
      document.getElementById('drink-title').innerText = item.title;
      document.getElementById('drink-tag').innerText = item.tag;
      document.getElementById('drink-desc').innerText = item.desc;
    }

    function promptDoraRecipe() {
      const currentDrink = drinksList[currentDrinkIdx].title;
      injectUserPrompt("Can you share the barista recipe and secret tips for " + currentDrink + "?");
    }

    function toggleRecipeAccordion() {
      const panel = document.getElementById('recipe-accordion-panel');
      const icon = document.getElementById('accordion-icon');
      if (panel && icon) {
        panel.classList.toggle('hidden');
        icon.style.transform = panel.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
      }
    }

    // Web Audio API Ambient Sound Generator
    let audioCtx = null;
    let noiseNode = null;
    let gainNode = null;
    let isPlayingSoundscape = false;
    let currentSoundType = 'Rain on Awning';

    function initAudioContext() {
      if (!audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContext();
      }
    }

    function startBrownNoise(filterFreq = 800) {
      initAudioContext();
      if (noiseNode) {
        noiseNode.stop();
        noiseNode.disconnect();
      }
      const bufferSize = audioCtx.sampleRate * 2;
      const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const data = buffer.getChannelData(0);
      let lastOut = 0.0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        data[i] = (lastOut + (0.02 * white)) / 1.02;
        lastOut = data[i];
        data[i] *= 3.5; // Gain boost
      }
      noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = buffer;
      noiseNode.loop = true;

      const filter = audioCtx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.value = filterFreq;

      gainNode = audioCtx.createGain();
      const vol = parseFloat(document.querySelector('input[type="range"]').value) / 100;
      gainNode.gain.value = vol * 0.25;

      noiseNode.connect(filter);
      filter.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      noiseNode.start();
    }

    function stopNoise() {
      if (noiseNode) {
        try { noiseNode.stop(); noiseNode.disconnect(); } catch(e) {}
        noiseNode = null;
      }
    }

    function toggleSoundscapePlay() {
      isPlayingSoundscape = !isPlayingSoundscape;
      const icon = document.getElementById('soundscape-play-icon');
      const headerIcon = document.getElementById('header-lofi-icon');
      const headerText = document.getElementById('header-lofi-text');

      if (isPlayingSoundscape) {
        icon.innerText = 'pause';
        headerIcon.innerText = 'pause';
        headerText.innerText = 'Lo-Fi Stop';
        playSelectedSound();
        showToast("Soundscape playing softly: " + currentSoundType + " 🎶");
      } else {
        icon.innerText = 'play_arrow';
        headerIcon.innerText = 'play_arrow';
        headerText.innerText = 'Lo-Fi Play';
        stopNoise();
        showToast("Soundscape paused");
      }
    }

    function playSelectedSound() {
      if (!isPlayingSoundscape) return;
      if (currentSoundType.includes('Rain')) {
        startBrownNoise(750);
      } else if (currentSoundType.includes('Espresso')) {
        startBrownNoise(350);
      } else if (currentSoundType.includes('Vinyl')) {
        startBrownNoise(1200);
      } else {
        startBrownNoise(500);
      }
    }

    function setSoundscape(name, el) {
      currentSoundType = name;
      document.querySelectorAll('.soundscape-btn').forEach(btn => {
        btn.classList.remove('bg-primary-container', 'text-on-primary-container', 'active');
        btn.classList.add('bg-surface-container-low', 'text-on-surface-variant');
      });
      if (el) {
        el.classList.remove('bg-surface-container-low', 'text-on-surface-variant');
        el.classList.add('bg-primary-container', 'text-on-primary-container', 'active');
      }
      if (isPlayingSoundscape) {
        playSelectedSound();
      }
      showToast("Atmosphere: " + name);
    }

    function updateSoundVol(val) {
      document.getElementById('sound-vol-label').innerText = val + '%';
      if (gainNode && audioCtx) {
        gainNode.gain.setValueAtTime((parseFloat(val) / 100) * 0.25, audioCtx.currentTime);
      }
    }

    // Voice & TTS Settings
    let currentVoiceSpeed = 1.0;
    let currentVoicePitch = 1.0;

    function setPlaybackSpeed(spd, btn) {
      currentVoiceSpeed = spd;
      document.querySelectorAll('.speed-chip').forEach(b => {
        b.classList.remove('bg-primary-container', 'text-on-primary-container', 'font-bold');
        b.classList.add('text-on-surface-variant');
      });
      btn.classList.add('bg-primary-container', 'text-on-primary-container', 'font-bold');
      btn.classList.remove('text-on-surface-variant');
      showToast("Voice speed: " + spd + "x");
    }

    function updateVoiceTone(val) {
      if (val === 'bubbly') currentVoicePitch = 1.25;
      else if (val === 'calm') currentVoicePitch = 0.85;
      else currentVoicePitch = 1.0;
      document.getElementById('pitch-val').innerText = currentVoicePitch + 'x';
      showToast("Timbre modulated to " + val);
    }

    function speakText(text) {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      const clean = text.replace(/[*_#`~>]/g, ' ').replace(/\n+/g, '. ');
      const u = new SpeechSynthesisUtterance(clean);
      u.rate = currentVoiceSpeed;
      u.pitch = currentVoicePitch;

      // Animate waveform while speaking
      const bars = document.getElementById('audio-waveform-bars');
      u.onstart = () => {
        if (bars) bars.style.opacity = '1';
        triggerAvatarWink();
      };
      u.onend = () => {
        if (bars) bars.style.opacity = '0.5';
      };
      window.speechSynthesis.speak(u);
    }

    function replayCurrentSpeech() {
      const speechEl = document.getElementById('live-speech-text');
      if (speechEl) {
        speakText(speechEl.innerText);
      }
    }

    // Dora Mood Reactions & Avatar integration
    let triggerAvatarWink = () => {};
    let triggerAvatarSquint = () => {};

    function setDoraMood(moodLabel, speechReaction, eyeCode) {
      const emojiMap = {
        'wink': '😉',
        'surprised': '😮',
        'happy': '😊',
        'focus': '🧐'
      };
      document.getElementById('current-mood-emoji').innerText = emojiMap[eyeCode] || '😊';
      document.getElementById('current-mood-label').innerText = moodLabel;
      
      const speechEl = document.getElementById('live-speech-text');
      speechEl.style.opacity = '0';
      setTimeout(() => {
        speechEl.innerText = '"' + speechReaction + '"';
        speechEl.style.opacity = '1';
        speakText(speechReaction);
      }, 150);

      if (eyeCode === 'wink') triggerAvatarWink();
      if (eyeCode === 'happy') triggerAvatarSquint();
    }

    // Tip Heart Button Action
    let tipCount = 142;
    function sendHeartWarmth() {
      tipCount++;
      document.getElementById('tip-counter').innerText = tipCount;
      showToast("💖 Dora is smiling! Tip added to the jar.");
      triggerAvatarWink();
    }

    function showToast(msg) {
      const toast = document.getElementById('heart-toast');
      const text = document.getElementById('toast-message');
      if (toast && text) {
        text.innerText = msg;
        toast.classList.remove('opacity-0', 'translate-y-4');
        toast.classList.add('opacity-100', 'translate-y-0');
        setTimeout(() => {
          toast.classList.remove('opacity-100', 'translate-y-0');
          toast.classList.add('opacity-0', 'translate-y-4');
        }, 2200);
      }
    }

    // Microphone Input
    let isRecording = false;
    let recognition = null;

    function toggleMicrophone() {
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showToast("Speech recognition not supported in this browser. Please type!");
        return;
      }
      isRecording = !isRecording;
      const micIcon = document.getElementById('mic-icon');
      const micBtn = document.getElementById('mic-toggle-btn');
      const avatarStatus = document.getElementById('avatar-status-text');

      if (isRecording) {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN'; // Optimized for Indian English / Hinglish

        recognition.onstart = () => {
          micIcon.innerText = 'graphic_eq';
          micBtn.classList.add('ring-4', 'ring-primary/40');
          avatarStatus.innerText = "Dora is hearing your voice...";
        };

        recognition.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          injectUserPrompt(transcript);
        };

        recognition.onerror = () => {
          toggleMicrophone();
        };

        recognition.onend = () => {
          isRecording = false;
          micIcon.innerText = 'mic';
          micBtn.classList.remove('ring-4', 'ring-primary/40');
          avatarStatus.innerText = "Dora is listening • Ambient Mode";
        };

        recognition.start();
      } else {
        if (recognition) recognition.stop();
        micIcon.innerText = 'mic';
        micBtn.classList.remove('ring-4', 'ring-primary/40');
        avatarStatus.innerText = "Dora is listening • Ambient Mode";
      }
    }

    // Modal Control
    function openStatsModal() {
      document.getElementById('statsModal').classList.remove('hidden');
      document.getElementById('statsModal').classList.add('flex');
      fetch('/api/stats').then(r => r.json()).then(data => {
        document.getElementById('statChats').innerText = data.total_messages || 0;
        document.getElementById('statDebriefs').innerText = data.total_debriefs || 0;
        document.getElementById('statGoals').innerText = data.pending_goals || 0;

        const moodsList = document.getElementById('statMoodsList');
        if (data.top_moods && data.top_moods.length) {
          moodsList.innerHTML = data.top_moods.map(([m, c]) => `
            <div class="flex justify-between items-center py-0.5 border-b border-surface-container">
              <span>${m}</span>
              <span class="font-bold text-primary">${c}</span>
            </div>
          `).join('');
        }

        const langsList = document.getElementById('statLangsList');
        if (data.languages && data.languages.length) {
          langsList.innerHTML = data.languages.map(([l, c]) => `
            <div class="flex justify-between items-center py-0.5 border-b border-surface-container">
              <span>${l.split('(')[0].trim()}</span>
              <span class="font-bold text-tertiary">${c} turns</span>
            </div>
          `).join('');
        }
      });
    }

    function openChaiChillModal() {
      document.getElementById('chillModal').classList.remove('hidden');
      document.getElementById('chillModal').classList.add('flex');
    }

    function closeModal(id) {
      document.getElementById(id).classList.add('hidden');
      document.getElementById(id).classList.remove('flex');
    }

    function closeModalOnBackdrop(e, id) {
      if (e.target.id === id) closeModal(id);
    }

    async function submitChaiChill() {
      const wins = document.getElementById('chillWins').value.trim();
      const frustrations = document.getElementById('chillFrustrations').value.trim();
      const mood = document.getElementById('chillMood').value.trim();

      if (!wins && !frustrations) {
        alert("Please share at least a win or frustration from today!");
        return;
      }
      closeModal('chillModal');
      document.getElementById('chillWins').value = '';
      document.getElementById('chillFrustrations').value = '';
      document.getElementById('chillMood').value = '';

      const summary = `☕ Chai & Chill Evening Recap:\\n- Wins: ${wins || 'None'}\\n- Headaches: ${frustrations || 'None'}\\n- Mood: ${mood || '8/10'}`;
      appendMessage("You", summary, true);

      document.getElementById('avatar-status-text').innerText = "Dora is writing your evening wrap-up...";
      const res = await fetch('/api/debrief', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wins, frustrations, mood })
      });
      const data = await res.json();
      appendMessage("Dora", data.reply, false, data.thought, "☕ Chai & Chill Wrap-Up");
      document.getElementById('live-speech-text').innerText = '"' + data.reply + '"';
      speakText(data.reply);
      document.getElementById('avatar-status-text').innerText = "Dora is listening • Ambient Mode";
    }

    function promptRenameCompanion() {
      const cur = document.getElementById('companion-name-badge').innerText;
      const n = prompt("What nickname would you like to give your companion?", cur);
      if (n && n.trim()) {
        fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: `/name ${n.trim()}` })
        }).then(r => r.json()).then(data => {
          document.getElementById('companion-name-badge').innerText = n.trim();
          document.getElementById('companion-header-name').innerText = n.trim();
          document.getElementById('bubble-barista-name').innerText = n.trim();
          appendMessage("Dora", data.reply, false);
        });
      }
    }

    async function triggerVisionSnapshot() {
      showToast("📸 Capturing desktop screen peek...");
      document.getElementById('avatar-status-text').innerText = "Dora is inspecting your screen...";
      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: '/snap' })
        });
        const data = await res.json();
        appendMessage("Dora", data.reply, false, data.thought, "📸 Vision Peek");
        document.getElementById('live-speech-text').innerText = '"' + data.reply + '"';
        speakText(data.reply);
      } catch(e) {
        showToast("Screen peek complete!");
      } finally {
        document.getElementById('avatar-status-text').innerText = "Dora is listening • Ambient Mode";
      }
    }

    function scrollToChat() {
      document.getElementById('chat-messages-container').scrollIntoView({ behavior: 'smooth' });
    }

    // Unified Chat Message Submission (Works from center input, footer input, and chips)
    function handleFooterSubmit(e) {
      if (e) e.preventDefault();
      const footerInput = document.getElementById('footer-input-field');
      const text = footerInput ? footerInput.value.trim() : '';
      if (!text) return;
      footerInput.value = '';
      submitChatMessage(text);
    }

    function handleUserSubmit(e) {
      if (e) e.preventDefault();
      const input = document.getElementById('user-input-field');
      const text = input ? input.value.trim() : '';
      if (!text) return;
      input.value = '';
      submitChatMessage(text);
    }

    function injectUserPrompt(txt) {
      submitChatMessage(txt);
    }

    async function submitChatMessage(text) {
      if (!text || !text.trim()) return;
      const cleanText = text.trim();

      // Clear both inputs
      const centerInput = document.getElementById('user-input-field');
      if (centerInput) centerInput.value = '';
      const footerInput = document.getElementById('footer-input-field');
      if (footerInput) footerInput.value = '';

      appendMessage("You", cleanText, true);

      // Update UI state
      const statusEl = document.getElementById('avatar-status-text');
      if (statusEl) statusEl.innerText = "Dora is thinking in English...";
      const speechEl = document.getElementById('live-speech-text');
      if (speechEl) speechEl.innerText = '"Steaming freshly grounded thoughts for you right now..."';
      const bars = document.getElementById('audio-waveform-bars');
      if (bars) bars.style.opacity = '1';

      const t0 = performance.now();
      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: cleanText })
        });
        const data = await res.json();
        const latencyMs = Math.round(performance.now() - t0);
        const latLabel = document.getElementById('latency-label');
        if (latLabel) latLabel.innerText = `Latency: ${latencyMs}ms • GPU`;

        appendMessage("Dora", data.reply, false, data.thought, data.mode, data.language);

        // Update live speech bubble
        const lines = data.reply.split('\n');
        const firstLine = lines[0].replace(/[*#_`]/g, '').trim();
        if (speechEl) speechEl.innerText = '"' + (firstLine || data.reply.slice(0, 140)) + '"';

        // Speak aloud
        speakText(data.reply);
      } catch (err) {
        console.error("Chat error:", err);
        appendMessage("Dora", "⚠️ Could not connect to local server. Please check terminal.", false);
      } finally {
        if (statusEl) statusEl.innerText = "Dora is listening • Ambient Mode";
      }
    }

    function appendMessage(sender, text, isUser, thought = null, mode = null, language = null) {
      const container = document.getElementById('chat-messages-container');
      if (!container) return;

      const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      const msgDiv = document.createElement('div');
      msgDiv.className = `flex flex-col gap-1 ${isUser ? 'items-end' : 'items-start'} transition-all`;

      if (isUser) {
        msgDiv.innerHTML = `
          <div class="flex items-center gap-1.5 text-[10px] text-outline font-semibold">
            <span>You • ${time}</span>
            <span class="w-2 h-2 rounded-full bg-primary"></span>
          </div>
          <div class="bg-primary-container text-on-primary-container p-3 rounded-2xl rounded-tr-sm text-xs shadow-[inset_1px_1px_2px_rgba(255,255,255,0.7),0_2px_6px_rgba(247,141,167,0.2)] max-w-[95%] leading-relaxed whitespace-pre-wrap">
            ${text}
          </div>
        `;
      } else {
        let thoughtHtml = '';
        if (thought) {
          thoughtHtml = `
            <div class="thought-pill" onclick="this.querySelector('.thought-details').style.display = this.querySelector('.thought-details').style.display === 'block' ? 'none' : 'block'">
              <div class="flex items-center justify-between font-bold">
                <span>🧠 English Brain Cognition</span>
                <span class="text-[9px] opacity-75">Click to toggle</span>
              </div>
              <div class="thought-details">${thought}</div>
            </div>
          `;
        }

        const parsedContent = (typeof marked !== 'undefined') ? marked.parse(text) : text;

        msgDiv.innerHTML = `
          <div class="flex items-center gap-1.5 text-[10px] text-outline font-semibold">
            <span class="w-2 h-2 rounded-full bg-primary-container"></span>
            <span>Dora • ${time}</span>
            ${mode ? `<span class="px-1.5 py-0.2 bg-primary/10 text-primary rounded text-[9px]">${mode}</span>` : ''}
            ${language ? `<span class="px-1.5 py-0.2 bg-tertiary/10 text-tertiary rounded text-[9px]">${language}</span>` : ''}
          </div>
          <div class="bg-surface-container-low p-3 rounded-2xl rounded-tl-sm text-xs text-on-surface shadow-[inset_1px_1px_2px_rgba(255,255,255,0.9),0_2px_6px_rgba(74,46,43,0.04)] max-w-[95%] leading-relaxed chat-bubble-markdown">
            ${thoughtHtml}
            ${parsedContent}
          </div>
        `;
      }

      container.appendChild(msgDiv);
      container.scrollTop = container.scrollHeight;
    }

    function clearChatLog() {
      const container = document.getElementById('chat-messages-container');
      if (container) {
        container.innerHTML = `
          <div class="text-center py-4 text-xs text-outline font-medium">
            Order dialogue cleared. Dora is ready for a fresh warm brew! ☕
          </div>
        `;
      }
    }

    // 3D Three.js Interactive Avatar Initialization
    (function initThreeJSDora() {
      const containerEl = document.getElementById('threejs-container-ANIMATION_1');
      if (!containerEl) return;

      const width = containerEl.clientWidth || 320;
      const height = containerEl.clientHeight || 300;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
      camera.position.set(0, 0, 8.5);

      const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.shadowMap.enabled = true;
      containerEl.appendChild(renderer.domElement);

      // Ambient & Directional Lighting
      const ambientLight = new THREE.AmbientLight(0xfff5f0, 1.3);
      scene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xffeedd, 1.6);
      keyLight.position.set(5, 8, 6);
      scene.add(keyLight);

      const fillLight = new THREE.PointLight(0xffb5c2, 1.4, 25);
      fillLight.position.set(-6, -3, 4);
      scene.add(fillLight);

      const rimLight = new THREE.PointLight(0x7ac1eb, 1.2, 20);
      rimLight.position.set(0, 5, -4);
      scene.add(rimLight);

      // Head Group
      const headGroup = new THREE.Group();
      scene.add(headGroup);

      // Face Pill Backdrop (using CapsuleGeometry with fallback)
      let faceGeo;
      if (THREE.CapsuleGeometry) {
        faceGeo = new THREE.CapsuleGeometry(2.3, 1.4, 32, 64);
      } else {
        faceGeo = new THREE.SphereGeometry(2.3, 32, 32);
        faceGeo.scale(1.2, 0.9, 0.7);
      }
      const faceMat = new THREE.MeshPhongMaterial({
        color: 0xffffff,
        shininess: 35,
        specular: 0xffeef2,
        transparent: true,
        opacity: 0.96
      });
      const faceBackdrop = new THREE.Mesh(faceGeo, faceMat);
      faceBackdrop.rotation.z = Math.PI / 2;
      faceBackdrop.position.set(0, 0, -0.6);
      headGroup.add(faceBackdrop);

      // Blush cheeks
      const cheekGeo = new THREE.SphereGeometry(0.42, 24, 24);
      cheekGeo.scale(1.4, 0.7, 0.4);
      const cheekMat = new THREE.MeshLambertMaterial({
        color: 0xf592a0,
        transparent: true,
        opacity: 0.75
      });
      const leftCheek = new THREE.Mesh(cheekGeo, cheekMat);
      leftCheek.position.set(-2.2, -0.85, 0.2);
      headGroup.add(leftCheek);

      const rightCheek = leftCheek.clone();
      rightCheek.position.set(2.2, -0.85, 0.2);
      headGroup.add(rightCheek);

      // Cute Red Nose Bead
      const noseGeo = new THREE.SphereGeometry(0.36, 32, 32);
      const noseMat = new THREE.MeshPhongMaterial({
        color: 0xee4b5e,
        shininess: 90,
        specular: 0xffffff
      });
      const nose = new THREE.Mesh(noseGeo, noseMat);
      nose.position.set(0, -0.32, 0.95);
      headGroup.add(nose);

      // Whiskers
      const whiskerMat = new THREE.MeshBasicMaterial({ color: 0x6e473b });
      function createWhisker(x, y, z, rotZ, length) {
        const geo = new THREE.CylinderGeometry(0.02, 0.02, length, 12);
        const m = new THREE.Mesh(geo, whiskerMat);
        m.position.set(x, y, z);
        m.rotation.z = rotZ;
        return m;
      }
      headGroup.add(createWhisker(-1.8, -0.3, 0.35, 1.45, 1.1));
      headGroup.add(createWhisker(-1.85, -0.5, 0.35, 1.57, 1.15));
      headGroup.add(createWhisker(1.8, -0.3, 0.35, -1.45, 1.1));
      headGroup.add(createWhisker(1.85, -0.5, 0.35, -1.57, 1.15));

      // Sclera / Eyes
      const eyeScleraGeo = new THREE.SphereGeometry(1.05, 32, 32);
      eyeScleraGeo.scale(0.85, 1.25, 0.8);
      const eyeWhiteMat = new THREE.MeshPhongMaterial({
        color: 0xfcfcfd,
        shininess: 60,
        specular: 0xffffff
      });

      // Left Eye
      const leftEyeGroup = new THREE.Group();
      leftEyeGroup.position.set(-0.84, 0.5, 0.45);
      const leftSclera = new THREE.Mesh(eyeScleraGeo, eyeWhiteMat);
      leftEyeGroup.add(leftSclera);

      const pupilGeo = new THREE.SphereGeometry(0.38, 24, 24);
      pupilGeo.scale(0.8, 1.15, 0.3);
      const pupilMat = new THREE.MeshPhongMaterial({
        color: 0x221715,
        shininess: 100,
        specular: 0xffffff
      });
      const leftPupil = new THREE.Mesh(pupilGeo, pupilMat);
      leftPupil.position.set(0.12, 0, 0.72);
      leftEyeGroup.add(leftPupil);

      const glintGeo = new THREE.SphereGeometry(0.1, 16, 16);
      const glintMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const leftGlint1 = new THREE.Mesh(glintGeo, glintMat);
      leftGlint1.position.set(0.2, 0.16, 0.82);
      leftEyeGroup.add(leftGlint1);

      headGroup.add(leftEyeGroup);

      // Right Eye
      const rightEyeGroup = new THREE.Group();
      rightEyeGroup.position.set(0.84, 0.5, 0.45);
      const rightSclera = new THREE.Mesh(eyeScleraGeo, eyeWhiteMat);
      rightEyeGroup.add(rightSclera);

      const rightPupil = new THREE.Mesh(pupilGeo, pupilMat);
      rightPupil.position.set(-0.12, 0, 0.72);
      rightEyeGroup.add(rightPupil);

      const rightGlint1 = new THREE.Mesh(glintGeo, glintMat);
      rightGlint1.position.set(-0.04, 0.16, 0.82);
      rightEyeGroup.add(rightGlint1);

      headGroup.add(rightEyeGroup);

      // Floating Café Orbs
      const orbsGroup = new THREE.Group();
      scene.add(orbsGroup);
      const orbMats = [
        new THREE.MeshPhongMaterial({ color: 0xffcad4, shininess: 40, transparent: true, opacity: 0.75 }),
        new THREE.MeshPhongMaterial({ color: 0xd8b4a0, shininess: 40, transparent: true, opacity: 0.7 }),
        new THREE.MeshPhongMaterial({ color: 0xffffff, shininess: 80, transparent: true, opacity: 0.85 }),
        new THREE.MeshPhongMaterial({ color: 0xb5835a, shininess: 30, transparent: true, opacity: 0.6 })
      ];
      const orbMeshes = [];
      for (let i = 0; i < 9; i++) {
        const r = 0.22 + Math.random() * 0.3;
        const mesh = new THREE.Mesh(new THREE.SphereGeometry(r, 16, 16), orbMats[i % orbMats.length]);
        mesh.position.set((Math.random() - 0.5) * 11, (Math.random() - 0.5) * 7, -1.5 + (Math.random() - 0.5) * 3);
        mesh.userData = { speedY: 0.006 + Math.random() * 0.009, baseY: mesh.position.y, freq: 1 + Math.random() * 2 };
        orbsGroup.add(mesh);
        orbMeshes.push(mesh);
      }

      // Mouse pupil tracking
      let targetMouseX = 0, targetMouseY = 0, curMouseX = 0, curMouseY = 0;
      window.addEventListener('mousemove', (e) => {
        targetMouseX = (e.clientX / window.innerWidth) * 2 - 1;
        targetMouseY = -(e.clientY / window.innerHeight) * 2 + 1;
      });

      // Blinking & Expression Triggers
      let blinkTimer = 0, isBlinking = false, blinkScaleY = 1;
      let winkTimer = 0, isWinking = false;

      triggerAvatarWink = () => {
        isWinking = true;
        winkTimer = 0;
      };

      triggerAvatarSquint = () => {
        isBlinking = true;
        blinkTimer = 0;
      };

      const clock = new THREE.Clock();
      function animate() {
        requestAnimationFrame(animate);
        const delta = clock.getDelta();
        const time = clock.getElapsedTime();

        curMouseX += (targetMouseX - curMouseX) * 0.08;
        curMouseY += (targetMouseY - curMouseY) * 0.08;

        headGroup.rotation.y = curMouseX * 0.35;
        headGroup.rotation.x = -curMouseY * 0.25;
        headGroup.position.y = Math.sin(time * 1.6) * 0.12;

        const pupilOffsetX = curMouseX * 0.24;
        const pupilOffsetY = curMouseY * 0.22;
        leftPupil.position.x = 0.12 + pupilOffsetX;
        leftPupil.position.y = pupilOffsetY;
        rightPupil.position.x = -0.12 + pupilOffsetX;
        rightPupil.position.y = pupilOffsetY;

        // Spontaneous blinking
        if (!isBlinking && !isWinking && Math.random() < 0.006) {
          isBlinking = true;
          blinkTimer = 0;
        }

        if (isBlinking) {
          blinkTimer += delta * 12;
          blinkScaleY = Math.max(0.08, Math.abs(Math.cos(blinkTimer)));
          if (blinkTimer >= Math.PI) {
            isBlinking = false;
            blinkScaleY = 1;
          }
          leftEyeGroup.scale.y = blinkScaleY;
          rightEyeGroup.scale.y = blinkScaleY;
        }

        if (isWinking) {
          winkTimer += delta * 10;
          const winkScale = Math.max(0.08, Math.abs(Math.cos(winkTimer)));
          rightEyeGroup.scale.y = winkScale;
          if (winkTimer >= Math.PI) {
            isWinking = false;
            rightEyeGroup.scale.y = 1;
          }
        }

        orbMeshes.forEach((orb, idx) => {
          orb.position.y = orb.userData.baseY + Math.sin(time * orb.userData.freq + idx) * 0.35;
          orb.rotation.x += 0.005;
          orb.rotation.y += 0.008;
        });

        cheekMat.opacity = 0.72 + Math.sin(time * 3) * 0.12;
        renderer.render(scene, camera);
      }
      animate();

      window.addEventListener('resize', () => {
        const w = containerEl.clientWidth || 320;
        const h = containerEl.clientHeight || 300;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      });
    })();
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTML_TEMPLATE

@app.get("/api/status")
async def status_endpoint():
    return JSONResponse({
        "status": "online",
        "model": chat_engine.model_name,
        "rag_facts_count": len(chat_engine.rag.knowledge_docs),
        "rag_dialogues_count": len(chat_engine.rag.dialogues),
        "companion_name": chat_engine.brain.companion_name
    })

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return JSONResponse({
            "reply": "Say something, bhai! Main sun raha hu.",
            "thought": "",
            "mode": "Casual / Banter",
            "language": "Hinglish"
        })

    # Slash command routing
    cmd = user_msg.split()[0].lower()

    if cmd == "/vibe":
        vibe_res = chat_engine.superpowers.vibe_dj(user_msg[5:].strip() or "chill")
        reply = (
            f"🎵 **Vibe DJ Pick ({vibe_res['category']})**: **{vibe_res['track']}**\n\n"
            f"✨ **Vibe**: {vibe_res['vibe_description']}\n\n"
            f"🔗 [Listen on YouTube]({vibe_res['youtube_url']}) • "
            f"🔗 [Listen on Spotify]({vibe_res['spotify_url']})"
        )
        return JSONResponse({
            "reply": reply,
            "thought": f"Vibe DJ activated for query: '{user_msg[5:].strip()}'. Curated music track matched.",
            "mode": "🎵 Vibe DJ Mode",
            "language": "Indian English"
        })

    if cmd == "/hype":
        hype_speech = chat_engine.superpowers.instant_hype(user_msg[5:].strip() or None, language="Hinglish")
        return JSONResponse({
            "reply": f"🔥 **{hype_speech}**",
            "thought": "Instant Hype-Man triggered. High-energy motivational injection.",
            "mode": "🔥 Instant Hype-Man",
            "language": "Hinglish"
        })

    if cmd == "/roast":
        goal = user_msg[6:].strip() or "Finish today's pending work"
        pact = chat_engine.superpowers.start_accountability(goal, 45)
        return JSONResponse({
            "reply": pact,
            "thought": f"Accountability target registered in SQLite: '{goal}'. Friendly roast locked in.",
            "mode": "🔥 Accountability & Roast",
            "language": "Hinglish"
        })

    if cmd == "/wingman":
        draft = user_msg[8:].strip() or "Can we talk tomorrow instead?"
        rewrites = chat_engine.superpowers.wingman_rewrite(draft)
        reply = (
            f"🎭 **Wingman Text Doctor — 3 Style Options**:\n\n"
            f"**1. Casual & Chill:**\n> {rewrites['casual']}\n\n"
            f"**2. Corporate Diplomatic:**\n> {rewrites['diplomatic']}\n\n"
            f"**3. Direct / No BS:**\n> {rewrites['direct']}"
        )
        return JSONResponse({
            "reply": reply,
            "thought": f"Wingman engine analyzed awkward draft '{draft}' and generated 3 social styles.",
            "mode": "🎭 Wingman Mode",
            "language": "English"
        })

    if cmd == "/snap":
        try:
            res = chat_engine.vision.analyze_snapshot()
            return JSONResponse({
                "reply": f"📸 {res}",
                "thought": "Vision screen snapshot captured and analyzed.",
                "mode": "📸 Vision Companion",
                "language": "English / Hinglish"
            })
        except Exception as e:
            return JSONResponse({
                "reply": f"📸 Screen snapshot captured! (Run `ollama pull moondream` if you'd like live visual AI commentary: {e})",
                "thought": f"Vision error fallback: {e}",
                "mode": "📸 Vision Companion",
                "language": "English"
            })

    if cmd == "/chill":
        reply = (
            "☕ **Chai & Chill Evening Wind-Down Debrief**:\n\n"
            "Take 2 minutes to unwind, bhai! Let's reflect on your day:\n\n"
            "1. **What was your biggest win today** (big or small)?\n"
            "2. **What was the biggest headache or friction point**?\n"
            "3. **How are you feeling right now** (1-10)?\n\n"
            "👉 *Tip: You can reply right here in chat, or click the **'Chai & Chill'** tab at the top to save it to your private life diary!*"
        )
        return JSONResponse({
            "reply": reply,
            "thought": "Chai & Chill debrief activated. Prompts presented to wind down user.",
            "mode": "☕ Chai & Chill",
            "language": "Hinglish"
        })

    if cmd == "/stats":
        dashboard = chat_engine.superpowers.get_stats_dashboard()
        return JSONResponse({
            "reply": f"```text\n{dashboard}\n```",
            "thought": "Queried local SQLite Life Diary & Mood statistics.",
            "mode": "📊 Life Diary Stats",
            "language": "English"
        })

    if cmd == "/name":
        parts = user_msg.split(maxsplit=1)
        if len(parts) > 1:
            new_name = parts[1].strip()
            chat_engine.brain.set_name(new_name)
            return JSONResponse({
                "reply": f"Done! From now on, call me **{new_name}**! 🤝 Always got your back, boss.",
                "thought": f"Companion renamed to {new_name}.",
                "mode": "🤝 Identity Update",
                "language": "Indian English"
            })
        return JSONResponse({
            "reply": "Usage: `/name <new nickname>` (e.g. `/name Dora` or `/name Veer`)",
            "thought": "",
            "mode": "Adaptive",
            "language": "English"
        })

    if cmd == "/help":
        help_md = (
            "🚀 **Companion Superpowers & Slash Commands**:\n\n"
            "| Command | Description |\n"
            "|---|---|\n"
            "| `☕ /chill` | 3-step evening wind-down debrief that saves to your diary |\n"
            "| `🎵 /vibe <mood>` | Vibe DJ curated tracks (Hindi lo-fi, Marathi drill, phonk, focus) |\n"
            "| `🔥 /roast <goal>` | Set an accountability target with deadline roast |\n"
            "| `🎭 /wingman <text>` | Rewrite awkward drafts into Casual, Diplomatic, and Direct |\n"
            "| `🚀 /hype [topic]` | Instant motivational speech in your native dialect |\n"
            "| `📸 /snap` | Vision screen capture commentary |\n"
            "| `📊 /stats` | View private SQLite Life Diary & mood statistics |\n"
            "| `🏷️ /name <name>` | Rename your companion anytime |\n"
            "| `❓ /help` | View this cheat sheet |"
        )
        return JSONResponse({
            "reply": help_md,
            "thought": "Help documentation displayed.",
            "mode": "Help & Guide",
            "language": "English"
        })

    # Autonomous Continuous Self-Learning: Extract new habits, facts, and preferences
    chat_engine.learner.extract_and_learn(user_msg)

    # Standard conversational turn
    detection = chat_engine.brain.detect_language_and_script(user_msg)
    lang = detection["language"]
    mood, mode = chat_engine.brain.infer_sentiment_and_mode(user_msg)
    rag_facts = chat_engine.rag.retrieve(user_msg, top_k=2)
    dialogue_exemplar = chat_engine.rag.retrieve_dialogue_exemplar(user_msg, lang=lang)
    
    serious_keywords = ["bug", "error", "code", "deploy", "server", "python", "javascript", "react", "sql", "api", "database", "502", "crash", "function", "git", "protein", "intake", "creatine", "how", "why", "what", "fix", "explain"]
    is_serious = any(k in user_msg.lower() for k in serious_keywords)
    joke = None if is_serious else chat_engine.memory.check_inside_jokes(user_msg, language=lang)

    system_prompt = chat_engine.brain.construct_system_prompt(
        user_msg=user_msg,
        memory_context=rag_facts,
        inside_joke=joke,
        dialogue_exemplar=dialogue_exemplar,
        target_language=lang,
        target_script=detection["script"]
    )

    raw_response = chat_engine.send_to_ollama(system_prompt, user_msg)
    clean_reply, thought = chat_engine.brain.extract_thought_and_response(raw_response, target_script=detection["script"])

    # Persist interaction to SQLite Diary & Dynamic Conversational RAG Self-Learning
    chat_engine.memory.log_interaction(
        user_msg=user_msg,
        assistant_reply=clean_reply,
        lang=f"{lang} ({detection['script']})",
        mood=mood,
        thought_summary=thought[:100] if thought else mode
    )
    chat_engine.rag.add_chat_interaction(user_msg, clean_reply, lang=lang)

    return JSONResponse({
        "reply": clean_reply,
        "thought": thought,
        "mode": mode,
        "language": f"{lang} ({detection['script']})"
    })

@app.post("/api/debrief")
async def debrief_endpoint(request: Request):
    data = await request.json()
    wins = data.get("wins", "").strip()
    frustrations = data.get("frustrations", "").strip()
    mood = data.get("mood", "").strip()

    debrief_prompt = (
        f"Here is my evening wind-down recap:\n"
        f"- Today's Wins: {wins}\n"
        f"- Friction / Headaches: {frustrations}\n"
        f"- Current Mood / Energy: {mood}\n\n"
        f"Give me a warm, loyal best friend wrap-up to help me relax, celebrate the progress, let go of the stress, and sleep peacefully."
    )

    detection = chat_engine.brain.detect_language_and_script(f"{wins} {frustrations}")
    lang = detection["language"]
    
    sys_prompt = chat_engine.brain.construct_system_prompt(
        user_msg=debrief_prompt,
        target_language=lang,
        target_script=detection["script"]
    )

    raw_response = chat_engine.send_to_ollama(sys_prompt, debrief_prompt)
    clean_reply, thought = chat_engine.brain.extract_thought_and_response(raw_response, target_script=detection["script"])

    # Save to SQLite daily debriefs
    chat_engine.memory.save_debrief(wins, frustrations, mood, clean_reply)

    return JSONResponse({
        "reply": clean_reply,
        "thought": thought,
        "mode": "☕ Chai & Chill Evening Wrap-Up",
        "language": lang
    })

@app.get("/api/stats")
async def stats_endpoint():
    return JSONResponse(chat_engine.memory.get_stats_summary())

if __name__ == "__main__":
    print("=" * 60)
    print("☕ Starting Café Dora (Local Best Friend) on http://localhost:7860 ...")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=7860)
